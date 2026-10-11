"""Doha rain-flood mapping with Sentinel-1 SAR change detection.

All functions work on small, clipped rasters so the notebook runs on a laptop.
Data is read from data/sample_input/ if present, otherwise downloaded from the
Microsoft Planetary Computer STAC API (free, no API key needed).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr
import rioxarray  # noqa: F401  (registers the .rio accessor)
from scipy import ndimage

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"
CRS = "EPSG:32639"  # UTM zone 39N, covers all of Qatar
PIXEL_M = 20
PIXEL_KM2 = PIXEL_M * PIXEL_M / 1e6

# ESA WorldCover classes present in Qatar
WORLDCOVER = {
    10: "Tree cover", 20: "Shrubland", 30: "Grassland", 40: "Cropland",
    50: "Built-up", 60: "Bare / sparse", 80: "Permanent water", 90: "Wetland",
    95: "Mangroves",
}


# --------------------------------------------------------------------------
# Data access
# --------------------------------------------------------------------------
def _catalog():
    import planetary_computer
    import pystac_client
    return pystac_client.Client.open(STAC_URL, modifier=planetary_computer.sign_inplace)


def _load(collection, bbox, date, bands):
    import odc.stac
    items = list(_catalog().search(collections=[collection], bbox=bbox, datetime=date).items())
    if not items:
        raise ValueError(f"No {collection} scene over {bbox} on {date}")
    ds = odc.stac.load(items, bands=bands, bbox=bbox, crs=CRS, resolution=PIXEL_M,
                       groupby="solar_day", chunks={})
    return ds.isel(time=0).compute(), [i.id for i in items]


def download_inputs(bbox, s1_dates, s2_date, out_dir):
    """Download and clip every input layer to the AOI and save as GeoTIFFs.

    s1_dates: dict like {"baseline": "2018-10-03", "before": ..., "after": ...}
    Returns a dict of scene IDs for provenance.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    provenance = {}

    for label, date in s1_dates.items():
        ds, ids = _load("sentinel-1-rtc", bbox, date, ["vv"])
        # store backscatter in dB x 100 as int16 to keep the sample small
        db = 10 * np.log10(ds.vv.where(ds.vv > 0))
        db = (db * 100).round().fillna(-32768).astype("int16")
        db.rio.write_nodata(-32768, inplace=True)
        db.rio.to_raster(out_dir / f"s1_vv_db_{label}_{date}.tif", compress="deflate")
        provenance[f"s1_{label}"] = ids

    ds, ids = _load("sentinel-2-l2a", bbox, s2_date, ["B04", "B03", "B02"])
    rgb = xr.concat([ds.B04, ds.B03, ds.B02], dim="band")
    rgb = (rgb.astype("float32") / 3000 * 255).clip(0, 255).astype("uint8")
    rgb.rio.to_raster(out_dir / f"s2_rgb_{s2_date}.tif", compress="deflate")
    provenance["s2_rgb"] = ids

    ds, ids = _load("esa-worldcover", bbox, "2021", ["map"])
    ds["map"].astype("uint8").rio.to_raster(out_dir / "worldcover_2021.tif", compress="deflate")
    provenance["worldcover"] = ids
    return provenance


def read_inputs(in_dir, s1_dates, s2_date):
    """Read the clipped GeoTIFFs back as arrays on a common grid."""
    in_dir = Path(in_dir)
    vv = {}
    for label, date in s1_dates.items():
        da = rioxarray.open_rasterio(in_dir / f"s1_vv_db_{label}_{date}.tif", masked=True).squeeze("band", drop=True)
        vv[label] = (da / 100).astype("float32")
    ref = vv["before"]
    rgb = rioxarray.open_rasterio(in_dir / f"s2_rgb_{s2_date}.tif").rio.reproject_match(ref)
    wc = rioxarray.open_rasterio(in_dir / "worldcover_2021.tif").squeeze("band", drop=True)
    wc = wc.rio.reproject_match(ref, resampling=0)  # nearest neighbour for classes
    return vv, rgb, wc


# --------------------------------------------------------------------------
# Analysis
# --------------------------------------------------------------------------
def land_mask(worldcover, coast_buffer_m=300):
    """Land pixels, excluding a buffer along the sea and other permanent water.

    The buffer removes shoreline artefacts: wind-roughened shallow water and
    land reclaimed between the 2018 event and the 2021 land-cover map.
    """
    water = (worldcover == 80) | (worldcover == 0)
    near_water = ndimage.binary_dilation(water, iterations=max(1, coast_buffer_m // PIXEL_M))
    return ~near_water


def despeckle(db, size=5):
    """Median filter to suppress SAR speckle (NaNs filled with the median first)."""
    a = np.asarray(db, dtype="float32")
    filled = np.where(np.isnan(a), np.nanmedian(a), a)
    return np.where(np.isnan(a), np.nan, ndimage.median_filter(filled, size))


def detect_change(vv_before, vv_after, land_mask,
                  wet_db=3.0, pond_db=-3.0, water_db=-15.0, min_pixels=4):
    """Classify land pixels from a before/after Sentinel-1 VV pair.

    - wet:  backscatter rose by > wet_db (soil moisture raises the dielectric constant)
    - pond: backscatter dropped by > |pond_db| AND is now darker than water_db
            (smooth standing water reflects the radar pulse away from the sensor)
    Small isolated pond specks (< min_pixels) are removed as noise.
    """
    diff = vv_after - vv_before
    wet = (diff > wet_db) & land_mask
    pond = (diff < pond_db) & (vv_after < water_db) & land_mask
    labels, n = ndimage.label(pond)
    if n:
        sizes = ndimage.sum(pond, labels, range(1, n + 1))
        pond = np.isin(labels, 1 + np.flatnonzero(sizes >= min_pixels))
    return diff, wet, pond


def exposure_table(wet, pond, worldcover, land):
    """Area (km2) of wet ground and standing water per land-cover class, within the analysed land."""
    rows = []
    for code, name in WORLDCOVER.items():
        cls = (worldcover == code) & land
        if cls.sum() * PIXEL_KM2 < 0.1 or code == 80:  # skip absent / negligible classes
            continue
        rows.append({
            "land_cover": name,
            "class_area_km2": cls.sum() * PIXEL_KM2,
            "wet_ground_km2": (wet & cls).sum() * PIXEL_KM2,
            "standing_water_km2": (pond & cls).sum() * PIXEL_KM2,
        })
    df = pd.DataFrame(rows)
    df["wet_ground_pct"] = 100 * df.wet_ground_km2 / df.class_area_km2
    return df.round(3).sort_values("wet_ground_km2", ascending=False).reset_index(drop=True)


def ponding_hotspots(pond, ref_da, worldcover, top=15):
    """Connected standing-water patches, largest first, with lat/lon centroids."""
    from pyproj import Transformer
    labels, n = ndimage.label(pond)
    if not n:
        return pd.DataFrame()
    idx = np.arange(1, n + 1)
    sizes = ndimage.sum(pond, labels, idx)
    cents = ndimage.center_of_mass(pond, labels, idx)
    xs, ys = ref_da.x.values, ref_da.y.values
    to_ll = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
    rows = []
    for lab, size, (r, c) in zip(idx, sizes, cents):
        lon, lat = to_ll.transform(np.interp(c, np.arange(len(xs)), xs),
                                   np.interp(r, np.arange(len(ys)), ys))
        lc = np.bincount(worldcover[labels == lab].astype(int)).argmax()
        rows.append({"area_ha": size * PIXEL_KM2 * 100, "lat": lat, "lon": lon,
                     "land_cover": WORLDCOVER.get(lc, str(lc))})
    df = pd.DataFrame(rows).sort_values("area_ha", ascending=False).head(top)
    df.insert(0, "rank", range(1, len(df) + 1))
    return df.round({"area_ha": 2, "lat": 5, "lon": 5}).reset_index(drop=True)


def impact_grid(wet, pond, land, ref_da, cell_m=1000):
    """Summarise impact on a regular grid (default 1 km cells).

    impact_pct = share of a cell's land that is rain-saturated or ponded.
    Returns the grid as an array plus a table of every cell, ranked, with
    centre and corner coordinates so planners know which neighbourhoods to
    inspect first.
    """
    from pyproj import Transformer
    k = cell_m // PIXEL_M
    h, w = wet.shape
    hit = (wet | pond).astype(float)
    rows = []
    to_ll = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
    xs, ys = ref_da.x.values, ref_da.y.values
    grid = np.full((int(np.ceil(h / k)), int(np.ceil(w / k))), np.nan)
    for gi, r in enumerate(range(0, h, k)):
        for gj, c in enumerate(range(0, w, k)):
            l = land[r:r + k, c:c + k]
            if l.sum() < 0.5 * k * k:  # skip cells that are mostly sea
                continue
            pct = 100 * hit[r:r + k, c:c + k][l].mean()
            grid[gi, gj] = pct
            lon, lat = to_ll.transform(xs[min(c + k // 2, w - 1)], ys[min(r + k // 2, h - 1)])
            lon0, lat0 = to_ll.transform(xs[c] - PIXEL_M / 2, ys[min(r + k, h) - 1] - PIXEL_M / 2)
            lon1, lat1 = to_ll.transform(xs[min(c + k, w) - 1] + PIXEL_M / 2, ys[r] + PIXEL_M / 2)
            rows.append({"impact_pct": pct, "lat": lat, "lon": lon, "grid_row": gi, "grid_col": gj,
                         "wet_ha": wet[r:r + k, c:c + k].sum() * PIXEL_KM2 * 100,
                         "standing_water_ha": pond[r:r + k, c:c + k].sum() * PIXEL_KM2 * 100,
                         "lat_min": lat0, "lon_min": lon0, "lat_max": lat1, "lon_max": lon1})
    df = pd.DataFrame(rows).sort_values("impact_pct", ascending=False)
    df.insert(0, "rank", range(1, len(df) + 1))
    return grid, df.round({"impact_pct": 1, "lat": 5, "lon": 5, "wet_ha": 1, "standing_water_ha": 2,
                           "lat_min": 5, "lon_min": 5, "lat_max": 5, "lon_max": 5}).reset_index(drop=True)


def false_alarm_check(vv_a, vv_b, land_mask, **kwargs):
    """Run the same detector on a dry-weather pair: anything flagged is a false alarm."""
    _, wet, pond = detect_change(vv_a, vv_b, land_mask, **kwargs)
    return wet.sum() * PIXEL_KM2, pond.sum() * PIXEL_KM2

"""Figure for the slides/README: why an optical water index fails after a storm over Doha.

Downloads Sentinel-2 L2A for 12 Oct and 22 Oct 2018 (free, no key), computes the
MNDWI water-index change and shows that cloud shadows are mistaken for flood water.
Run from the repository root:  python src/make_why_radar_figure.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import floodmap as fm

BBOX = [51.40, 25.18, 51.62, 25.38]
OUT = Path(__file__).resolve().parent.parent / "docs" / "figures" / "why_radar.png"


def mndwi(ds):
    g, s = ds.B03.astype("float32"), ds.B11.astype("float32")
    return ((g - s) / (g + s + 1e-6)).values


def rgb(ds):
    return np.clip(np.stack([ds.B04, ds.B03, ds.B02], -1).astype("float32") / 3000, 0, 1)


def main():
    bands = ["B02", "B03", "B04", "B11", "SCL"]
    before, _ = fm._load("sentinel-2-l2a", BBOX, "2018-10-12", bands)
    after, _ = fm._load("sentinel-2-l2a", BBOX, "2018-10-22", bands)
    mb, ma = mndwi(before), mndwi(after)
    sea = (before.SCL.values == 6) | (mb > 0.3)
    flagged_cloud = np.isin(after.SCL.values, [3, 8, 9, 10])
    false_flood = (ma > 0) & ((ma - mb) > 0.25) & ~sea & ~flagged_cloud

    fig, ax = plt.subplots(1, 2, figsize=(16, 8))
    ax[0].imshow(rgb(after))
    ax[0].set_title("Sentinel-2, 22 Oct 2018 (2 days after the storm)\nlabelled '2.2% cloud', but full of small clouds and shadows")
    ax[1].imshow(rgb(after))
    ax[1].imshow(np.ma.masked_where(~false_flood, false_flood), cmap="autumn", interpolation="nearest")
    ax[1].set_title(f"Optical water index 'flood' ({false_flood.sum() * fm.PIXEL_KM2:.0f} km², red)\n= mostly cloud shadows missed by the cloud mask")
    for a in ax:
        a.axis("off")
    fig.suptitle("Why Doha Flood Watch uses radar: optical sensors are fooled by storm clouds",
                 fontsize=15, weight="bold", y=1.02)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=110, bbox_inches="tight")
    print("wrote", OUT)


if __name__ == "__main__":
    main()

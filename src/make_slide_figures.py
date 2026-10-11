"""Figures for the Slidev presentation, built from the committed sample data (no download).

Run from the repository root:  python src/make_slide_figures.py
Writes to docs/figures/:
  radar_before_after.png  threshold_chart.png  top5_zoom.png  cover_bg.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

import floodmap as fm

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "sample_input"
OUT = ROOT / "docs" / "figures"
S1_DATES = {"baseline": "2018-10-03", "before": "2018-10-15", "after": "2018-10-27"}
S2_DATE = "2018-10-12"

# Deck palette
NAVY, SAND, INK2, MUTED = "#0F2233", "#F6F4EF", "#3D4B5C", "#6A7684"
STORM, DRY = "#1F5FD6", "#C0473F"  # blue/red pair that stays distinct for colour-blind viewers
WET_OVERLAY = ListedColormap(["#2F7BFF"])

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["IBM Plex Sans", "Segoe UI", "Arial", "DejaVu Sans"],
    "axes.edgecolor": "#C9C4B8", "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": NAVY, "figure.facecolor": SAND, "axes.facecolor": SAND, "savefig.facecolor": SAND,
})


def load():
    vv, rgb, wc = fm.read_inputs(DATA, S1_DATES, S2_DATE)
    land = fm.land_mask(wc.values)
    f = {k: fm.despeckle(v.values) for k, v in vv.items()}
    diff, wet, pond = fm.detect_change(f["before"], f["after"], land)
    grid, cells = fm.impact_grid(wet, pond, land, vv["before"])
    return f, np.moveaxis(rgb.values, 0, -1), land, diff, wet, cells


def crop(a, r, c, half, fill=0):
    """Square window centred on (r, c); pads with `fill` where it runs off the map edge."""
    pad = [(half, half), (half, half)] + [(0, 0)] * (a.ndim - 2)
    return np.pad(a, pad, constant_values=fill)[r:r + 2 * half, c:c + 2 * half]


def radar_before_after(f, land, diff, cells):
    k = 1000 // fm.PIXEL_M
    top2 = cells.iloc[1]  # a dense inland neighbourhood in western Doha
    r, c = int(top2.grid_row) * k + k // 2, int(top2.grid_col) * k + k // 2
    half = 150  # 150 px * 20 m = 3 km each side -> 6 km window
    fig, ax = plt.subplots(1, 3, figsize=(18, 6.4))
    ax[0].imshow(crop(f["before"], r, c, half), cmap="gray", vmin=-22, vmax=2)
    ax[0].set_title("Before · 15 Oct 2018", fontsize=20, color=NAVY, pad=12, weight="bold")
    ax[1].imshow(crop(f["after"], r, c, half), cmap="gray", vmin=-22, vmax=2)
    ax[1].set_title("After · 27 Oct 2018", fontsize=20, color=NAVY, pad=12, weight="bold")
    d = np.where(crop(land, r, c, half), crop(diff, r, c, half), np.nan)
    im = ax[2].imshow(d, cmap="RdBu", vmin=-6, vmax=6)
    ax[2].set_title("Change: blue = wetter ground", fontsize=20, color=NAVY, pad=12, weight="bold")
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    cax = make_axes_locatable(ax[2]).append_axes("right", size="5%", pad=0.12)
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("Backscatter change (dB)", fontsize=14, color=INK2)
    cb.outline.set_visible(False)
    for a in ax:
        a.set_xticks([]); a.set_yticks([])
        for s in a.spines.values():
            s.set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "radar_before_after.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def threshold_chart(f, land):
    thr = [2.0, 2.5, 3.0, 3.5, 4.0, 5.0]
    storm, dry = [], []
    for t in thr:
        _, w, _ = fm.detect_change(f["before"], f["after"], land, wet_db=t)
        storm.append(w.sum() * fm.PIXEL_KM2)
        dry.append(fm.false_alarm_check(f["baseline"], f["before"], land, wet_db=t)[0])
    x = np.arange(len(thr))
    w = 0.38
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.bar(x - w / 2 - 0.01, storm, w, color=STORM, label="Storm (15 to 27 Oct)", zorder=3)
    ax.bar(x + w / 2 + 0.01, dry, w, color=DRY, label="Dry week, no rain (3 to 15 Oct)", zorder=3)
    for i, (s, d) in enumerate(zip(storm, dry)):
        ax.text(i, s + 4, f"{s / d:.1f}×", ha="center", va="bottom", fontsize=15, color=NAVY, weight="bold")
    ax.set_xticks(x, [f"{t:g} dB" + ("\n(used)" if t == 3.0 else "") for t in thr], fontsize=14)
    ax.get_xticklabels()[thr.index(3.0)].set_fontweight("bold")
    ax.set_ylabel("Area flagged as wet (km²)", fontsize=15)
    ax.set_xlabel("Detection threshold (backscatter increase)", fontsize=15)
    ax.tick_params(axis="y", labelsize=13, length=0)
    ax.tick_params(axis="x", length=0)
    ax.grid(axis="y", color="#E2DED4", lw=1, zorder=0)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.set_ylim(0, max(storm) * 1.18)
    ax.legend(frameon=False, fontsize=14, loc="upper right")
    ax.set_title("Storm signal vs dry-week false alarms   (label = signal-to-noise)",
                 fontsize=16, color=NAVY, loc="left", pad=14)
    plt.tight_layout()
    plt.savefig(OUT / "threshold_chart.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    return list(zip(thr, storm, dry))


def top5_zoom(rgb, wet, cells):
    k = 1000 // fm.PIXEL_M
    half = 60  # 60 px * 20 m = 1.2 km each side
    fig, ax = plt.subplots(1, 5, figsize=(22, 5.6))
    for i, (_, r) in enumerate(cells.head(5).iterrows()):
        rr, cc = int(r.grid_row) * k + k // 2, int(r.grid_col) * k + k // 2
        img = np.clip(crop(rgb, rr, cc, half, fill=246).astype("float32") / 255 * 0.9, 0, 1) ** 1.5
        ax[i].imshow(img)
        m = crop(wet, rr, cc, half, fill=False)
        ax[i].imshow(np.ma.masked_where(~m, m), cmap=WET_OVERLAY, alpha=0.8, interpolation="nearest")
        # outline the ranked 1 km cell
        r0 = c0 = half - k // 2
        ax[i].add_patch(plt.Rectangle((c0, r0), k, k, fill=False, ec="#FFD166", lw=2.5))
        ax[i].set_title(f"#{int(r['rank'])}  ·  {r.impact_pct:.1f}% saturated", fontsize=19, weight="bold", color=NAVY, pad=10)
        ax[i].set_xlabel(f"{r.lat:.4f}° N, {r.lon:.4f}° E", fontsize=14, color=INK2, labelpad=8)
        ax[i].set_xticks([]); ax[i].set_yticks([])
        for s in ax[i].spines.values():
            s.set_visible(False)
    plt.tight_layout()
    plt.savefig(OUT / "top5_zoom.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def cover_bg(rgb, wet):
    img = rgb.astype("float32") / 255 * 0.42 + np.array([0.02, 0.05, 0.09])
    blue = np.array([0.18, 0.48, 1.0])
    img[wet] = img[wet] * 0.35 + blue * 0.65
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    h, w = wet.shape
    ax.imshow(np.clip(img, 0, 1)[int(h * 0.22):int(h * 0.22) + int(w * 9 / 16), :], aspect="auto")
    ax.axis("off")
    fig.savefig(OUT / "cover_bg.jpg", dpi=100, pil_kwargs={"quality": 85})
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    f, rgb, land, diff, wet, cells = load()
    radar_before_after(f, land, diff, cells)
    rows = threshold_chart(f, land)
    top5_zoom(rgb, wet, cells)
    cover_bg(rgb, wet)
    for t, s, d in rows:
        print(f"{t:>4} dB  storm {s:6.1f} km2  dry {d:5.1f} km2  S/N {s / d:4.1f}x")
    print("wrote figures to", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

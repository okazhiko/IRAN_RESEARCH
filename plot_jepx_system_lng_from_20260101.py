import os
from datetime import date
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "Merged.csv"
RUN_DATE = os.environ.get("RUN_DATE", date.today().strftime("%Y%m%d"))
OUTPUT_PATH = BASE_DIR / "results" / RUN_DATE / f"{RUN_DATE}_jepx_system_lng_from_20260101.png"
MPLCONFIGDIR = BASE_DIR / ".mplconfig"
START_DATE = pd.Timestamp("2026-01-01")
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"]).rename(
        columns={
            "date": "time",
            "system_price(avg)": "jepx_price",
            "sytem_price(avg)": "jepx_price",
            "LNG(close)": "lng_price",
        }
    )
    filtered_df = df[df["time"] >= START_DATE].copy()
    jepx_df = filtered_df[["time", "jepx_price"]].dropna().sort_values("time")
    lng_df = filtered_df[["time", "lng_price"]].dropna().sort_values("time")

    overlap_start = max(jepx_df["time"].min(), lng_df["time"].min())
    overlap_end = min(jepx_df["time"].max(), lng_df["time"].max())

    jepx_filtered = jepx_df[(jepx_df["time"] >= overlap_start) & (jepx_df["time"] <= overlap_end)]
    lng_filtered = lng_df[(lng_df["time"] >= overlap_start) & (lng_df["time"] <= overlap_end)]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    ax1.plot(jepx_filtered["time"], jepx_filtered["jepx_price"], color="green", linewidth=1.5)
    ax2.plot(lng_filtered["time"], lng_filtered["lng_price"], color="orange", linewidth=1.5)

    ax1.set_title("JEPX System Price and JKM Price")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("JEPX System Price (JPY/kWh)", color="green")
    ax2.set_ylabel("JKM Price(JPY/unit)", color="orange")
    ax1.tick_params(axis="y", labelcolor="green")
    ax2.tick_params(axis="y", labelcolor="orange")
    ax1.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()

import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "Merged.csv"
RUN_DATE = os.environ.get("RUN_DATE", date.today().strftime("%Y%m%d"))
OUTPUT_DIR = BASE_DIR / "results" / RUN_DATE
MPLCONFIGDIR = BASE_DIR / ".mplconfig"
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AREA_NAME_MAP = {
    "中国": "chugoku",
    "中部": "chubu",
    "九州": "kyushu",
    "北海道": "hokkaido",
    "北陸": "hokuriku",
    "四国": "shikoku",
    "東京": "tokyo",
    "東北": "tohoku",
    "関西": "kansai",
}


def main() -> None:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    area_columns = sorted(col for col in df.columns if col.startswith("area_price_"))
    df = df.sort_values("date")

    latest_date = df["date"].max()
    cutoff_date = latest_date - timedelta(days=364)
    filtered_df = df[df["date"] >= cutoff_date].copy()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)

    for area_column in area_columns:
        area = area_column.removeprefix("area_price_")
        area_slug = AREA_NAME_MAP.get(area, str(area).lower())
        area_df = filtered_df[["date", area_column]].dropna().copy()
        if area_df.empty:
            continue

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(area_df["date"], area_df[area_column], color="#1f77b4", linewidth=1.5)
        ax.set_title("JEPX Area Price")
        ax.set_xlabel("Date")
        ax.set_ylabel("Area Price (avg)")
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
        fig.autofmt_xdate()
        fig.tight_layout()
        output_path = OUTPUT_DIR / f"{RUN_DATE}_jepx_{area_slug}.png"
        fig.savefig(output_path, dpi=200)
        plt.close(fig)


if __name__ == "__main__":
    main()

import os
from pathlib import Path
from datetime import date

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "Merged.csv"
RUN_DATE = os.environ.get("RUN_DATE", date.today().strftime("%Y%m%d"))
OUTPUT_PATH = BASE_DIR / "results" / RUN_DATE / f"{RUN_DATE}_oil.png"
MPLCONFIGDIR = BASE_DIR / ".mplconfig"
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"]).rename(
        columns={"date": "time", "OIL(close)": "oil_close"}
    )
    df = df[["time", "oil_close"]].dropna().sort_values("time")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    MPLCONFIGDIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["time"], df["oil_close"], color="#1f77b4", linewidth=1.5)
    ax.set_title("OIL_MATBAROFEX_WTI1! Close Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Close")
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()

#!/bin/zsh

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
RUN_DATE=$(date '+%Y%m%d')
OUTPUT_DIR="$SCRIPT_DIR/results/$RUN_DATE"

mkdir -p "$OUTPUT_DIR"
export RUN_DATE

python3 "$SCRIPT_DIR/plot_oil_close.py"
python3 "$SCRIPT_DIR/plot_jepx_area.py"
python3 "$SCRIPT_DIR/plot_jepx_system_lng.py"
python3 "$SCRIPT_DIR/plot_oil_close_from_20260101.py"
python3 "$SCRIPT_DIR/plot_jepx_system_lng_from_20260101.py"

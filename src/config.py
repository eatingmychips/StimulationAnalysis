from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

VERTICAL_DATA_DIR = DATA_RAW

# Number of Frequencies 
FREQUENCIES = [10, 20, 30, 40, 50]


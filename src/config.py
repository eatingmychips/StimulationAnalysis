from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw" 
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

VERTICAL_DATA_DIR = DATA_RAW / "AllAcrylic"

C0_DIRECTORY = DATA_RAW / "C0"

C3_DIRECTORY = DATA_RAW / "C3"

C4_DIRECTORY = DATA_RAW / "C4"

C9_DIRECTORY = DATA_RAW / "C9"

C10_DIRECTORY = DATA_RAW / "C10"


# Number of Frequencies 
FREQUENCIES = [10, 20, 30, 40, 50]
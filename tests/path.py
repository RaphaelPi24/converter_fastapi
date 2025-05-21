from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES_DIR = PROJECT_ROOT / "tests"
INPUT_DIR = FILES_DIR / "files before conversion"
OUTPUT_DIR = FILES_DIR / "files after conversion"
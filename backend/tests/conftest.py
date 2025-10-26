import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_ROOT = ROOT_DIR.parent

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

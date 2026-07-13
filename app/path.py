from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
IMAGES_DIR = ASSETS_DIR / "images"
DASHBOARD_IMAGES_DIR = IMAGES_DIR / "dashboard"

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

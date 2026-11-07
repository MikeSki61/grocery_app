from pathlib import Path
from platformdirs import user_data_dir, user_config_dir

APP_NAME = "MKL Grocery"
APP_AUTHOR = "Mike Kwiatkowsky"

DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
DATA_FILE = DATA_DIR / "grocery_list.json"
EXPORT_FILE = DATA_DIR / "exported_grocery_list.txt"

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
CONFIG_FILE = CONFIG_DIR / "settings.json"


def ensure_dirs():
    # Data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Config directory
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
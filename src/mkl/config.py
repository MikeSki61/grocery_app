import json
from mkl import constants
from mkl.paths import CONFIG_FILE

DEFAULT_SETTINGS = {
    "store default": constants.STORE_DEFAULT,
    "tax rate": 0.08,
}


def save_settings(settings: dict):
    with CONFIG_FILE.open("w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


def load_settings():
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(data)
        return settings
    
    save_settings(DEFAULT_SETTINGS)
    return DEFAULT_SETTINGS.copy()

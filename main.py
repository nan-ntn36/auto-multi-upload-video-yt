from config.config_loader import load_config
from ui.main_ui import create_main_ui

if __name__ == "__main__":
    config = load_config()
    create_main_ui(config)

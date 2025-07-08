import yaml
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_PATH = Path("config.yaml")

DEFAULT_CONFIG = {
    "app": {
        "name": "SmartThermo",
        "version": "1.0.0",
        "features": ["temperature_control", "remote_access", "energy_saving"],
        "mode": "off",
        "set_point": 70
    },
    "logging": {
        "level": "info",
        "file": "logs/output.log"
    }
}

@dataclass
class SmartThermo:
    name: str
    version: str
    features: list
    mode: str
    set_point: int

    def change_mode(self, new_mode:str):
        print(f"Mode: {self.mode}.")
        if new_mode not in ["off","heat","cool"]:
            raise ValueError("Mode not found (off, heat, cool).")
        print("Mode set!")
        self.mode = new_mode
    
    def update_temp(self, new_temp:int):
        print(f"Temperature: {self.set_point}.")
        if new_temp not in range(18,30):
            raise ValueError("Temperature not found (18-30).")
        print("Temp set!")
        self.set_point = new_temp

    def __str__(self):
        return(f"Name: {self.name}\nVersion: {self.version}\nFeatures: {self.features}\nMode: {self.mode}\nSet point: {self.set_point}")
        
def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as file:
            try:
                return yaml.safe_load(file)["app"]
            except:
                print("Error occurred!")
                return DEFAULT_CONFIG["app"]
    else:
        print("config.yaml not found. Creating with default values...")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        yaml.safe_dump(config, file)
        
def main():
    app_cfg = load_config()
    required_keys = ["name", "version", "features", "mode", "set_point"]
    for key in required_keys:
        if key not in app_cfg:
            raise KeyError(f"Missing required config key: {key}")

    my_thermo = SmartThermo(
    name=app_cfg["name"],
    version=app_cfg["version"],
    features=app_cfg["features"],
    mode=app_cfg["mode"],
    set_point=app_cfg["set_point"])

    my_thermo.update_temp(20)
    print(my_thermo)

    log_cfg = DEFAULT_CONFIG["logging"]
    print(f"Logging: {log_cfg['level']} -> {log_cfg['file']}")
    new_config = {}

    new_config["app"] = {
    "name": my_thermo.name,
    "version": my_thermo.version,
    "features": my_thermo.features,
    "mode": my_thermo.mode,
    "set_point": my_thermo.set_point}

    new_config["logging"] = log_cfg
    save_config(new_config)

if __name__ == "__main__":
    main()

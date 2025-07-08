import yaml
from dataclasses import dataclass, field
from pathlib import Path
import sys, os
from pydantic import BaseModel, ValidationError #Stretch
from typing import List #Stretch
import logging #Stretch
from datetime import datetime
 
env = os.getenv("ENV", "default")  # ENV=dev eg to modify name => ENV=prod python load_config.py
CONFIG_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(f"config-{env}.yaml") #Help w/Chat

DEFAULT_CONFIG = {
    "app": {
        "name": "SmartThermo",
        "version": "1.0.0",
        "features": ["temperature_control", "remote_access", "energy_saving"],
        "mode": "off",
        "set_point": 70,
        "last_modified": datetime.now().isoformat()
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

class AppConfig(BaseModel):
    name: str
    version: str
    features: List[str]
    mode: str
    set_point: int

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r") as file:
            try:
                return yaml.safe_load(file)  # return whole config
            except:
                print("Error occurred!")
                return DEFAULT_CONFIG  # also full config
    else:
        print("config.yaml not found. Creating with default values...")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_PATH, "w") as file:
        yaml.safe_dump(config, file)

def take_actions(my_thermo):
    while True:
        action = input("Choose action [mode/temp/show/exit]: ").strip().lower()
        if action == "mode":
            new_mode = input("Enter mode [off, heat, cool]: ")
            try:
                my_thermo.change_mode(new_mode)
            except ValueError as e:
                print(e)
        elif action == "temp":
            try:
                new_temp = int(input("Enter new temperature (18-30): "))
                my_thermo.update_temp(new_temp)
            except ValueError as e:
                print(e)
        elif action == "show":
            print(my_thermo)
        elif action == "exit":
            break
        else:
            print("Unknown command.")

def main():
    config = load_config()  # FIX: config is now defined before use

    log_cfg = config.get("logging", DEFAULT_CONFIG["logging"])
    logging.basicConfig(
        filename=log_cfg["file"],
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )  # FIX: logging set up after config loaded

    try:
        app_cfg = AppConfig(**config["app"])  # Pydantic validation
    except ValidationError as e:  # FIX: specific exception
        logging.error(f"Invalid config: {e}")
        exit(1)
    
    my_thermo = SmartThermo(
        name=app_cfg.name,
        version=app_cfg.version,
        features=app_cfg.features,
        mode=app_cfg.mode,
        set_point=app_cfg.set_point
    )

    take_actions(my_thermo)

    print(f"Logging: {log_cfg['level']} -> {log_cfg['file']}")

    new_config = {
        "app": {
            "name": my_thermo.name,
            "version": my_thermo.version,
            "features": my_thermo.features,
            "mode": my_thermo.mode,
            "set_point": my_thermo.set_point,
            "last_modified": datetime.now().isoformat()
        },
        "logging": log_cfg
    }

    save_config(new_config)
    print("Config saved!")

if __name__ == "__main__":
    main()
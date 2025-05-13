# dataset_recorder/data_logger.py

import os
import json
from datetime import datetime

class RawDataLogger:
    def __init__(self, username, label, folder="data/recordings"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}_{label}_{timestamp}.json"
        self.filepath = os.path.join(folder, filename)
        os.makedirs(folder, exist_ok=True)
        self.label = label
        self.buffer = []

        print(f" Guardando en: {self.filepath}")

    def log(self, raw_data):
        if "eSense" in raw_data and "eegPower" in raw_data:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "label": self.label,
                "raw": {
                    "eSense": raw_data["eSense"],
                    "eegPower": raw_data["eegPower"],
                    "poorSignalLevel": raw_data.get("poorSignalLevel", -1)
                }
            }
            self.buffer.append(entry)

    def close(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.buffer, f, indent=2, ensure_ascii=False)
        print(f"\n Sesión finalizada. Se guardaron {len(self.buffer)} muestras en {self.filepath}")
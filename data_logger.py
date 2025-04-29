# synapseart/data/data_logger.py
import os
import json
from datetime import datetime

class DataLogger:
    def __init__(self, base_path="data/raw"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        self.log_file = None

    def start_session(self, username: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_folder = os.path.join(self.base_path, username)
        os.makedirs(user_folder, exist_ok=True)
        self.log_file = open(os.path.join(user_folder, f"{timestamp}.jsonl"), "w", encoding="utf-8")
        print(f"Registrando datos en {self.log_file.name}")

    def log(self, raw_data: dict, normalized_data: dict, emotion_data: dict):
        if self.log_file is None:
            raise RuntimeError("Session not started. Llama primero a start_session(username).")
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "raw_eeg": raw_data,
            "normalized_eeg": normalized_data,
            "emotions": emotion_data
        }

        self.log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
        self.log_file.flush()

    def end_session(self):
        if self.log_file:
            self.log_file.close()
            print(" Sesión finalizada y datos guardados.")
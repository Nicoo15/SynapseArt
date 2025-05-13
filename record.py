# record.py
from data_recorder.data_logger import RawDataLogger
from src.devices.neurosky_client import NeuroSkyClient

import json
import time

def main():
    print("🔌 Conectando a la diadema NeuroSky...")
    client = NeuroSkyClient()
    client.connect()
    print(" Conectado a NeuroSky")

    username = input(" Nombre del participante: ").strip()
    emotion = input(" Emoción que está sintiendo: ").strip().lower()

    logger = RawDataLogger(username, emotion)

    try:
        print("\n Grabando datos en crudo... Presiona CTRL+C para detener.")
        while True:
            raw_data = client.read_data()
            if raw_data:
                print(json.dumps(raw_data, indent=2, ensure_ascii=False))
                logger.log(raw_data)
                time.sleep(0.3)
    except KeyboardInterrupt:
        logger.close()
    finally:
        client.close()

if __name__ == "__main__":
    main()
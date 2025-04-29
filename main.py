from src.devices.neurosky_client import NeuroSkyClient
from src.processing.emotion_normalizer import EmotionNormalizer
from src.processing.emotion_classifier import EmotionClassifier
from data_logger import DataLogger

import json
import time

def main():
    print("🔌 Conectando a la diadema NeuroSky...")
    client = NeuroSkyClient()
    client.connect()

    print("Inicializando módulos de procesamiento...")
    normalizer = EmotionNormalizer()
    classifier = EmotionClassifier()
    logger = DataLogger()

    print("Etiqueta la emoción actual del usuario (escribe y pulsa ENTER)")
    print("Opciones: felicidad, tristeza, calma, excitación, preocupación, enfado, depresión, serenidad")
    user_label = input("Etiqueta: ").strip().lower()

    print("\n Grabando datos... Presiona CTRL+C para detener.\n")
    try:
        while True:
            raw_data = client.read_data()
            if not raw_data or "eegPower" not in raw_data:
                continue

            normalized = normalizer.normalize(raw_data)
            emotions = classifier.classify(normalized)

            print(json.dumps(emotions, ensure_ascii=False, indent=2))

            logger.log_data(
                raw_eeg=raw_data,
                normalized=normalized,
                emotions=emotions,
                label=user_label
            )

            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n Grabación detenida por el usuario.")
    finally:
        client.close()

if __name__ == "_main_":
    main()
from src.devices.neurosky_client import NeuroSkyClient
from src.processing.emotion_normalizer import EmotionNormalizer
from src.processing.emotion_classifier import EmotionClassifier
from src.udp_sender import UDPSender

import json
import time

def main():
    print("🔌 Conectando a la diadema NeuroSky...")
    client = NeuroSkyClient()
    client.connect()
    print(" Conectado a NeuroSky")

    print("Inicializando módulos de procesamiento...")
    normalizer = EmotionNormalizer()
    classifier = EmotionClassifier()
    udp_sender = UDPSender(ip='127.0.0.1', port=7000)
    print(" Módulos inicializados")

    print("\nEnviando emociones por UDP... Presiona CTRL+C para detener.\n")

    try:
        while True:
            raw_data = client.read_data()
            if not raw_data or "eegPower" not in raw_data or "eSense" not in raw_data:
                continue

            # Unificar eegPower y eSense en un solo diccionario
            eeg_values = {**raw_data["eegPower"], **raw_data["eSense"]}

            # Normalizar y clasificar
            normalized = normalizer.normalize_all(eeg_values)
            emotions = classifier.classify_emotions(normalized)

            # Imprimir y enviar
            print(json.dumps(emotions, ensure_ascii=False, indent=2))
            udp_sender.send(emotions)


    except KeyboardInterrupt:
        print("\n Conexión finalizada por el usuario.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
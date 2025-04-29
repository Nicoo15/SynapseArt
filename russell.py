#prueba para normalizar emociones correctamete

#en esta clase recibo datos de la diadema , los normalizo y clasifico para imprimir en consola y hacer pruebas de que estan correctos y funcionan correctamente.

# esta clase no envia datos solo es de prueba para ver si los datos que recibo de la diadema son correctos y que funcionan correctamente.

import socket
import json
import time
import numpy as np
from collections import deque

def conectar_neurosky():
    host = '127.0.0.1'
    port = 13854
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall('{"enableRawOutput": true, "format": "Json"}\n'.encode('utf-8'))
    print("Conectado a NeuroSky")
    return sock

class EmotionProcessor:
    def __init__(self, window_size=10):
        self.buffers = {
            'delta': deque(maxlen=window_size),
            'theta': deque(maxlen=window_size),
            'alpha': deque(maxlen=window_size),
            'beta': deque(maxlen=window_size),
            'gamma': deque(maxlen=window_size),
        }
        self.ranges = {
            'delta': (1000, 100000),
            'theta': (1000, 100000),
            'alpha': (1000, 100000),
            'beta': (500, 100000),
            'gamma': (100, 50000)
        }

    def normalize(self, val, band):
        min_val, max_val = self.ranges[band]
        val = max(min_val, min(val, max_val))
        return (val - min_val) / (max_val - min_val) * 100

    def process(self, eeg_data):
        for band in self.buffers:
            self.buffers[band].append(self.normalize(eeg_data.get(band, 0), band))

        delta = np.mean(self.buffers['delta'])
        theta = np.mean(self.buffers['theta'])
        alpha = np.mean(self.buffers['alpha'])
        beta = np.mean(self.buffers['beta'])
        gamma = np.mean(self.buffers['gamma'])

        emociones = {
            "tristeza": round(delta * 0.4 + theta * 0.4, 2),
            "depresion": round(delta * 0.6 + theta * 0.3, 2),
            "calma": round(alpha * 0.5 + theta * 0.3, 2),
            "serenidad": round(alpha * 0.4 + theta * 0.4, 2),
            "felicidad": round(alpha * 0.3 + beta * 0.4 + gamma * 0.3, 2),
            "excitacion": round(beta * 0.4 + gamma * 0.5, 2),
            "preocupacion": round(gamma * 0.6 + beta * 0.3, 2),
            "enfado": round(gamma * 0.4 + beta * 0.3 + delta * 0.3, 2)
        }

        valence = emociones["felicidad"] - emociones["tristeza"] - emociones["depresion"]
        arousal = emociones["excitacion"] + emociones["enfado"] - emociones["calma"] - emociones["serenidad"]

        if valence >= 50 and arousal >= 50:
            estado = "Activa/positiva: excitación y felicidad"
        elif valence >= 50 and arousal < 50:
            estado = "Pasiva/positiva: serenidad y calma"
        elif valence < 50 and arousal < 50:
            estado = "Negativa/pasiva: tristeza y depresión"
        else:
            estado = "Negativa/activa: enfado y preocupación"

        emociones["attention"] = eeg_data.get("attention", 50)
        emociones["meditation"] = eeg_data.get("meditation", 50)
        emociones["calificado_por"] = estado

        return emociones

def main():
    sock = conectar_neurosky()
    processor = EmotionProcessor()

    buffer = b""
    print(" Recibiendo datos... Presiona Ctrl+C para salir.\n")

    try:
        while True:
            data = sock.recv(1024)
            buffer += data
            while b'\r' in buffer:
                line, buffer = buffer.split(b'\r', 1)
                try:
                    json_data = json.loads(line.decode('utf-8'))
                    if 'eegPower' in json_data:
                        eeg = json_data['eegPower']
                        emotions = processor.process(eeg)
                        print(json.dumps(emotions, indent=2))
                except Exception as e:
                    pass
            time.sleep(0.3)
    except KeyboardInterrupt:
        sock.close()
        print("Conexión finalizada.")

if __name__ == "__main__":
    main()



            

# estas emociones son conseguidas gracias a un estudio de la universidad de Stanford que se basa en las bandas cerebrales y como estas afectan a las emociones de las personas.
    # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5938543/
    
    # por ejemplo en la diadema neurosky se mide la actividad de las ondas cerebrales en las bandas delta, theta, alpha, beta y gamma. las cuales se asocian a diferentes estados emocionales.
    #la depresion, porque se activa cuando estamos en un estado de sueño profundo o de meditacion.
    # theta: se asocia con la s delta: se asocia con la tristeza y erenidad y la calma, porque se activa cuando estamos en un estado de relajacion. Por ejemplo cuando estamos meditando.
    # alpha: se asocia con la calma, porque se activa cuando estamos en un estado de relajacion. Por ejemplo cuando estamos meditando. Pero tambien se asocia con la felicidad.
    # beta: se asocia con la felicidad y la excitacion, porque se activa cuando estamos en un estado de felicidad o de excitacion. Por ejemplo cuando estamos haciendo deporte.
    # gamma: se asocia con la felicidad y la excitacion, porque se activa cuando estamos en un estado de felicidad o de excitacion. Por ejemplo cuando estamos haciendo deporte. Pero tambien se asocia con la preocupacion.
    # estos datos son sacados de la pagina de neurosky y de la pagina de la universidad de stanford, y son datos reales que se han sacado de estudios realizados por estas instituciones.
    # https://store.neurosky.com/pages/eeg-band-power-values-explained
    
    # el valor maximo de alpha es 500000, el valor maximo de beta es 500000, el valor maximo de gamma es 1000000, el valor maximo de theta es 300000 y el valor maximo de delta es 1500000.
    # el valor minimo es 0 en todas.

    # Por ello a la hora de normalizar los valores de las bandas cerebrales para clasificar las emociones segun el modelo de Russell, se ha decidido que los valores maximos sean los que se han mencionado anteriormente, comprendido entre 100 valor maximo y 0 valor minimo para clasificar las emociones.

    # la funcion normalizar hace que self min valor sea 0 y self max valor sea 100, y se normaliza el valor de las bandas cerebrales para clasificar las emociones segun el modelo de Russell.
    # la funcion clasificar_emociones se encarga de clasificar las emociones segun el modelo de Russell, y se basa en los valores normalizados de las bandas cerebrales para clasificar las emociones segun el modelo de Russell.
    # estos valores son sacados de estudios realizados por la universidad de stanford y por neurosky, y son datos reales que se han sacado de estos estudios.

    # 
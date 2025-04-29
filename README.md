# SynapseArt

*TFG - Ingeniería del Software*  
Visualización artística de emociones humanas en tiempo real usando EEG y TouchDesigner.

## 🧠 Descripción

Este sistema conecta una diadema NeuroSky MindWave con un sistema de visualización en tiempo real. Las señales cerebrales se procesan y transforman en emociones que se representan visualmente mediante un roble digital.

## 🎯 Objetivos

- Procesar señales EEG en tiempo real.
- Inferir emociones mediante el modelo de Russell.
- Enviar datos emocionales a TouchDesigner vía UDP.
- Almacenar datos etiquetados para entrenar modelos supervisados.

## 📁 Estructura del Proyecto

```plaintext
synapseart/
├── data/
│   └── recordings/            # Donde se guardan los JSON etiquetados
│       └── user_01_2024-03-28.json
├── src/                       # Código fuente de la aplicación
│   ├── __init__.py
│   ├── devices/
│   │   └── neurosky_client.py # Conexión con NeuroSky
│   ├── processing/
│   │   ├── emotion_normalizer.py
│   │   └── emotion_classifier.py
│   ├── utils/
│   │   ├── json_utils.py
│   │   └── udp_sender.py
├── tests/                     # Pruebas unitarias si las necesitas
├── main.py                    # Script principal (envía emociones por UDP)
├── data_logger.py             # Guardado etiquetado en crudo (MVP)
├── russell.py                 # Pruebas de clasificación de emociones
├── sypnase.py                 # Visualización en TouchDesigner
├── requirements.txt           # Librerías necesarias
└── README.md                  # Documentación del proyecto
```


## ⚙️ Ejecución

```bash
python main.py
```
Para guardar datos etiquetados con emociones reales:
```bash
python data_logger.py
```

📡 Formato de salida emocional
{
  "attention": 47,
  "meditation": 47,
  "tristeza": 21,
  "depresion": 15,
  "calma": 50,
  "serenidad": 42,
  "felicidad": 64,
  "excitacion": 52,
  "preocupacion": 31,
  "enfado": 15,
  "clasificacion_global": "Activa/positiva"
}
## 🧠 Modelo de emociones
Basado en el modelo de Russell y referencias científicas de NeuroSky y Stanford:

Activa/positiva: excitación, felicidad

Pasiva/positiva: serenidad, calma

Negativa/pasiva: tristeza, depresión

Negativa/activa: preocupación, enfado

Futura implementacion de modelo IA para clasificacion de emociones.

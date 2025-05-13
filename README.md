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
│   └── recordings/                  # Datos crudos etiquetados por usuario y emoción
│       └── Nico_felicidad_2025-05-13.json
│
├── dataset_recorder/
│   ├── data_logger.py              # Clase que gestiona y guarda sesiones etiquetadas
│   
│
├── src/
│   ├── devices/
│   │   └── neurosky_client.py      # Cliente TCP para recibir datos EEG
│   ├── processing/
│   │   ├── emotion_normalizer.py   # Normaliza valores EEG entre 0 y 100
│   │   └── emotion_classifier.py   # Clasifica emociones con base en EEG y modelo Russell
│   ├── utils/
│   │   ├── json_utils.py           # Utilidades para guardar datos como JSON
│   │   └── udp_sender.py           # Cliente UDP para enviar emociones a TouchDesigner
│   └── __init__.py
│
├── main.py                         # Script principal: procesa y envía emociones por UDP
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Documentación del proyecto
└── record.py                   # Script para grabar sesiones con etiqueta en tiempo real
```


## ⚙️ Ejecución

```bash
python main.py
```
Para guardar datos etiquetados con emociones reales:
```bash
python record.py
```

📡 Formato de salida emocional
```json
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
```
## 🧠 Modelo de emociones
Basado en el modelo de Russell y referencias científicas de NeuroSky y Stanford:

Activa/positiva: excitación, felicidad

Pasiva/positiva: serenidad, calma

Negativa/pasiva: tristeza, depresión

Negativa/activa: preocupación, enfado

Futura implementacion de modelo IA para clasificacion de emociones.

class EmotionClassifier:
    def __init__(self):
        pass

    def classify_emotions(self, eeg):
        # Emociones individuales en escala 0-100
        emociones = {
            "attention": eeg["attention"],
            "meditation": eeg["meditation"],
            "tristeza": int(eeg["delta"] * 0.5 + eeg["theta"] * 0.3),
            "depresion": int(eeg["delta"] * 0.7 + eeg["lowAlpha"] * 0.2),
            "calma": int(eeg["highAlpha"] * 0.5 + eeg["meditation"] * 0.5),
            "serenidad": int(eeg["theta"] * 0.4 + eeg["meditation"] * 0.6),
            "felicidad": int(eeg["highBeta"] * 0.5 + eeg["highGamma"] * 0.5),
            "excitacion": int(eeg["lowBeta"] * 0.5 + eeg["lowGamma"] * 0.5),
            "preocupacion": int(eeg["lowGamma"] * 0.6 + eeg["delta"] * 0.4),
            "enfado": int(eeg["highBeta"] * 0.6 + eeg["lowGamma"] * 0.4)
        }

        # Etiqueta general basada en Russell
        etiqueta = self.categorize_russell(emociones)

        return emociones | {"categoria_russell": etiqueta}

    def categorize_russell(self, emo):
        # Clasificación según máximos dominantes
        etiquetas = {
            "Activa/positiva": emo["felicidad"] + emo["excitacion"],
            "Pasiva/positiva": emo["serenidad"] + emo["calma"],
            "Negativa/pasiva": emo["tristeza"] + emo["depresion"],
            "Negativa/activa": emo["enfado"] + emo["preocupacion"]
        }
        return max(etiquetas, key=etiquetas.get)
class EmotionClassifier:
    def __init__(self):
        pass

    def classify_emotions(self, eeg):
        # Emociones individuales en escala 0-100
        emociones = {
            "attention": eeg["attention"],
            "meditation": eeg["meditation"],
            "tristeza": round(eeg["delta"] * 0.5 + eeg["theta"] * 0.3, 2),
            "depresion": round(eeg["delta"] * 0.7 + eeg["lowAlpha"] * 0.2, 2),
            "calma": round(eeg["highAlpha"] * 0.5 + eeg["meditation"] * 0.5, 2),
            "serenidad": round(eeg["theta"] * 0.4 + eeg["meditation"] * 0.6, 2),
            "felicidad": round(eeg["highBeta"] * 0.5 + eeg["highGamma"] * 0.5, 2),
            "excitacion": round(eeg["lowBeta"] * 0.5 + eeg["lowGamma"] * 0.5, 2),
            "preocupacion": round(eeg["lowGamma"] * 0.6 + eeg["delta"] * 0.4, 2),
            "enfado": round(eeg["highBeta"] * 0.6 + eeg["lowGamma"] * 0.4, 2)
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
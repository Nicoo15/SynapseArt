class EmotionNormalizer:
    def __init__(self):
        # Rango estimado de valores reales según documentación y pruebas
        self.ranges = {
            'delta': (10000, 300000),
            'theta': (5000, 80000),
            'lowAlpha': (3000, 60000),
            'highAlpha': (2000, 40000),
            'lowBeta': (1000, 25000),
            'highBeta': (1000, 15000),
            'lowGamma': (500, 10000),
            'highGamma': (500, 10000),
            'attention': (0, 100),
            'meditation': (0, 100)
        }

    def normalize(self, val, band_type):
        min_val, max_val = self.ranges.get(band_type, (0, 100))
        val = max(min_val, min(val, max_val))
        return round((val - min_val) / (max_val - min_val) * 100, 2)

    def normalize_all(self, eeg_data):
        normalized = {}
        for key, val in eeg_data.items():
            normalized[key] = self.normalize(val, key)
        return normalized
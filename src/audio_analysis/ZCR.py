# src/audio_analysis/ZCR.py
# ゼロ交差率（音のざらつき・子音感）

import numpy as np
import librosa

def calc_zcr(segment):
    if len(segment) == 0:
        return 0.0

    zcr = librosa.feature.zero_crossing_rate(segment)

    return float(np.mean(zcr))
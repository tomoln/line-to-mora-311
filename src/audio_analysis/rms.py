import numpy as np
import librosa

# RMS（音量）

def calc_rms(segment):
    if len(segment) == 0:
        return 0.0

    rms = np.mean(librosa.feature.rms(y=segment))
    return float(rms)
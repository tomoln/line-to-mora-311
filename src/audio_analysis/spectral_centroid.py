# src/audio_analysis/spectral_centroid.py
# スペクトル重心（音の明るさ）

import numpy as np
import librosa

def calc_spectral_centroid(segment, sr):
    if len(segment) == 0:
        return 0.0

    centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)

    return float(np.mean(centroid))
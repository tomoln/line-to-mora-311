import numpy as np
import librosa

# F0（ピッチ）

def calc_f0(segment):
    if len(segment) == 0:
        return 0.0

    f0, _, _ = librosa.pyin(
        segment,
        fmin=librosa.note_to_hz("C2"),
        fmax=librosa.note_to_hz("C7")
    )

    if f0 is None:
        return 0.0

    f0_clean = f0[~np.isnan(f0)]
    return float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0.0
# src/audio_analysis/librosa_v.py
# モーラごとの音声特徴量を抽出するコード

import librosa

from .duration import calc_duration
from .rms import calc_rms
from .f0 import calc_f0
from .spectral_centroid import calc_spectral_centroid
from .ZCR import calc_zcr
from src.whisper.whisper_audio_to_str import find_input_wav

INPUT_PATH = "confirm/010_mora_to_japanese.txt"
OUTPUT_PATH = "confirm/011_add_audio_parameters.txt"


def load_mora_file(path):
    moras = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 3:
                continue

            text, start, end = parts
            moras.append({
                "text": text,
                "start": float(start),
                "end": float(end)
            })
    return moras


def extract_features(y, sr, start, end):
    start_sample = int(start * sr)
    end_sample = int(end * sr)

    segment = y[start_sample:end_sample]

    return {
        "duration": calc_duration(start, end),
        "rms": calc_rms(segment),
        "f0": calc_f0(segment),
        "spectral_centroid": calc_spectral_centroid(segment, sr),
        "zcr": calc_zcr(segment)
    }


def save_results(moras, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# text start(s) end(s) duration(s) rms f0(Hz) spectral_centroid(Hz) zcr\n")

        for m in moras:
            line = f"{m['text']} {m['start']:.3f} {m['end']:.3f} "
            line += f"{m['duration']:.3f} {m['rms']:.5f} {m['f0']:.2f} "
            line += f"{m['spectral_centroid']:.2f} {m['zcr']:.5f}\n"
            f.write(line)


def run_librosa_analysis():
    y, sr = librosa.load(find_input_wav(), sr=None)
    moras = load_mora_file(INPUT_PATH)

    results = []
    for m in moras:
        feat = extract_features(y, sr, m["start"], m["end"])
        results.append({**m, **feat})

    save_results(results, OUTPUT_PATH)
    return results
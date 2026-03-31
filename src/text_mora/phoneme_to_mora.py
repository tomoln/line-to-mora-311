# src/text_mora/phoneme_to_mora.py
# MFAのタイムスタンプ付き音素列をモーラに変換するコード

import os

VOWELS = {"a", "i", "u", "e", "o"}
SPECIAL_MORA = {"N", "cl"}  # 撥音・促音


def load_mfa_timestamp(path="confirm/008_text_mfa_timestamp.txt"):
    phonemes = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            p, start, end = line.strip().split()
            phonemes.append((p, float(start), float(end)))
    return phonemes


def phoneme_to_mora(phonemes):
    moras = []
    i = 0

    while i < len(phonemes):
        p, start, end = phonemes[i]

        # ===== 母音だけ（aなど） =====
        if p in VOWELS:
            moras.append((p, start, end))
            i += 1
            continue

        # ===== 撥音・促音 =====
        if p in SPECIAL_MORA:
            moras.append((p, start, end))
            i += 1
            continue

        # ===== 子音 → 次が母音なら結合 =====
        if i + 1 < len(phonemes):
            next_p, next_start, next_end = phonemes[i + 1]

            if next_p in VOWELS:
                mora = p + next_p
                moras.append((mora, start, next_end))
                i += 2
                continue

        # ===== フォールバック（単体） =====
        moras.append((p, start, end))
        i += 1

    return moras


def save_mora(moras, path="confirm/009_text_to_mora.txt"):
    os.makedirs("confirm", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for mora, start, end in moras:
            f.write(f"{mora} {start:.3f} {end:.3f}\n")

    print("mora saved →", path)


def run_phoneme_to_mora():
    phonemes = load_mfa_timestamp()
    moras = phoneme_to_mora(phonemes)
    save_mora(moras)
    return moras   # ← これ追加
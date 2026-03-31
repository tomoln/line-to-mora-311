# src/text_mora/phoneme_to_mora.py
# MFAの音素タイムスタンプ → モーラ変換（メモリ対応版）

import os

# ===== 定義 =====
VOWELS = {"a", "i", "u", "e", "o"}
SPECIAL_MORA = {"N", "cl"}  # 撥音・促音


# ===== フォールバック用（確認ファイル読み込み）=====
def load_mfa_timestamp(path="confirm/008_text_mfa_timestamp.txt"):
    phonemes = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            p, start, end = line.strip().split()
            phonemes.append((p, float(start), float(end)))

    return phonemes


# ===== 音素 → モーラ変換 =====
def phoneme_to_mora(phonemes):
    moras = []
    i = 0

    while i < len(phonemes):
        p, start, end = phonemes[i]

        # ===== 母音単体 =====
        if p in VOWELS:
            moras.append((p, start, end))
            i += 1
            continue

        # ===== 撥音・促音 =====
        if p in SPECIAL_MORA:
            moras.append((p, start, end))
            i += 1
            continue

        # ===== 子音 + 母音 =====
        if i + 1 < len(phonemes):
            next_p, next_start, next_end = phonemes[i + 1]

            if next_p in VOWELS:
                mora = p + next_p
                moras.append((mora, start, next_end))
                i += 2
                continue

        # ===== フォールバック（単体）=====
        moras.append((p, start, end))
        i += 1

    return moras


# ===== 保存 =====
def save_mora(moras, path="confirm/009_text_to_mora.txt"):
    os.makedirs("confirm", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for mora, start, end in moras:
            f.write(f"{mora} {start:.3f} {end:.3f}\n")

    print("mora saved →", path)


# ===== 実行関数（メモリ優先）=====
def run_phoneme_to_mora(phonemes=None):
    # メモリ優先
    if phonemes is None:
        print("⚠️ fallback: loading from file")
        phonemes = load_mfa_timestamp()

    moras = phoneme_to_mora(phonemes)
    save_mora(moras)

    return moras


# ===== 単体実行用 =====
if __name__ == "__main__":
    result = run_phoneme_to_mora()

    print("\n--- preview ---")
    for r in result[:10]:
        print(r)
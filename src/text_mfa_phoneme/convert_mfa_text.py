# text_mfa_phoneme/convert_mfa_text.py
# 音素をMFA形式に変換するためのコード

import os
from .phoneme_map import PHONEME_MAP

def convert_to_mfa(phoneme_str: str) -> str:
    tokens = phoneme_str.split()

    converted = []
    for p in tokens:
        if p in PHONEME_MAP:
            converted.append(PHONEME_MAP[p])
        else:
            print(f"[WARN] 未定義音素: {p}")
            converted.append("spn")  # 安全対応

    return " ".join(converted)


def convert_and_save(phoneme_str: str, filename: str = "007_text_mfa_phoneme.txt"):
    mfa_phoneme = convert_to_mfa(phoneme_str)

    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(mfa_phoneme)

    print("mfa→", mfa_phoneme)

    return mfa_phoneme
# text_clean/no_noise_neologdn.py
# 前段の結果を取得して、neologdnで整形する関数を定義

from src.text_normalize.unicodedata_Normalize import normalize_text
from src.text_replace.correct_text import correct_text
import neologdn
import os

def save_confirm_text(filename: str, text: str):
    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def clean_text(audio_path: str) -> str:
    # ① 正規化
    text = normalize_text(audio_path)

    # ② 辞書置換 ← ★ここ追加
    text = correct_text(text)

    # ★ ここ追加（確認用保存）
    save_confirm_text("003_text_replace.txt", text)

    # ③ neologdnで整形
    text = neologdn.normalize(text)

    save_confirm_text("004_text_clean.txt", text)

    return text

def main():
    audio_path = "input/001.wav"
    cleaned = clean_text(audio_path)
    print("cleaned→", cleaned)

if __name__ == "__main__":
    main()
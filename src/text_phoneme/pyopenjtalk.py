# text_phoneme/pyopenjtalk.py
# pyopenjtalkを利用して、カナから音素への変換を行う。

import os
import pyopenjtalk

# 既存のカナ生成を利用
from src.text_to_kana.fugashi_yomi import text_to_kana
from src.text_mfa_phoneme.convert_mfa_text import convert_and_save


def kana_to_phoneme():
    """
    ① 音声 → テキスト（clean済）
    ② テキスト → カナ（fugashi）
    ③ カナ → 音素（pyopenjtalk）
    ④ 保存
    """

    audio_path = "input/001.wav"

    # ①② カナ取得
    kana_text = text_to_kana(audio_path)

    # ③ 音素変換
    phoneme = pyopenjtalk.g2p(kana_text)
    print("phoneme→", phoneme)

    # ④ 保存
    save_text("006_text_phoneme.txt", phoneme)

    # ⑤ MFA変換＋保存（丸投げ）
    convert_and_save(phoneme)


def save_text(filename: str, text: str):
    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
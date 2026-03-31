# main.py
# 全体の流れを管理するコード

from src.text_phoneme.pyopenjtalk import kana_to_phoneme
from src.text_mfa_phoneme.convert_mfa_text import convert_and_save
from src.text_mfa_timestamp.Montreal_Forced_Aligner import run_mfa_alignment


def main():
    phoneme_str = kana_to_phoneme()  # 006を返す想定
    convert_and_save(phoneme_str)    # 007生成
    run_mfa_alignment()              # 008生成


if __name__ == "__main__":
    main()
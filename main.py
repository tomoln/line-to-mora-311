# main.py
# 全体の流れを管理するコード

from src.text_phoneme.pyopenjtalk import kana_to_phoneme
from src.text_mfa_phoneme.convert_mfa_text import convert_and_save
from src.text_mfa_timestamp.Montreal_Forced_Aligner import run_mfa_alignment
from src.text_mora.phoneme_to_mora import run_phoneme_to_mora
from src.text_mora_jp.mora_to_japanese import run_mora_to_japanese
from src.audio_analysis.librosa_v import run_librosa_analysis


def main():
    phoneme_str = kana_to_phoneme()   # 006
    convert_and_save(phoneme_str)     # 007
    phonemes = run_mfa_alignment()    # ← ★受け取る（重要）
    moras = run_phoneme_to_mora(phonemes)  # ← ★渡す
    run_mora_to_japanese(moras)
    run_librosa_analysis()


if __name__ == "__main__":
    main()
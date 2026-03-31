# src/audio_table/run_audio_table_pipeline.py
# textgrid → 単語分割 → モーラマージ → JSON化 まで一気に実行

from src.audio_table.textgrid_sep import main as run_textgrid_sep
from src.audio_table.merge_word_and_mora import main as run_merge
from src.audio_table.txt_to_json import txt_to_json as run_txt_to_json


def main():
    print("=== Step 1: TextGrid → 単語抽出 ===")
    run_textgrid_sep()

    print("=== Step 2: 単語 × モーラ マージ ===")
    run_merge()

    print("=== Step 3: JSON変換 ===")
    run_txt_to_json()

    print("=== 完了 ===")


if __name__ == "__main__":
    main()
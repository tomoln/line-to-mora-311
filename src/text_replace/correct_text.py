# src/text_correct/correct_text.py

from src.text_replace.loader import load_replace_dict

REPLACE_DICT = load_replace_dict("dict/replace_dict.txt")


def correct_text(text: str) -> str:
    for wrong, correct in REPLACE_DICT.items():
        text = text.replace(wrong, correct)
    return text
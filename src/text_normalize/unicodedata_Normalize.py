# text_normalize/unicodedata_Normalize.py
# unicodedataを使ってテキストを正規化するコード

from src.whisper.whisper_audio_to_str import Whisper_audio_to_str, find_input_wav
import unicodedata
import os

def save_confirm_text(filename: str, text: str):
    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def normalize_text(audio_path: str) -> str:
    # whisper/whisper_audio_to_str.py の Whisper_audio_to_str を呼ぶ
    text = Whisper_audio_to_str(audio_path)
    text = unicodedata.normalize("NFKC", text)
    
    save_confirm_text("002_text_normalize.txt", text) 

    return text

def main():
    audio_path = find_input_wav()
    normalized = normalize_text(audio_path)
    print("normalized→", normalized)

if __name__ == "__main__":
    main()
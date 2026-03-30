# whisper/whisper_audio_to_str.py
# whisperを使用して音声ファイルをテキストに変換する関数を定義

import whisper
import os

# モデルは外に出して高速化
model = whisper.load_model("small")


def Whisper_audio_to_str(audio_path: str) -> str:
    result = model.transcribe(audio_path, language="ja")
    text = result["text"]

    # 👇 confirmフォルダに保存
    save_confirm_text("001_whisper.txt", text)

    return text


def save_confirm_text(filename: str, text: str):
    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    audio_path = os.path.join("input", "001.wav")
    text = Whisper_audio_to_str(audio_path)
    print(text)
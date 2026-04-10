# whisper/whisper_audio_to_str.py
# whisperを使用して音声ファイルをテキストに変換する関数を定義

import whisper
import os
import glob

# モデルは外に出して高速化
model = whisper.load_model("small")


def find_input_wav(input_dir: str = "input") -> str:
    files = glob.glob(os.path.join(input_dir, "*.wav"))
    if len(files) == 0:
        raise FileNotFoundError(f"{input_dir} にwavファイルが見つかりません")
    if len(files) > 1:
        raise ValueError(f"{input_dir} にwavファイルが複数あります: {files}")
    return files[0]


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
    audio_path = find_input_wav()
    text = Whisper_audio_to_str(audio_path)
    print(text)
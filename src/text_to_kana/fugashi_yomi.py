# text_to_kana/fugashi_yomi.py
# fugashiを使ってテキストをカタカナに変換するコード

from src.text_clean.no_noise_neologdn import clean_text
from src.whisper.whisper_audio_to_str import find_input_wav
from fugashi import Tagger
import os

tagger = Tagger()

def text_to_kana(audio_path: str) -> str:
    # text_clean/no_noise_neologdn.py の clean_text を呼び出して、テキストをきれいにする
    text = clean_text(audio_path)

    result = []

    for word in tagger(text):
        # UniDicは feature に読みが入ってる
        kana = word.feature.kana

        if kana is None:
            # 読みが取れない場合はそのまま
            result.append(word.surface)
        else:
            result.append(kana)

    return "".join(result)

def save_confirm_text(filename: str, text: str):
    os.makedirs("confirm", exist_ok=True)
    path = os.path.join("confirm", filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    audio_path = find_input_wav()
    kana_text = text_to_kana(audio_path)
    print("kana→", kana_text)

    save_confirm_text("005_text_to_kana.txt", kana_text) 

if __name__ == "__main__":
    main()
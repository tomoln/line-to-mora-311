# audio_table/txt_to_json.py
# 単語・モーラのテキストファイルをJSONに変換

import json
import os

INPUT_PATH = "confirm/012_merge_word_and_mora.txt"
OUTPUT_PATH = "out_json/out.json"


def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0


def safe_int(v):
    try:
        return int(v)
    except:
        return None


def txt_to_json():
    results = []
    current_word = None

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # ヘッダー除外
    for line in lines[1:]:
        cols = line.rstrip("\n").split("\t")

        # カラム数揃える（空欄対策）
        cols += [""] * (14 - len(cols))

        (
            slice_id,
            word_id,
            word,
            word_start,
            word_end,
            mora_id,
            mora,
            mora_start,
            mora_end,
            duration,
            rms,
            f0,
            centroid,
            zcr,
        ) = cols

        # 新しい単語開始
        if word_id != "":
            current_word = {
                "word_id": safe_int(word_id),
                "word": word,
                "start": safe_float(word_start),
                "end": safe_float(word_end),
                "moras": []
            }
            results.append(current_word)

        # モーラ追加
        if current_word is not None:
            current_word["moras"].append({
                "slice_id": safe_int(slice_id),
                "mora_id": safe_int(mora_id),
                "text": mora,
                "start": safe_float(mora_start),
                "end": safe_float(mora_end),
                "duration": safe_float(duration),
                "rms": safe_float(rms),
                "f0": safe_float(f0),
                "spectral_centroid": safe_float(centroid),
                "zcr": safe_float(zcr),
            })

    # 出力ディレクトリ作成
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"saved -> {OUTPUT_PATH}")


if __name__ == "__main__":
    txt_to_json()
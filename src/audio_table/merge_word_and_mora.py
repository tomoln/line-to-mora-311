# src/audio_table/merge_word_and_mora.py
# 単語（TextGrid）とモーラ（音響特徴量）をマージする

import os


TEXTGRID_PATH = "src/audio_table/textgrid_sep.txt"
MORA_PATH = "confirm/011_add_audio_parameters.txt"
OUTPUT_PATH = "confirm/012_merge_word_and_mora.txt"


def load_words(path):
    words = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines[1:]:  # ヘッダー除外
        line = line.strip()
        if not line:
            continue

        xmin, xmax, text = line.split(",", 2)

        xmin = float(xmin)
        xmax = float(xmax)
        text = text.strip()

        if text == "":
            continue  # 空白はスキップ

        words.append({
            "start": xmin,
            "end": xmax,
            "text": text
        })

    return words


def load_moras(path):
    moras = []
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()

        mora = parts[0]
        start = float(parts[1])
        end = float(parts[2])
        duration = float(parts[3])
        rms = float(parts[4])
        f0 = float(parts[5])
        sc = float(parts[6])
        zcr = float(parts[7])

        moras.append({
            "mora": mora,
            "start": start,
            "end": end,
            "duration": duration,
            "rms": rms,
            "f0": f0,
            "sc": sc,
            "zcr": zcr
        })

    return moras


def merge(words, moras):
    results = []

    slice_id = 1
    word_id = 1
    mora_index = 0

    for word in words:
        word_start = word["start"]
        word_end = word["end"]
        word_text = word["text"]

        mora_id = 1
        first_in_word = True

        # この単語に属するモーラを処理
        while mora_index < len(moras):
            mora = moras[mora_index]

            # モーラが単語より前ならスキップ（基本起きない想定）
            if mora["end"] <= word_start:
                mora_index += 1
                continue

            # モーラが単語の外に出たら次の単語へ
            if mora["start"] >= word_end:
                break

            # 単語内のモーラ
            row = []

            # slice ID
            row.append(str(slice_id))

            # 単語情報（最初のモーラだけ）
            if first_in_word:
                row.append(str(word_id))
                row.append(word_text)
                row.append(f"{word_start}")
                row.append(f"{word_end}")
                first_in_word = False
            else:
                row.extend(["", "", "", ""])

            # モーラ情報
            row.append(str(mora_id))
            row.append(mora["mora"])
            row.append(f"{mora['start']}")
            row.append(f"{mora['end']}")
            row.append(f"{mora['duration']}")
            row.append(f"{mora['rms']}")
            row.append(f"{mora['f0']}")
            row.append(f"{mora['sc']}")
            row.append(f"{mora['zcr']}")

            results.append("\t".join(row))

            # 更新
            slice_id += 1
            mora_id += 1
            mora_index += 1

        word_id += 1

    return results


def save(path, lines):
    header = [
        "slice ID",
        "単語ID",
        "単語",
        "単語スタートタイム(s)",
        "単語エンドタイム(s)",
        "モーラID",
        "モーラ",
        "モーラスタートタイム(s)",
        "モーラエンドタイム(s)",
        "duration(s)",
        "rms",
        "f0(Hz)",
        "spectral_centroid(Hz)",
        "zcr"
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(header) + "\n")
        for line in lines:
            f.write(line + "\n")


def main():
    words = load_words(TEXTGRID_PATH)
    moras = load_moras(MORA_PATH)

    merged = merge(words, moras)
    save(OUTPUT_PATH, merged)

    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
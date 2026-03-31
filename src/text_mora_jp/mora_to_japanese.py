# text_mora_jp/mora_to_japanese.py
# モーラ → 日本語表記変換

import os

# ===== IPA → 擬似ローマ字 =====
def normalize_ipa(mora):
    mora = mora.replace("ː", "")

    mora = mora.replace("ɴ", "N")
    mora = mora.replace("ŋ", "N")
    mora = mora.replace("ɯ", "u")

    mora = mora.replace("ɕ", "sh")
    mora = mora.replace("tɕ", "ch")
    mora = mora.replace("dʑ", "j")
    mora = mora.replace("ɾ", "r")
    mora = mora.replace("ɡ", "g")
    mora = mora.replace("ç", "h")
    mora = mora.replace("c", "h")
    mora = mora.replace("ɲ", "ny")
    mora = mora.replace("j", "y")

    return mora

# ===== テキスト辞書読み込み =====
def load_mora_map(path="src/text_mora_jp/mora_map.txt"):
    mora_map = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # コメント・空行スキップ
            if not line or line.startswith("#"):
                continue

            key, value = line.split()
            mora_map[key] = value

    return mora_map


# ===== モーラ → かな =====
def mora_to_japanese(moras):
    mora_map = load_mora_map()

    result = []

    for mora, start, end in moras:
        norm = normalize_ipa(mora)
        jp = mora_map.get(norm)

        if jp is None:
            print("未変換:", mora, "→", norm)
            jp = norm

        result.append((jp, start, end))

    return result


# ===== 保存 =====
def save_japanese_mora(moras, path="confirm/010_mora_to_japanese.txt"):
    os.makedirs("confirm", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for mora, start, end in moras:
            f.write(f"{mora} {start:.3f} {end:.3f}\n")

    print("japanese mora saved →", path)


# ===== 実行 =====
def run_mora_to_japanese(moras):
    jp_moras = mora_to_japanese(moras)
    save_japanese_mora(jp_moras)
    return jp_moras
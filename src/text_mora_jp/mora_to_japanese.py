import os

# ===== IPA → 擬似ローマ字 =====
def normalize_ipa(mora):
    # 長音削除
    mora = mora.replace("ː", "")

    # 鼻音
    mora = mora.replace("ɴ", "N")
    mora = mora.replace("ŋ", "N")
    mora = mora.replace("ɰ̃", "u")
    mora = mora.replace("̃", "")

    # 母音
    mora = mora.replace("ɯ", "u")
    mora = mora.replace("ɨ", "u")

    # 子音
    mora = mora.replace("ɕ", "sh")
    mora = mora.replace("tɕ", "ch")
    mora = mora.replace("dʑ", "j")
    mora = mora.replace("ɾ", "r")
    mora = mora.replace("ɡ", "g")
    mora = mora.replace("ɸ", "h")
    mora = mora.replace("ç", "h")
    mora = mora.replace("ɲ", "ny")
    mora = mora.replace("ʲ", "y")

    return mora


# ===== IPAモーラ → かな =====
MORA_MAP = {
    # 母音
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",

    # k
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",

    # s
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",

    # t
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",

    # n
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",

    # h
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",

    # m
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",

    # y
    "ya": "や", "yu": "ゆ", "yo": "よ",

    # r
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",

    # w
    "wa": "わ", "wo": "を",

    # g
    "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",

    # z/j
    "za": "ざ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",

    # d
    "da": "だ", "de": "で", "do": "ど",

    # b
    "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",

    # p
    "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",

    # ===== 拗音 =====
    "sha": "しゃ", "shu": "しゅ", "sho": "しょ",
    "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
    "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
    "ja": "じゃ", "ju": "じゅ", "jo": "じょ",
    "bya": "びゃ", "byu": "びゅ", "byo": "びょ",
    "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",

    # 特殊
    "N": "ん",
    "cl": "っ",
}


# ===== ③ モーラ → かな =====
def mora_to_japanese(moras):
    result = []

    for mora, start, end in moras:
        norm = normalize_ipa(mora)

        jp = MORA_MAP.get(norm)

        # デバッグ（超重要）
        if jp is None:
            print("未変換:", mora, "→", norm)
            jp = norm  # fallback

        result.append((jp, start, end))

    return result


# ===== ④ 保存 =====
def save_japanese_mora(moras, path="confirm/010_mora_to_japanese.txt"):
    os.makedirs("confirm", exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        for mora, start, end in moras:
            f.write(f"{mora} {start:.3f} {end:.3f}\n")

    print("japanese mora saved →", path)


# ===== ⑤ 実行 =====
def run_mora_to_japanese(moras):
    jp_moras = mora_to_japanese(moras)
    save_japanese_mora(jp_moras)
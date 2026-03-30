# src/text_mfa_phoneme/phoneme_map.py

PHONEME_MAP = {
    # 母音
    "a": "a", "i": "i", "u": "u", "e": "e", "o": "o",
    "I": "i", "U": "u",

    # 子音
    "k": "k", "g": "g",
    "s": "s", "sh": "sh", "z": "z", "j": "j",
    "t": "t", "ch": "ch", "ts": "ts",
    "d": "d",
    "n": "n", "N": "N",
    "h": "h", "f": "f",
    "b": "b", "p": "p",
    "m": "m", "y": "y", "r": "r", "w": "w",

    # 拗音
    "ky": "ky", "gy": "gy",
    "ny": "ny", "hy": "hy",
    "by": "by", "py": "py",
    "my": "my", "ry": "ry",

    # 追加（実戦用）
    "v": "v",
    "dy": "dy", "ty": "ty",
    "gw": "gw", "kw": "kw",

    # 特殊
    "cl": "q",
    "pau": "sil",
    "sil": "sil",
}
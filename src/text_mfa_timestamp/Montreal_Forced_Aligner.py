# text_mfa_timestamp/Montreal_Forced_Aligner.py
# Montreal Forced Aligner を使って音素のタイムスタンプを取得するコード

import os
import subprocess


def run_mfa_alignment():
    # ===== パス設定 =====
    wav_path = "input/001.wav"
    text_path = "confirm/004_text_clean.txt"

    corpus_dir = "mfa_tmp/corpus"
    output_dir = "mfa_tmp/output"

    os.makedirs(corpus_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("confirm", exist_ok=True)

    # ===== MFA用 corpus 構成 =====
    # MFAは wav + 同名 txt が必要
    wav_dst = os.path.join(corpus_dir, "001.wav")
    txt_dst = os.path.join(corpus_dir, "001.lab")

    # コピー
    import shutil
    shutil.copy(wav_path, wav_dst)
    shutil.copy(text_path, txt_dst)

    # ===== MFA 実行 =====
    # ※事前に acoustic model / dictionary は用意必要
    command = [
        "mfa",
        "align",
        corpus_dir,
        r"C:\Users\k.uehara\Documents\MFA\pretrained_models\dictionary\japanese_mfa.dict",
        r"C:\Users\k.uehara\Documents\MFA\pretrained_models\acoustic\japanese_mfa.zip",
        output_dir,
        "--clean",
        "--overwrite"
    ]

    subprocess.run(command, check=True)

    # ===== 結果取得（TextGrid）=====
    tg_path = os.path.join(output_dir, "001.TextGrid")

    # 簡易パース（必要最低限）
    timestamps = []
    with open(tg_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if "intervals [" in line:
            xmin = float(lines[i+1].split("=")[1].strip())
            xmax = float(lines[i+2].split("=")[1].strip())
            text = lines[i+3].split("=")[1].strip().replace('"', '')

            if text != "":
                timestamps.append(f"{text} {xmin:.3f} {xmax:.3f}")

    # ===== 保存 =====
    out_path = "confirm/008_text_mfa_timestamp.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(timestamps))

    print("timestamp saved →", out_path)
# text_mfa_timestamp/Montreal_Forced_Aligner.py
# Montreal Forced Aligner を使って音素タイムスタンプを取得（メモリ + ファイル出力）

import os
import subprocess
import shutil

from src.whisper.whisper_audio_to_str import find_input_wav


def run_mfa_alignment():
    # ===== パス設定 =====
    wav_path = find_input_wav()
    text_path = "confirm/004_text_clean.txt"

    corpus_dir = "mfa_tmp/corpus"
    output_dir = "mfa_tmp/output"

    os.makedirs(corpus_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("confirm", exist_ok=True)

    # ===== MFA用 corpus 構成 =====
    wav_dst = os.path.join(corpus_dir, "001.wav")
    txt_dst = os.path.join(corpus_dir, "001.lab")

    shutil.copy(wav_path, wav_dst)
    shutil.copy(text_path, txt_dst)

    # ===== MFA 実行 =====
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

    print("Running MFA alignment...")
    subprocess.run(command, check=True)

    # ===== TextGrid 読み込み =====
    tg_path = os.path.join(output_dir, "001.TextGrid")

    if not os.path.exists(tg_path):
        raise FileNotFoundError(f"TextGrid not found: {tg_path}")

    with open(tg_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # ===== phoneme（phones tier）抽出 =====
    timestamps = []
    in_phone_tier = False

    for i, line in enumerate(lines):
        line = line.strip()

        # --- tier判定 ---
        if 'name = "phones"' in line:
            in_phone_tier = True
            continue

        if 'name =' in line and 'phones' not in line:
            in_phone_tier = False

        if not in_phone_tier:
            continue

        # --- interval抽出 ---
        if line.startswith("intervals ["):
            xmin = float(lines[i + 1].split("=")[1].strip())
            xmax = float(lines[i + 2].split("=")[1].strip())
            text = lines[i + 3].split("=")[1].strip().replace('"', '')

            # 無音除外
            if text in ["", "sil", "sp"]:
                continue

            timestamps.append((text, xmin, xmax))

    # ===== 確認用ファイル出力 =====
    out_path = "confirm/008_text_mfa_timestamp.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        for p, s, e in timestamps:
            f.write(f"{p} {s:.3f} {e:.3f}\n")

    print("timestamp saved →", out_path)

    # ===== メモリ返却 =====
    return timestamps


# ===== 単体実行用 =====
if __name__ == "__main__":
    result = run_mfa_alignment()
    print("\n--- preview ---")
    for r in result[:10]:
        print(r)
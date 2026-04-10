# mp3ファイルをwavファイルに変換するスクリプト
# ffmpegがインストールされていることを前提としています。

import subprocess

import os

input_file = "benri-tools/g_22.mp3"
output_file = os.path.splitext(input_file)[0] + ".wav"

subprocess.run([
    "ffmpeg",
    "-i", input_file,
    output_file
], check=True)

print("変換完了！")
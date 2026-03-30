# mp3ファイルをwavファイルに変換するスクリプト
# ffmpegがインストールされていることを前提としています。

import subprocess

input_file = "input.mp3"
output_file = "output.wav"

subprocess.run([
    "ffmpeg",
    "-i", input_file,
    output_file
], check=True)

print("変換完了！")
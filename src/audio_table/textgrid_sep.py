# audio_table/textgrid_sep.py
# MFAのTextGridから、item [1]の区間を抽出してCSV

import os

INPUT_DIR = "mfa_tmp/output"
OUTPUT_DIR = "src/audio_table"
OUTPUT_FILE = "textgrid_sep.txt"


def extract_item1_intervals(textgrid_path):
    with open(textgrid_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    intervals = []

    in_item1 = False

    xmin = xmax = text = None

    for line in lines:
        line = line.strip()

        if line.startswith("item [1]:"):
            in_item1 = True
            continue

        if line.startswith("item [2]:"):
            break

        if not in_item1:
            continue

        if "intervals [" in line:
            xmin = xmax = text = None
            continue

        if line.startswith("xmin"):
            xmin = float(line.split("=")[1].strip())

        elif line.startswith("xmax"):
            xmax = float(line.split("=")[1].strip())

        elif line.startswith("text"):
            text = line.split("=", 1)[1].strip().strip('"')

            if xmin is not None and xmax is not None:
                intervals.append((xmin, xmax, text))

    return intervals


def run():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as out_f:
        out_f.write("xmin,xmax,text\n")

        for file_name in os.listdir(INPUT_DIR):
            if not file_name.endswith(".TextGrid"):
                continue

            path = os.path.join(INPUT_DIR, file_name)
            intervals = extract_item1_intervals(path)

            for xmin, xmax, text in intervals:
                out_f.write(f"{xmin},{xmax},{text}\n")

            print(f"Processed: {file_name}")

    print(f"Saved: {output_path}")


# 👇これ追加
def main():
    run()


if __name__ == "__main__":
    main()
# src/text_correct/loader.py

def load_replace_dict(path: str) -> dict:
    replace_dict = {}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            wrong, correct = line.split(",", 1)
            replace_dict[wrong] = correct

    return replace_dict
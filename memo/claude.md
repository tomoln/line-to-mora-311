# このプロジェクトについて

## 目的

日本語音声（WAV）をモーラ単位に分割し、各モーラの音声特徴量をJSONで出力するツール。

---

## 実行方法

```bash
# 004まで（文字起こし〜テキスト整形）
python main_to_004.py

# 全工程
python main.py
```

`input/` に WAV を1つ置いて実行する。ファイル名は何でもよい（`find_input_wav()` で自動検出）。

---

## パイプライン

```
input/*.wav
  │
  ├─ whisper          → confirm/001_whisper.txt
  ├─ text_normalize   → confirm/002_text_normalize.txt
  ├─ text_replace     → confirm/003_text_replace.txt  （dict/replace_dict.txt で置換）
  ├─ 004 text_clean   → confirm/004_text_clean.txt
  │
  │  ※ 005(text_to_kana) / 006(text_phoneme) / 007(text_mfa_phoneme) は現在カット
  │    main.py には呼び出しが残っているが、MFA前の前処理として動いている
  │
  ├─ 008 MFA          → confirm/008_text_mfa_timestamp.txt  + mfa_tmp/output/001.TextGrid
  ├─ 009 phoneme→mora → confirm/009_text_to_mora.txt
  ├─ 010 mora→日本語  → confirm/010_mora_to_japanese.txt
  ├─ 011 librosa解析  → confirm/011_add_audio_parameters.txt
  └─ 012 audio_table  → out_json/out.json
```

---

## 主要ファイル

| ファイル | 役割 |
|---|---|
| `main.py` | 全工程を実行 |
| `main_to_004.py` | 004まで実行 |
| `src/whisper/whisper_audio_to_str.py` | whisper文字起こし + `find_input_wav()` 定義 |
| `src/text_normalize/unicodedata_Normalize.py` | Unicode正規化 |
| `src/text_replace/correct_text.py` | 辞書置換 |
| `src/text_clean/no_noise_neologdn.py` | neologdn整形（004） |
| `src/text_mfa_timestamp/Montreal_Forced_Aligner.py` | MFA実行・TextGrid解析 |
| `src/text_mora/phoneme_to_mora.py` | 音素→モーラ変換 |
| `src/text_mora_jp/mora_to_japanese.py` | モーラ→日本語かな変換 |
| `src/audio_analysis/librosa_v.py` | librosaで音声特徴量抽出 |
| `src/audio_table/run_audio_table_pipeline.py` | TextGrid→単語×モーラ→JSON |
| `dict/replace_dict.txt` | whisper誤認識の置換辞書 |

---

## 重要な共通パターン

- **`find_input_wav()`** : `src/whisper/whisper_audio_to_str.py` に定義。`input/` 内のWAVを自動検出。0個・2個以上でエラー。各モジュールでインポートして使う。
- **`confirm/` フォルダ** : 各ステップの中間出力。番号付きファイル名で管理。
- モジュール間のデータ受け渡しは**戻り値**で行う（ファイル経由ではない）。

---

## 環境

- conda環境名: `audio_clean`（Python 3.10）
- 主要ライブラリ: openai-whisper, Montreal_Forced_Aligner, librosa, spacy, fugashi, neologdn, pyopenjtalk
- MFAモデル: `japanese_mfa`（acoustic + dictionary）
- `environment_minimal.yml` で環境再現可能

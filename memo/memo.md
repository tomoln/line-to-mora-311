
requirements.txt
から、インストールが必要なライブラリが何かわかりますか？
行が多いので、時間かかりそうなら別に調べてほしくないけど
コードとかは書かないで良いです

このファイルは conda/pipの環境スナップショット（pip freeze相当）であり、@ file:///D:/bld/... のようなビルドサーバー上のパスが含まれているため、他の環境では pip install -r で直接使うことはできません。

全部で約114パッケージが列挙されています。プロジェクト（line-to-mora）との関係で 主要なものを分類すると：

音声処理系

openai-whisper
Montreal_Forced_Aligner (MFA)
kalpy-kaldi
librosa, soundfile, soxr
pyopenjtalk
praatio
日本語NLP系

fugashi, unidic-lite
neologdn
SudachiPy, SudachiDict-core
spacy (+ spacy-legacy, spacy-loggers)
pynini
機械学習・数値計算系

torch==2.11.0+cpu
numpy, scipy, scikit-learn
numba, llvmlite
hdbscan
DB/API系

psycopg2, pgvector, SQLAlchemy
httpx, requests
ユーティリティ

tqdm, rich, click, typer
pydantic
tiktokne

今win使ってる。
これをデプロイして、後でmacで続き始めるんだけど、
これ環境違うからそのまま使えないじゃん
どうやってデプロイして渡せば良い？

問題: 今の environment.yml や requirements.txt にはWindowsのビルドハッシュ（py310h458dff3_0 など）が入っているので、そのままMacでは使えない。

推奨手順
1. クロスプラットフォーム用の environment.yml を作る（Windows側で実行）

conda env export --no-builds > environment_cross.yml
--no-builds でビルド固有の文字列を除いてくれるため、Mac でも使えるようになります。

2. コードをgitにpush

git add environment_cross.yml
git commit -m "add cross-platform environment"
git push
3. Mac側で環境を再現

git clone <repo>
conda env create -f environment_cross.yml
conda activate audio_clean
それでも動かない場合（Macで一部パッケージが見つからない）
--from-history オプションで「自分が明示的にインストールしたパッケージだけ」を出力する方法もあります。依存関係はcondaが自動解決するため、よりクリーンです：


conda env export --from-history > environment_minimal.yml
ただし、openai-whisper や Montreal_Forced_Aligner など特殊なパッケージは手動で追加確認が必要なことがあります。

まとめ: conda env export --no-builds > environment_cross.yml → push → Macで conda env create -f environment_cross.yml が一番手軽です

下記みたいのがベスト

name: audio_clean
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - montreal-forced-aligner
  - sudachipython
  - spacy
  - sudachidict-core
  - pip
  - pip:
    - openai-whisper
    - pyopenjtalk
    - neologdn
    # その他pipで入れたものがあれば追加

## mac側の作業

macでクローン

こう？

# 1. cloneする
git clone <リポジトリのURL>
cd line-to-mora-311

# 2. conda環境を作る
conda env create -f environment_minimal.yml

# 3. 環境を有効化
conda activate audio_clean

# 4. 動作確認
python main.py

# conda環境を作ったときに引っ掛かりそうなポイント

先ほど挙げた3点が主なものです：

1. pyopenjtalk のビルドエラー
C++のビルドが必要なため失敗することがある。


brew install cmake
で解決することが多い。

2. montreal-forced-aligner の依存解決に時間がかかる / 失敗する
conda-forgeのパッケージが多く、solverが詰まることがある。libmambaを使うと速くなる：

# 辞書のインストールが多分必要
conda activate audio_clean
mfa model download acoustic japanese_mfa
mfa model download dictionary japanese_mfa


conda install -n base conda-libmamba-solver
conda config --set solver libmamba
3. torch==2.11.0+cpu が見つからない
+cpu のバージョン指定はcondaでは解決できないことがある。その場合は environment_minimal.yml の pip セクションに追加：


    - pip:
      - torch==2.11.0
実際には 2のMFAが一番ハマりやすいです。エラーが出たらメッセージを見せてもらえれば対応できます



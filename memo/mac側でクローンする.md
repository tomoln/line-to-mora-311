## クローン側の作業(mac)

# 1. cloneする
git clone https://github.com/tomoln/line-to-mora-311.git
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



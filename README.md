# lambda-apigateway


## 環境構築
### 環境
- Windows 10以上
- エディター：Visual Studio Code
- Python 3.12

### インストール
- [pyenv](https://zenn.dev/lot36z/articles/1c734bde03677c)
- [black](https://dev.classmethod.jp/articles/vscode_black_flake8/)

### 仮想環境構築

初回
```
cd lambda-apigateway

# 仮想環境作成
python -m venv .venv

# 仮想環境立ち上げ
source .venv/Scripts/activate

# Pythonのバージョン固定
pyenv install 3.10.11
pyenv local 3.10.11

# Pythonのバージョン確認
pyenv version

# ライブラリのインストール
pip install -r src/requirements.txt
pip install -r tests/requirements.txt

# AWSのリージョン設定 ※boto3で必要なため
aws configure --region <AWSリージョン名>
```

2回目以降
```
#仮想環境立ち上げ
source .venv/Scripts/activate

# AWSのリージョン設定 ※boto3で必要なため
aws configure --region <AWSリージョン名>
```

## 開発
### コードフォーマッター
```
black <対象パス>
```

## 単体テスト

テスト実行・カバレッジ取得
```
python -m pytest tests/unit/test_app.py -vv --cov=src.app --cov-branch
```

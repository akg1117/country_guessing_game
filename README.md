# 国あてゲーム

## 概要
ChatGPTを使った国名当てゲームです。  
ヒントや質問を活用して、国名を当てます。

## 特徴
- 難易度選択（かんたん・ふつう・むずかしい）
- 質問は最大5回まで
- ヒント表示・国名予想・結果発表
- 国名リスト・プロンプトは日本語

## セットアップ方法

1. 仮想環境の作成（推奨）
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. 必要パッケージのインストール
   ```
   pip install -r requirements.txt
   ```

3. `.env`ファイルを作成し、OpenAI APIキーを記入
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. アプリの起動
   ```
   python run.py
   ```

## ディレクトリ構成
- app/
  - __init__.py
  - routes.py
  - game_ai.py
  - models.py
  - data/
  - static/
  - templates/
- run.py
- requirements.txt
- .env  ← プロジェクトルート（このファイルと同じ場所）に作成

## 注意事項
- `.env`ファイルには `OPENAI_API_KEY=あなたのChatGPT APIキー` を記載し、作成してください。

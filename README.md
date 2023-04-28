# 開発環境構築
## リポジトリのインストール
```bash
git clone https://github.com/shogogoto/tracer_back.git
```
## パッケージのインストール
プロジェクトルートで以下を実行
```bash
pipenv sync --dev
```


# テスト実行
ファイルを追加・更新することを検知して、自動でユニットテストを実行する
```bash
pipenv run test
```

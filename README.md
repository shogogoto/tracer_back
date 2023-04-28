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
テスト実行前にデータベースNeo4jを起動する必要がある
プロジェクトルート(docker-compose.ymlがあるパス))で以下を実行
```bash
# dockerのデーモンを起動する
sudo service docker start
docker compose up -d
```

ファイルを追加・更新することを検知して、自動でユニットテストを実行する
プロジェクトルートで以下を実行
```bash
pipenv run test
```

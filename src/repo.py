from os import environ

from neomodel import (
    db,
    config,
    install_all_labels
)

config.DATABASE_URL = "{}://{}:{}@{}".format(
        environ["NEO4J_PROTOCOL"],
        environ["NEO4J_USER"],
        environ["NEO4J_PASSWORD"],
        environ["NEO4J_URI"],
        )

# ↓自動作成は本番環境では非推奨
config.AUTO_INSTALL_LABELS = True

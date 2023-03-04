from os import environ

from neomodel import (
    db,
    config,
    install_all_labels
)

config.DATABASE_URL = "neo4j+s://{}:{}@{}".format(
        environ["NEO4J_USER"],
        environ["NEO4J_PASSWORD"],
        environ["NEO4J_URI"],
        )

install_all_labels()

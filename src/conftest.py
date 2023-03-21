from neomodel import db, clear_neo4j_database


def pytest_collection_finish():
    clear_neo4j_database(db)

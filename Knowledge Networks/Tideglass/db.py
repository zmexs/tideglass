import os

from pymongo import MongoClient, ASCENDING

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.environ.get("MONGO_DB", "memory_star")

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    return _client[DB_NAME]


def init_db():
    db = get_db()
    db.nodes.create_index([("type", ASCENDING), ("name", ASCENDING)], unique=True)
    db.aliases.create_index([("alias", ASCENDING)], unique=True)
    db.edges.create_index([("src", ASCENDING), ("dst", ASCENDING)])
    # 触发一次连接检查
    db.command("ping")
    return True
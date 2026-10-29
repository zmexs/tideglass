import os
from pymongo import MongoClient

URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
DB = os.environ.get("MONGO_DB", "memory_star")

print("URI =", URI)
print("DB  =", DB)

try:
    client = MongoClient(URI, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    print("✅ MongoDB 连接成功")
except Exception as e:
    print("❌ 连接失败：", type(e).__name__, e)
    print("→ 检查 MongoDB 服务是否启动：net start MongoDB / brew services list / docker ps")
    raise SystemExit

db = client[DB]
print("nodes 数量 =", db.nodes.count_documents({}))
print("edges 数量 =", db.edges.count_documents({}))
print("数据库列表 =", client.list_database_names())
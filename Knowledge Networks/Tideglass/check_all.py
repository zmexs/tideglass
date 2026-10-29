import build_graph
from db import get_db

db = get_db()
print("库名:", db.name)
print("nodes 数量:", db.nodes.count_documents({}))
print("edges 数量:", db.edges.count_documents({}))

print("\n--- 前 5 个 node ---")
for n in db.nodes.find({}).limit(5):
    print({k: str(v) for k, v in n.items()})

print("\n--- 前 5 个 edge ---")
for e in db.edges.find({}).limit(5):
    print({k: str(v) for k, v in e.items()})

path = build_graph.build()
print("\n生成文件:", path)
html = open(path, encoding="utf-8").read()
i = html.find("const GRAPH_DATA")
print("注入片段:", html[i:i+300])
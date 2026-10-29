import sys
from bson import ObjectId
from db import get_db

def search_memory(keyword):
    db = get_db()
    # 模糊搜索节点
    nodes = list(db.nodes.find({"name": {"$regex": keyword, "$options": "i"}}))
    if not nodes:
        return f"未找到关于【{keyword}】的记忆。"

    results = []
    for node in nodes:
        node_id = str(node["_id"])
        # 找相关连线
        edges = list(db.edges.find({"$or": [{"src": node_id}, {"dst": node_id}]}))
        
        facts = []
        for e in edges:
            s = db.nodes.find_one({"_id": ObjectId(e["src"])})
            d = db.nodes.find_one({"_id": ObjectId(e["dst"])})
            if s and d:
                # 使用 .get() 防止因为缺少字段导致报错
                s_name = s.get('name', '未知')
                d_name = d.get('name', '未知')
                rel = e.get('relation', '相关')
                facts.append(f"{s_name} {rel} {d_name}")
                
        summary = node.get('summary', '无')
        if facts:
            results.append(f"【{node['name']}】类型:{node['type']}, 描述:{summary}\n关联关系:\n" + "\n".join(facts))
        else:
            results.append(f"【{node['name']}】类型:{node['type']}, 描述:{summary}\n(暂无关联关系)")

    return "\n\n".join(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = sys.argv[1]
        print(search_memory(query))
    else:
        print("请提供查询词")
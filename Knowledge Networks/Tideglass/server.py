from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from db import get_db
import os

app = Flask(__name__, static_folder='.')
CORS(app) # 允许跨域请求

COLORS = {
    "人物": "#ff6b6b", "项目": "#4dabf7", "概念": "#69db7c",
    "事件": "#ffd43b", "实体": "#adb5bd",
}

@app.route('/')
def index():
    # 返回你的前端页面
    return send_from_directory('.', 'star_template.html')

@app.route('/api/graph')
def get_graph_data():
    # 这个接口负责实时从 MongoDB 查数据，并打包成 JSON 给前端
    db = get_db()
    nodes = list(db.nodes.find({}))
    edges = list(db.edges.find({}))

    visible = {str(n["_id"]) for n in nodes if not n.get("privacy")}
    deg = {}
    for e in edges:
        if e["src"] in visible and e["dst"] in visible:
            deg[e["src"]] = deg.get(e["src"], 0) + 1
            deg[e["dst"]] = deg.get(e["dst"], 0) + 1

    vnodes = []
    for n in nodes:
        nid = str(n["_id"])
        if nid not in visible:
            continue
        color = COLORS.get(n.get("type"), COLORS["实体"])
        vnodes.append({
            "id": nid,
            "label": n.get("name", ""),
            "group": n.get("type", "实体"),
            "summary": n.get("summary") or "",
            "source": n.get("source") or "",
            "confidence": n.get("confidence"),
            "title": n.get("summary") or n.get("name", ""),
            "size": 8 + deg.get(nid, 0) * 4,
            "created_at": n.get("created_at", "")
        })

    vedges = [
        {
            "from": e["src"],
            "to": e["dst"],
            "label": e.get("relation", ""),
            "width": float(e.get("weight") or 1.0),
        }
        for e in edges
        if e["src"] in visible and e["dst"] in visible
    ]

    return jsonify({"nodes": vnodes, "edges": vedges})

if __name__ == '__main__':
    print("🚀 记忆星图后端已启动: http://127.0.0.1:5000")
    print("👉 请用浏览器打开这个网址查看，不要再双击 html 文件了！")
    app.run(host='127.0.0.1', port=5000, debug=True)
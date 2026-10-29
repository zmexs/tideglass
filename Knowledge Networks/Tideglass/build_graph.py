import json
import os

import memory

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, "star_template.html")
if not os.path.exists(TEMPLATE):
    TEMPLATE = os.path.join(BASE, "star.html")
OUT_DIR = os.path.join(BASE, "output")
OUT_HTML = os.path.join(OUT_DIR, "star.html")

COLORS = {
    "人物": "#ff6b6b", "项目": "#4dabf7", "概念": "#69db7c",
    "事件": "#ffd43b", "实体": "#adb5bd",
}


def short_label(name, typ):
    """笔记节点只显示文件名，图上不挤。"""
    if typ != "项目":
        return name
    base = name.replace("\\", "/").split("/")[-1]
    if base.endswith(".md"):
        base = base[:-3]
    return base


def node_size(typ, degree):
    if typ == "项目":
        return 7 + min(degree, 3)
    return 12 + min(degree, 10) * 3


def load_data():
    nodes, edges = memory.load_graph()

    visible = {n["id"] for n in nodes if not n.get("privacy")}
    deg = {}
    for e in edges:
        if e["src"] in visible and e["dst"] in visible:
            deg[e["src"]] = deg.get(e["src"], 0) + 1
            deg[e["dst"]] = deg.get(e["dst"], 0) + 1

    vnodes = []
    for n in nodes:
        if n["id"] not in visible:
            continue
        typ = n.get("type", "实体")
        color = COLORS.get(typ, COLORS["实体"])
        name = n.get("name", "")
        vnodes.append({
            "id": n["id"],
            "label": short_label(name, typ),
            "group": typ,
            "summary": n.get("summary") or "",
            "source": n.get("source") or "",
            "confidence": n.get("confidence"),
            "title": n.get("summary") or name,
            "color": {"background": color, "border": "#ffffff"},
            "size": node_size(typ, deg.get(n["id"], 0)),
            "font": {"size": 11 if typ == "项目" else 14},
        })

    vedges = [
        {
            "from": e["src"],
            "to": e["dst"],
            "label": "",
            "width": 1.0 if e.get("rel") in ("那天", "收录", "关于") or e.get("relation") in ("那天", "收录", "关于") else 2.0,
            "color": {"color": "rgba(126,186,255,0.45)", "highlight": "#9ed4ff", "hover": "#9ed4ff"},
        }
        for e in edges
        if e["src"] in visible and e["dst"] in visible
    ]
    return {"nodes": vnodes, "edges": vedges}


def build():
    if not os.path.exists(TEMPLATE):
        raise FileNotFoundError(f"找不到模板 {TEMPLATE}")
    data = load_data()
    with open(TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("__GRAPH_DATA__", payload)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return OUT_HTML


if __name__ == "__main__":
    print("星图已生成:", build())

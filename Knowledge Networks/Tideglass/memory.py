from datetime import datetime

from bson import ObjectId

from db import get_db


def _now():
    return datetime.utcnow().isoformat()


def upsert_node(type_, name, summary=None, source=None, confidence=0.8, privacy=0):
    db = get_db()
    update = {
        "$set": {
            "type": type_,
            "name": name,
            "confidence": confidence,
            "privacy": privacy,
            "updated_at": _now(),
        },
        "$setOnInsert": {"created_at": _now()},
    }
    if summary is not None:
        update["$set"]["summary"] = summary
    if source is not None:
        update["$set"]["source"] = source

    res = db.nodes.find_one_and_update(
        {"type": type_, "name": name},
        update,
        upsert=True,
        return_document=True,
    )
    return str(res["_id"])


def add_alias(node_id, alias):
    db = get_db()
    db.aliases.update_one(
        {"alias": alias},
        {"$set": {"node_id": str(node_id)}},
        upsert=True,
    )


def resolve_node(name):
    db = get_db()
    doc = db.nodes.find_one({"name": name})
    if doc:
        return str(doc["_id"])
    alias = db.aliases.find_one({"alias": name})
    if alias:
        return alias["node_id"]
    return None


def add_edge(src_name, dst_name, relation, weight=1.0, source=None,
             src_type="实体", dst_type="实体"):
    src_id = resolve_node(src_name) or upsert_node(src_type, src_name, source=source)
    dst_id = resolve_node(dst_name) or upsert_node(dst_type, dst_name, source=source)
    db = get_db()
    db.edges.insert_one({
        "src": src_id,
        "dst": dst_id,
        "relation": relation,
        "weight": float(weight),
        "source": source,
        "created_at": _now(),
    })
    return src_id, dst_id


def add_event(content, node_name=None, time=None, source=None):
    node_id = resolve_node(node_name) if node_name else None
    db = get_db()
    db.events.insert_one({
        "node_id": node_id,
        "time": time or _now(),
        "content": content,
        "source": source,
    })


def search(keyword):
    db = get_db()
    regex = {"$regex": keyword, "$options": "i"}
    rows = db.nodes.find({"$or": [{"name": regex}, {"summary": regex}]})
    return [_clean_node(r) for r in rows]


def _clean_node(doc):
    d = dict(doc)
    d["id"] = str(d.pop("_id"))
    return d


def load_graph():
    db = get_db()
    nodes = [_clean_node(n) for n in db.nodes.find({})]
    edges = [
        {
            "src": e["src"],
            "dst": e["dst"],
            "relation": e.get("relation", ""),
            "weight": e.get("weight", 1.0),
            "source": e.get("source"),
        }
        for e in db.edges.find({})
    ]
    return nodes, edges
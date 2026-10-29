import json
import re

import memory


def extract_rule_based(text, source="手动"):
    """极简规则：识别 “A 关系 B” 句式，如 “张三 负责 AI助手”"""
    results = {"nodes": [], "edges": []}
    pattern = re.compile(r"([\u4e00-\u9fa5A-Za-z0-9]+)\s*(负责|使用|属于|喜欢|参与|创建)\s*([\u4e00-\u9fa5A-Za-z0-9]+)")
    for m in pattern.finditer(text):
        a, rel, b = m.group(1), m.group(2), m.group(3)
        results["edges"].append({"src": a, "dst": b, "relation": rel})
    return results


def extract_with_llm(text, llm_call):
    """llm_call(prompt)->str，返回 JSON 字符串。自己接你的模型。"""
    prompt = f"""从下面文本抽取记忆，只输出 JSON，不要解释。
格式：
{{"nodes":[{{"type":"人物","name":"张三","summary":""}}],
  "edges":[{{"src":"张三","dst":"AI助手","relation":"负责"}}],
  "events":[{{"time":"","content":"","node":"张三"}}]}}
文本：
{text}
"""
    raw = llm_call(prompt)
    raw = re.sub(r"^```json|```$", "", raw.strip(), flags=re.M).strip()
    return json.loads(raw)


def save_extraction(data, source="手动"):
    for n in data.get("nodes", []):
        memory.upsert_node(n.get("type", "实体"), n["name"], n.get("summary"), source)
    for e in data.get("edges", []):
        memory.add_edge(e["src"], e["dst"], e["relation"], source=source)
    for ev in data.get("events", []):
        memory.add_event(ev.get("content"), ev.get("node"), ev.get("time"), source)
    return len(data.get("nodes", [])), len(data.get("edges", []))
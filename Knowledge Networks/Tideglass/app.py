import argparse

import build_graph
import db
import extract
import memory


def main():
    parser = argparse.ArgumentParser(description="记忆星图 CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="初始化数据库")

    p_add = sub.add_parser("add", help="添加一条记忆文本")
    p_add.add_argument("text")
    p_add.add_argument("--source", default="手动")

    p_node = sub.add_parser("node", help="手动加节点")
    p_node.add_argument("type")
    p_node.add_argument("name")
    p_node.add_argument("--summary", default=None)

    p_edge = sub.add_parser("edge", help="手动加关系")
    p_edge.add_argument("src")
    p_edge.add_argument("dst")
    p_edge.add_argument("relation")

    p_search = sub.add_parser("search", help="搜索")
    p_search.add_argument("keyword")

    sub.add_parser("graph", help="生成星图 HTML")

    args = parser.parse_args()
    db.init_db()

    if args.cmd == "init":
        print("数据库已初始化")
    elif args.cmd == "add":
        data = extract.extract_rule_based(args.text, args.source)
        n, e = extract.save_extraction(data, args.source)
        print(f"写入节点 {n}，关系 {e}")
    elif args.cmd == "node":
        print("节点 id:", memory.upsert_node(args.type, args.name, args.summary))
    elif args.cmd == "edge":
        memory.add_edge(args.src, args.dst, args.relation)
        print("关系已写入")
    elif args.cmd == "search":
        for r in memory.search(args.keyword):
            print(r)
    elif args.cmd == "graph":
        print("星图:", build_graph.build())


if __name__ == "__main__":
    main()
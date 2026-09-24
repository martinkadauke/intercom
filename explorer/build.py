"""Build the Klingelbox explorer into one self-contained HTML file.

    python build.py            -> dist/klingelbox-explorer.html

Inputs (all in this folder):
    skeleton.json  structure: zones, layers, nodes, edges, tours, solder jobs, open points
    layout.json    canvas coordinates, short type tags, wire route overrides
    texts.json     optional EN/DE copy per node, edge, tour and solder job;
                   anything missing falls back to the skeleton's names and hints
    template.html  page, styles and the rendering engine

The build refuses to write if a reference is broken, so a typo in an id shows
up here and not as a silently missing wire on the page.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "dist" / "klingelbox-explorer.html"


def load(name, required=True):
    p = HERE / name
    if not p.exists():
        if required:
            sys.exit(f"missing {name}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def check(sk, ly, tx):
    errors = []
    node_ids = {n["id"] for n in sk["nodes"]}
    layer_ids = {l["id"] for l in sk["layers"]}
    zone_ids = {z["id"] for z in sk["zones"]}
    edge_ids = {e["id"] for e in sk["edges"]}
    for n in sk["nodes"]:
        if n["zone"] not in zone_ids:
            errors.append(f"node {n['id']}: unknown zone {n['zone']}")
        if n["id"] not in ly["nodes"]:
            errors.append(f"node {n['id']}: no position in layout.json")
    for nid in ly["nodes"]:
        if nid not in node_ids:
            errors.append(f"layout.json places unknown node {nid}")
    for e in sk["edges"]:
        for end in ("from", "to"):
            if e[end] not in node_ids:
                errors.append(f"edge {e['id']}: unknown {end} {e[end]}")
        if e["layer"] not in layer_ids:
            errors.append(f"edge {e['id']}: unknown layer {e['layer']}")
    for rid in ly.get("routes", {}):
        if rid not in edge_ids:
            errors.append(f"layout.json routes unknown edge {rid}")
    for t in sk["tours"]:
        for i, st in enumerate(t["steps"]):
            for n in st["nodes"]:
                if n not in node_ids:
                    errors.append(f"tour {t['id']} step {i+1}: unknown node {n}")
            for e in st["edges"]:
                if e not in edge_ids:
                    errors.append(f"tour {t['id']} step {i+1}: unknown edge {e}")
    for s in sk["solder"]:
        if s["node"] not in node_ids:
            errors.append(f"solder job for unknown node {s['node']}")
    for kind, ids in (("nodes", node_ids), ("edges", edge_ids),
                      ("tours", {t["id"] for t in sk["tours"]}),
                      ("solder", {s["node"] for s in sk["solder"]})):
        for k in tx.get(kind, {}):
            if k not in ids:
                errors.append(f"texts.json {kind}: unknown id {k}")
    for kind in ("nodes", "edges", "tours", "solder"):
        for k, v in tx.get(kind, {}).items():
            for lang in ("en", "de"):
                if lang not in v:
                    errors.append(f"texts.json {kind} {k}: no {lang}")
    for t in sk["tours"]:
        tt = tx.get("tours", {}).get(t["id"])
        if tt:
            for lang in ("en", "de"):
                if len(tt[lang].get("steps", [])) != len(t["steps"]):
                    errors.append(f"texts.json tour {t['id']} {lang}: step count differs")
    return errors


def main():
    sk = load("skeleton.json")
    ly = load("layout.json")
    tx = load("texts.json", required=False)
    errors = check(sk, ly, tx)
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s), nothing written")
    missing = {
        kind: sorted(set(ids) - set(tx.get(kind, {})))
        for kind, ids in (("nodes", [n["id"] for n in sk["nodes"]]),
                          ("edges", [e["id"] for e in sk["edges"]]),
                          ("tours", [t["id"] for t in sk["tours"]]),
                          ("solder", [s["node"] for s in sk["solder"]]))
    }
    data = {"skeleton": sk, "layout": ly, "texts": tx, "state": sk.get("state", "")}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (HERE / "template.html").read_text(encoding="utf-8")
    if "__KB_DATA__" not in html:
        sys.exit("template.html has no __KB_DATA__ placeholder")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html.replace("__KB_DATA__", blob), encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE)} ({OUT.stat().st_size // 1024} KB)")
    for kind, ids in missing.items():
        if ids:
            print(f"  no text yet for {len(ids)} {kind}: {', '.join(ids)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the MDX/graph contract without requiring an Astro runtime."""
from __future__ import annotations
import argparse, datetime as dt, json, os, re, subprocess, sys, tempfile
from pathlib import Path
import yaml
from seedtool import load_graph

STATUSES = {"outline", "draft", "reviewed", "published"}
LEVELS = ["intuition", "fundamentals", "deep"]
SECTIONS = {"overview", "why", "mechanism", "math", "example", "code", "visual", "limitations", "history", "related", "references"}
ID = re.compile(r"^[a-z]+:[a-z0-9]+(?:-[a-z0-9]+)*$")
WIKI = re.compile(r"^wiki:[a-z0-9]+(?:-[a-z0-9]+)*$")

def frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else ({}, text)

def graph_ids(paths: str):
    out = {"entities": {}, "claims": {}, "sources": {}}
    for raw in filter(None, (x.strip() for x in paths.split(','))):
        p = Path(raw)
        if not p.exists(): continue
        g = load_graph(p)
        for key in out:
            for ident, value in g[key].items():
                if ident in out[key]: raise ValueError(f"duplicate graph id: {ident}")
                out[key][ident] = value
    return out

def issue(items, code, file, message, warning=False):
    items.append({"level": "warning" if warning else "error", "code": code, "file": str(file), "message": message})

def validate_one(path: Path, g, seen, items):
    meta, body = frontmatter(path.read_text(encoding="utf8")); ref = path.name
    required = {"id","entity","title","subtitle","status","levels","sections","authors","ai_generated","review","published_at","sources","claims","labs","figures","updated_at"}
    missing = required - set(meta)
    if missing: issue(items,"V-SCHEMA",ref,f"missing frontmatter: {', '.join(sorted(missing))}"); return
    slug = path.stem
    if not WIKI.match(str(meta["id"])) or meta["id"] != f"wiki:{slug}": issue(items,"V-SCHEMA",ref,"id must be wiki:<filename slug>")
    if not ID.match(str(meta["entity"])) or meta["entity"] not in g["entities"]: issue(items,"V-SCHEMA",ref,"unknown entity")
    if str(meta["entity"]).split(":",1)[-1] != slug: issue(items,"V-SCHEMA",ref,"slug must equal entity slug")
    if meta["entity"] in seen: issue(items,"V-SCHEMA",ref,"one wiki per entity")
    seen.add(meta["entity"])
    if meta["status"] not in STATUSES: issue(items,"V-SCHEMA",ref,"invalid status")
    if not isinstance(meta["levels"],list) or any(x not in LEVELS for x in meta["levels"]) or meta["levels"] != sorted(meta["levels"], key=LEVELS.index): issue(items,"V-SCHEMA",ref,"invalid or unordered levels")
    if not isinstance(meta["sections"],list) or any(x not in SECTIONS for x in meta["sections"]): issue(items,"V-SCHEMA",ref,"invalid sections")
    actual = set(re.findall(r"<Section\s+[^>]*\bid=[\"']([^\"']+)", body))
    if actual != set(meta["sections"]): issue(items,"V-SCHEMA",ref,"frontmatter sections do not match Section ids")
    for ident in re.findall(r"<ConceptLink\s+[^>]*\bid=[\"']([^\"']+)", body):
        if ident not in g["entities"]: issue(items,"V-LINK-1",ref,f"unknown ConceptLink {ident}")
    cites = re.findall(r"<Cite\s+([^>]+)", body)
    for attrs in cites:
        src = re.search(r"\bsrc=[\"']([^\"']+)", attrs); claim = re.search(r"\bclaim=[\"']([^\"']+)", attrs)
        ident = (src or claim).group(1) if (src or claim) else ""
        collection = "sources" if src else "claims"
        if not ident or ident not in g[collection]: issue(items,"V-CITE-1",ref,f"unknown cite {ident}")
        elif ident not in meta[collection]: issue(items,"V-CITE-3",ref,f"cite {ident} absent from frontmatter")
        elif claim and g["claims"][ident].get("status") in {"rejected","deprecated"}: issue(items,"V-STATUS",ref,f"cites hidden claim {ident}")
        elif claim and g["claims"][ident].get("status") in {"proposed","disputed"}: issue(items,"V-STATUS",ref,f"cites {g['claims'][ident].get('status')} claim {ident}",True)
    for sec in ("math","history","mechanism"):
        if sec in actual and meta["status"] != "outline":
            m = re.search(rf"<Section\s+[^>]*\bid=[\"']{re.escape(sec)}[\"'][^>]*>(.*?)</Section>", body, re.S)
            if m and "<Cite" not in m.group(1): issue(items,"V-CITE-2",ref,f"{sec} needs a Cite")
    review = meta.get("review")
    if meta["status"] in {"reviewed","published"} and (not isinstance(review,dict) or not str(review.get("by","")).startswith("human:") or review.get("decision") != "approve"): issue(items,"V-STATUS",ref,"human approval required")
    if meta["status"] == "published" and not meta.get("published_at"): issue(items,"V-STATUS",ref,"published_at required")
    if meta.get("ai_generated") and meta["status"] in {"reviewed","published"} and not review: issue(items,"V-STATUS",ref,"AI content needs human review")
    figures = {x.get("id"):x for x in meta.get("figures",[]) if isinstance(x,dict)}
    for ident in re.findall(r"<Figure\s+[^>]*\bid=[\"']([^\"']+)", body):
        if ident not in figures or figures[ident].get("origin") != "self-made": issue(items,"V-FIG",ref,f"Figure {ident} must be listed self-made")
    for code in re.findall(r"```python\s+verify\s*\n(.*?)```",body,re.S):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)/"verify.py"; p.write_text(code,encoding="utf8")
            exe = Path(".venv/bin/python") if Path(".venv/bin/python").exists() else Path(sys.executable)
            try: run = subprocess.run([str(exe),str(p)],capture_output=True,text=True,timeout=20)
            except subprocess.TimeoutExpired: issue(items,"V-CODE-1",ref,"verify block timed out"); continue
            if run.returncode: issue(items,"V-CODE-1",ref,(run.stderr or run.stdout).strip()[:300])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--wiki-dir",default=os.getenv("AIXON_WIKI_DIR","src/content/wiki")); ap.add_argument("--graph",default=os.getenv("AIXON_GRAPH","data/seed/seed_graph.yaml,data/graph/atlas.yaml")); ap.add_argument("--json",action="store_true"); args=ap.parse_args()
    items=[]
    try: g=graph_ids(args.graph)
    except Exception as e: print(str(e),file=sys.stderr); return 1
    seen=set()
    for p in sorted(Path(args.wiki_dir).glob("*.mdx")): validate_one(p,g,seen,items)
    report={"errors":[x for x in items if x["level"]=="error"],"warnings":[x for x in items if x["level"]=="warning"]}
    if args.json: print(json.dumps(report,ensure_ascii=False,indent=2))
    else:
        for x in items: print(f"{x['level'].upper()} {x['code']} {x['file']}: {x['message']}")
        print(f"{len(report['errors'])} error(s), {len(report['warnings'])} warning(s)")
    return 1 if report["errors"] else 0
if __name__ == "__main__": raise SystemExit(main())

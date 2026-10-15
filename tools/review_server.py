#!/usr/bin/env python3
"""Local-only human review application (ADR-021, ADR-025, ADR-026)."""
from __future__ import annotations

import argparse
import datetime as dt
import hmac
import importlib
import json
import mimetypes
import os
import secrets
import subprocess
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import yaml

HERE = Path(__file__).resolve().parent
APP_DIR = HERE / "review_app"
sys.path.insert(0, str(HERE))
import public_gate as pg  # noqa: E402
import review  # noqa: E402
import seedtool as st  # noqa: E402


TYPE_LABELS = {
    "ResearchField": "연구 분야", "ResearchProblem": "연구 문제", "Concept": "개념",
    "Method": "방법", "Model": "모델", "Paper": "논문", "Dataset": "데이터셋",
    "Metric": "평가 지표", "Benchmark": "벤치마크", "LearningObjective": "학습 목표",
    "LearningResource": "학습 자료", "AssessmentItem": "평가 문항", "LabExperiment": "실험실",
}
PREDICATE_LABELS = {
    "INTRODUCES": "제시", "EXTENDS": "확장", "ADAPTS": "적용", "ADDRESSES": "문제 해결",
    "MITIGATES": "완화", "PREREQUISITE_OF": "선수 지식", "RECOMMENDED_BEFORE": "권장 선수",
    "PART_OF": "구성 요소", "IS_A": "한 종류", "CITES": "인용", "EVALUATED_ON": "평가",
    "TRAINED_ON": "학습", "IMPROVES_ON": "성능 비교", "COMPARED_WITH": "비교",
}
COMMIT_PATHS = ("review", "data", "src/content/wiki")


def claim_sentence(record: dict, names: dict[str, str]) -> str:
    """Keep the Korean predicate wording aligned with src/lib/predicates.ts."""
    subject, obj = names.get(str(record.get("subject")), str(record.get("subject", ""))), names.get(str(record.get("object")), str(record.get("object", "")))
    qualifier = record.get("qualifiers") or {}
    predicate = record.get("predicate", "")
    templates = {
        "INTRODUCES": f"{subject}은(는) {obj}을(를) 제시했다", "EXTENDS": f"{subject}은(는) {obj}을(를) 확장했다",
        "ADAPTS": f"{subject}은(는) {obj}을(를) 적용했다", "ADDRESSES": f"{subject}은(는) {obj} 문제를 다룬다",
        "MITIGATES": f"{subject}은(는) {obj}을(를) 완화한다", "PREREQUISITE_OF": f"{subject}은(는) {obj}의 선수 지식이다",
        "RECOMMENDED_BEFORE": f"{subject}은(는) {obj}보다 먼저 배우기를 권장한다", "PART_OF": f"{subject}은(는) {obj}의 일부다",
        "IS_A": f"{subject}은(는) {obj}의 한 종류다", "CITES": f"{subject}은(는) {obj}을(를) 인용한다",
        "EVALUATED_ON": f"{subject}은(는) {obj}에서 평가됐다", "TRAINED_ON": f"{subject}은(는) {obj}(으)로 학습됐다",
        "IMPROVES_ON": f"{subject}은(는) {qualifier.get('benchmark', '보고된 벤치마크')}의 {qualifier.get('metric', '지표')}에서 {obj}보다 좋은 결과를 보고했다",
        "COMPARED_WITH": f"{subject}은(는) {obj}과(와) 비교됐다",
    }
    sentence = templates.get(predicate, f"{subject}은(는) {obj}과(와) {predicate} 관계다")
    return f"{sentence} ({qualifier['conditions']})" if qualifier.get("conditions") else sentence


def approval(record: dict, wiki: bool = False, body: str = "") -> str:
    return (pg.wiki_approval(record, body) if wiki else st.approval_state(record)) or "pending"


def review_by(record: dict) -> str | None:
    value = record.get("review")
    return value.get("by") if isinstance(value, dict) and isinstance(value.get("by"), str) else None


def text_fragment(url: str, quote_text: str) -> str:
    if not url or not quote_text:
        return url
    words = " ".join(str(quote_text).split()[:12])
    return f"{url}#:~:text={quote(words, safe='')}" if words else url


def worksheets(review_dir: Path) -> dict[str, dict]:
    """The last matching top-level worksheet is the current pre-review opinion."""
    found: dict[str, dict] = {}
    if not review_dir.is_dir():
        return found
    for path in sorted(review_dir.glob("*.yaml"), key=lambda item: item.stat().st_mtime):
        try:
            contents = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        for item in contents.get("items", []) if isinstance(contents, dict) else []:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                found[item["id"]] = {
                    "recommendation": item.get("recommendation"), "notes": item.get("notes", ""),
                    "fix": item.get("fix", ""), "worksheet": path.name,
                }
    return found


def _confirm_status(confirm: object, url: str, passage: str) -> str | None:
    """Read both the current confirm shape and simple URL-keyed variants."""
    if isinstance(confirm, dict):
        if url in confirm and isinstance(confirm[url], dict):
            result = confirm[url].get("status") or confirm[url].get("result")
            return str(result) if result else None
        if confirm.get("url") == url:
            result = confirm.get("status") or confirm.get("result")
            return str(result) if result else None
        for value in confirm.values():
            outcome = _confirm_status(value, url, passage)
            if outcome:
                return outcome
    if isinstance(confirm, list):
        for value in confirm:
            outcome = _confirm_status(value, url, passage)
            if outcome:
                return outcome
    return None


def cross_reviews(review_root: Path, ident: str) -> list[dict]:
    reports: list[dict] = []
    cross_dir = review_root / "cross"
    if not cross_dir.is_dir():
        return reports
    for release_dir in sorted(path for path in cross_dir.iterdir() if path.is_dir()):
        confirm_path = release_dir / "confirm.json"
        try:
            confirm = json.loads(confirm_path.read_text(encoding="utf-8")) if confirm_path.exists() else None
        except json.JSONDecodeError:
            confirm = None
        for path in sorted(release_dir.glob("*.yaml")):
            if path.name == "packet.yaml":
                continue
            try:
                report = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            for item in report.get("items", []) if isinstance(report, dict) else []:
                if not isinstance(item, dict) or item.get("id") != ident:
                    continue
                checks = []
                for check in item.get("checks", []) or []:
                    if not isinstance(check, dict):
                        continue
                    sources = []
                    for source in check.get("sources", []) or []:
                        if isinstance(source, dict):
                            source = dict(source)
                            source["confirm"] = _confirm_status(confirm, str(source.get("url", "")), str(source.get("passage", "")))
                            sources.append(source)
                    checks.append({"field": check.get("field"), "text": check.get("text"), "verdict": check.get("verdict"), "note": check.get("note", ""), "sources": sources})
                reports.append({"release": report.get("release", release_dir.name), "reviewer": report.get("reviewer", path.stem), "start": report.get("start"), "decision": item.get("decision"), "fix": item.get("fix", ""), "unchecked": item.get("unchecked", []), "checks": checks})
    return reports


def cross_problems(release: str, ident: str) -> list[str] | None:
    try:
        module = importlib.import_module("cross_review")
        result = module.check_release(release)
    except (ImportError, AttributeError, OSError, ValueError):
        return None
    if isinstance(result, dict):
        candidate = result.get(ident, [])
    else:
        candidate = [problem for problem in result if getattr(problem, "id", None) == ident or (isinstance(problem, dict) and problem.get("id") == ident)]
    return [str(problem) for problem in candidate]


class ReviewService:
    def __init__(self, paths: list[str], wiki_dir: str, review_dir: str, default_by: str, token: str):
        self.paths, self.wiki_dir, self.review_dir = paths, Path(wiki_dir), Path(review_dir)
        self.default_by, self.token = default_by, token

    def queue(self) -> dict:
        graph = st.load_graph(self.paths)
        names = {ident: str(record.get("name") or record.get("title") or ident) for ident, record in graph["entities"].items()}
        gate = pg.gate(self.paths, str(self.wiki_dir))
        public = set(gate["entities"]) | set(gate["claims"]) | set(gate["wiki"])
        pre = worksheets(self.review_dir)
        records = []
        for ident, record in sorted(graph["entities"].items()):
            typ = graph["types"].get(ident, "")
            if typ == "Source":
                continue
            is_item = typ == "AssessmentItem" and record.get("kind") == "lab_prediction"
            if typ == "Claim":
                kind, label, title = "claim", "주장", claim_sentence(record, names)
                details = self.claim_details(record, graph)
            elif is_item:
                kind, label, title = "item", "실험 예측 문항", str(record.get("name") or record.get("prompt") or ident)
                details = {key: record.get(key) for key in ("prompt", "choices", "answer", "tolerance", "rationale")}
            elif typ in pg.ENTITY_TYPES:
                kind, label, title = "entity", TYPE_LABELS.get(typ, typ), names[ident]
                details = self.entity_details(record, typ)
            else:
                continue
            records.append(self.base_record(ident, kind, label, title, approval(record), review_by(record), ident in public, details, pre))
        for path in sorted(self.wiki_dir.glob("*.mdx")) if self.wiki_dir.is_dir() else []:
            meta, body = pg.read_wiki(path)
            ident = meta.get("id")
            if not isinstance(ident, str):
                continue
            details = {"status": meta.get("status"), "entity": meta.get("entity"), "claims": meta.get("claims", []), "source": path.read_text(encoding="utf-8")}
            records.append(self.base_record(ident, "wiki", "위키", str(meta.get("title") or ident), approval(meta, True, body), review_by(meta), ident in public, details, pre))
        return {"records": records, "default_by": self.default_by, "agent_session": review.agent_session()}

    def base_record(self, ident, kind, label, title, state, approved_by, is_public, details, pre):
        item = {"id": ident, "kind": kind, "type_label": label, "title": title, "state": state, "approved_by": approved_by, "public": is_public, "details": details, "pre_review": pre.get(ident), "cross_review": cross_reviews(self.review_dir, ident)}
        releases = {entry["release"] for entry in item["cross_review"] if entry.get("release")}
        problems = {release: cross_problems(str(release), ident) for release in releases}
        if any(value is not None for value in problems.values()):
            item["cross_review_problems"] = problems
        return item

    @staticmethod
    def entity_details(record: dict, typ: str) -> dict:
        details = {"aliases": record.get("aliases", []), "summary": record.get("summary"), "fields": record.get("fields", [])}
        if typ == "Paper":
            identifiers = record.get("identifiers") or {}
            arxiv = identifiers.get("arxiv")
            details["paper"] = {"title": record.get("title") or record.get("name"), "authors": record.get("authors", []), "date": record.get("earliest_public_date"), "venue": record.get("venue"), "arxiv": f"https://arxiv.org/abs/{arxiv}" if arxiv else None}
        return details

    @staticmethod
    def claim_details(record: dict, graph: dict) -> dict:
        evidence = []
        for row in record.get("evidence", []) or []:
            source = graph["sources"].get(row.get("source"), {})
            fulltext = source.get("fulltext_url") or source.get("url")
            evidence.append({"quote": row.get("quote"), "locator": row.get("locator"), "type": row.get("type"), "stance": row.get("stance"), "source_title": source.get("title") or source.get("name") or row.get("source"), "source_version": source.get("version") or source.get("identifiers", {}).get("arxiv"), "fulltext_url": fulltext, "text_link": text_fragment(str(fulltext or ""), str(row.get("quote") or ""))})
        return {"predicate": record.get("predicate"), "predicate_label": PREDICATE_LABELS.get(record.get("predicate"), record.get("predicate")), "subject": record.get("subject"), "object": record.get("object"), "status": record.get("status"), "confidence": record.get("confidence"), "qualifiers": record.get("qualifiers", {}), "note": record.get("note", ""), "evidence": evidence}

    def write_decisions(self, by: str, decisions: list[dict]) -> dict:
        if review.agent_session():
            raise PermissionError("AI 에이전트 세션에서는 승인 기록을 만들 수 없습니다 (ADR-021).")
        if not isinstance(by, str) or not st.HUMAN_RE.match(by):
            raise PermissionError("검토자 ID는 human:<id> 형식이어야 합니다.")
        if not decisions:
            raise ValueError("기록할 결정이 없습니다.")
        entries = []
        for decision in decisions:
            ident, action = decision.get("id"), decision.get("decision")
            if not isinstance(ident, str) or action not in {"approve", "fix", "exclude"}:
                raise ValueError("각 결정에는 id와 approve|fix|exclude 결정이 필요합니다.")
            entries.append({"id": ident, "decision": action, "notes": str(decision.get("note", "")), "publish": bool(decision.get("publish", False))})
        self.review_dir.joinpath("decisions").mkdir(parents=True, exist_ok=True)
        now = dt.datetime.now(dt.timezone.utc)
        path = self.review_dir / "decisions" / f"{now.strftime('%Y%m%dT%H%M%S%fZ')}.yaml"
        path.write_text(yaml.safe_dump({"reviewed_at": now.isoformat(), "by": by, "items": entries}, allow_unicode=True, sort_keys=False), encoding="utf-8")
        result = review.approve_batch(self.paths, str(self.wiki_dir), path, by, now.date().isoformat(), entries)
        return {**result, "decision_file": str(path)}

    @staticmethod
    def commit_push(by: str, approved: int) -> str:
        if review.agent_session():
            raise PermissionError("AI 에이전트 세션에서는 커밋하거나 배포할 수 없습니다 (ADR-021).")
        if not isinstance(by, str) or not st.HUMAN_RE.match(by):
            raise PermissionError("검토자 ID는 human:<id> 형식이어야 합니다.")
        paths = list(COMMIT_PATHS)
        output = []
        for command in (["git", "add", "--", *paths], ["git", "diff", "--cached", "--quiet", "--", *paths]):
            run = subprocess.run(command, text=True, capture_output=True, check=False)
            output.append("$ " + " ".join(command) + "\n" + run.stdout + run.stderr)
            if command[1:4] == ["diff", "--cached", "--quiet"] and run.returncode == 0:
                raise ValueError("커밋할 review/, data/, src/content/wiki/ 변경이 없습니다.")
            if run.returncode not in (0, 1):
                raise RuntimeError("".join(output))
        for command in (["git", "commit", "-m", f"review: {approved} approved by {by}", "--", *paths], ["git", "push"]):
            run = subprocess.run(command, text=True, capture_output=True, check=False)
            output.append("$ " + " ".join(command) + "\n" + run.stdout + run.stderr)
            if run.returncode:
                raise RuntimeError("".join(output))
        return "".join(output)


class Handler(BaseHTTPRequestHandler):
    service: ReviewService

    def log_message(self, _format, *_args):
        """Avoid access logs: a query string would expose the one-time token."""

    def send_json(self, status: int, body: dict):
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded))); self.end_headers(); self.wfile.write(encoded)

    def authorized(self) -> bool:
        token = parse_qs(urlparse(self.path).query).get("token", [self.headers.get("X-Review-Token", "")])[0]
        return hmac.compare_digest(str(token).encode(), self.service.token.encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/queue":
            if not self.authorized(): return self.send_json(HTTPStatus.FORBIDDEN, {"error": "검수 토큰이 필요합니다."})
            try: return self.send_json(HTTPStatus.OK, self.service.queue())
            except Exception as exc: return self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
        path = APP_DIR / ("index.html" if parsed.path == "/" else parsed.path.lstrip("/"))
        if not path.is_file() or APP_DIR not in path.resolve().parents:
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "찾을 수 없습니다."})
        content = path.read_bytes(); self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(content))); self.end_headers(); self.wfile.write(content)

    def do_POST(self):
        if not self.authorized(): return self.send_json(HTTPStatus.FORBIDDEN, {"error": "검수 토큰이 필요합니다."})
        try:
            length = int(self.headers.get("Content-Length", "0")); body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict): raise ValueError("JSON 객체가 필요합니다.")
            if urlparse(self.path).path == "/api/decisions":
                return self.send_json(HTTPStatus.OK, self.service.write_decisions(body.get("by", ""), body.get("decisions", [])))
            if urlparse(self.path).path == "/api/commit-push":
                return self.send_json(HTTPStatus.OK, {"output": self.service.commit_push(body.get("by", ""), int(body.get("approved", 0)))})
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "찾을 수 없습니다."})
        except PermissionError as exc: return self.send_json(HTTPStatus.FORBIDDEN, {"error": str(exc)})
        except ValueError as exc: return self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc: return self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", help="comma-separated graph files")
    parser.add_argument("--wiki-dir", default=os.environ.get("AIXON_WIKI_DIR", "src/content/wiki"))
    parser.add_argument("--review-dir", default="review", help=argparse.SUPPRESS)
    parser.add_argument("--port", type=int, default=4400)
    parser.add_argument("--by", default="human:keeweon")
    args = parser.parse_args(argv)
    token = secrets.token_urlsafe(32)
    Handler.service = ReviewService(pg.graph_paths(args.graph), args.wiki_dir, args.review_dir, args.by, token)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"http://127.0.0.1:{server.server_port}/?token={token}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

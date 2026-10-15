# REQUIREMENT_TRACEABILITY — P0 요구사항 추적표 (v0.1)

> 요구사항 정의: [07_MVP_ROADMAP.md §1](../07_MVP_ROADMAP.md). 시나리오: [CONTENT_VALIDATION_PLAN.md §2](../CONTENT_VALIDATION_PLAN.md). 경로·파일명은 구현 결과에 맞춰 갱신한다(마지막 갱신: 2026-10-15, 감사 반영 — [08_ARCHITECTURE_REVIEW.md](../08_ARCHITECTURE_REVIEW.md)).

| ID | 사용자 시나리오 | 데이터 엔티티 | 인터페이스(정적 경로·산출물) | UI 컴포넌트 | 구현 모듈 | 인수 기준 | 검증 테스트 |
|---|---|---|---|---|---|---|---|
| R-01 | J1 지형 파악 | ResearchField, KU, Paper, Problem, Claim(02 §4, §7) | `/fields/<slug>/`, `/e/<type>/<slug>/`, `graph.json` | 분야·Entity 페이지 | `data/**/*.yaml`, `src/lib/graph/`, `tools/seedtool.py` | G 0, 인용 100%, arXiv 대조 100% | V-GRAPH, V-QUOTE, V-ID, `tests/unit/graph.test.ts` |
| R-02 | J1 | Field 계층(`parents`), 소속(`fields`) | `/atlas/`, `graph.json` | `GraphView mode=atlas`, 노드 패널, 목록 보기 | `src/islands/GraphView.tsx`, `src/lib/graph/view.ts`(보이는 노드 80개 상한) | 점진 확장·필터·패널 이동 | `tests/unit/view.test.ts`, E2E-1, E2E-7, E2E-11 |
| R-03 | J3 개념 이해 | Wiki 문서(CONTENT_SCHEMA §2) | `/wiki/<slug>/` | `Section`, `Level`, 단계 전환 | `src/content.config.ts`, `src/components/wiki/` | 스키마 위반 시 빌드 실패 | V-SCHEMA-1…3, E2E-1 |
| R-04 | J3 | `wiki:scaled-dot-product-attention`, 관련 Claim·Source | `/wiki/scaled-dot-product-attention/` | 위 + Lab | `src/content/wiki/scaled-dot-product-attention.mdx` | 9개 섹션, 숫자 assert 통과 | V-CODE-1, E2E-1, E2E-2 |
| R-05 | J3 | `figures[]` | (빌드 결과 HTML) | KaTeX, Shiki, `Figure` | remark-math, rehype-katex | katex-error 0, MathML, alt | V-MATH, V-FIG-1, E2E-8 |
| R-06 | J3 → J1 | Entity ID(불변) | `ConceptLink` → `/wiki/…` 또는 `/e/…`, `/atlas/#node-<id>` | `ConceptLink`, "그래프에서 보기" | `src/lib/url.ts`, 컴포넌트 | 깨진 참조 0 | V-LINK-1, V-DIST-LINK, E2E-1 |
| R-07 | 모든 진입 | Entity 이름·별칭 | `node-index.json`, `/pagefind/`, `/search/` | 헤더 빠른 검색, Pagefind UI | `src/lib/search.ts`, `src/pages/node-index.json.ts`, pagefind | 2글자 한국어("어텐"), 별칭·한국어 이름("스케일드"), 결과 → 이동 | V-SEARCH, `tests/unit/search.test.ts`, E2E-5 |
| R-08 | J5 신뢰 | Claim, Evidence, Source | `/claims/<slug>/` | Evidence Inspector, 참고문헌 | `src/pages/claims/` | 인용·위치·링크·상태·검토 | E2E-3, V-CITE-1…3 |
| R-09 | 모든 것의 기준 | `data/seed/seed_graph.yaml`, fixtures | — | — | `tools/seedtool.py` | Claim 105(verified 95, disputed 1, proposed 8, rejected 1), 인용 offline 132/132(오케스트레이터 실행), golden 계획 | V-QUOTE, `pytest tools`(`test_seedtool.py` T1–T18, `test_public_gate.py`, `test_verify_identifiers.py`) |
| R-10 | 공개 | — | `dist-public/`, `.github/workflows/pages.yml` | — | astro config(base, trailingSlash) | 직접 링크·새로고침 200 | E2E-6, V-DIST-LINK (실배포 NOT RUN) |
| R-11 | 유지보수 | — | `make verify`, `artifacts/verification/runs/*/summary.json`, `ci.yml` | — | `Makefile`, `tools/*.py` | 한 명령으로 전 계층, 실패 시 non-zero | 하네스 자체 실행 기록 |
| R-12 | J3 | LabExperiment, lab_prediction 문항, golden fixture | Wiki 안 island | `SoftmaxTemperatureLab` | `src/lib/lab/`, `src/islands/SoftmaxTemperatureLab.tsx` | 화면 수치 = fixture(4자리) | V-LAB L1–L7, `tests/unit/lab.test.ts`, E2E-2 |
| R-13 | J2 계보 | 연구 Claim(INTRODUCES·EXTENDS·ADAPTS·IMPROVES_ON·…) | `/trace/` | `GraphView mode=trace` | `src/islands/GraphView` | 연도 배치, 간선 → Claim, CITES 숨김 기본 | E2E-4, V-CITES-NOT-INFLUENCE |
| R-14 | J1 | Wiki status, Claim status | `/coverage/`, 배지 | Coverage 표, 상태 배지 | `src/pages/coverage.astro`, `src/lib/coverage.ts`, `src/lib/badges.ts` | 5단계 상태 집계, 배지 3축(인용 확인 / 사람 검토 / 공개, ADR-022) | V-STATUS-1, `tests/unit/coverage.test.ts`, E2E-7 |
| R-15 | J5 | 엔티티·Claim·Wiki의 `review`(`by: human:*`, `reviewed_hash`), `published_at` | `AIXON_BUILD=public`(기본값 없음), `.aixon/public-gate.json` | "준비 중"·"(검토 대기)" 표시 | 공개 관문 ADR-021: `tools/public_gate.py`(허용 목록 계산), `tools/review.py`(승인 기록), `src/lib/graph/`(가시성 한 모듈), `tools/check_dist.py`(public 모드: 관문 재계산 + taint 테스트) | 미승인·오래된 승인 0, 관문 없음·오래됨 → 빌드 실패 | `tools/test_public_gate.py`, seedtool G022, E2E-9, V-PUBLIC, V-STATUS-2, `tests/unit/graph.test.ts` |
| R-16 | 공개 품질 | — | `sitemap-index.xml`, `robots.txt` | 반응형 레이아웃, aria | 레이아웃 | 가로 넘침 0, SEO 기본 | V-SEO, E2E-7, E2E-8 |

## 역추적: 구현 요소 → 요구사항

| 구현 요소 | 요구사항 | 비고 |
|---|---|---|
| `tools/seedtool.py validate/quotes` | R-01, R-09, R-11, R-15 | 빌드 전 관문. G022–G025·W107–W111 포함 |
| `tools/public_gate.py`, `tools/review.py` | R-15 | 공개 허용 목록 계산, 사람 승인 기록(에이전트 세션에서는 거부 — 실수 방지) |
| `tools/check_dist.py` | R-10, R-15, R-16 | V-DIST-LINK, V-MATH, V-SEO, V-PUBLIC, V-SEC, V-NO-CDN |
| `tools/validate_content.py` | R-03, R-04, R-05 | V-SCHEMA, V-CITE, V-CODE, V-STATUS, V-LINK, V-FIG, V-LABREF, MDX import·raw HTML 금지 |
| `src/lib/coverage.ts`, `src/lib/search.ts`, `src/lib/graph/view.ts` | R-14, R-07, R-02·R-13 | 단위 테스트 `tests/unit/{coverage,search,view}.test.ts` |
| `tests/e2e/e2e-01…11` | R-02, R-04, R-06–R-08, R-10, R-12–R-16 | 01 그래프→Wiki→그래프, 02 Lab 수치, 03 Evidence Inspector, 04 Trace, 05 Pagefind, 06 직접 링크, 07 레이아웃, 08 SEO·접근성, 09 공개 관문, 10 ViT 여정(시드), 11 Atlas 조작 |
| `tools/seedtool.py plan/mastery` | (P2) | 04 문서 기준 구현 유지 — v0.1 사이트는 사용하지 않음 |
| `tools/verify_identifiers.py` | R-01, R-09 | 네트워크 필요 → 수동·CI 선택 단계 |
| `tools/gen_lab_fixtures.py` | R-12 | numpy 기준값 |
| `study/physical-ai/` | (P0 밖, 사용자 별도 요청) | Physical AI 로드맵 학습 앱(Artifact) |
| 06 문서 FastAPI·SQLite 설계 | (P2) | 보존 |

P0 요구사항 중 매핑이 없는 항목: **없음**. 매핑이 없는 구현 요소는 P2로 명시한 것뿐이다.

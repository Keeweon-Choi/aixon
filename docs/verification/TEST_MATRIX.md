# TEST_MATRIX — 요구사항별 검증 계층과 결과

> 2026-10-15. 결과는 깨끗한 환경 실행 `artifacts/verification/runs/20261015T040334Z/`(`b6ca3d7`, 13단계 PASS)에서 가져왔다. 판정과 해석은 [MVP_ACCEPTANCE_REPORT.md](MVP_ACCEPTANCE_REPORT.md), 계획은 [VERIFICATION_PLAN.md](VERIFICATION_PLAN.md), 규칙 정의는 [CONTENT_VALIDATION_PLAN.md](../CONTENT_VALIDATION_PLAN.md)에 있다.
> 상태는 PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE만 쓴다. "—"는 그 계층에 해당 검사가 없다는 뜻이다(돌리지 않았다는 뜻이 아니다).

읽는 법.

- **정적 검사** 열: `make lint`(prettier, eslint, astro check, ruff)와 `make typecheck`(astro check, tsc)는 모든 코드에 공통으로 PASS였다. 열에는 그 요구사항에만 해당하는 것을 적는다.
- **E2E** 열의 숫자는 Playwright 결과 건수다(desktop + mobile 합). fixture 빌드는 `tests/fixtures/`의 결정적인 그래프·Wiki, seed 빌드는 실제 `data/seed` + `data/graph/atlas.yaml`이다. E2E-10은 seed에서만 돈다.
- **실제 사용 확인** 열: 최종 독립 리뷰(Opus 5.5 High, `85c3c39`)의 브라우저 사용 스크린샷 번호. 경로는 `artifacts/verification/final-review-20261015/shots/`이고 사람이 아니라 AI가 본 것이다. 한글이 네모로 보이는 것은 헤드리스 머신에 글꼴이 없어서다.
- 단위 열의 개수는 `pytest --collect-only` 결과다(합계 201). vitest는 5개 파일 22개다.

## 1. 요구사항별 매트릭스

| 요구사항 | 정적 검사 | 단위 | 데이터·콘텐츠 | 빌드·산출물 | E2E fixture | E2E seed | 실제 사용 확인 | 결과 |
|---|---|---|---|---|---|---|---|---|
| R-01 AI 전체 분야 Knowledge Graph | 공통 | `test_seedtool.py` 63개, `graph.test.ts` | `seedtool validate` G 0 (V-GRAPH). 인용 132/132 (V-QUOTE, 수동). arXiv 67/67 (V-ID, 수동) | `check-dist` 632쪽 | E2E-11 (14) | E2E-1 (10), E2E-7 (22) | 09–11 Atlas | PASS |
| R-02 Interactive Atlas | 공통 | `view.test.ts` 10개 | — | `check-dist` | E2E-1 (10), E2E-7 (22), E2E-11 (14) | E2E-1 (10), E2E-7 (22), E2E-10 ① | 09 Atlas, 10 Atlas CV, 11 ViT 패널, 16 딥링크 | PASS |
| R-03 Wiki 콘텐츠 모델·렌더러 | 공통 | `test_validate_content.py` 43개, `test_fixtures.py` 9개, `graph.test.ts` (Wiki 가시성) | `validate_content` V-SCHEMA-1~3 (`validate`, `validate-fixtures`) | `build`: zod 스키마 위반이면 실패. 632쪽 성공 | E2E-1 (10) | E2E-1 "related concepts respect direction and status" | 04–05 Wiki | PASS |
| R-04 대표 개념 교육 페이지 | 공통 | `test_validate_content.py` (`python verify` 허용 import, 실패 메시지) | V-CODE-1 (SDPA의 `python verify` 블록), 섹션 9개 | `build` | E2E-1, E2E-2 | E2E-1, E2E-2 | 04–07 | PASS (내용의 사람 검토는 NOT RUN) |
| R-05 수식·코드·다이어그램 | 공통 | `test_check_dist.py` (V-MATH 실패 케이스) | V-FIG-1 | `check-dist`: `katex-error` 0, MathML (V-MATH) | E2E-8 "KaTeX output includes MathML" | — | 05 Wiki 전체 | PASS |
| R-06 Graph ↔ Wiki 이동 | 공통 | — | V-LINK-1 | `check-dist`: 내부 링크 해석 (V-DIST-LINK), `check-dist-seed` | E2E-1 (10) | E2E-1 (ConceptLink → Entity → Atlas, Wiki → Entity, Wiki → Atlas) | 03 Entity, 05 Wiki, 16 딥링크 | PASS |
| R-07 검색 | 공통 | `search.test.ts` 3개 | — | Pagefind 색인 632쪽 (`logs/06-build.log`) | E2E-1 (한국어 2글자, 키보드), E2E-5 (2) | E2E-1 | 02, 15 검색 | PASS (E2E-5는 fixture만) |
| R-08 근거·참고문헌 | 공통 | `test_seedtool.py` | V-CITE-1~3 | `check-dist` | E2E-3 (12) | E2E-1 "references and inline citations are human readable" | 08 Claim | PASS |
| R-09 검증된 시드 콘텐츠 | 공통 | `test_seedtool.py` T1–T18, `test_public_gate.py`, `test_verify_identifiers.py` | Claim 105 (95/1/8/1), 인용 132/132, 식별자 67/67, golden 계획 (P15·P15b) | — | — | E2E-10 (실제 시드 여정) | — | PASS |
| R-10 GitHub Pages 배포 | 공통 | `test_check_dist.py` (base 경로) | — | `check-dist-public`, `check-dist-seed` (base `/aixon/`) | E2E-6 (8) | E2E-6 (8) | 실배포: 해당 없음 | PASS (로컬 재현). 실배포 NOT RUN |
| R-11 자동 검증 하네스 | 공통 | `test_verify.py` 8개, `test_scan_secrets.py` 21개 | `graph-validation.json` 기록 | `summary.json`, 로그, Playwright 보고서 수집 | — | — | — | PASS (로컬). GitHub `ci.yml` NOT RUN |
| R-12 Interactive Lab | 공통 | `lab.test.ts` (V-LAB L1–L7) | `test_fixture_lab_matches_the_seed_contract` (numpy fixture) | `build` | E2E-2 (2) | E2E-2 (2), E2E-10 ④ | 06 Lab, 07 퀴즈 | PASS |
| R-13 연구 계보(Trace) | 공통 | `view.test.ts` (연도 순서, CITES 제외, 술어 필터), `test_seedtool.py` T16 | V-CITES-NOT-INFLUENCE | `check-dist` | E2E-4 (14) | E2E-10 ② | 12 Trace, 13 Trace → Claim, after-fix `trace-*` | PASS |
| R-14 콘텐츠 상태·Coverage | 공통 | `coverage.test.ts` | V-STATUS-1 | `check-dist` | E2E-7 (22) | E2E-7 (22) | 14 Coverage | PASS |
| R-15 콘텐츠 공개 관문 | 공통 | `test_public_gate.py` 6개, `graph.test.ts` ("fails closed", "requires a current public gate"), `test_check_dist.py` public 케이스 | seedtool G022. `public_gate.py` 계산 (`validate` 단계) | `build-public` 7쪽, `check-dist-public` (관문 재계산, taint) | E2E-9 (10) | — | — | PASS (관문). 공개할 콘텐츠는 BLOCKED (B-02) |
| R-16 SEO·접근성·반응형 | 공통 | `test_check_dist.py` 48개 | — | `check-dist`: V-SEO, V-SEC, V-NO-CDN | E2E-7 (22), E2E-8 (28) | E2E-7 (22) | 모바일 01–15, after-fix `atlas-selected-mobile` | PASS (색인·보조기기는 NOT RUN) |

## 2. 규칙 그룹(V-*)별 결과

| 규칙 | 무엇을 | 어디서 돌았나 | 결과 |
|---|---|---|---|
| V-GRAPH | 그래프 불변식 G001~G025 | `make validate` (`seedtool validate`), `test_seedtool.py` | PASS (G 0, 경고 159건은 비치명) |
| V-QUOTE | 인용문이 지정 버전 원문에 있음 | `seedtool quotes --offline` (수동, 캐시 필요) | PASS (132/132). `make verify`에는 들어 있지 않다 |
| V-ID | arXiv ID ↔ 제목 | `verify_identifiers.py` (수동, 네트워크 필요) | PASS (67/67). `make verify`에는 들어 있지 않다 |
| V-CITES-NOT-INFLUENCE | CITES가 영향 관계가 되지 않음 | `test_seedtool.py` T16, `view.test.ts`, E2E-4, E2E-10 ② | PASS |
| V-VERIFIED-ONLY | proposed·disputed가 선수 계산·공개 그래프에 안 들어감 | `graph.test.ts`, `view.test.ts` (verified-only 필터), E2E-11 | PASS |
| V-SCHEMA / V-LINK / V-CITE / V-STATUS / V-CODE / V-FIG | Wiki 계약, 링크, 인용, 상태, 계산 블록, 그림 | `make validate`, `validate-fixtures`, `test_validate_content.py` | PASS ("0 error(s), 0 warning(s)") |
| MDX 보안 규칙 | import·raw HTML·`on*`·`javascript:` 금지 | `test_mdx_security_rules_reject_unsafe_content` (3건), `validate_content.py` | PASS |
| V-BUILD | `astro build` 성공 (preview, public) | `make build`, `make build-public` | PASS |
| V-MATH / V-DIST-LINK / V-SEO / V-SEC / V-NO-CDN | 산출물 검사 | `check-dist`, `check-dist-public`, `check-dist-seed`, `test_check_dist.py` | PASS (public에서 404 canonical 경고 1건, exit 0) |
| V-PUBLIC | 미승인 Wiki·Claim·AI 요약이 public에 없음 | E2E-9, `check_dist.py --mode public`, `test_public_gate.py` | PASS |
| V-SECRETS | 비밀 유출 없음 | `make secrets` | PASS (3317개 파일) |
| V-LAB L1–L7 | softmax 합, shift invariance, 수치 안정성, fixture 일치, 난수, 분산, SDPA 통계 | `lab.test.ts`, E2E-2 | PASS |
| V-LOADER / V-SEARCH | 로더 병합·중복 ID·빌드 모드 필터, 노드 검색 | `graph.test.ts`, `search.test.ts` | PASS |
| V-PLANNER (P2 기준 구현) | 학습 계획 | `test_seedtool.py` M·P 시리즈, golden | PASS (기준 구현 유지. v0.1 사이트는 쓰지 않음) |

## 3. E2E 시나리오별 결과

| 시나리오 | fixture | seed | 비고 |
|---|---|---|---|
| E2E-1 Graph → Wiki → Related → Graph | PASS (10) | PASS (10) | |
| E2E-2 Lab 수치 | PASS (2) | PASS (2) | |
| E2E-3 Evidence Inspector | PASS (12) | — | seed에서는 돌리지 않는다 |
| E2E-4 Trace | PASS (14) | — | seed 쪽은 E2E-10 ② |
| E2E-5 Pagefind | PASS (2) | — | |
| E2E-6 직접 링크·새로고침 | PASS (8) | PASS (8) | `/aixon/` base |
| E2E-7 레이아웃 | PASS (22) | PASS (22) | |
| E2E-8 SEO·접근성 | PASS (28) | — | |
| E2E-9 공개 관문 | PASS (10) | — | fixture public 빌드만 |
| E2E-10 Understanding Vision Transformer | — (seed 전용) | ① Explore, ② Trace, ③ Learn, ④ Lab: PASS (8). ⑤ Remember, ⑥ Resume: NOT APPLICABLE (4 skipped) | `test.fixme("P2 (ADR-019)")` |
| E2E-11 Atlas 조작 | PASS (14) | — | I-40 수정 뒤 2코어 반복 통과 |
| 합계 | 122 expected, 0 unexpected, 0 flaky | 50 expected, 4 skipped, 0 unexpected, 0 flaky | `playwright-{fixture,seed}.json` |

## 4. `make verify` 13단계 (2코어, 깨끗한 환경)

실행 `20261015T040334Z`, 커밋 `b6ca3d7`, git dirty false, 합계 232.18초. 로그는 `artifacts/verification/runs/20261015T040334Z/logs/`.

| # | 단계 | 명령 | 상태 | 시간(초) | 로그 |
|---|---|---|---|---|---|
| 1 | lint | `make lint` | PASS | 20.01 | `01-lint.log` |
| 2 | typecheck | `make typecheck` | PASS | 18.71 | `02-typecheck.log` |
| 3 | test | `make test` | PASS | 21.56 | `03-test.log` |
| 4 | validate | `make validate` | PASS | 1.77 | `04-validate.log` |
| 5 | validate-fixtures | `make validate-fixtures` | PASS | 0.32 | `05-validate-fixtures.log` |
| 6 | build | `make build` | PASS | 2.84 | `06-build.log` |
| 7 | check-dist | `make check-dist` | PASS | 0.46 | `07-check-dist.log` |
| 8 | build-public | `make build-public` | PASS | 2.34 | `08-build-public.log` |
| 9 | check-dist-public | `make check-dist-public` | PASS | 1.38 | `09-check-dist-public.log` |
| 10 | e2e | `make e2e` | PASS | 83.38 | `10-e2e.log` |
| 11 | e2e-seed | `make e2e-seed` | PASS | 72.11 | `11-e2e-seed.log` |
| 12 | check-dist-seed | `make check-dist-seed` | PASS | 1.52 | `12-check-dist-seed.log` |
| 13 | secrets | `make secrets` | PASS | 4.83 | `13-secrets.log` |

## 5. 다른 실행 기록

| 실행 | 커밋 | 결과 | 의미 |
|---|---|---|---|
| `20261015T030106Z` | `85c3c39` | PASS (12단계) | 최종 리뷰 수정 전. `check-dist-seed` 단계가 아직 없었다 |
| `20261015T034011Z` | `118eb36` | FAIL (`e2e`, `e2e-seed`) | 2코어에서 Atlas 클릭 간헐 실패 (I-40) |
| `20261015T040334Z` | `b6ca3d7` | PASS (13단계) | 위 수정 뒤 최종 실행 |

I-40 수정의 반복 시험 (2코어, `--repeat-each=10`): 수정 전 1/10, 3/10 실패 → 수정 후 70/70, 40/40 통과. 최종 실행의 작업 로그에는 E2E-11 desktop ×5 → 35 통과, E2E-10 desktop ×5 → 20 통과(10 skipped)가 더 있다.

## 6. 이 매트릭스에 없는 것

| 항목 | 상태 |
|---|---|
| GitHub Actions 실행 (`ci.yml`, `pages.yml`, `verify-online.yml`) | NOT RUN |
| 실제 GitHub Pages 배포·공개 URL | NOT RUN |
| 사용자가 직접 써 본 확인, 콘텐츠의 사람 검토 | NOT RUN |
| 숙련도 저장·재계산 (E2E-10 ⑤⑥), 계정, 학습 이력, LLM API | NOT APPLICABLE (P2, ADR-019) |
| DB 마이그레이션 | NOT APPLICABLE (v0.1에 DB 없음, ADR-015) |

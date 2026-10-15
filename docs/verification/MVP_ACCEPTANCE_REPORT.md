# MVP_ACCEPTANCE_REPORT — AIXON v0.1 인수 보고서

> 2026-10-15. 범위는 ADR-019(v0.1 = Knowledge Atlas + Interactive AI Wiki)다. 요구사항은 [07_MVP_ROADMAP.md §1](../07_MVP_ROADMAP.md), 추적은 [REQUIREMENT_TRACEABILITY.md](REQUIREMENT_TRACEABILITY.md), 계획은 [VERIFICATION_PLAN.md](VERIFICATION_PLAN.md), 테스트별 결과는 [TEST_MATRIX.md](TEST_MATRIX.md)에 있다.
> 상태는 PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE 다섯 가지만 쓴다. 증거 파일 경로는 저장소 기준이다. `artifacts/verification/runs/`와 `final-review-*/`는 git에 넣지 않는 로컬 증거이고, 통합 저장소 `~/wt/aixon-base`에 있다.
> 기준 커밋: 깨끗한 환경 검증은 `b6ca3d7`에서 돌렸다. 그 뒤 `main`의 커밋은 문서, `.gitignore`, 재현용 `tools/clean_env_verify.sh`(검증 파이프라인 밖)뿐이고 검증 대상 코드는 바뀌지 않았다(`git diff --stat b6ca3d7..main -- src tests tools/*.py Makefile`가 비어 있다).

## 1. 판정 요약

**판정: PASS (조건 4개).** v0.1의 코드, 검증 하네스, 시드 그래프는 인수 기준을 채웠다. Critical 미해결은 0건이다. 다만 아래 네 가지는 하지 않았거나 못 했으므로 "공개 가능"이라는 뜻은 아니다.

| # | 조건 | 상태 |
|---|---|---|
| 1 | 실제 GitHub Pages 배포 | NOT RUN (사용자 승인 필요, B-01) |
| 2 | 사람의 콘텐츠 승인 | 0건. 공개 빌드는 정적 7쪽뿐이다 (B-02) |
| 3 | GitHub에서 도는 Actions(`ci.yml`, `pages.yml`, `verify-online.yml`) | NOT RUN (원격 저장소가 없다) |
| 4 | 사람이 직접 써 본 확인 | NOT RUN. "실제 사용 확인"은 AI 리뷰어가 브라우저로 한 것이다 (§3.2) |

핵심 숫자는 아래와 같다. 모두 §7의 파일에서 확인했다.

| 항목 | 값 | 출처 |
|---|---|---|
| 깨끗한 환경 `make verify` | 13단계 PASS, 232.18초, git dirty false | `artifacts/verification/runs/20261015T040334Z/summary.json` |
| vitest / pytest | 22 / 201 통과 | 같은 실행의 `logs/03-test.log` |
| Playwright fixture | 122 expected, 0 unexpected, 0 flaky | `test-results/playwright-fixture.json` |
| Playwright seed | 50 expected, 4 skipped, 0 unexpected, 0 flaky | `test-results/playwright-seed.json` |
| 빌드 | preview 632쪽, public 7쪽 | `logs/07-check-dist.log`, `logs/09-check-dist-public.log` |
| 시드 Claim | 105 (verified 95, disputed 1, proposed 8, rejected 1) | `data/seed/seed_graph.yaml` |
| 인용 원문 대조 | 132/132 found (오프라인, `content_sha256` 고정) | §4 |
| arXiv 식별자 | 67/67 일치 (Atlas 54 + 시드 13) | §4 |
| 그래프 G 오류 | 0 (경고 159건은 §9) | `graph-validation.json` |
| 사람 승인 | 0건 | `tools/public_gate.py` 출력 "0 entities, 0 claims, 0 wiki" |

건너뛴 4건은 E2E-10의 ⑤ Remember, ⑥ Resume(데스크톱·모바일)이고 P2 범위라서 NOT APPLICABLE이다(ADR-019).

## 2. P0 요구사항 R-01 ~ R-16

"최종 상태"는 깨끗한 환경 실행(`b6ca3d7`)을 기준으로 한다. "리뷰어 PARTIAL"은 최종 독립 리뷰(§3.2)가 `85c3c39`에서 부분 충족으로 본 항목이고, 그 뒤 수정과 재검증을 거쳤다. 테스트 이름은 [TEST_MATRIX.md](TEST_MATRIX.md)에서 찾을 수 있다.

| ID | 요구 | 최종 상태 | 근거 | 비고 |
|---|---|---|---|---|
| R-01 | AI 전체 분야 Knowledge Graph | PASS | 분야 92개(기준 ≥ 80). G 오류 0. 인용 132/132. arXiv 67/67. `tools/test_seedtool.py` 63개, `tests/unit/graph.test.ts` | 인용이 술어를 뒷받침하는지는 기계 검사가 없다(I-24). 사람 검토 몫이다 |
| R-02 | Interactive Atlas | PASS | `tests/unit/view.test.ts` 10개. E2E-1·7·11 fixture와 seed. E2E-10 ① | 이전 간헐 실패는 I-40으로 고쳤다(§8) |
| R-03 | Wiki 콘텐츠 모델과 렌더러 | PASS | `make validate`(V-SCHEMA, "0 error(s)"), `tests/python/test_validate_content.py` 43개, E2E-1 "관련 개념" 방향·상태 | 리뷰어 PARTIAL(관련 목록이 Claim 방향·상태를 무시, M1) → 수정 |
| R-04 | 대표 개념 교육 페이지 | PASS | `src/content/wiki/scaled-dot-product-attention.mdx`: 섹션 9개(기준 9개 이상), `python verify` 블록은 `make validate`에서 실행·통과. E2E-1·2 | 문서 상태는 `draft`, `review: null`. 내용 정확성의 사람 검토는 하지 않았다 |
| R-05 | 수식·코드·다이어그램 | PASS | `check_dist.py` V-MATH(`katex-error` 0, MathML), E2E-8 "KaTeX output includes MathML", V-FIG-1 | |
| R-06 | Graph ↔ Wiki 이동 | PASS | V-LINK-1, E2E-1(Wiki → Entity, Wiki → Atlas 노드), `check-dist`의 링크 검사 | 리뷰어 PARTIAL(Wiki에서 Entity/Atlas로 가는 링크 없음) → 링크 추가 |
| R-07 | 검색 | PASS | `tests/unit/search.test.ts` 3개, E2E-1 "2-character Korean query", E2E-5 Pagefind | E2E-5는 fixture 빌드에서만 돈다. 실제 시드 빌드는 Pagefind 색인 632쪽까지만 확인했다(`logs/06-build.log`) |
| R-08 | 근거·참고문헌 | PASS | E2E-3 12건(fixture), E2E-1 "references and inline citations are human readable" | 화면 상태 문구는 "인용 확인"(ADR-022). E2E-3에 "bare verified가 없다"는 음성 검사가 있다 |
| R-09 | 검증된 시드 콘텐츠 | PASS | Claim 105(95/1/8/1), 인용 132/132, golden 계획 `test_t18_p15` 등 3개 통과 | §4. 사람 승인 0건 |
| R-10 | GitHub Pages 배포 | PASS (로컬 재현). 실배포는 NOT RUN | `/aixon/` base로 E2E-6 fixture 8건·seed 8건, `check-dist-public`, `check-dist-seed`. `.github/workflows/pages.yml`은 작성만 했다 | 리뷰어 PARTIAL(Lab "근거 보기" 링크가 base 경로를 무시, M2) → 수정, `check-dist-seed` 단계 추가 |
| R-11 | 자동 검증 하네스 | PASS (로컬) | `make verify` 13단계, `tests/python/test_verify.py` 8개(실패한 단계가 있어도 끝까지 돌고 exit 1). 실패 실행의 기록은 `20261015T034011Z`(summary 상태 FAIL) | `ci.yml` 실행은 NOT RUN |
| R-12 | Interactive Lab | PASS | `tests/unit/lab.test.ts`(V-LAB L1–L7), E2E-2 fixture 2건·seed 2건(numpy fixture와 4자리 일치), E2E-10 ④ | |
| R-13 | 연구 계보(Trace) | PASS | E2E-4 14건(fixture), `view.test.ts`(연도 순서, CITES 제외, 술어 필터), E2E-10 ② | 리뷰어 PARTIAL(술어 필터 없음) → 필터 추가 |
| R-14 | 콘텐츠 상태·Coverage | PASS | `tests/unit/coverage.test.ts`, V-STATUS-1, E2E-7 | |
| R-15 | 콘텐츠 공개 관문 | PASS (관문 동작). 공개할 콘텐츠는 BLOCKED (B-02) | `tools/test_public_gate.py` 6개, seedtool G022, E2E-9 10건, `check_dist.py --mode public`의 taint 검사. 실제 데이터 public 빌드는 7쪽 | 승인 0건이라 관문이 비어 있는 것이 정상이다 |
| R-16 | SEO·접근성·반응형 | PASS | `check_dist.py`(V-SEO, V-SEC, V-NO-CDN), E2E-7 22건, E2E-8 28건(fixture) | 검색엔진 색인은 NOT RUN(배포 뒤에만 가능). 스크린 리더로 읽어 본 확인은 없다 |

R-03, R-06, R-10, R-13의 PARTIAL은 수정 뒤 PASS로 올렸다. 근거는 수정 검증(Opus 5.5 High, MERGE)과 깨끗한 환경 재실행이다. 리뷰어의 사용 흐름 전체를 수정 뒤에 처음부터 다시 걷지는 않았다. 수정 뒤에는 화면 3가지만 다시 봤다(§3.2).

## 3. 검증 결과: 테스트 통과와 실제 사용 확인

두 가지는 다른 증거다. 테스트가 통과해도 쓸 만한 화면인지는 따로 봐야 한다.

### 3.1 테스트 통과

| 계층 | 결과 | 증거 |
|---|---|---|
| 정적 검사 | PASS (prettier, eslint, astro check, ruff) | `logs/01-lint.log` |
| 타입 | PASS (astro check, tsc) | `logs/02-typecheck.log` |
| 단위 | PASS. vitest 22(5개 파일), pytest 201 | `logs/03-test.log` |
| 데이터·콘텐츠 | PASS. 공개 관문 계산, seedtool G 0, `validate_content` "0 error(s), 0 warning(s)" | `logs/04-validate.log`, `graph-validation.json` |
| fixture 검증 | PASS | `logs/05-validate-fixtures.log` |
| 빌드·산출물 | PASS. preview 632쪽, public 7쪽, seed 632쪽 | `logs/06`~`logs/09`, `logs/12` |
| E2E fixture | PASS. 122건 | `test-results/playwright-fixture.json` |
| E2E seed (실제 데이터) | PASS. 50건, 4건 skipped(NOT APPLICABLE) | `test-results/playwright-seed.json` |
| 비밀 검사 | PASS. 3317개 파일 | `logs/13-secrets.log` |
| 안정성 반복 (2코어) | PASS. E2E-11 desktop ×5 → 35 통과. E2E-10 desktop ×5 → 20 통과, 10 skipped | `clean-env-job.log` |
| 수동 외부 대조 | PASS (이 문서를 쓰며 직접 실행, §4) | 이 문서 |

`check-dist-public`은 `404.html`의 canonical 링크 경고 1건을 냈다. 종료 코드는 0이고, 검사기가 404 페이지의 canonical은 경고로만 다루도록 정해 둔 것이다(`test_canonical_of_the_404_page_is_only_a_warning`).

### 3.2 실제 사용 확인

| 확인 | 누가, 어떻게 | 증거 | 한계 |
|---|---|---|---|
| 최종 독립 리뷰 (Phase I) | Opus 5.5 High 리뷰어가 `85c3c39`의 실제 시드 빌드를 브라우저로 사용. 검색 → Wiki → Lab → 퀴즈 → Claim → Atlas → Trace → Coverage를 1280×900과 390×844에서 걸음. JS 오류 없음 | `artifacts/verification/final-review-20261015/shots/` 31장(데스크톱 16, 모바일 15) | 헤드리스 머신에 한글 글꼴이 없어 스크린샷의 한글이 네모로 보인다. 페이지 텍스트는 따로 확인했다. 사람이 아니라 AI가 본 것이다 |
| 리뷰 판정 | ACCEPT WITH FIXES. R-03, R-06, R-10, R-13이 PARTIAL, 나머지 PASS. Critical 없음 | 리뷰어 보고(오케스트레이터 전달) | 보고서 원문 파일은 찾지 못했다. 이 표는 전달된 요약이다 |
| 수정 뒤 화면 확인 | 수정 검증자가 Atlas 패널, Trace 레이블, 390px 가로 넘침을 다시 봄 | `final-review-20261015/after-fix-shots/` 6장 (`atlas-selected-*`, `trace-*`, `trace-selected-*`) | 위 3가지만이다. 전체 흐름 재실행은 아니다 |
| 데이터 직접 확인 | 이 문서 작성 중 직접 실행 | §4 | 네트워크 대조는 arXiv API 한 번의 응답이다 |
| 사용자가 직접 써 봄 | — | — | NOT RUN |
| 대표 Wiki의 설명 정확성을 사람이 읽고 검토 | — | — | NOT RUN (B-02) |

## 4. Seed Graph 상태

| 항목 | 값 | 확인 |
|---|---|---|
| Claim 수 | 105. verified 95, disputed 1(`clm:bn-mitigates-ics`), proposed 8, rejected 1(`vgg-extends-alexnet`) | 직접 집계(YAML) |
| 시드 규모 | 논문 15, 지식 단위 36, 학습 자료 73, 문항 19, Lab 1, 학습 목표 2 | `data/seed/README.md` (직접 세지 않음) |
| Atlas | 분야 92, 논문 54, 방법 54, 개념 13, 모델 6, 문제 17 | 직접 집계(YAML) |
| 그래프 검증 | `seedtool validate`: G 오류 0, exit 0. 경고 W103 1, W104 149, W111 9 | 직접 실행 |
| 인용 원문 대조 | `quotes --offline`: 132건 모두 `found`, exit 0 | 직접 실행 |
| 식별자 | `verify_identifiers.py`(온라인): 67건 모두 `match`, exit 0. 최종 리뷰어도 같은 결과 | 직접 실행 |
| golden 학습 계획 | `test_seedtool.py -k "t18 or p15"` 3개 통과 | 직접 실행 |
| 사람 승인 | 0건 (Claim 105개의 `review.by`가 `human:*`인 것 0개) | 직접 집계 |

`verified`는 "사람이 확인했다"가 아니다. 인용문이 지정한 버전의 원문에 있다는 기계 확인이다(ADR-022). 인용이 술어(INTRODUCES, ADAPTS 등)를 실제로 뒷받침하는지는 사람 검토 항목이다.

이 문서를 쓰며 다시 돌린 명령은 아래와 같다. 인용 캐시(`data/cache/fulltext`)는 git에 없어서 통합 저장소의 것을 지정했다.

```bash
.venv/bin/python tools/seedtool.py validate data/seed/seed_graph.yaml data/graph/atlas.yaml
.venv/bin/python tools/seedtool.py quotes --offline --cache ~/wt/aixon-base/data/cache/fulltext data/seed/seed_graph.yaml
.venv/bin/python tools/verify_identifiers.py data/seed/seed_graph.yaml data/graph/atlas.yaml   # 네트워크 필요
.venv/bin/python -m pytest tools/test_seedtool.py -k "t18 or p15"
```

인용 대조와 식별자 대조는 `make verify`에 들어 있지 않다. 캐시와 네트워크에 기대기 때문이다(`make verify-online`, 주 1회 CI 설정은 있으나 NOT RUN).

## 5. 공개 관문 상태

| 항목 | 상태 |
|---|---|
| 허용 목록 | 비어 있다. `public gate: 0 entities, 0 claims, 0 wiki, 0 excluded, 0 errors` (`logs/04-validate.log`) |
| 실제 데이터 public 빌드 | 정적 7쪽. `graph.json`은 비어 있다. `check_dist --mode public` OK (`logs/09-check-dist-public.log`) |
| fixture public 빌드 | fixture 스크립트가 만든 승인 레코드 4개만 나온다 (E2E-9 "publishes exactly the four human-approved records") |
| 미승인·오래된 승인 | 제외. 에이전트 서명(`agent:*`)과 `proposed` 상태는 공개되지 않는다 (`tools/test_public_gate.py`) |
| 관문 없음·오래됨·`AIXON_BUILD` 없음 | 빌드 실패 (I-23에서 오케스트레이터가 직접 확인, vitest `fails closed…`) |
| 승인 도구 | `tools/review.py list|show|approve`. 에이전트 세션에서는 거부하지만 보안 경계는 아니다 (ADR-021) |

공개 사이트를 채우는 일은 코드가 아니라 사람 검토 속도에 달려 있다(§12).

## 6. 깨끗한 환경 재현 방법

`b6ca3d7`의 새 clone에서 [`tools/clean_env_verify.sh`](../../tools/clean_env_verify.sh)로 돌렸다(`clean-env-job.log`). 이 스크립트가 `npm ci`와 `make verify`를 `taskset -c 0,1 nice -n 10`(2코어, 낮은 우선순위)으로 실행한다. 손으로 하면 아래와 같다.

```bash
git clone <저장소> aixon-clean && cd aixon-clean
git checkout b6ca3d7
npm ci
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
make verify
```

- Playwright용 Chromium이 있어야 한다(없으면 `npx playwright install chromium`).
- Node v22.23.2, Python 3.12.7, Playwright 1.64.1, GNU Make 4.3, WSL2 Linux에서 돌렸다(`summary.json`).
- 2코어 조건: `taskset -c 0,1 nice -n 10 make verify` (최종 실행은 이 조건이었다).
- 한 단계가 실패해도 끝까지 돌고, 하나라도 실패하면 exit 1이다. 증거는 `artifacts/verification/runs/<UTC 시각>/`에 쌓인다.
- 개별 실행: `make lint | typecheck | test | validate | build | check-dist | e2e | e2e-seed | secrets`.
- 안정성 반복(E2E-11, E2E-10 데스크톱 ×5)은 같은 작업 로그(`clean-env-job.log`)에 결과 줄만 남아 있고 명령은 남아 있지 않다.

## 7. 실행 증거 경로

| 무엇 | 경로 |
|---|---|
| 최종 깨끗한 환경 실행 (PASS, `b6ca3d7`) | `artifacts/verification/runs/20261015T040334Z/` (`summary.json`, `logs/01`~`13`, `graph-validation.json`, `test-results/playwright-{fixture,seed}.json`, `clean-env-job.log`) |
| 이전 PASS (`85c3c39`, 최종 리뷰 수정 전, 12단계) | `artifacts/verification/runs/20261015T030106Z/` |
| FAIL 기록 (`118eb36`, I-40) | `artifacts/verification/runs/20261015T034011Z/`, 실패 스크린샷·trace 사본 `artifacts/verification/clean-fail-20261015T034011Z/` |
| 최종 리뷰 스크린샷 (수정 전) | `artifacts/verification/final-review-20261015/shots/` (31장) |
| 수정 뒤 화면 확인 | `artifacts/verification/final-review-20261015/after-fix-shots/` (6장) |
| 검증 하네스 설명 | `README.md`, `tools/verify.py` |
| 결함 기록 | [ISSUE_LOG.md](ISSUE_LOG.md) |

## 8. 실패했다가 고친 것

| ID | 무엇이 실패했나 | 고친 것 | 확인 |
|---|---|---|---|
| I-36 | 깨끗한 환경 1회차에서 12단계가 PASS한 뒤 `verify.py`가 보고서 폴더를 만들지 않아 멈췄고 `summary.json`이 남지 않았다 | `mkdir(parents=True, exist_ok=True)` | 회귀 테스트 `test_playwright_reports_and_failure_evidence_are_copied`(수정 전 코드에서 실패 확인). 2회차 PASS(`20261015T030106Z`) |
| I-37 | public `graph.json`의 `fields`·`parents`와 노드 패널에 비공개 분야 ID가 남았다 | 공개 엔티티만 남기도록 필터 | E2E-9 "references the non-public" |
| I-38 | 실데이터에서 "어텐션" 검색 시 SDPA가 상위 8개 밖 | 같은 점수면 Wiki가 있는 노드를 먼저 | `search.test.ts`, E2E-1 |
| I-39 | MDX 검사 우회(`javascript:` 링크, `\$` 뒤 HTML) | 검사 범위 확대 | `test_mdx_security_rules_reject_unsafe_content` 3건 추가 |
| I-40 | 2코어 깨끗한 환경 실행(`118eb36`)에서 Atlas 분야 노드 클릭이 간헐적으로 실패해 FAIL | 화면 맞춤을 배치가 바뀔 때만, 선택 노드와 드러난 노드 기준으로 (`1143827`, 병합 `270dc58`) | 2코어 `--repeat-each=10`: 수정 전 1/10, 3/10 실패 → 수정 후 70/70, 40/40. 이후 전체 실행 PASS |
| 최종 리뷰 지적 | R-03 관련 개념(M1), R-10 Lab 링크 base(M2), R-06 Wiki → Entity/Atlas, R-13 술어 필터 | `fix/final-review` 병합(`9613280`). Claim 상태 문구를 "인용 확인"으로 바꿈(`118eb36`) | 새 테스트가 수정 전에 실패하고 수정 후 통과. 각 수정을 되돌리면 해당 테스트가 실패(음성 대조). 검증 Opus 5.5 High: MERGE |

최종 리뷰 지적 중 M1·M2는 아직 ISSUE_LOG에 별도 행이 없다(§10).

## 9. NOT RUN / NOT APPLICABLE

| 상태 | 항목 | 이유 |
|---|---|---|
| NOT RUN | 실제 GitHub Pages 배포와 공개 URL 검증 | 저장소 생성·push는 사용자 승인 필요(B-01). 대신 `/aixon/` base를 재현한 로컬 preview로 E2E-6 |
| NOT RUN | GitHub Actions 실행(`ci.yml`, `pages.yml`) | 원격 저장소가 없다. 워크플로 파일만 있다 |
| NOT RUN | 주간 온라인 검사(`verify-online.yml`) | 위와 같다. 같은 검사를 이번에 수동으로 한 번 돌렸다(§4) |
| NOT RUN | 사용자가 직접 사용 | — |
| NOT RUN | 대표 Wiki와 시드 Claim의 사람 검토 | 사용자 몫(B-02) |
| NOT RUN | 검색엔진 색인, 외부 링크 생존 검사 | 배포 뒤에만 가능 / P1 (CONTENT_VALIDATION_PLAN §3) |
| NOT RUN | 스크린 리더 등 보조기기 확인 | aria-label과 MathML 존재만 E2E-8로 확인했다 |
| NOT APPLICABLE | E2E-10 ⑤ Remember, ⑥ Resume (4건 skipped) | 숙련도 저장·재계산은 P2(ADR-019). 학습 경로 계산 자체는 `test_seedtool.py` P15·P15b가 검증 |
| NOT APPLICABLE | 계정, 개인 숙련도, 학습 이력·복습, LLM API, 백엔드 | P2(ADR-019) |
| NOT APPLICABLE | DB 마이그레이션 | v0.1에는 DB가 없다(ADR-015) |

지침(`AUTONOMOUS_MVP_LOOP.md`)의 Phase G 여정 "Understanding Vision Transformer"는 E2E-10에 해당한다. ①~④는 실제 시드에서 PASS, ⑤⑥은 NOT APPLICABLE이다.

### 지침 §11 인수 게이트 대조

| 게이트 | 상태 | 비고 |
|---|---|---|
| P0 요구사항 충족 | PASS | §2 |
| Explore / Trace / Learn / Interactive Lab | PASS | E2E-10 ①~④ |
| Remember (학습 이력 영속화·복원) | NOT APPLICABLE | P2 |
| Seed Graph 검증, G 오류 0, 근거 확인 | PASS | §4 |
| Golden Learning Path | PASS | `test_seedtool.py` P15·P15b |
| Citation / Prerequisite 구분 | PASS | V-CITES-NOT-INFLUENCE (T16, E2E-4, E2E-10 ②) |
| Lint / Typecheck / Unit / Build / E2E | PASS | §3.1 |
| CI 검증 | NOT RUN | 제한 사항으로 명시(§1 조건 3) |
| 증거 (보고서, 추적표, 실행 요약, 남은 이슈, 실행 명령) | PASS | 이 문서와 [TEST_MATRIX.md](TEST_MATRIX.md) |

## 10. 남은 이슈

미해결 Critical은 없다. 상세는 [08_ARCHITECTURE_REVIEW.md §4·§6](../08_ARCHITECTURE_REVIEW.md)와 [ISSUE_LOG.md](ISSUE_LOG.md)에 있다.

| 구분 | 항목 |
|---|---|
| Open | I-14 `~/aixon/ss_copilot.html` 처리 방침(B-05) |
| Accepted | I-33 타입 접두 ID·URL (ADR-023, 옛 URL 이동 안내 페이지는 미구현). F-26 Python이 공개를 판정, TS는 관문 파일만 읽음 |
| Backlog (공개 품질) | CSP, GitHub Actions SHA 고정, 공개 빌드 최소 카드, 모바일 목록 분야 필터, alt/title 이중 낭독 |
| Backlog (데이터) | EXTENDS "inspired by" rubric, ADAPTS 근거 vs qualifier, 입도 문제(위치 인코딩·잔차 연결), Atlas 저자 "X et al.", arXiv v1 날짜 자동 채움, slug 규칙 위반 3건, 수준 ↔ 차원 대응, 안 쓰는 술어 동결 |
| Backlog (도구) | 검토 화면(큐레이션 UI, P1), Python에서 `graph.json` 내보내기, 일괄 승인 명령(§12) |
| 경고 | seedtool 경고 159건(W103 1, W104 149 참조되지 않는 엔티티, W111 9). W111은 선수 관계 9건이 PART_OF 근거를 그대로 쓴다는 뜻이며 사람 검토 힌트다 |
| P2 | 학습 엔진 전체(I-12 포함) |

문서 불일치는 이 보고서를 쓴 직후 고쳤다: 08 문서의 F-13 상태와 `make verify` 기록, VERIFICATION_PLAN의 pytest 수, 07 문서 Sprint 4·5 상태, ISSUE_LOG의 최종 리뷰 지적 행(I-41…I-44).

## 11. 사용자 결정이 필요한 것

자세한 내용은 [BLOCKERS.md](../development/BLOCKERS.md)에 있다. 전부 아직 열려 있다.

| ID | 결정할 것 | 이 보고서와의 관계 |
|---|---|---|
| B-01 | 저장소 이름·공개 여부·push 승인 | 실배포 NOT RUN의 원인 |
| B-02 | public에 담을 콘텐츠: 시드 Claim, 대표 Wiki, Atlas 요약의 사람 검토 | 승인 0건의 원인. §12 참고 |
| B-03 | 콘텐츠 라이선스(텍스트·코드·그림) | 공개 전 필수 |
| B-04 | `~/aixon`의 git 관리와 원격 저장소 | |
| B-05 | `ss_copilot.html` 삭제 여부 | I-14 |
| B-06 | 식별자 검증(arXiv)의 CI 단계 | 이번에는 수동 실행으로 대체(§4) |
| B-07 | 공개 저장소 정책: 무료 Pages는 공개 저장소를 요구하고, 그러면 미검토 초안·`docs/`·git 이력이 모두 보인다. (a) 비공개 + 유료 Pages (b) `dist-public`만 받는 별도 공개 저장소 (c) 공개 저장소 + 초안 표시, `ss_copilot.html`·`study/` 제외 | 공개 방식을 정한다 |
| B-08 | 공개 저장소의 커밋 이력: 통합 저장소의 옛 커밋 메시지에 AI 공동 작성자 표시 줄이 있다. 새 저장소로 시작하거나 이력 정리를 승인 | 이력 재작성은 승인 없이 하지 않는다 |

## 12. 사람이 할 콘텐츠 검토를 줄이는 안

지금 승인은 하나씩 한다. 사람 검토 대상은 시드 Claim, 엔티티, 대표 Wiki다. 아래는 제안이고 구현하지 않았다.

1. **사전 검수표.** 오케스트레이터가 Opus에게 Claim마다 판별 질문(02 §8: 인용이 이 술어를 뒷받침하는가, 방향이 맞는가, 조건이 빠지지 않았는가)을 묻고, 인용 속 숫자를 Claim·Wiki 본문의 숫자와 대조한 결과를 표로 만든다. 열은 Claim ID, 술어, 인용 발췌, 판별 질문별 답, 수치 대조, 의심 여부다.
2. **사용자는 표에서 확인한 것만 승인한다.** 의심으로 표시된 줄부터 원문과 직접 맞춰 본다. 확인한 ID만 `tools/review.py approve <id> --by human:<이름> --checked support,numbers,direction,conditions`로 기록한다.
3. **사전 검수는 승인이 아니다.** Opus의 결과는 `review`에 쓰지 않는다. `agent:*` 서명은 공개되지 않는다(ADR-021). 같은 계열 모델이 만든 내용을 같은 계열 모델이 검수하므로 편향이 남는다. 그래서 승인된 항목 중 일부는 사용자가 무작위로 골라 원문을 직접 대조하는 것을 권한다.
4. **일괄 승인 명령은 아직 없다.** `approve`는 ID 하나씩이다. 표를 쓰게 되면 ID 목록 파일을 받는 옵션을 추가하되, 각 레코드의 현재 `reviewed_hash`에 묶고 사용자 세션에서만 돌게 한다. 필요하면 추가한다.
5. **첫 공개는 작게 시작할 수 있다.** 대표 Wiki(SDPA)는 Claim 12개와 논문 4편을 인용한다(frontmatter 기준). 이 Wiki와 Claim 12개, 그리고 Claim 양 끝의 엔티티만 먼저 승인하면 공개 사이트에 처음으로 내용이 생긴다. 엔티티 수는 세어 보지 않았다.

이 안의 효과(검토 시간이 얼마나 줄지)는 측정하지 않았다.

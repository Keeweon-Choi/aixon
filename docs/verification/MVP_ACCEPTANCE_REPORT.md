# MVP_ACCEPTANCE_REPORT — AIXON v0.1 인수 보고서

> 2026-10-15. 범위는 ADR-019(v0.1 = Knowledge Atlas + Interactive AI Wiki)다. 요구사항은 [07_MVP_ROADMAP.md §1](../07_MVP_ROADMAP.md), 추적은 [REQUIREMENT_TRACEABILITY.md](REQUIREMENT_TRACEABILITY.md), 계획은 [VERIFICATION_PLAN.md](VERIFICATION_PLAN.md), 테스트별 결과는 [TEST_MATRIX.md](TEST_MATRIX.md)에 있다.
> 상태는 PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE 다섯 가지만 쓴다. 증거 파일 경로는 저장소 기준이다. `artifacts/verification/runs/`와 `final-review-*/`는 git에 넣지 않는 로컬 증거이고, 정본 저장소 `~/aixon`에 있다(첫 인수 전 실행 일부는 `~/wt/aixon-base`).
> 기준 커밋: 깨끗한 환경 검증은 최신 실행이 `ab363f0`(`artifacts/verification/runs/20261015T064959Z`, 13단계 PASS)다. 이력으로 남기는 실행은 셋이다. `67854ae`(`20261015T051054Z`, 콘텐츠 게시 전), 첫 인수 때의 `b6ca3d7`(`20261015T040334Z`), 그리고 게시 작업 중의 `186294f`(`20261015T063931Z`, 13단계 PASS)다. 게시 작업 중 실패한 실행도 둘 있다. `a420066`의 실행은 `check-dist-public`에서, `ba511b4`의 실행(`20261015T063234Z`)은 `e2e-seed` E2E-1에서 실패했고 모두 고쳤다(§8). `20261015T063234Z`의 증거는 깨끗한 환경 clone에만 남아 있다. GitHub의 CI는 `ab363f0`에서 전체 `make verify`를 돌려 성공했다(run 38695150153).
> 마지막 확인(2026-10-15 18:1x): Python 환경을 uv로 옮기고 Anaconda를 지운 상태(venv 밖 `python3`는 `/usr/bin` 3.10)에서 새 클론 `72fdaf4`의 깨끗한 환경 검증 13단계 PASS(`artifacts/verification/runs/20261015T091221Z`, uv Python 3.12.15, E2E fixture 124·seed 50). 같은 상태에서 `make verify-online`도 통과(인용 132 found, 식별자 67/67). `ab363f0` 뒤 바뀐 것은 문서, 검증 스크립트의 venv 생성(uv), requirements 고정 방식뿐이다.

> 2026-10-15 14:3x 갱신. 첫 인수(13:3x) 뒤 바뀐 것은 다음과 같다.
>
> - 공개 저장소 `Keeweon-Choi/aixon`을 만들고 GitHub Pages에 실제 배포했다. 공개 주소는 https://keeweon-choi.github.io/aixon/ 이다.
> - GitHub에서 CI, Pages, Verify Online이 돌았다. 처음 실패한 것은 고쳐서 다시 PASS했다(§8).
> - 배포된 사이트를 Playwright로 실제 사용해 보았다(§3.2). 사람이 쓴 것은 아니다.
> - 최신 코드(`67854ae`)로 깨끗한 환경 `make verify`를 다시 돌려 13단계 PASS.
> - 사용자 결정으로 B-01, B-03, B-04, B-05, B-07, B-08이 닫혔다. B-02는 AI 교차 검증 경로(ADR-026)로 바뀌었고 도구를 만드는 중이다. 게시된 콘텐츠는 아직 0건이다.
> - 그대로인 것: 사람 승인 0건, 사람이 직접 써 본 확인, 검색엔진 색인, 스크린 리더 확인은 NOT RUN.

> 2026-10-15 15:5x 갱신 — 첫 콘텐츠 공개. 14:3x 갱신 뒤 바뀐 것은 다음과 같다.
>
> - AI 교차 검증 도구(ADR-026)와 로컬 검수 화면(ADR-025)을 병합했다(`285ba74`, `7016084`). 둘 다 Opus 검증자가 "수정 필요"로 판정한 뒤 검증 커밋을 더해 병합했다(§8).
> - 첫 릴리스 `first-release` 44건(엔티티 27, Claim 12, 문항 4, Wiki 1)을 Opus 5.5 High 검증자 6명이 두 차례 검증해 승인했다. 승인 커밋은 `a420066`이다. 기록은 [RELEASE.md](../../review/cross/first-release/RELEASE.md)에 있다. 승인한 것은 AI 패널이고 사람 승인은 0건이다.
> - 공개 관문 결과는 엔티티 31(문항 포함), Claim 12, Wiki 1, 출처 6, 제외 0, 오류 0이다. 배포된 사이트에 처음으로 내용이 생겼다.
> - 배포된 사이트를 내용이 있는 상태로 다시 Playwright로 써 보았다(`deploy-smoke-20261015T064629Z`, §3.2). 사람이 쓴 것은 아니다.
> - 게시 작업에서 실패 셋을 고쳤다. `check-dist` 오염 검사의 오탐(`ba511b4`), E2E-1의 시드 가정(`186294f`), 홈의 "0개 노드"(`ab363f0`)다(§8).
> - 최신 코드(`ab363f0`)로 깨끗한 환경 `make verify`를 다시 돌려 13단계 PASS. GitHub CI 38695150153과 Pages 38695150022도 성공했다.
> - 공개 뒤 GitHub Verify Online(run 38695949526, `ee55e50`)도 성공했다. 인용 132건 found(W106 경고 32), 식별자 67/67 일치. 증거는 `artifacts/verification/verify-online-gh-38695949526/`.
> - B-02는 첫 릴리스에 한해 ADR-026 경로로 해결됐다. 사람 검토는 로컬 검수 화면에서 선택 사항이다.
> - 그대로인 것: 사람 승인 0건, 사람이 직접 써 본 확인, 검색엔진 색인, 스크린 리더 확인은 NOT RUN. E2E-10 ⑤⑥은 NOT APPLICABLE(P2).

## 1. 판정 요약

**판정: PASS.** [AUTONOMOUS_MVP_LOOP §11](../AUTONOMOUS_MVP_LOOP.md) MVP Acceptance Gate의 항목은 모두 PASS이거나, 범위 밖이라 NOT APPLICABLE이거나, 지침이 허용한 대로 실행 제한을 밝혔다. Critical 미해결은 0건이다.

| 영역 | 게이트 항목 | 상태 | 근거 |
|---|---|---|---|
| Functional | P0 요구사항 R-01–R-16(07 문서의 인수 기준) | PASS | §2 |
| Functional | Explore·Trace·Interactive Lab 동작, 핵심 E2E 사용자 시나리오 | PASS | E2E fixture 124(리뷰 화면 테스트 2건 포함), seed 50(E2E-10 ①–④) |
| Functional | Learn(맞춤 학습 경로)·Remember(학습 이력 영속·복원) | NOT APPLICABLE | 사용자 범위 재조정으로 P2(ADR-019). 계획기 기준 구현은 golden 테스트 통과 |
| Knowledge | Seed 검증, Critical 불변식 위반 0, Verified 근거 확인, Golden Learning Path, Citation/Prerequisite 구분 | PASS | §4, T16·V-CITES-NOT-INFLUENCE |
| Engineering | Lint·Typecheck·Unit·Integration·Playwright E2E·Build·회귀 | PASS | `runs/20261015T064959Z` 13단계 (`ab363f0`). 이전 실행 `20261015T063931Z`(`186294f`), `20261015T051054Z`(`67854ae`), `20261015T040334Z`(`b6ca3d7`)도 13단계 PASS |
| Engineering | DB Migration | NOT APPLICABLE | v0.1에는 DB가 없다(ADR-015) |
| Engineering | CI 검증 성공 또는 실제 실행 제한 사항 명시 | PASS | GitHub Actions CI 성공: 최신 run 38695150153(`ab363f0`, 3분 55초). 앞선 성공은 38683822123(`2355c44`), 38685394647(`67854ae`), 38686155036(`c6851db`, 3분 53초), 38693966099(`186294f`, 4분 14초). https://github.com/Keeweon-Choi/aixon/actions/runs/38695150153 . 깨끗한 환경 실행 `20261015T064959Z`는 추가 증거다 |
| Evidence | 검증 보고서·추적표·실행 요약·E2E 증거·이슈 목록·재현 명령 | PASS | 이 문서, TEST_MATRIX, §6·§7 |

**공개 준비는 인수 기준 밖이다.** 처음에는 외부 배포 금지 때문에 하지 못했으나 사용자가 배포를 승인해서(B-01) 1·3은 했다. 2는 사람 승인 대신 AI 교차 검증 경로(ADR-026)로 바뀌었고 첫 릴리스 44건을 그 경로로 게시했다. 4는 사용자만 할 수 있다. 배포된 사이트에는 이제 내용이 있다. 사람 승인은 여전히 0건이다.

| # | 공개 준비 항목 | 상태 |
|---|---|---|
| 1 | 실제 GitHub Pages 배포 | PASS. https://keeweon-choi.github.io/aixon/ , 최신 Pages run 38695150022(`ab363f0`) 성공. 앞선 성공은 38683822204(`2355c44`), 38685394691(`67854ae`), 38686154994(`c6851db`), 38693966125(`186294f`). 이제 배포된 사이트에 내용이 있다. 내용이 있는 상태의 스모크 테스트 PASS(`artifacts/verification/deploy-smoke-20261015T064629Z/`, 배포 `186294f`): 게시된 12개 경로 200, 비공개 `/e/concept/softmax/`와 `/e/method/linear-attention/` 404, 콘솔 오류·실패 요청·가로 넘침 없음. Wiki 배너 "AI 교차 검증 2명, 2026-10-15", KaTeX 50개 노드·오류 0, 랩 상호작용·퀴즈·검색 동작(§3.2). 내용이 없던 때의 스모크는 `deploy-smoke-20261015T045518Z/`(이력). 그 뒤 `ab363f0`의 배포를 curl로 확인했다. 홈이 "인공지능 · 15개 노드"를 보이고 `/about/`에 "AI 교차 검증" 절이 있다. 한계: 화면 글꼴이 없는 환경이라 스크린샷의 한글이 네모로 보여 텍스트는 DOM으로 확인했다 |
| 2 | 콘텐츠 승인 | 사람 승인 0건. AI 교차 검증 패널이 44건을 승인하고 게시했다(승인 커밋 `a420066`, [ADR-026](../DECISIONS.md), [CROSS_REVIEW.md](CROSS_REVIEW.md), 기록 [RELEASE.md](../../review/cross/first-release/RELEASE.md)). 첫 릴리스의 B-02는 이 경로로 해결됐다. 사람이 읽고 확인한 것은 아니다 |
| 3 | GitHub에서 도는 Actions(`ci.yml`, `pages.yml`, `verify-online.yml`) | CI PASS(38695150153), Pages PASS(38695150022), Verify Online은 재실행에서 PASS(run 38686154873, `c6851db` 시점). 실패와 수정은 §8 |
| 4 | 사람이 직접 써 본 확인 | NOT RUN. 사람은 사이트를 써 보지 않았다. 배포 사이트는 AI가 Playwright로 썼다 (§3.2) |

핵심 숫자는 아래와 같다. 모두 §7의 파일에서 확인했다.

| 항목 | 값 | 출처 |
|---|---|---|
| 깨끗한 환경 `make verify` | 13단계 PASS, 165.43초, git dirty false, 커밋 `ab363f0` (이력: `67854ae` 108.15초, `b6ca3d7` 232.18초, 모두 13단계 PASS) | `artifacts/verification/runs/20261015T064959Z/summary.json` |
| vitest / pytest | 25 / 242 통과 (`67854ae`는 22 / 206, `b6ca3d7`은 22 / 201) | 같은 실행의 `logs/03-test.log` |
| Playwright fixture | 124 expected(리뷰 화면 테스트 2건 포함), 0 unexpected, 0 flaky | `test-results/playwright-fixture.json` |
| Playwright seed | 50 expected, 4 skipped, 0 unexpected, 0 flaky | `test-results/playwright-seed.json` |
| 빌드 | preview 632쪽, public 62쪽 (콘텐츠 게시 전에는 7쪽) | `logs/07-check-dist.log`, `logs/09-check-dist-public.log` |
| 시드 Claim | 105 (verified 95, disputed 1, proposed 8, rejected 1) | `data/seed/seed_graph.yaml` |
| GitHub Actions | CI 38695150153(`ab363f0`) 성공, Pages 38695150022 성공, Verify Online 38686154873 성공(인용 132 found + 경고 31, 식별자 67/67. `c6851db` 시점) | §1, §8 |
| 인용 원문 대조 | 132/132 found (오프라인, `content_sha256` 고정. GitHub 온라인 실행도 132 found) | §4 |
| arXiv 식별자 | 67/67 일치 (Atlas 54 + 시드 13) | §4 |
| 그래프 G 오류 | 0 (경고 159건은 §9) | `graph-validation.json` |
| 공개 관문 | 엔티티 31, Claim 12, Wiki 1, 제외 0, 오류 0 (AI 교차 검증 패널 승인 44건) | `logs/04-validate.log`의 "public gate: 31 entities, 12 claims, 1 wiki, 0 excluded, 0 errors" |
| 사람 승인 | 0건 | 게시된 Wiki의 `review.by`는 `panel:first-release`(`method: cross-review`). 사람 서명(`human:*`)은 없다 |

건너뛴 4건은 E2E-10의 ⑤ Remember, ⑥ Resume(데스크톱·모바일)이고 P2 범위라서 NOT APPLICABLE이다(ADR-019).

## 2. P0 요구사항 R-01 ~ R-16

"최종 상태"는 깨끗한 환경 실행(처음에는 `b6ca3d7`, 지금은 `ab363f0`)을 기준으로 한다. "리뷰어 PARTIAL"은 최종 독립 리뷰(§3.2)가 `85c3c39`에서 부분 충족으로 본 항목이고, 그 뒤 수정과 재검증을 거쳤다. 테스트 이름은 [TEST_MATRIX.md](TEST_MATRIX.md)에서 찾을 수 있다.

| ID | 요구 | 최종 상태 | 근거 | 비고 |
|---|---|---|---|---|
| R-01 | AI 전체 분야 Knowledge Graph | PASS | 분야 92개(기준 ≥ 80). G 오류 0. 인용 132/132. arXiv 67/67. `tools/test_seedtool.py` 63개, `tests/unit/graph.test.ts` | 인용이 술어를 뒷받침하는지는 기계 검사가 없다(I-24). 사람 검토 몫이다 |
| R-02 | Interactive Atlas | PASS | `tests/unit/view.test.ts` 10개. E2E-1·7·11 fixture와 seed. E2E-10 ① | 이전 간헐 실패는 I-40으로 고쳤다(§8) |
| R-03 | Wiki 콘텐츠 모델과 렌더러 | PASS | `make validate`(V-SCHEMA, "0 error(s)"), `tests/python/test_validate_content.py` 43개, E2E-1 "관련 개념" 방향·상태 | 리뷰어 PARTIAL(관련 목록이 Claim 방향·상태를 무시, M1) → 수정 |
| R-04 | 대표 개념 교육 페이지 | PASS | `src/content/wiki/scaled-dot-product-attention.mdx`: 섹션 9개(기준 9개 이상), `python verify` 블록은 `make validate`에서 실행·통과. E2E-1·2 | 문서 상태는 `published`, `review.by: panel:first-release`(AI 교차 검증 2명 + 표본 감사 1명, 2026-10-15). 내용 정확성의 사람 검토는 하지 않았다 |
| R-05 | 수식·코드·다이어그램 | PASS | `check_dist.py` V-MATH(`katex-error` 0, MathML), E2E-8 "KaTeX output includes MathML", V-FIG-1 | |
| R-06 | Graph ↔ Wiki 이동 | PASS | V-LINK-1, E2E-1(Wiki → Entity, Wiki → Atlas 노드), `check-dist`의 링크 검사 | 리뷰어 PARTIAL(Wiki에서 Entity/Atlas로 가는 링크 없음) → 링크 추가 |
| R-07 | 검색 | PASS | `tests/unit/search.test.ts` 3개, E2E-1 "2-character Korean query", E2E-5 Pagefind | E2E-5는 fixture 빌드에서만 돈다. 실제 시드 빌드는 Pagefind 색인 632쪽까지만 확인했다(`logs/06-build.log`) |
| R-08 | 근거·참고문헌 | PASS | E2E-3 12건(fixture), E2E-1 "references and inline citations are human readable" | 화면 상태 문구는 "인용 확인"(ADR-022). E2E-3에 "bare verified가 없다"는 음성 검사가 있다 |
| R-09 | 검증된 시드 콘텐츠 | PASS | Claim 105(95/1/8/1), 인용 132/132, golden 계획 `test_t18_p15` 등 3개 통과 | §4. 사람 승인 0건. 이 중 12건은 AI 교차 검증 패널이 승인해 공개됐다 |
| R-10 | GitHub Pages 배포 | PASS (07 기준: `pages.yml`, base 경로·디렉터리 URL, 로컬 직접 링크·새로고침 재현). 실배포도 했다: https://keeweon-choi.github.io/aixon/ | `/aixon/` base로 E2E-6 fixture 8건·seed 8건, `check-dist-public`, `check-dist-seed`. 실배포는 Pages run 38683822204·38685394691·38686154994·38693966125·38695150022 성공. 배포 사이트 스모크: 게시 전 6개 경로 200(`deploy-smoke-20261015T045518Z/`), 게시 뒤 12개 경로 200과 비공개 경로 404(`deploy-smoke-20261015T064629Z/`). 콘솔 오류·실패 요청·가로 넘침 없음(§3.2) | 리뷰어 PARTIAL(Lab "근거 보기" 링크가 base 경로를 무시, M2) → 수정, `check-dist-seed` 단계 추가 |
| R-11 | 자동 검증 하네스 | PASS (로컬, GitHub CI 포함) | `make verify` 13단계, `tests/python/test_verify.py` 8개(실패한 단계가 있어도 끝까지 돌고 exit 1). 실패 실행의 기록은 `20261015T034011Z`(summary 상태 FAIL) | GitHub의 `ci.yml`도 같은 `make verify`를 돌려 성공했다(§1) |
| R-12 | Interactive Lab | PASS | `tests/unit/lab.test.ts`(V-LAB L1–L7), E2E-2 fixture 2건·seed 2건(numpy fixture와 4자리 일치), E2E-10 ④ | |
| R-13 | 연구 계보(Trace) | PASS | E2E-4 14건(fixture), `view.test.ts`(연도 순서, CITES 제외, 술어 필터), E2E-10 ② | 리뷰어 PARTIAL(술어 필터 없음) → 필터 추가 |
| R-14 | 콘텐츠 상태·Coverage | PASS | `tests/unit/coverage.test.ts`, V-STATUS-1, E2E-7 | |
| R-15 | 콘텐츠 공개 관문 | PASS (07 기준: public 빌드에 미승인 Wiki·Claim·AI 요약 0). 승인은 사람 서명 대신 AI 교차 검증 패널(ADR-026)이 했다 | `tools/test_public_gate.py` 6개, seedtool G022, E2E-9 10건, `check_dist.py --mode public`의 taint 검사. 실제 데이터 public 빌드는 62쪽(`ab363f0`) | 관문 결과는 엔티티 31, Claim 12, Wiki 1이다. 비공개 `/e/concept/softmax/`와 `/e/method/linear-attention/`는 배포 사이트에서 404다(§3.2) |
| R-16 | SEO·접근성·반응형 | PASS | `check_dist.py`(V-SEO, V-SEC, V-NO-CDN), E2E-7 22건, E2E-8 28건(fixture) | 검색엔진 색인은 NOT RUN(배포는 됐으나 색인 확인은 하지 않았다). 스크린 리더로 읽어 본 확인은 없다. 배포 사이트의 `robots.txt`와 sitemap은 `/aixon/` base로 맞다(§3.2) |

R-03, R-06, R-10, R-13의 PARTIAL은 수정 뒤 PASS로 올렸다. 근거는 수정 검증(Opus 5.5 High, MERGE)과 깨끗한 환경 재실행이다. 리뷰어의 사용 흐름 전체를 수정 뒤에 처음부터 다시 걷지는 않았다. 수정 뒤에는 화면 3가지만 다시 봤다(§3.2).

## 3. 검증 결과: 테스트 통과와 실제 사용 확인

두 가지는 다른 증거다. 테스트가 통과해도 쓸 만한 화면인지는 따로 봐야 한다.

### 3.1 테스트 통과

아래 증거 경로는 별도 표기가 없으면 `artifacts/verification/runs/20261015T064959Z/`(`ab363f0`) 기준이다. 이전 실행(`b6ca3d7`, `67854ae`)과 달라진 것은 public 쪽수(7 → 62), fixture(122 → 124), vitest(22 → 25), pytest(206 → 242)다. preview 632쪽, seed 50 + 4 skipped는 같다.

| 계층 | 결과 | 증거 |
|---|---|---|
| 정적 검사 | PASS (prettier, eslint, astro check, ruff) | `logs/01-lint.log` |
| 타입 | PASS (astro check, tsc) | `logs/02-typecheck.log` |
| 단위 | PASS. vitest 25(6개 파일), pytest 242 (`67854ae`는 206, `b6ca3d7`은 201) | `logs/03-test.log` |
| 데이터·콘텐츠 | PASS. 공개 관문 계산, seedtool G 0, `validate_content` "0 error(s), 0 warning(s)" | `logs/04-validate.log`, `graph-validation.json` |
| fixture 검증 | PASS | `logs/05-validate-fixtures.log` |
| 빌드·산출물 | PASS. preview 632쪽, public 62쪽, seed 632쪽 | `logs/06`~`logs/09`, `logs/12` |
| E2E fixture | PASS. 124건(리뷰 화면 테스트 2건 포함) | `test-results/playwright-fixture.json` |
| E2E seed (실제 데이터) | PASS. 50건, 4건 skipped(NOT APPLICABLE) | `test-results/playwright-seed.json` |
| 비밀 검사 | PASS. 3454개 파일 (`67854ae`는 3323, `b6ca3d7`은 3317) | `logs/13-secrets.log` |
| 안정성 반복 (2코어) | PASS. E2E-11 desktop ×5 → 35 통과. E2E-10 desktop ×5 → 20 통과, 10 skipped. `b6ca3d7` 실행에서 한 것이고 `67854ae`에서는 다시 하지 않았다 | `runs/20261015T040334Z/clean-env-job.log` |
| 수동 외부 대조 | PASS (이 문서를 쓰며 직접 실행, §4) | 이 문서 |

`check-dist-public`은 `404.html`의 canonical 링크 경고 1건을 냈다. 종료 코드는 0이고, 검사기가 404 페이지의 canonical은 경고로만 다루도록 정해 둔 것이다(`test_canonical_of_the_404_page_is_only_a_warning`).

### 3.2 실제 사용 확인

| 확인 | 누가, 어떻게 | 증거 | 한계 |
|---|---|---|---|
| 최종 독립 리뷰 (Phase I) | Opus 5.5 High 리뷰어가 `85c3c39`의 실제 시드 빌드를 브라우저로 사용. 검색 → Wiki → Lab → 퀴즈 → Claim → Atlas → Trace → Coverage를 1280×900과 390×844에서 걸음. JS 오류 없음 | `artifacts/verification/final-review-20261015/shots/` 31장(데스크톱 16, 모바일 15) | 헤드리스 머신에 한글 글꼴이 없어 스크린샷의 한글이 네모로 보인다. 페이지 텍스트는 따로 확인했다. 사람이 아니라 AI가 본 것이다 |
| 리뷰 판정 | ACCEPT WITH FIXES. R-03, R-06, R-10, R-13이 PARTIAL, 나머지 PASS. Critical 없음 | 리뷰어 보고(오케스트레이터 전달) | 보고서 원문 파일은 찾지 못했다. 이 표는 전달된 요약이다 |
| 수정 뒤 화면 확인 | 수정 검증자가 Atlas 패널, Trace 레이블, 390px 가로 넘침을 다시 봄 | `final-review-20261015/after-fix-shots/` 6장 (`atlas-selected-*`, `trace-*`, `trace-selected-*`) | 위 3가지만이다. 전체 흐름 재실행은 아니다 |
| 데이터 직접 확인 | 이 문서 작성 중 직접 실행 | §4 | 네트워크 대조는 arXiv API 한 번의 응답이다 |
| 배포된 사이트 스모크 테스트 | 오케스트레이터가 Playwright(chromium, 1280×800과 390×844)로 https://keeweon-choi.github.io/aixon/ 를 실제로 사용. `/`, `/about/`, `/atlas/`, `/search/`, `/coverage/`, `/trace/` 모두 200, `/nope-404/`는 404 페이지. 콘솔 오류는 404 페이지의 예상된 리소스 오류뿐이고 실패한 요청과 가로 넘침은 없었다. `robots.txt`의 Sitemap은 `https://keeweon-choi.github.io/aixon/sitemap-index.xml`, sitemap URL은 `/aixon/` base를 가진다 | `artifacts/verification/deploy-smoke-20261015T045518Z/` (`results.json`, 스크린샷 14장. git에는 없고 디스크에만 있다) | 로컬 헤드리스 Chromium에 한글 글꼴이 없어 스크린샷의 한글이 네모로 보인다. 텍스트는 DOM에서 확인했다(h1 문구 맞음). 실제 브라우저는 시스템 글꼴을 쓴다(`font-family: system-ui, sans-serif`). 공개 콘텐츠가 비어 있어(승인 0건) 홈, 방법론, 빈 Atlas만 확인했다. AI가 본 것이다 |
| 내용이 있는 배포 사이트 사용 (첫 콘텐츠 공개 뒤) | 오케스트레이터가 Playwright(chromium, 1280×800과 390×844)로 배포 `186294f`의 공개 주소를 실제로 사용. 게시된 12개 경로 모두 200. 비공개 `/e/concept/softmax/`와 `/e/method/linear-attention/`는 404. 확인한 것: ① Wiki 배너 "AI 교차 검증 2명, 2026-10-15", 초안 배너 없음. ② KaTeX 50개 노드, 오류 0, 출처가 적힌 은행·강 예시 문단 있음. ③ 엔티티·Claim 페이지에 "인용 확인(기계)"와 "AI 교차 검증 2명" 표시. ④ 랩이 hydration 뒤 동작(최대 확률 T=1에서 0.5492, T=0.05에서 1.0000). ⑤ 퀴즈 채점 동작. ⑥ Pagefind 검색 "attention" 결과 10개. ⑦ 홈 개수 엔티티 31 · Claim 12 · Wiki 1. 게시된 페이지에서 콘솔 오류와 실패한 요청 없음, 두 너비 모두 가로 넘침 없음. 이 사용에서 홈의 "인공지능 · 0개 노드"를 찾아 `ab363f0`으로 고쳤다(§8) | `artifacts/verification/deploy-smoke-20261015T064629Z/` (`results.json`, `interact.json`, 스크린샷. git에는 없고 디스크에만 있다) | 홈 수정(`ab363f0`) 뒤의 배포는 이 스모크 테스트가 아니라 curl로 확인했다: 홈이 "인공지능 · 15개 노드"를 보이고 `/about/`에 "AI 교차 검증" 절이 있다. 글꼴 없는 환경이라 스크린샷의 한글은 네모다. AI가 본 것이고, 사람이 쓴 것이 아니다 |
| 사용자가 직접 써 봄 | — | — | NOT RUN. 사람이 이 사이트를 써 본 적이 없다 |
| 대표 Wiki의 설명 정확성을 사람이 읽고 검토 | — | — | NOT RUN. AI 교차 검증 패널이 검토했다(`RELEASE.md`). 사람 검토는 로컬 검수 화면에서 선택 사항이다 |

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

인용 대조와 식별자 대조는 `make verify`에 들어 있지 않다. 캐시와 네트워크에 기대기 때문이다(`make verify-online`). GitHub에서는 `verify-online.yml`(주 1회 + 수동)로 돈다. 첫 통과 실행은 38686154873이다(§8).

## 5. 공개 관문 상태

| 항목 | 상태 |
|---|---|
| 허용 목록 | 엔티티 31(문항 4 포함), Claim 12, Wiki 1, 출처 6, 제외 0, 오류 0. `public gate: 31 entities, 12 claims, 1 wiki, 0 excluded, 0 errors` (`logs/04-validate.log`). 콘텐츠 게시 전에는 0/0/0이었다 |
| 실제 데이터 public 빌드 | 정적 62쪽. `check_dist --mode public` OK (`logs/09-check-dist-public.log`). 콘텐츠 게시 전에는 7쪽이었다 |
| fixture public 빌드 | fixture 스크립트가 만든 승인 레코드 4개만 나온다 (E2E-9 "publishes exactly the four human-approved records") |
| 미승인·오래된 승인 | 제외. 에이전트 서명(`agent:*`)과 `proposed` 상태는 공개되지 않는다 (`tools/test_public_gate.py`) |
| 관문 없음·오래됨·`AIXON_BUILD` 없음 | 빌드 실패 (I-23에서 오케스트레이터가 직접 확인, vitest `fails closed…`) |
| 승인 도구 | `tools/review.py list|show|approve`. 에이전트 세션에서는 거부하지만 보안 경계는 아니다 (ADR-021). 일괄 승인 `approve-batch`와 `publish`는 `ea87acf`에 병합됐다(수정 `2355c44`). AI 교차 검증 경로(ADR-026)의 도구는 `285ba74`에, 로컬 검수 화면(ADR-025)은 `7016084`에 병합됐다. 첫 릴리스 44건은 이 경로로 `a420066`에서 승인·게시됐다. 되돌리려면 `git revert a420066`이다 |

첫 릴리스 뒤에도 공개 사이트를 채우는 일은 코드가 아니라 검토 속도에 달려 있다(§12). 다음 릴리스 후보도 같은 패널을 거친다.

## 6. 깨끗한 환경 재현 방법

`ab363f0`의 새 clone에서 [`tools/clean_env_verify.sh`](../../tools/clean_env_verify.sh)로 돌렸다(`clean-env-job.log`의 첫 줄 `[clean] commit ab363f0, node v22.23.2, Python 3.12.7`). 이전에는 `67854ae`, 첫 인수 때는 `b6ca3d7`에서 같은 방법으로 돌렸다. 이 스크립트가 `npm ci`와 `make verify`를 `taskset -c 0,1 nice -n 10`(2코어, 낮은 우선순위)으로 실행한다. 손으로 하면 아래와 같다.

```bash
git clone <저장소> aixon-clean && cd aixon-clean
git checkout ab363f0
npm ci
uv venv --python 3.12 .venv && uv pip install -r requirements-dev.txt
make verify
```

- Playwright용 Chromium이 있어야 한다(없으면 `npx playwright install chromium`).
- Node v22.23.2, Python 3.12.7, Playwright 1.64.1, GNU Make 4.3, WSL2 Linux에서 돌렸다(`summary.json`).
- 2코어 조건: `taskset -c 0,1 nice -n 10 make verify` (최종 실행은 이 조건이었다).
- 한 단계가 실패해도 끝까지 돌고, 하나라도 실패하면 exit 1이다. 증거는 `artifacts/verification/runs/<UTC 시각>/`에 쌓인다.
- 개별 실행: `make lint | typecheck | test | validate | build | check-dist | e2e | e2e-seed | secrets`.
- 안정성 반복(E2E-11, E2E-10 데스크톱 ×5)은 `b6ca3d7` 실행의 작업 로그(`runs/20261015T040334Z/clean-env-job.log`)에 결과 줄만 남아 있고 명령은 남아 있지 않다.
- `67854ae` 실행은 새 clone, `npm ci`, 새 venv, `taskset -c 0,1`(2코어)이었다.

## 7. 실행 증거 경로

| 무엇 | 경로 |
|---|---|
| 최신 깨끗한 환경 실행 (PASS 13/13, `ab363f0`) | `artifacts/verification/runs/20261015T064959Z/` (`summary.json`, `logs/01`~`13`, `graph-validation.json`, `test-results/playwright-{fixture,seed}.json`, `clean-env-job.log`) |
| 콘텐츠 게시 중 깨끗한 환경 실행 (PASS 13/13, `186294f`, 이력) | `artifacts/verification/runs/20261015T063931Z/` |
| 콘텐츠 게시 중 깨끗한 환경 실행 (FAIL, `ba511b4`: e2e-seed E2E-1 2건. 이력) | `20261015T063234Z`. 깨끗한 환경 clone에만 있고 이 저장소 디스크에는 없다. `a420066`의 실패 실행(`check-dist-public`)은 증거 경로를 따로 기록하지 않았다 |
| 이전 깨끗한 환경 실행 (PASS 13/13, `67854ae`, 이력) | `artifacts/verification/runs/20261015T051054Z/` |
| 첫 인수 때 깨끗한 환경 실행 (PASS, `b6ca3d7`, 이력) | `artifacts/verification/runs/20261015T040334Z/` (같은 구성) |
| 배포된 사이트 스모크 테스트 (내용 있음, `186294f` 배포) | `artifacts/verification/deploy-smoke-20261015T064629Z/` (`results.json`, `interact.json`, 스크린샷. git에 없음) |
| 배포된 사이트 스모크 테스트 (내용 없음, 이력) | `artifacts/verification/deploy-smoke-20261015T045518Z/` (`results.json`, 스크린샷 14장. git에 없음) |
| 첫 릴리스 게시 기록 | [`review/cross/first-release/RELEASE.md`](../../review/cross/first-release/RELEASE.md) (검증자, 진행, 독립성 기록, 공개된 레코드 44건) |
| GitHub Verify Online 증거 | `artifacts/verification/verify-online-gh-38686154873/`(통과), `verify-online-gh-38685733040-failed/`(실패. `.gitignore`로 git에서 제외, 디스크에 있음) |
| GitHub Actions 실행 | CI 38683822123·38685394647·38686155036·38693966099·38695150153 성공(최신 마지막). Pages 38683822204·38685394691·38686154994·38693966125·38695150022 성공(최신 마지막). https://github.com/Keeweon-Choi/aixon/actions |
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
| 배포 1 (Pages) | Pages run 38682916304(`77240e4`) 실패. `check-dist-public`의 V-SEO에서 sitemap 호스트 `keeweon-choi.github.io`와 `PUBLIC_SITE`의 `https://Keeweon-Choi.github.io`가 달랐다. `repository_owner`는 대소문자를 유지하고 Astro는 소문자로 바꾼다 | `tools/check_dist.py`가 사이트 origin을 소문자로 비교(`e8f9adc`) | 테스트 `test_site_origin_is_compared_case_insensitively`. 수정 전 코드는 이 테스트를 실패한다(음성 대조). 이후 Pages `38683822204` 성공 |
| 배포 2 (CI) | CI run 38684800306(`d0720ce`) 실패. lint 한 단계만: prettier가 `review/first-release.yaml`(검수표 데이터 파일)을 검사했다. 나머지 12단계는 GitHub에서 PASS | `review/`를 `.prettierignore`에 추가, `data/`와 같은 취급(`67854ae`) | CI 38685394647 성공(2분 35초), 깨끗한 환경 `20261015T051054Z` 13/13 |
| 배포 3 (Verify Online) | `67854ae`의 수동 실행 38685394444가 `seedtool quotes`에서 실패. 증거가 올라오지 않았다(업로드 단계에 `if: always()`가 없었다). 재실행 38685733040도 실패: 132/132 found인데 arXiv HTML 4건(2012.12877v2, 1512.03385v1, 2103.14030v2, 1409.0473v7)의 40행이 `source_changed`. 같은 시각 로컬 fetch는 고정된 해시와 맞았다(빈 캐시, 132 found, exit 0). 클라이언트에 따라 받는 바이트가 다르다 | 업로드를 실패 때도 하도록 수정(`76a139e`). 02 문서가 W106을 경고로 정의하므로 구현을 경고로 바꿈(`c6851db`, 테스트와 음성 대조) | 재실행 38686154873 성공: 인용 132 found + `source_changed` 경고 31건, 식별자 67/67 일치 |
| 게시 1 (병합 직후) | 도구를 병합한 뒤 통합 오류 둘. 로컬 검수 화면이 실제 `confirm.json`을 읽지 못했고, `check_release`의 호출 시그니처가 어긋났다. 또 arXiv 캐시를 시드에 쓰인 버전에만 쓰도록, 필수 필드를 저장된 키에 맞추도록 고쳤다 | `a9097a5`, `4bc4ee5` | 이후 단계의 깨끗한 환경 실행 |
| 게시 2 (도구 검증) | 도구 두 갈래를 Opus 검증자가 봤다. 교차 검증 도구는 그대로는 "수정 필요", 검증 커밋 3개 뒤 병합(`285ba74`, 음성 대조 46개). 로컬 검수 화면도 데이터 손실 버그를 포함해 "수정 필요", 검증 커밋 14개 뒤 병합(`7016084`, 음성 대조 55개) | 검증 커밋 | 병합 뒤 `make verify` |
| 게시 3 (check-dist 오탐) | `a420066`의 깨끗한 환경 실행이 `check-dist-public`에서 실패. 공개 문장 안에 들어 있는 텍스트를 오염(taint) 누출로 판정한 오탐이었다 | 공개 문장 속 텍스트는 누출이 아니라고 `check_dist` 규칙을 고침(`ba511b4`) | 이후 실행에서 `check-dist-public` PASS |
| 게시 4 (E2E-1 시드 가정) | `ba511b4`의 실행(`20261015T063234Z`)이 `e2e-seed`의 E2E-1 2건에서 실패. 테스트가 게시 전 시드 Wiki를 가정하고 있었다 | 게시된 시드 Wiki를 따르도록 E2E-1을 고침(`186294f`) | 깨끗한 환경 `20261015T063931Z` 13/13 PASS |
| 게시 5 (홈 "0개 노드") | 배포된 사이트를 쓰다가 발견. 홈이 "인공지능 · 0개 노드"를 보였다. 분야 노드가 직접 소속만 세었다 | 최상위 분야의 개수에 하위 분야의 노드를 포함(`ab363f0`). 공개 15, preview 205 | 깨끗한 환경 `20261015T064959Z` 13/13 PASS, 배포된 홈이 "인공지능 · 15개 노드"(curl) |
| 최종 리뷰 지적 | R-03 관련 개념(M1), R-10 Lab 링크 base(M2), R-06 Wiki → Entity/Atlas, R-13 술어 필터 | `fix/final-review` 병합(`9613280`). Claim 상태 문구를 "인용 확인"으로 바꿈(`118eb36`) | 새 테스트가 수정 전에 실패하고 수정 후 통과. 각 수정을 되돌리면 해당 테스트가 실패(음성 대조). 검증 Opus 5.5 High: MERGE |

최종 리뷰 지적 중 M1·M2는 아직 ISSUE_LOG에 별도 행이 없다(§10).

## 9. NOT RUN / NOT APPLICABLE

| 상태 | 항목 | 이유 |
|---|---|---|
| PASS | 실제 GitHub Pages 배포와 공개 URL 검증 | https://keeweon-choi.github.io/aixon/ . Pages run 38683822204·38685394691·38686154994·38693966125·38695150022 성공, 스모크 테스트 `deploy-smoke-20261015T045518Z/`(내용 없음)와 `deploy-smoke-20261015T064629Z/`(내용 있음)(§3.2) |
| PASS | GitHub Actions 실행(`ci.yml`, `pages.yml`) | CI 38683822123·38685394647·38686155036·38693966099·38695150153, Pages 위와 같음. 실패한 실행과 수정은 §8 |
| PASS | AI 교차 검증 패널의 승인·게시(ADR-026, 첫 릴리스 44건) | 승인 커밋 `a420066`, 기록 `review/cross/first-release/RELEASE.md`. 이 PASS는 "AI 패널이 기준을 통과시켰다"는 뜻이다. 사람이 확인했다는 뜻이 아니다 |
| PASS | 주간 온라인 검사(`verify-online.yml`, 주 1회 + 수동) | 수동 실행 38686154873 성공(인용 132 found + 경고 31, 식별자 67/67). 앞선 실행 2건은 실패 후 수정(§8). |
| NOT RUN | 사용자가 직접 사용 | 사람이 사이트를 써 본 적이 없다. 배포 사이트를 AI가 Playwright로 쓴 것(§3.2)은 이 항목이 아니다 |
| NOT RUN | 대표 Wiki와 시드 Claim의 사람 검토 | 사람 승인 0건. 사용자는 AI 교차 검증 경로를 택했고(ADR-026) 게시된 44건은 그 경로로 승인됐다. 사람 검토는 로컬 검수 화면(ADR-025)에서 선택 사항이고, 게시되지 않은 시드 Claim과 엔티티는 아직 패널을 거치지 않았다(B-02, §12) |
| NOT RUN | 검색엔진 색인 | 배포는 됐으나 색인 여부를 확인하지 않았다 |
| NOT RUN | 외부 링크 생존 검사 | P1 (CONTENT_VALIDATION_PLAN §3) |
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
| CI 검증 | PASS | GitHub Actions CI 38686155036(`c6851db`, 전체 `make verify`) 성공. 38683822123, 38685394647도 성공(§1, §8) |
| 증거 (보고서, 추적표, 실행 요약, 남은 이슈, 실행 명령) | PASS | 이 문서와 [TEST_MATRIX.md](TEST_MATRIX.md) |

## 10. 남은 이슈

미해결 Critical은 없다. 상세는 [08_ARCHITECTURE_REVIEW.md §4·§6](../08_ARCHITECTURE_REVIEW.md)와 [ISSUE_LOG.md](ISSUE_LOG.md)에 있다.

| 구분 | 항목 |
|---|---|
| Resolved | I-14 `~/aixon/ss_copilot.html`: 삭제(B-05, 사용자 10-15) |
| Resolved | B-02 첫 릴리스의 콘텐츠 게시: ADR-026 경로로 44건 공개(`a420066`). 이후 릴리스 후보는 같은 패널을 거친다 |
| Accepted | I-33 타입 접두 ID·URL (ADR-023, 옛 URL 이동 안내 페이지는 미구현). F-26 Python이 공개를 판정, TS는 관문 파일만 읽음 |
| Backlog (공개 품질) | CSP, GitHub Actions SHA 고정, 공개 빌드 최소 카드, 모바일 목록 분야 필터, alt/title 이중 낭독 |
| Backlog (데이터) | EXTENDS "inspired by" rubric, ADAPTS 근거 vs qualifier, 입도 문제(위치 인코딩·잔차 연결), Atlas 저자 "X et al.", arXiv v1 날짜 자동 채움, slug 규칙 위반 3건, 수준 ↔ 차원 대응, 안 쓰는 술어 동결 |
| Backlog (도구) | 검토 화면(큐레이션 UI, P1. 로컬 검수 화면은 `7016084`에 병합됨), Python에서 `graph.json` 내보내기. 일괄 승인 명령은 구현됨(§12) |
| Backlog (첫 릴리스 메모, `RELEASE.md`. 게시를 막지 않음) | `clm:intro-additive-attention`에 논문 §3.1 문장을 두 번째 근거로 추가. 실험실 온도 모드의 logit 입력이 5칸이라 문항 `ai:lab-softmax-temp-01`의 [2, 1, 0]을 정확히 넣을 수 없음. 인용문 두 개가 원문의 수식 앞에서 끊김. 외부 데이터 문제: OpenAlex `W2626778328`의 DOI와 연도 필드가 잘못 합쳐져 있음. 검증자 독립성: 검증자들이 같은 임시 폴더를 썼으므로 다음 릴리스부터 검증자마다 폴더를 따로 지정 |
| 경고 | seedtool 경고 159건(W103 1, W104 149 참조되지 않는 엔티티, W111 9). W111은 선수 관계 9건이 PART_OF 근거를 그대로 쓴다는 뜻이며 사람 검토 힌트다 |
| P2 | 학습 엔진 전체(I-12 포함) |

문서 불일치는 이 보고서를 쓴 직후 고쳤다: 08 문서의 F-13 상태와 `make verify` 기록, VERIFICATION_PLAN의 pytest 수, 07 문서 Sprint 4·5 상태, ISSUE_LOG의 최종 리뷰 지적 행(I-41…I-44).

## 11. 사용자 결정

자세한 내용은 [BLOCKERS.md](../development/BLOCKERS.md)에 있다. 2026-10-15 사용자 결정으로 모두 닫혔다. B-02는 첫 릴리스에 한해 닫혔고, 이후 릴리스는 같은 경로를 쓴다.

| ID | 결정할 것 | 상태 |
|---|---|---|
| B-01 | 저장소 이름·공개 여부·push 승인 | 해결. 공개 저장소 `Keeweon-Choi/aixon`, 배포 승인("그냥 배포해도 돼 클로드 표시는 상관없으. 사람이 학습할 수 있는 내용의 정합성만 확보되면 돼"). 배포 완료 |
| B-02 | public에 담을 콘텐츠의 검토 방식 | 첫 릴리스에 한해 해결(2026-10-15, 커밋 `a420066`). 사람 승인 대신, 근거가 실제 웹 출처인 독립 AI 검토자들(추론 능력 동급)이 교차 검증을 통과한 콘텐츠를 자동 게시해도 된다고 사용자가 허용했고, 그 경로(ADR-026, 기준 [CROSS_REVIEW.md](CROSS_REVIEW.md))로 44건을 공개했다([RELEASE.md](../../review/cross/first-release/RELEASE.md)). LLM이 지어낸 내용은 안 되고 사람이 쓴 비유는 된다. 사람 검토는 로컬 검수 화면(ADR-025)에서 선택 사항이다. 사람 승인은 0건이다 |
| B-03 | 콘텐츠 라이선스 | 해결. 텍스트 CC BY 4.0(`LICENSE-CONTENT.md`), 코드 MIT(`LICENSE`) |
| B-04 | `~/aixon`의 git 관리와 원격 저장소 | 해결. git 저장소로 만듦 |
| B-05 | `ss_copilot.html` 삭제 여부 | 해결. 삭제 |
| B-06 | 식별자 검증(arXiv)의 CI 단계 | 해결. GitHub의 `verify-online.yml`(주 1회 + 수동). 첫 통과 실행 38686154873 |
| B-07 | 공개 저장소 정책 | 해결. (c) 공개 저장소 |
| B-08 | 공개 저장소의 커밋 이력 | 해결. 이력의 Claude 공동 작성자 줄은 받아들이고 이력은 다시 쓰지 않는다 |

## 12. 사람이 할 콘텐츠 검토를 줄이는 안

지금 승인은 하나씩 한다. 사람 검토 대상은 시드 Claim, 엔티티, 대표 Wiki다. 첫 릴리스 44건은 AI 패널이 승인했다. 아래는 처음 낸 제안이다. 제안 뒤의 진행은 이렇다.

| 안 | 상태 |
|---|---|
| 1 사전 검수표 | 완료. `review/first-release.yaml`·`.md`, 44건 중 승인 권고 41, 수정 3 (사전 검수 결과이고 승인이 아니다). 수정은 `89310e5`에 반영 |
| 4 일괄 승인 명령 | 완료. `tools/review.py approve-batch`, `publish`. 병합 `ea87acf`, 수정 `2355c44` |
| AI 교차 검증 패널(새 경로, ADR-026) | 첫 릴리스 완료. 44건 승인·게시(승인 커밋 `a420066`, 기록 [RELEASE.md](../../review/cross/first-release/RELEASE.md)). 다음 릴리스 후보는 같은 패널을 거친다 |
| 사람 승인 | 0건. 사람 검토는 로컬 검수 화면(ADR-025)에서 선택 사항이다 |

아래 원문은 그대로 둔다. 4항의 "아직 없다"는 위 표와 같이 지금은 구현되어 있다.

1. **사전 검수표.** 오케스트레이터가 Opus에게 Claim마다 판별 질문(02 §8: 인용이 이 술어를 뒷받침하는가, 방향이 맞는가, 조건이 빠지지 않았는가)을 묻고, 인용 속 숫자를 Claim·Wiki 본문의 숫자와 대조한 결과를 표로 만든다. 열은 Claim ID, 술어, 인용 발췌, 판별 질문별 답, 수치 대조, 의심 여부다.
2. **사용자는 표에서 확인한 것만 승인한다.** 의심으로 표시된 줄부터 원문과 직접 맞춰 본다. 확인한 ID만 `tools/review.py approve <id> --by human:<이름> --checked support,numbers,direction,conditions`로 기록한다.
3. **사전 검수는 승인이 아니다.** Opus의 결과는 `review`에 쓰지 않는다. `agent:*` 서명은 공개되지 않는다(ADR-021). 같은 계열 모델이 만든 내용을 같은 계열 모델이 검수하므로 편향이 남는다. 그래서 승인된 항목 중 일부는 사용자가 무작위로 골라 원문을 직접 대조하는 것을 권한다.
4. **일괄 승인 명령은 아직 없다.** `approve`는 ID 하나씩이다. 표를 쓰게 되면 ID 목록 파일을 받는 옵션을 추가하되, 각 레코드의 현재 `reviewed_hash`에 묶고 사용자 세션에서만 돌게 한다. 필요하면 추가한다.
5. **첫 공개는 작게 시작할 수 있다.** 대표 Wiki(SDPA)는 Claim 12개와 논문 4편을 인용한다(frontmatter 기준). 이 Wiki와 Claim 12개, 그리고 Claim 양 끝의 엔티티만 먼저 승인하면 공개 사이트에 처음으로 내용이 생긴다. 엔티티 수는 세어 보지 않았다.

이 안의 효과(검토 시간이 얼마나 줄지)는 측정하지 않았다.

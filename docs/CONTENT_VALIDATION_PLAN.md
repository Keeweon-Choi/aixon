# CONTENT_VALIDATION_PLAN — Graph·Wiki·사이트 검증 계획

> 무엇을, 어떤 도구로, 언제 검증하는지. 각 항목은 ID를 갖고 `docs/verification/TEST_MATRIX.md`와 연결된다. 실패하면 빌드·CI가 멈춘다(경고 W는 보고만).
> 실행: `make verify`(전체), 개별 `make validate | test | build | check-dist | e2e`.

## 1. 계층별 검증 항목

### L-G Graph (빌드 전, `tools/seedtool.py`)

| ID | 검사 | 도구 | 실패 시 |
|---|---|---|---|
| V-GRAPH | 02 §9 불변식 G001–G018(ID·참조·정의역·중복 식별자·근거 정책·선수 순환·OR 그룹·차원·구성 순환·대칭·ADAPTS·시간 정합성·IMPROVES_ON 수치 방향·반려 재등장·인용 형식·문항) | `seedtool validate <graph paths>` | 빌드 중단 |
| V-QUOTE | 모든 Evidence 인용문이 Source 원문(특정 버전)에 있다 | `seedtool quotes`(온라인, 캐시 `data/cache/fulltext`) | 오류(사람 확인) |
| V-ID | Paper의 arXiv ID ↔ 제목이 arXiv API와 일치 | `tools/verify_identifiers.py` | 해당 Paper 식별자 미검증 배지 |
| V-CITES-NOT-INFLUENCE | CITES만 있는 쌍에서 EXTENDS·ADAPTS가 생기지 않는다 | `test_seedtool.py` T16, vitest 그래프 로더 | 테스트 실패 |
| V-VERIFIED-ONLY | 미검증(proposed)·disputed 관계는 public 그래프와 선수 계산에 들어가지 않는다 | vitest(로더 필터), T17 | 테스트 실패 |

### L-C Content (빌드 전, `tools/validate_content.py`)

| ID | 검사 |
|---|---|
| V-SCHEMA-1 | frontmatter가 CONTENT_SCHEMA §2를 따른다(빌드의 zod 스키마도 같은 검사) |
| V-SCHEMA-2 | 파일명 slug = `id` slug = `entity` slug, entity당 Wiki 하나 |
| V-SCHEMA-3 | frontmatter `sections` = 본문 `<Section id>` 집합, level 값 유효 |
| V-LINK-1 | 모든 `<ConceptLink id>`가 Graph에 있다 |
| V-CITE-1 | 모든 `<Cite src|claim>` 대상이 Graph에 있다 |
| V-CITE-2 | `math`·`mechanism`·`history` 섹션(상태 ≥ draft)에 `<Cite>`가 하나 이상 |
| V-CITE-3 | 본문에서 인용한 Source·Claim이 frontmatter `sources`·`claims`에 있다 |
| V-STATUS-1 | CONTENT_SCHEMA §2.2 상태 조건(reviewed·published는 사람 review, published는 published_at) |
| V-STATUS-2 | `ai_generated: true` ⇒ reviewed 이상이면 `review.by`가 `human:` |
| V-STATUS-3 | 인용한 Claim이 rejected·deprecated면 오류, proposed·disputed면 경고 |
| V-CODE-1 | ```` ```python verify ```` 블록이 모두 실행·통과(20초 제한, numpy만) |
| V-FIG-1 | `<Figure id>`가 frontmatter `figures`에 있고 `origin: self-made`, `alt`가 있다 |

### L-B Build·Dist (빌드 후)

| ID | 검사 | 도구 |
|---|---|---|
| V-BUILD | `astro build`(preview·public) 성공, MDX·스키마 오류 0 | `make build`, `make build-public` |
| V-MATH | 출력 HTML에 `katex-error` 없음, KaTeX에 MathML 포함 | `check_dist.py`, E2E-8 |
| V-DIST-LINK | 모든 내부 `href`·`src`가 실제 파일로 해석된다(base 포함) | `check_dist.py` |
| V-SEO | 페이지마다 `<title>`, meta description, `lang="ko"`, `h1` 하나; `sitemap-index.xml`, `robots.txt`(public은 허용, preview는 차단) | `check_dist.py`, E2E-8 |
| V-NO-CDN | 외부 CDN 스크립트·스타일 없음(KaTeX CSS도 로컬 번들) | `check_dist.py` |
| V-PUBLIC | public 빌드에 미승인 Wiki·Claim·AI 요약이 없다 | E2E-9 |
| V-SECRETS | 저장소에 키·비밀이 없다 | `scan_secrets.py` |

### L-U Unit (vitest, pytest)

| ID | 검사 |
|---|---|
| V-LAB-L1…L7 | 05 §5.4: softmax 합 1(1e-12), shift invariance, ±1000·T=0.05에서 NaN 없음, golden fixture 일치(1e-12), mulberry32(42) 정확 일치, Var(q·k)≈d_k(5%), SDPA 통계 fixture 일치(1e-9) |
| V-LOADER | YAML 병합, 중복 ID 예외, 빌드 모드 필터, intro year, 차원별 선수 |
| V-SEARCH | 노드 빠른 검색: 2글자 한국어·별칭·대소문자 무시 |
| V-URL | base 경로 접두 |
| V-PLANNER (P2 기준 구현) | `tools/test_seedtool.py` M1–M9, P1–P14(04 문서) — 학습 엔진은 P2지만 기준 구현과 테스트는 유지한다 |

## 2. 브라우저 E2E (Playwright, `astro preview`, `AIXON_BASE=/aixon/`, desktop 1280×900 + mobile 390×844)

| ID | 시나리오 | 기대 결과(교차 검증) |
|---|---|---|
| **E2E-1** | **Graph → Wiki → Related → Graph**: 홈 → 빠른 검색 "어텐션" → Scaled Dot-Product Attention → Entity → "Wiki 읽기" → 단계 전환 → 본문의 softmax `ConceptLink` → softmax Entity → "그래프에서 보기" | Wiki에 KaTeX 수식·코드 블록·초안 배너가 있다. 단계 전환이 보이는 섹션을 바꾼다. Atlas가 softmax 노드를 선택한 상태로 열린다(패널 이름 일치) |
| E2E-2 | Lab 수치 | 화면의 `prob-*`가 fixture(독립 numpy 계산)와 소수 4자리까지 일치. 모드 B 평균 최대 가중치 0.9548(scaling off)·0.3646(on) |
| E2E-3 | Evidence Inspector | 인용·위치·원문 링크(`#:~:text=`)·상태 배지. disputed Claim은 지지·반대 근거를 모두 보인다 |
| E2E-4 | Trace | 모델 노드에 연도, 간선(또는 목록 행) 클릭 → Claim 페이지 |
| E2E-5 | Pagefind 검색 | Wiki 본문 단어로 검색 → 결과 → 해당 페이지로 이동 |
| E2E-6 | GitHub Pages 직접 링크·새로고침 | `/aixon/wiki/…/`, `/aixon/e/…/`, `/aixon/claims/…/`를 직접 열고 새로고침해도 같은 `h1`. 없는 경로는 404 페이지 |
| E2E-7 | 데스크톱·모바일 레이아웃 | 주요 화면 가로 넘침 없음. 모바일에서 그래프는 목록 보기 |
| E2E-8 | SEO·접근성 기본 | title·description·lang·h1, 그래프 노드 aria-label, MathML |
| E2E-9 | public 빌드 관문 | `dist-public`에 draft Wiki·미승인 Claim이 없고, 승인된 문서는 있다. robots.txt 허용 |

| **E2E-10** | **Understanding Vision Transformer**(지침 Phase G 여정의 v0.1 판, 실제 시드로만 실행): ① Explore — Atlas에서 Computer Vision 분야 → `model:vit` 노드 → 패널의 분야·논문 ② Trace — `/trace/`에서 ViT와 Transformer 사이 `ADAPTS` 간선 → Claim 페이지(Evidence Inspector) ③ Learn — ViT·SDPA 페이지의 선수 개념 목록(REQUIRES Claim)을 따라 SDPA Wiki로 이동 ④ Lab — temperature 변경 → 확률 변화 → 예측 문제 제출 | ① 분야에 Computer Vision, 논문에 Dosovitskiy 2020 ② 관계 유형 `ADAPTS`, 인용 원문·위치·arXiv 링크, 연도 순서 Transformer(2017) < ViT(2020), CITES만 있는 쌍은 영향 관계로 그려지지 않음 ③ 화면의 선수 목록 = 시드의 verified REQUIRES 간선(로더 결과와 교차 확인) ④ 화면 수치 = fixture, 채점 결과 표시. **⑤ Remember·⑥ Resume(숙련도 저장·재계산)은 P2(ADR-019) → NOT APPLICABLE.** 학습 경로 계산 자체는 `test_seedtool.py` P15·P15b(golden 계획)가 검증한다 |

E2E 테스트는 **결정적인 fixture 그래프·Wiki**(`tests/fixtures/`)로 돈다. 실제 시드에 대해서는 같은 E2E-1·2·6·7과 E2E-10을 시드 경로 환경 변수로 한 번 더 돌린다(`make e2e-seed`, 07 문서 Sprint 4 완료 조건).

## 3. 하지 않는 것 (MVP 범위 밖)

- 실제 GitHub Pages 배포와 공개 URL 검증: 저장소·push가 필요하므로 사용자 승인 뒤에 한다. 대신 base 경로를 재현한 로컬 preview로 E2E-6을 검증한다(인수 보고서에 NOT RUN으로 따로 적는다).
- 외부 링크(논문·교재 URL) 생존 검사: 네트워크가 필요하고 결과가 흔들린다. 수동 실행 도구로만 둔다(P1).
- 검색엔진 실제 색인 여부: 배포 뒤에만 확인할 수 있다.

## 4. 증거 보존

`make verify`는 `artifacts/verification/runs/<UTC>/`에 `summary.json`(단계, 명령, 종료 코드, 시간, 로그 경로), 단계별 로그, `graph-validation.json`, 실패한 Playwright 테스트의 trace·스크린샷을 남긴다. 성공한 실행의 영상은 저장하지 않는다.

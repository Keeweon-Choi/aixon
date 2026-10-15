# 08. Architecture Review — 독립 설계 감사와 처리 현황

> 감사 2026-10-15 03:10–03:45 · 이 문서 작성 2026-10-15. 결정은 [DECISIONS.md](DECISIONS.md) ADR-021–024, 결함 기록은 [verification/ISSUE_LOG.md](verification/ISSUE_LOG.md) I-23 이후, 사용자 결정은 [development/BLOCKERS.md](development/BLOCKERS.md).

## 1. 목적

설계자와 다른 검토자가 v0.1 설계(그래프·공개 관문·Wiki·사이트·검증 하네스)를 독립적으로 점검해, 공개 전에 고쳐야 할 결함을 찾는다. 이 문서는 지적 31건과 각각의 처리 상태·증거를 한 곳에 모은다.

## 2. 방법과 기록의 한계

| 항목 | 내용 |
|---|---|
| 검토자 | 설계를 쓰지 않은 독립 에이전트(sonnet 서브에이전트) |
| 시간 | 2026-10-15 03:10–03:45 |
| 관점 | 8개 관점. 관점 목록은 원본 보고서와 함께 유실되어 여기서 복원하지 않는다 |
| 다시 실행한 것 | Claim 105건 전수 열람(ADR-022 기록). 그 밖에 검토자가 재실행한 검사의 목록은 남아 있지 않다 |
| **원본 유실** | 감사 보고서 파일(`scratchpad/design_audit.md`)은 04:27 WSL 재시작으로 `/tmp`가 지워지며 사라졌다. **아래 표는 오케스트레이터의 요약·판정 기록이지 원문이 아니다.** 지적 문구는 한 줄로 줄인 것이다 |
| 이 문서의 검증 | 문서만 고쳤다. 이 문서를 쓰면서 새로 실행한 검사는 없다. 표의 “실행”은 오케스트레이터가 실행했다고 보고한 것이다 |

## 3. 요약

| 심각도 | 건수 |
|---|---|
| Critical | 2 |
| Major | 17 |
| Minor | 8 |
| Enhancement | 4 |
| 합계 | 31 |

| 처리 상태 | 건수 | 항목 |
|---|---|---|
| Fixed | 20 | F-01–09, 11, 12, 14–17, 19, 21, 24, 27, 31 (F-08은 설정만 고침, 실제 배포 NOT RUN) |
| Fixed(일부) + Backlog | 5 | F-18, 20, 22, 25, 29 |
| Accepted | 2 | F-10, F-26 |
| In progress | 1 | F-13 |
| Backlog | 3 | F-23, 28, 30 |

Critical 2건은 모두 고쳤다. 남은 Major는 F-13(진행 중)과 F-10(수용)이다. 첫 공개의 선행 조건은 이 문서가 아니라 BLOCKERS B-01–B-07의 사용자 결정이다.

## 4. 지적 목록

| ID | 심각도 | 지적(한 줄) | 상태 | 증거·검사 |
|---|---|---|---|---|
| F-01 | Critical | 공개 관문을 위조할 수 있고 기본값이 전량 공개(fail-open) | Fixed | ADR-021. `tools/public_gate.py`가 허용 목록 `.aixon/public-gate.json` 계산, 승인은 `review.by: human:*` + `reviewed_hash`(G022), `AIXON_BUILD` 기본값 없음, `tools/review.py`(에이전트 세션 거부 — 실수 방지), `check_dist.py` public 모드가 관문 재계산 + taint 테스트. 실행: `tools/test_public_gate.py`; 관문 없이 public 빌드 → 실패; 그래프 파일 수정으로 관문이 오래됨 → 빌드 exit 1; dist-public 사본에 미승인 요약·노드 주입 → V-PUBLIC 오류 2건 |
| F-02 | Critical | `verified`가 인용 존재만 뜻하는데 사실 확인처럼 보임 | Fixed | ADR-022(배지 3축: 인용 확인 / 사람 검토 / 공개). Claim 26건 교정(DeiT 84.2 − 77.9 = +6.3, INTRODUCES·ADDRESSES·ADAPTS 근거를 저자 의도 문장으로, ResNet Table 3 행 인용, “VGG-16 is based on our test”는 stance `qualifies`). 실행: 오프라인 인용 대조 132/132 found; 변조 인용 → not_found, exit 1. 인용이 술어를 뒷받침하는지는 기계 검사 없음(사람 검토) |
| F-03 | Major | 선수 관계가 의존 근거 없이 verified | Fixed | G023(인용이 subject 언급, 단어 접두 일치, 선택 `key_terms`), W111(PART_OF 근거 재사용 = 사람 검토 힌트), 5건 proposed로 내림, 인용 6건 교체, golden 계획 재생성(softmax-temperature는 sdpa@derive의 선수가 아님). 실행: tools 테스트 통과 |
| F-04 | Major | Wiki `<Cite claim>`이 Claim의 근거와 맞지 않음 | Fixed | 대표 SDPA 개정: Cite는 관계를 진술하는 Claim을, 해석은 Source를 가리킴. 의미 일치의 자동 검사는 없음(사람 검토) |
| F-05 | Major | 관문의 적용 범위가 좁음(분류·메타데이터·질문 제외) | Fixed | 엔티티 단위 `review` 하나가 모든 서술 필드를 덮음(`summary_review` 폐지), 상태 × 승인 규칙(`verified`·`disputed` + 승인 + 공개 끝점), taint 테스트. 저장소 공개 여부는 사용자 결정 → BLOCKERS B-07 |
| F-06 | Major | 승인이 내용에 묶여 있지 않음 | Fixed | `reviewed_hash`; 변경 후에는 G022 stale |
| F-07 | Major | 공개 빌드에서 Wiki ↔ 그래프 해석이 어긋남 | Fixed | 가시성 모듈 하나(`isVisible`/`wikiFor`); 비공개 Claim을 인용하면 “(검토 대기)”로 링크 없이 표시; 공개 문서가 비공개 Claim을 인용하면 public_gate 오류 |
| F-08 | Major | 배포가 검증 결과에 묶여 있지 않음 | Fixed(설정) | `pages.yml` build → deploy를 `needs`로 연결, validate에 atlas·관문, verify에 public 빌드·check, 주간 verify-online. **워크플로 실행과 실제 배포는 NOT RUN**(사용자 승인 필요, B-01) |
| F-09 | Major | 시드가 Atlas 분야와 연결되지 않음 | Fixed | 시드 도메인 엔티티 61개에 `fields`, `field:ml-mathematics` 추가, W107 |
| F-10 | Major | ID·URL에 타입 접두가 있어 재분류 시 링크가 깨짐 | Accepted | ADR-023: 공개 전 위험 수용, 이후 재분류는 merged tombstone + 이동 안내, G024 slug 유일. 이동 안내 페이지 생성은 미구현 |
| F-11 | Major | 유형 사이 중복 엔티티 | Fixed | 중복 분야 4개 제거·구성원 이동, G024, W108 |
| F-12 | Major | Astro 7 함정(remark 분리, MDX import) | Fixed | `@astrojs/markdown-remark` 7.3.1 + remark-math/rehype-katex, `<Lab id>` 래퍼로 MDX에 import 없음, MDX import 금지를 콘텐츠 검증기에 추가(작업 H1). V-MATH |
| F-13 | Major | 검사 결과가 재현되지 않음 | In progress | 작업 F13: `quotes --pin`으로 `content_sha256` 고정, `--write-checked` 정상화, 잘못된 arXiv 확인 표시 제거. pypdf는 I-18에서 requirements에 추가 |
| F-14 | Major | E2E 계획이 실제 데이터와 맞지 않음 | Fixed | 시드 KU 한국어 이름·별칭(“스케일드”, 2글자 “어텐”), d_k 512 선택지, `make e2e-seed` + E2E-10, `.katex-display` 넘침 CSS |
| F-15 | Major | 테스트 품질(T16, 느슨한 단언) | Fixed | T16 재작성(논문 사이 CITES가 선수 관계를 만들면 안 됨), T1–T15가 G 코드 집합을 정확히 단언(본질적 연쇄는 문서화), fixture 기준 오류 수정, golden 비교가 내용 해시 무시, T18 경고 스냅샷 `data/seed/validate_snapshot.json`, coverage 집계 단위 테스트 |
| F-16 | Major | Wiki 단계 구조(직관 단계가 자족적이지 않음) | Fixed | 직관 단계에서 d_k 정의, 기초 단계에 “왜 √d_k”와 인용, 한계를 기초 단계로, 단계는 첫 그림 전에 CSS로 적용, V-CITE-2는 deep 밖의 인용만 셈(H1) |
| F-17 | Major | 오해를 부르는 서술 | Fixed | 역사(dot-product attention은 이미 흔했고 Transformer가 1/√d_k 스케일링을 더함), “거의 one-hot”은 d_k = 512 수치와 함께만, 순열 등변성을 정확히 쓰고 코드로 assert, Swin 인용, 단일 헤드·마스크 없음 범위, 번역 표시 |
| F-18 | Major | 실행 가능 콘텐츠 | Fixed(일부) | `python verify`는 `python -I`·축소 환경·import 허용 목록; MDX raw HTML·`on*`·`javascript:` 금지(H1); check_dist V-SEC; seedtool G025(https만). **CSP는 Backlog** |
| F-19 | Major | 복사 요약 | Fixed | I-21(요약 70개 교체) + W109/W110 |
| F-20 | Minor | 공개 빌드의 빈 페이지 | Fixed(일부) | 공개 홈 안내, ConceptLink 대체 표시. 최소 카드·모바일 목록의 분야 필터는 Backlog |
| F-21 | Minor | Wiki 세부 | Fixed | 자체 예문, Lab 앞 예측 후 공개, Lab 문항 프롬프트에 가정 추가, 기호 설명, 본문 숫자 전부 assert, SVG 화살촉. alt/title 이중 낭독은 Backlog |
| F-22 | Minor | 온톨로지 rubric | Fixed(일부) | stance 수정, IMPROVES_ON 문장에서 “같은 조건” 제거. Backlog: EXTENDS “inspired by” rubric(02 §8.1), ADAPTS 근거와 qualifier, 위치 인코딩·잔차 연결 입도 |
| F-23 | Minor | 메타데이터 세부 | Backlog | Atlas 저자 “X et al.”, arXiv v1 날짜 불일치(네트워크 가능할 때 자동 채움), slug 규칙 위반 3건(li2020-pytorch, mitchell2019-modelcards, van2016-pixelrnn), ba2016의 venue 노트 문구 |
| F-24 | Minor | 문서 불일치 | Fixed | 이 감사 반영 커밋의 문서 수정: CONTENT_SCHEMA 예시, 02 §9(G019–G025·W107–W111), S6/S8 번호, `aixon` 식별자 규칙, 07 summary_review, slug 유일성, `src:pdf:*`, 노드 상한 80, validate 출력 설명, ADR-024, `specs/codex_site_mvp.md` 대체 안내. 자동 검사 없음(문서 대조) |
| F-25 | Minor | 보안 기타 | Fixed(일부) | scan_secrets 오탐 수정(H1). Actions SHA 고정과 CSP는 Backlog. `ss_copilot.html`·`study/`를 공개 저장소에서 제외하는 문제는 BLOCKERS B-07 |
| F-26 | Minor | 이중 엔진, P2 결합 | Accepted | Python이 공개 여부를 판정(단일 원천), TS 로더는 관문 파일만 읽음. seedtool의 P2 부분은 유지(ADR-019). Python에서 `graph.json` 내보내기는 Backlog |
| F-27 | Minor | 정직성 세부 | Fixed | ISSUE_LOG 머리글 문구 수정, R-14 coverage 테스트(`tests/unit/coverage.test.ts`) |
| F-28 | Enhancement | 수준(level) ↔ 차원(dimension) 대응 | Backlog | — |
| F-29 | Enhancement | 검토 도구 | Fixed(일부) | `tools/review.py list/show/approve`. 검토 화면(큐레이션 UI)은 P1 |
| F-30 | Enhancement | 쓰지 않는 술어 동결 | Backlog | — |
| F-31 | Enhancement | 배지 3축 | Fixed | ADR-022 |

## 5. 수용한 위험

| 위험 | 수용 이유 | 근거 |
|---|---|---|
| 타입 접두 ID·URL(F-10) | 공개 전이라 외부 링크가 없다. 지금 바꾸면 시드·지도·명세·테스트를 모두 다시 써야 하고 이득은 공개 뒤에 생긴다 | ADR-023 |
| 승인 도구의 에이전트 거부는 보안 경계가 아님(F-01) | 환경 변수 검사는 실수만 막는다. 실제 통제는 git diff 검토와 배포 환경의 필수 검토자 | ADR-021 |
| Python이 공개를 판정, TS는 결과 파일만 읽음(F-26) | 판정 규칙이 한 곳에 있고, 이중 구현보다 낫다 | ADR-021, ADR-019 |
| 정적 퀴즈의 정답이 번들에 있음(F-24 정리 중 확인) | 저장·이해관계가 없다. P2에서 응답을 저장하면 서버 채점으로 바꾼다 | ADR-024 |
| 공개 직후 사이트가 비어 보임 | 승인 0건이면 홈·방법론·빈 지도뿐. 검토 속도가 공개량을 정한다 | ADR-017, ADR-021 |

## 6. 백로그

| 항목 | 출처 |
|---|---|
| CSP, GitHub Actions SHA 고정 | F-18, F-25 |
| 공개 빌드 최소 카드, 모바일 목록의 분야 필터 | F-20 |
| alt/title 이중 낭독 정리 | F-21 |
| EXTENDS “inspired by” rubric(02 §8.1), ADAPTS 근거 vs qualifier, 위치 인코딩·잔차 연결 입도 | F-22 |
| Atlas 저자 “X et al.”, arXiv v1 날짜 자동 채움, slug 규칙 위반 3건, ba2016 venue 노트 | F-23 |
| Python에서 `graph.json` 내보내기 | F-26 |
| 수준 ↔ 차원 대응 | F-28 |
| 검토 화면(큐레이션 UI) | F-29 |
| 쓰지 않는 술어 동결 | F-30 |
| 옛 URL 이동 안내 페이지 생성 | F-10 |

## 7. 아직 열려 있는 것

| 항목 | 상태 |
|---|---|
| F-13 재현 가능한 검사 | 진행 중 |
| 실제 배포, 저장소 공개 정책, 라이선스, 승인 0건 → 공개 콘텐츠 | 사용자 결정(BLOCKERS B-01–B-07) |
| 전체 `make verify` 녹색 기록 | 이 문서 작성 시점에 없음 |

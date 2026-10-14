# 07. MVP Roadmap — v0.1 Knowledge Atlas + Interactive AI Wiki

> 범위는 사용자 방향 수정(2026-10-15, ADR-019)을 따른다. 요구사항 ID는 [verification/REQUIREMENT_TRACEABILITY.md](verification/REQUIREMENT_TRACEABILITY.md)에서 데이터·화면·모듈·테스트와 연결된다.
> **MVP 성공은 기능 수나 데이터 건수가 아니라, Graph → Wiki → 근거 → Graph로 이어지는 경험의 정확성과 일관성으로 판단한다**(00 문서 §6 지표 S1–S7).

## 1. P0 (v0.1)

| ID | 기능 | 목적 | 의존 | 인수 기준 | 데이터 | 테스트 | 복잡도 | 위험 |
|---|---|---|---|---|---|---|---|---|
| R-01 | AI 전체 분야 Knowledge Graph | 넓은 지도 + 검증된 깊이 | seedtool | 분야 ≥ 80, 시드 Claim의 인용 원문 대조 100%, G 오류 0, 지도 논문 arXiv 대조 100% | `data/seed`, `data/graph/atlas.yaml` | V-GRAPH, V-QUOTE, V-ID | 중 | 넓은 분류의 AI 요약 품질(→ R-15로 공개 차단) |
| R-02 | Interactive Atlas | 분야 구조 탐색 | R-01, graph.json | 상위 분야에서 시작해 점진적으로 펼침, 노드 패널에서 Entity/Wiki로 이동, 유형·검증 필터, 목록 보기 | graph.json | E2E-1, E2E-7 | 중 | 그래프 자체가 목적이 되는 것(U1) |
| R-03 | Wiki 콘텐츠 모델과 렌더러 | 개념 교육 문서 | CONTENT_SCHEMA | frontmatter 스키마 검증(빌드 실패), `<Section>`/`<Level>` 단계 전환, 관련 개념·참고문헌 자동 생성 | `src/content/wiki` | V-SCHEMA, E2E-1 | 중 | 스키마 과설계 |
| R-04 | 대표 개념 교육 페이지 | 깊이의 기준 사례 | R-03, R-12 | Scaled Dot-Product Attention 문서가 11개 섹션 구조 중 9개를 갖추고 모든 숫자가 `python verify`로 확인됨 | MDX | V-CODE-1, E2E-1·2 | 중 | 내용 오류 → 사람 검토(R-15) |
| R-05 | 수식·코드·다이어그램 | 설명 수단 | R-03 | KaTeX 빌드 렌더링(오류 0, MathML 포함), Shiki 코드, 직접 만든 SVG(alt 필수) | — | V-MATH, V-FIG | 하 | — |
| R-06 | Graph ↔ Wiki 이동 | 탐색과 학습 연결 | R-01, R-03 | `<ConceptLink>`가 Entity ID로 연결(존재 검증), Entity → Wiki, Wiki → Atlas 노드 선택 | — | V-LINK-1, E2E-1 | 하 | ID 변경(불변 규칙으로 대응) |
| R-07 | 검색 | 빠른 진입 | 빌드 | 노드 빠른 검색(2글자 한국어), Pagefind 전문 검색 → 페이지 이동 | node-index.json, pagefind | V-SEARCH, E2E-5 | 하 | Pagefind 한국어 품질 |
| R-08 | 근거·참고문헌 | 신뢰 | R-01 | Claim 페이지(인용·위치·원문 링크·상태·검토), Wiki 참고문헌 자동 목록 | claims, sources | E2E-3, V-CITE | 하 | — |
| R-09 | 검증된 시드 콘텐츠 | 정확성의 기준 | — | 시드 Claim 105(검증 100, disputed 1, proposed 3, rejected 1), 인용 121/121, E2E 계획 golden | `data/seed` | V-QUOTE, P15·P15b | 상(완료) | — |
| R-10 | GitHub Pages 배포 | 공개 | R-15 | `pages.yml`, base 경로·디렉터리 URL, 로컬에서 직접 링크·새로고침 재현 | — | E2E-6, V-DIST-LINK | 하 | 실제 배포는 사용자 승인 필요(NOT RUN) |
| R-11 | 자동 검증 하네스 | 지속적 품질 | 전체 | `make verify` 한 번으로 정적·단위·검증·빌드·dist·E2E 실행, `summary.json` 증거, CI(`ci.yml`) | artifacts/ | 하네스 자체 | 중 | 느린 E2E |
| R-12 | Interactive Lab | 이해 확인 | R-03 | Softmax Temperature·SDPA Lab이 브라우저에서만 실행, 화면 수치 = 독립 계산(4자리), 예측 문제 채점 | lab fixtures | V-LAB L1–L7, E2E-2 | 중 | 수치 불일치 |
| R-13 | 연구 계보(Trace) | 관계 탐색 | R-01 | 시간축 계보, 술어 필터, 간선 → Claim 페이지, CITES ≠ 영향 표시 | graph.json | E2E-4, V-CITES-NOT-INFLUENCE | 중 | — |
| R-14 | 콘텐츠 상태·Coverage | 넓이와 깊이의 가시화 | R-01, R-03 | 상태 5단계(missing–published) 표시, Coverage 페이지(분야별 노드·Wiki·Claim 수) | — | V-STATUS, E2E-7 | 하 | — |
| R-15 | 콘텐츠 공개 관문 | AI 콘텐츠 자동 게시 금지 | R-03 | public 빌드에 미승인 Wiki·Claim·AI 요약 0 | review 필드 | E2E-9, V-STATUS-2 | 하 | 공개 사이트가 비어 보임(검토 속도) |
| R-16 | SEO·접근성·반응형 | 공개 품질 | 빌드 | title·description·lang·h1, sitemap, robots, 키보드·aria, 모바일 가로 넘침 0 | — | V-SEO, E2E-7·8 | 하 | — |

## 2. P1 / P2

| 단계 | 기능 | 비고 |
|---|---|---|
| P1 | Wiki 범위 확장(softmax, multi-head attention, positional encoding, ViT, ResNet…), Lab 추가(합성곱·수용 영역, 경사하강, 카메라 투영), 상세 연구 타임라인, 개념 비교, 학습 자료 확장, 자동 CITES(두 소스 합집합 + 원문 참고문헌 확인), 큐레이션 화면(검토 대기 목록), 외부 링크 생존 검사 | |
| P2 | 사용자 계정, 개인 숙련도·학습 경로(04 문서, seedtool 기준 구현), 학습 이력·복습(FSRS), LLM API(설명 보조·후보 제안), 다중 사용자 백엔드(06 문서 FastAPI·SQLite 설계) | 조사 E 권고 반영(I-12) |

## 3. Sprint (논리적 순서와 객관적 완료 조건)

| Sprint | 목표 | 완료 조건(모두 자동 검증 가능) | 상태(2026-10-15 03:0x) |
|---|---|---|---|
| 0 | 조사·설계·검증된 시드 | 조사 10건, 설계 문서, seedtool 60 테스트 통과, 시드 G 0·인용 121/121, 지도 arXiv 54/54, E2E golden 계획 | **완료** |
| 1 | 사이트 기반 | Astro 설정, 그래프 로더(vitest), Entity·Field·Claim·Coverage·About·404 페이지, `make lint/typecheck/test` 통과 | 진행 중(Codex) |
| 2 | Wiki | Content Collection 스키마, 컴포넌트, 대표 문서, `validate_content.py` V-* 통과, KaTeX 오류 0 | 진행 중 |
| 3 | Island·검색 | Atlas·Trace·Lab island, 노드 검색, Pagefind, vitest L1–L7 | 진행 중 |
| 4 | E2E·배포 준비 | Playwright E2E-1…9 통과(desktop·mobile), public 빌드 관문, `check_dist` 통과, `pages.yml`, `make verify` 녹색, 실제 시드로 E2E-1·2·6·7 재실행 | 대기 |
| 5 | 독립 최종 리뷰·인수 | 리뷰어 지적 Critical/Major 0, `MVP_ACCEPTANCE_REPORT.md` | 대기 |

## 4. 열린 질문 (사용자 결정 필요)

1. **AIXON 콘텐츠 라이선스**(텍스트·코드·그림): 공개 전에 정해야 한다(예: 텍스트 CC BY 4.0, 코드 MIT).
2. **공개 범위와 시점**: 저장소 생성·push·GitHub Pages 활성화는 사용자 승인 뒤에 한다. public 빌드는 사람이 승인한 콘텐츠만 내보내므로, 첫 공개 전에 시드 Claim과 대표 Wiki 검토가 필요하다.
3. **넓은 지도(atlas.yaml)의 요약 문장**: AI 초안이다. 공개하려면 분야 단위로 검토 승인(`summary_review`)이 필요하다.

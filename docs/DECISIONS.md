# DECISIONS — Architecture Decision Records

> AIXON의 주요 기술·제품 결정. 각 결정은 **결정 · 대안 · 근거 · 트레이드오프 · 재검토 조건**으로 적는다. 결정을 바꿀 때는 기존 ADR을 지우지 않고 `Superseded by ADR-0xx`로 표시한다.
> 작성 2026-10-15. 모든 ADR의 상태는 Accepted(MVP 설계 기준)다.

| ADR | 제목 | 한 줄 결정 |
|---|---|---|
| 001 | 큐레이션 그래프 저장 위치 | git 안의 YAML이 정본, DB는 개인 데이터만 |
| 002 | Graph storage: PostgreSQL graph tables vs Neo4j | 둘 다 아님. 메모리 그래프(MVP) |
| 003 | 개인 데이터 DB | SQLite (PostgreSQL은 다중 사용자 때) |
| 004 | Modular monolith vs microservices | 프로세스 1개짜리 modular monolith |
| 005 | Deterministic graph engine vs LLM planner | 결정적 계획기. LLM은 경로 구조에 관여하지 않음 |
| 006 | Manual curation vs automated extraction | 수동 큐레이션 + 기계 검증. 자동 추출은 proposal로만 |
| 007 | Lab 계산 위치 | 브라우저(순수 TS) + golden fixture |
| 008 | 웹 스택: Next.js + FastAPI vs 단순 대안 | Vite React SPA + FastAPI |
| 009 | 검색 | 메모리 lexical → SQLite FTS5. 벡터 검색 없음 |
| 010 | 그래프 시각화 라이브러리 | React Flow + ELK.js(선수 DAG), 시간축은 직접 배치 |
| 011 | 학습자 상태 추정 | 차원별 규칙 기반 숙련도. FSRS는 P1 복습 일정 |
| 012 | 근거·신뢰도 표현 | 인용 기계 대조 + 사람 검토 분리, confidence는 서열 |
| 013 | 인증 | MVP에는 없음(localhost 바인딩) |
| 014 | 식별자 | 타입 접두 slug, Paper = work(버전은 Source) |

---

## ADR-001 큐레이션 지식 그래프의 정본은 git 안의 YAML

- **맥락**: 지식 그래프에는 개정 이력, 검토, 되돌리기, 버전 고정이 필요하다(요구사항 5.3 Revision History, Graph Version, Human Review). 사용자는 한 명이고 큐레이터도 같은 사람이다. LLM이나 도구가 만든 제안도 사람이 검토해야 한다.
- **결정**: 엔티티·Claim·Evidence·문항·목표·Lab 정의를 **YAML 파일로 git에 둔다**. 백엔드는 시작할 때와 publish할 때 YAML을 읽어 검증하고 메모리 스냅샷을 만든다. DB에는 개인 학습 데이터와 외부 원본 캐시만 둔다.
- **대안**: (a) DB를 정본으로 하고 revision 테이블, 스냅샷 테이블, 검토 워크플로를 직접 구현한다. (b) 정본은 YAML로 하되 DB 투영 테이블도 유지한다.
- **근거**: 개정 이력·diff 리뷰·되돌리기·브랜치를 git이 무료로 제공한다. "LLM이 제안하고 사람이 승인"하는 흐름이 **diff 검토**라는 익숙한 형태로 자연스럽게 생긴다. 그래프 버전은 내용 해시로 결정적으로 정할 수 있다. 1인이 관리할 수 있는 가장 적은 코드다.
- **트레이드오프**: 앱 안 큐레이션 UI(P1)가 파일을 써야 한다. 동시 편집에 약하다(단일 사용자라 문제없음). 그래프가 커지면 로딩 시간이 늘어난다.
- **재검토 조건**: ① 여러 큐레이터가 동시에 편집한다 ② 시작 시 YAML 로딩이 5초를 넘는다(약 5만 Claim 수준으로 추정) ③ 앱 안 편집 빈도가 git 워크플로보다 훨씬 많아진다.

## ADR-002 Graph storage: PostgreSQL Graph Tables vs Neo4j → MVP는 둘 다 쓰지 않는다

- **맥락**: 요구된 질의는 초점 노드 이웃(depth 1~2), `(KU, dimension)` 선수 폐포, 순환 검사, 위상 정렬이다. MVP 그래프는 노드 약 100~150개, Claim 약 100개다.
- **결정**: **메모리 그래프**(Python dict 인덱스 + 표준 라이브러리 `graphlib`)를 쓴다. 그래프 DB는 쓰지 않는다. 관계형 투영이 필요해지면 PostgreSQL(또는 SQLite) **엣지 테이블 + 재귀 CTE**로 간다. Neo4j는 그다음 단계다.
- **대안**: (a) PostgreSQL graph tables(node/edge 테이블, 재귀 CTE, 필요하면 closure table) (b) Neo4j(Cypher, 그래프 알고리즘 라이브러리) (c) SQLite 엣지 테이블.
- **근거**: 질의가 모두 O(V+E) 순회이고 규모가 작다. 그래프 DB를 두면 운영 서비스가 하나 늘고, 백업이 이원화되고, 두 번째 질의 언어를 배워야 한다. 얻는 성능은 측정 가능한 범위에서 0이다. 순환 검사와 위상 정렬은 표준 라이브러리로 된다.
- **트레이드오프**: 임의의 다중 홉 패턴 질의(Cypher 같은 것)를 사용자에게 줄 수 없다. 그래프 분석(중심성 등)은 직접 구현하거나 networkx를 추가해야 한다.
- **재검토 조건**: ① Claim 5만 개 초과 또는 메모리 사용 500MB 초과 ② 사용자가 임의의 다중 홉 질의를 자주 원한다 ③ 대규모 그래프 분석(P2 Large Graph Analytics)이 실제 요구가 된다. ①이면 관계형 엣지 테이블, ②·③이면 Neo4j 또는 PostgreSQL + Apache AGE를 비교한다.

## ADR-003 개인 데이터 DB는 SQLite

- **맥락**: 단일 사용자, 로컬 우선, Docker와 PostgreSQL 미설치(2026-10-15 확인), 쓰기 주체는 백엔드 프로세스 하나다.
- **결정**: SQLite(WAL) + SQLAlchemy 2.x + Alembic(batch 모드). 파일은 WSL ext4 안의 `${AIXON_DATA_DIR}/aixon.db`에 둔다.
- **대안**: PostgreSQL(네이티브 설치 또는 Docker Compose), DuckDB, 브라우저 IndexedDB.
- **근거**: 설치·운영이 필요 없다. 백업은 파일 하나이고, 테스트는 메모리 DB로 빠르고 격리된다. JSON 함수, 부분 인덱스, CHECK 제약, FTS5(trigram)가 MVP 요구를 충족한다. SQLAlchemy를 쓰면 PostgreSQL로 옮길 길이 열려 있다. 브라우저 저장소는 사이트 데이터를 지우면 사라지고 백업이 어렵고 비밀을 둘 곳이 없어서 제외했다.
- **트레이드오프**: 동시 쓰기는 한 번에 하나다. ALTER 제약 때문에 Alembic batch 모드가 필요하다. PostgreSQL 전용 기능(pgvector, 고급 FTS, 행 수준 보안)은 쓸 수 없다. 이식성을 위해 SQLite 전용 SQL은 검색 모듈 안으로 가둔다.
- **재검토 조건**: ① 다중 사용자 호스팅 ② 백엔드 프로세스가 둘 이상 동시에 쓴다(예: 상시 수집 워커) ③ 벡터 검색 도입(ADR-009) ④ DB가 수 GB 이상.

## ADR-004 Modular monolith (프로세스 1개)

- **결정**: Python 패키지 하나(`src/aixon`)를 도메인 모듈로 나누고(06 §3.1), FastAPI 프로세스 하나가 API와 빌드된 SPA를 같은 출처로 서빙한다. CLI는 같은 패키지의 진입점이다.
- **대안**: 그래프 서비스·학습 서비스·수집 서비스로 나눈 microservices, 수집용 별도 워커.
- **근거**: 1인 유지보수, 로컬 실행, 낮은 트래픽. 서비스 사이 계약·배포·관측 비용을 정당화할 부하나 팀 경계가 없다. 모듈 의존 규칙(06 §3.1)만 지켜도 나중에 분리할 수 있다.
- **트레이드오프**: 모듈 경계를 지키는 것은 규율(그리고 import 검사 테스트)에 달려 있다.
- **재검토 조건**: 대량 수집처럼 **독립적으로 확장하거나 오래 도는 작업**이 생겨 웹 프로세스에 부담을 줄 때 그 부분만 워커로 분리한다.

## ADR-005 Deterministic graph engine (LLM planner 아님)

- **결정**: 학습 경로는 04 §4의 결정적 알고리즘으로 만든다. LLM은 경로의 **구조**(어떤 단계, 어떤 순서)에 관여하지 않는다. P2에서 LLM은 이미 정해진 단계 위에 "설명 문장"이나 "자료 요약"만 덧붙일 수 있고, 화면에는 AI 생성 라벨이 붙는다.
- **대안**: LLM이 경로를 생성, LLM이 그래프 경로를 재정렬, 하이브리드.
- **근거**: 재현성(같은 입력 → 같은 출력), 설명 가능성(Claim 사슬), 검증 가능성(golden 테스트). LLM 경로는 선수 관계를 지어낼 수 있고 무엇을 근거로 했는지 추적할 수 없다. 원칙 2(Evidence over Plausibility), 원칙 5(Deterministic Core) 위반이다.
- **트레이드오프**: 그래프에 없는 지식은 경로에 나타나지 않는다(그래프 커버리지에 의존). 그래서 학습자가 "빠진 선수 개념"을 신고하는 피드백 경로(proposal)를 둔다.
- **재검토 조건**: 없음(원칙 수준의 결정). 다만 LLM 보조 기능의 범위는 P2에서 평가한다.

## ADR-006 수동 큐레이션 + 기계 검증 (자동 추출은 proposal로만)

- **결정**: MVP 그래프는 사람(또는 에이전트)이 원문을 근거로 작성한다. 인용문은 **원문 기계 대조**(`seedtool quotes`)로, 구조는 불변식 검증기로 확인한다. CITES처럼 서지 메타데이터에서 기계적으로 나오는 관계만 자동 생성한다(P1). LLM 기반 관계 추출(P2)은 결과를 `proposed`/proposal로만 넣고 자동 승인하지 않는다.
- **대안**: OpenAlex·S2 인용 그래프에서 대량 자동 구축, LLM으로 관계를 대량 추출해 confidence 임계값으로 자동 승인.
- **근거**: 원칙 1(Correctness over Coverage), 7(Small Verified Graph First). 인용은 영향이 아니므로(02 §1 O3) 자동 구축한 그래프는 대부분 CITES뿐이다. 그것은 기존 서비스(Connected Papers 등)가 이미 잘한다(01 문서).
- **트레이드오프**: 그래프가 느리게 자란다. **큐레이션 비용이 제품의 지속 가능성을 좌우한다**(08 문서 리스크 R-P2). 그래서 큐레이션 시간을 성공 지표로 측정한다(00 문서 S6).
- **재검토 조건**: 논문 1편을 큐레이션하는 시간이 계속 30분을 넘거나, 원하는 그래프 확장 속도를 못 따라갈 때 LLM proposal(P2)을 앞당긴다. 이때도 추출기별 precision을 측정한 뒤에 쓴다.

## ADR-007 Lab 계산은 브라우저에서

- **결정**: Lab의 수치 계산은 프런트엔드의 순수 TypeScript 모듈에서 한다. 난수는 seed를 둔 mulberry32를 쓴다. 정확성은 Python(numpy float64)이 만든 golden fixture와 Vitest로 비교한다(05 §5.4). 서버는 Lab 정의를 내려 주고 예측 응답을 채점·저장한다.
- **대안**: 서버에서 numpy로 계산한 결과를 API로 전송, Pyodide로 브라우저에서 Python 실행.
- **근거**: 슬라이더 조작에 즉시 반응해야 한다(네트워크 왕복 없음). 계산량이 작다(벡터 수십~수천 차원). 오프라인에서도 동작한다. Pyodide는 다운로드 크기와 시작 시간이 과하다.
- **트레이드오프**: 수치 코드가 TS와 Python 두 곳에 생긴다(Python은 fixture 생성기 수십 줄뿐). JS `Math` 함수는 언어 사이에 비트 단위로 같다는 보장이 없어서 비교는 허용오차(1e-12)로 한다. 정수 연산인 PRNG는 정확히 같아야 한다(확인함).
- **재검토 조건**: 대형 행렬, 학습된 모델 추론처럼 브라우저에서 무거운 계산이 필요한 Lab이 생길 때 그 Lab만 서버 계산이나 WebGPU를 검토한다.

## ADR-008 웹 스택: Vite React SPA + FastAPI

- **결정**: 프런트엔드는 Vite + React + TypeScript + Tailwind CSS + shadcn/ui. 라우팅은 React Router, 서버 상태는 TanStack Query. 백엔드는 FastAPI + Pydantic v2. 로컬 사용 시 FastAPI가 빌드된 SPA를 정적 파일로 서빙한다.
- **대안**: (a) Next.js + FastAPI(제시된 후보) (b) Next.js 풀스택(TS 하나, Route Handlers + Drizzle + SQLite) (c) 백엔드 없는 정적 SPA + IndexedDB (d) Python만으로(HTMX, Streamlit 등).
- **근거**:
  - SSR·SEO·서버 컴포넌트가 필요 없다(로컬 단일 사용자 앱). Next.js는 렌더링 모델, 캐시 의미론, 별도 Node 서버를 더하지만 얻는 것이 없다.
  - 도메인 핵심(그래프 검증, 계획기, 숙련도 규칙, 수집)은 Python이 맞다. 사용자의 주력 언어이고, 학술 API 클라이언트와 수치 생태계가 있고, 기준 구현(seedtool)이 이미 Python이다.
  - (b)는 언어가 하나라는 장점이 있지만 도메인 코드와 fixture 생성기를 TS로 옮겨야 한다. (c)는 데이터가 쉽게 사라지고 비밀을 둘 곳이 없다. (d)는 인터랙티브 그래프와 Lab에 맞지 않는다.
  - FastAPI의 OpenAPI → `openapi-typescript`로 타입을 하나의 원천에서 만든다.
- **트레이드오프**: 언어 두 개, 빌드 두 개. 개발 중에는 프로세스 두 개(Vite dev server와 API)를 띄운다.
- **재검토 조건**: 공개 웹 서비스로 전환하면서 SEO, 공유 가능한 공개 페이지, SSR이 필요해질 때 Next.js(또는 Astro 같은 정적 생성)를 재검토한다.

## ADR-009 검색: lexical, 벡터 검색 없음

- **결정**: MVP는 메모리 색인(이름·별칭 정확/접두/trigram, 요약 토큰)이다. P1에서 엔티티 수천 개 또는 메모 검색이 필요하면 SQLite FTS5(`tokenize='trigram'`)를 쓴다.
- **대안**: PostgreSQL FTS + pg_trgm, 하이브리드(BM25 + 임베딩), 벡터 DB.
- **근거**: 검색 대상은 이름 붙은 엔티티이고, 사용자는 보통 이름이나 약어로 찾는다("ViT", "ResNet", "softmax"). 임베딩을 쓰면 모델과 갱신 파이프라인과 평가가 필요한데, 이 규모에서 효과를 측정할 방법도 마땅하지 않다.
- **트레이드오프**: "어텐션이 왜 sqrt로 나누지?" 같은 자연어 질의는 찾지 못한다(그것은 LLM 보조나 Concept 페이지 탐색으로 대신한다).
- **재검토 조건**: 엔티티 5천 개 초과 **그리고** 검색 실패 기록(결과 없음 → 사용자가 다른 경로로 찾음)이 반복될 때 하이브리드를 시험한다. 이때 sqlite-vec와 pgvector를 비교하고 ADR-003과 함께 판단한다.

## ADR-010 그래프 시각화: React Flow + ELK.js, 시간축은 직접 배치

- **결정**: 두 그래프 화면 모두 렌더링과 상호작용에 React Flow(`@xyflow/react`)를 쓴다. 선수 DAG의 배치는 ELK.js `layered`(Web Worker)로 한다. Research Graph의 시간축 배치는 연도 → x, 레인 → y로 직접 계산한다(D3 불필요).
- **대안**: Cytoscape.js(Canvas, 내장 레이아웃 다수), D3(자유도 최대, 직접 구현량 최대), Sigma.js + graphology(WebGL, 대규모 그래프), dagre(단순 계층 배치).
- **근거**: 노드를 React 컴포넌트로 그릴 수 있다(검증 배지, 숙련도 링, 차원 칩). 접근성 기능(키보드 포커스, ARIA)과 상호작용이 내장되어 있다. 보이는 노드를 수십~백여 개로 제한하는 설계(U1)라서 DOM 렌더링 성능 한계에 닿지 않는다. ELK layered는 계층형 DAG 배치(층 배정, 교차 최소화)를 제공한다.
- **트레이드오프**: 수천 노드 전체 지도에는 맞지 않는다. ELK.js의 라이선스는 EPL-2.0(또는 GPL-3.0-or-later)이다. 수정하지 않은 패키지를 의존성으로 쓰는 것은 개인 프로젝트에서 문제가 되지 않을 것으로 판단하지만, 공개 배포 시 고지 의무를 확인한다(05 §4.4 조사).
- **재검토 조건**: 한 화면에 500개 이상 노드를 보여야 하는 요구(예: P2 분야 전체 지도)가 생기면 그 화면만 Sigma.js(WebGL) 또는 Cytoscape.js로 구현한다.

## ADR-011 학습자 상태: 차원별 규칙 기반 숙련도

- **결정**: `(unit, dimension)`마다 범주형 상태를 규칙(`mastery-v1`, 04 §3)으로 정한다. 자기보고는 진단 문항을 부르는 신호일 뿐이다. 복습 일정은 P1에서 FSRS 기본 파라미터로 한다.
- **대안**: Bayesian Knowledge Tracing, Item Response Theory, Elo, Deep Knowledge Tracing, 단일 숙련도 점수.
- **근거**: 사용자가 한 명이고 응답 데이터가 거의 없어 통계 모델의 파라미터를 적합할 수 없다. 기본 파라미터를 쓰면 정밀해 보이지만 측정하지 않은 숫자가 된다. 규칙은 설명 가능하고("서로 다른 문항 2개, 점수 3"), 고치기 쉽고, 다시 계산할 수 있다. 비교 분석은 04 §7에 있다.
- **트레이드오프**: 망각, 문항 난이도, 추측과 실수를 정량적으로 모델링하지 않는다.
- **재검토 조건**: 04 §7의 데이터 기준(예: 단위·차원당 응답 수십 개, 문항당 응답 다수)을 충족하고, 규칙 기반 결정이 틀린 사례(숙달로 판정했는데 다음 단계에서 계속 실패)가 기록상 반복될 때 BKT를 오프라인으로 시험한다.

## ADR-012 근거와 신뢰도의 표현

- **결정**: ① Claim 상태(proposed·verified·disputed·rejected·deprecated)와 **사람 검토 기록을 따로** 둔다. ② verified가 되려면 술어별 근거 정책(02 §7.5)을 충족해야 한다. ③ 인용문은 원문 기계 대조로 확인한다. ④ confidence는 **서열 값(high·medium·low)**이고 확률로 표시하지 않는다. ⑤ rejected는 tombstone으로 남긴다.
- **대안**: 숫자 confidence(0~1), 검토자 승인만으로 verified, 상태 없이 근거 개수만 표시.
- **근거**: 보정 데이터 없는 확률은 가짜 정밀도다. 인용 대조는 LLM의 판단이 아니라 재현 가능한 검사다. 에이전트 검증과 사람 검토를 분리하면 "에이전트가 확인했지만 사람은 아직 보지 않았다"는 사실을 숨기지 않을 수 있다.
- **트레이드오프**: 사용자는 "얼마나 믿을지"를 숫자로 볼 수 없다. 대신 근거를 직접 보게 한다(Evidence Inspector).
- **재검토 조건**: 자동 추출(P2)을 도입하면 추출기별 precision을 **별도 필드**로 기록한다(서열 confidence와 섞지 않는다).

## ADR-013 MVP에는 인증이 없다

- **결정**: 서버는 `127.0.0.1`에만 바인딩한다. 사용자 계정·로그인은 없다. 모든 데이터는 `learner_id = me`에 묶인다.
- **근거**: 단일 사용자 로컬 앱이다. 인증을 넣으면 세션·비밀번호·토큰 관리 코드가 생기는데 지킬 위협이 없다(06 §9의 CSRF·Origin 검사는 둔다).
- **재검토 조건**: 다른 기기·LAN·터널로 접근하거나 다중 사용자를 지원할 때. 그 전에 반드시 토큰 인증(최소한 단일 사용자 비밀 토큰)을 넣는다.

## ADR-014 식별자

- **결정**: 내부 ID는 타입 접두 kebab-case slug이고 불변이다(02 §3). Paper는 저작(work) 단위이며 arXiv·학회·저널 버전은 Source로 구분한다. Paper slug의 연도는 **최초 공개 연도**(arXiv v1)다. 외부 ID(DOI, arXiv, OpenAlex[목록], S2, DBLP, OpenReview)는 속성으로 둔다.
- **대안**: UUID, 외부 ID(DOI·OpenAlex)를 내부 키로 사용, 버전마다 Paper.
- **근거**: 사람이 읽고 git diff로 검토할 수 있다. 외부 ID는 없거나(NeurIPS에는 DOI가 없음), 여러 개거나(OpenAlex에 preprint와 proceedings가 따로 있음), 바뀔 수 있다(병합). Evidence가 버전을 가리키므로 절 번호가 버전마다 달라도 안전하다.
- **트레이드오프**: slug 충돌(같은 저자·연도·별칭)은 별칭을 바꿔 사람이 피해야 한다. 기억하기 쉬운 연도(예: ViT를 "2021"로 기억)와 slug 연도가 다를 수 있어서 aliases에 게재 연도 표기를 함께 둔다.
- **재검토 조건**: 큐레이션 그래프를 다른 사람과 공유하거나 병합할 때 전역 고유성을 위해 네임스페이스 접두를 검토한다.

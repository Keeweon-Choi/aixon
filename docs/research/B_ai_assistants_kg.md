# B. AI 연구 어시스턴트·구조화 학술지식 제품 경쟁 분석 (AIXON 설계 문서용)

- 조사 기준일은 2026-10-15입니다. 본문의 모든 출처는 "확인 2026-10-15"이며, 각 절 끝 출처 목록에 다시 적었습니다.
- 지정 대상 7종: Elicit, SciSpace, Consensus, scite.ai, ORKG(+ORKG Ask), Papers with Code, alphaXiv.
  - Papers with Code는 종료 여부와 후속 서비스를 함께 다룹니다. 후속은 Hugging Face Papers / Trending Papers와 paperswithcode.co 재개판입니다.
- 추가 1종: **Ai2 Asta**.
  - 추가한 이유: 답변의 주장마다 인용과 원문 발췌를 붙이는 문헌 요약 에이전트입니다. 핵심 코드가 Apache-2.0으로 공개돼 있어 AIXON의 기준 (8)·(10)과 직접 겹칩니다.
  - Semantic Scholar 본체는 A 문서(`A_literature_tools.md`) 1절에서 이미 다뤘으므로 여기서 반복하지 않습니다.
- 표기
  - **[2차]**: 뉴스·블로그·커뮤니티 같은 비공식 출처입니다.
  - **(추론)**: 내 판단입니다.
  - **(직접 확인)**: 2026-10-15에 curl이나 공개 API로 응답을 직접 받아 본 결과입니다.
  - **(직접 분석)**: 공개 데이터 파일을 내려받아 집계한 결과입니다. 방법을 함께 적었습니다.
  - **†**: 종료된 서비스의 과거 기능 기준 판정입니다. 현재는 해당 기능이 라이브로 제공되지 않습니다(6절).

### 판정 규칙 (A 문서와 같은 기준표)

두 문서의 표를 합칠 수 있도록 A 문서의 기준표를 그대로 씁니다.

| 기준 | 지원 | 부분 지원 |
|---|---|---|
| (1) Literature Discovery | 검색 또는 시드 기반 추천 제공 | — |
| (2) Citation & Relationship Visualization | 논문 간 관계를 그래프·맵으로 표시 | 목록·라벨만 제공하거나, 인용이 아닌 주제 유사도 맵 |
| (3) Research Evolution over time | 시간축 시각화 | 이전/이후 연구 탐색, 연도 색상, 시간 지표, 선행/후속 배너 등 |
| (4) Concept Knowledge Graph | 개념 엔티티와 개념 간 관계 | 주제 페이지·분류 체계·개념 라벨만 있음 |
| (5) Explicit Prerequisite Graph | "A를 알아야 B"를 나타내는 명시적 간선 | — |
| (6) Personalized Learning Paths | 학습자 상태에 따른 학습 순서 계획 | — |
| (7) Persistent Learner State | 지식·숙달 모델 | 계정에 영속 저장되는 연구 활동 상태(서재·평가·노트·알림)만 있음 |
| (8) Evidence & Provenance | 관계별 근거(인용 문장, 의도·성격 라벨) 제시 | 관계 산출 방식 공개 또는 관계 방향·점수만 표시, 개별 근거 텍스트 없음 |
| (9) Interactive Learning | 실습·연습·피드백 루프 | 읽기 보조형 인터랙션(용어 정의, 논문 Q&A)만 있음 |
| (10) API / OSS / Data reuse | 문서화된 API(유료 포함), 명시적 라이선스의 bulk 데이터, 또는 핵심 코드의 OSI 라이선스 공개 | early-access API, 클라이언트·MCP·내보내기만 공개 |

AI 어시스턴트에 적용할 때의 보충 해석입니다. 규칙 자체는 같습니다.
- (8) "지원": 답변 문장이나 추출 값마다 원문 인용문·스니펫·페이지 앵커를 보여 줍니다.
- (8) "부분 지원": 출처 논문, 작성자, 생성 방식(사람/AI)은 밝히지만 값별 근거 텍스트가 없습니다.
- (3) 일·주·월 트렌딩 같은 인기도 시간창과 인용 속도는 규칙상 "시간 지표"이므로 부분 지원입니다. 연구 흐름 자체를 시각화하는 기능은 아니라고 셀에 적었습니다.
- 공식 문서가 명시적으로 부정한 기능은 이번 조사에서 없었습니다. 그래서 "미지원(공식 근거 있음)" 셀은 없습니다. 종료된 Papers with Code는 † 표기로 구분했습니다.

---

## 0. 요약 표

| 제품 | (1) Literature Discovery | (2) Citation & Relationship Visualization | (3) Research Evolution | (4) Concept KG | (5) Prerequisite Graph | (6) Personalized Paths | (7) Persistent Learner State | (8) Evidence & Provenance | (9) Interactive Learning | (10) API/OSS/Data Reuse |
|---|---|---|---|---|---|---|---|---|---|---|
| Elicit | **지원** | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | **지원**(유료) |
| SciSpace | **지원** | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | 확인되지 않음 |
| Consensus | **지원** | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | 부분 지원 |
| scite.ai | **지원** | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | **지원**(유료) |
| ORKG (+ORKG Ask) | **지원** | 부분 지원 | 확인되지 않음 | **지원** | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | **지원** |
| Papers with Code (구 사이트, 2025-07 종료) † | **지원**† | 부분 지원† | **지원**† | **지원**† | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원† | 확인되지 않음 | **지원**(아카이브 데이터, 현재 유효) |
| Hugging Face Papers / Trending Papers | **지원** | 부분 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 확인되지 않음 | **지원** |
| paperswithcode.co (2026 재개판) | **지원** | 부분 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 확인되지 않음 |
| alphaXiv | **지원** | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | 부분 지원 |
| Ai2 Asta (추가) | **지원** | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | **지원** | 부분 지원 | **지원** |

이 표에서 바로 보이는 점:
- (5) Prerequisite Graph와 (6) Personalized Paths는 10개 행 모두 "확인되지 않음"입니다.
- (7)은 "부분 지원"이 최고 판정입니다. 서재·노트·읽기 상태 같은 활동 상태만 있고, 지식·숙달 모델은 확인되지 않았습니다.
- (9)도 "부분 지원"이 최고입니다. 논문 Q&A와 수식·용어 설명까지만 있고, 실습·연습·피드백 루프는 확인되지 않았습니다.
- 반대로 (8) 문장 단위 근거 제시는 6개 제품이 이미 "지원"입니다. AIXON의 차별점이 될 수 없습니다(11장).

### 0.1 운영 주체·상태·요금 요약

| 제품 | 운영 주체 | 상태 (2026-10-15) | 개인 무료 | 개인 유료 |
|---|---|---|---|---|
| Elicit | Elicit. Ought(비영리)에서 분사한 public benefit corporation(2023-09-25 발표) | 운영 중. 2026-09-30에 Find Papers / Extract Data / Chat with Papers를 Research Agent로 통합 | Basic: 138M+ 논문 무제한 검색, 요약·논문 채팅 무제한, Research Agent·Reports 제한 사용 | Pro US$49/인/월(연 $588 결제), Scale US$169/인/월(연 $2,028 결제), Enterprise 별도. API는 Pro 이상 |
| SciSpace | PubGenius Inc. (미국 캘리포니아 Milpitas) | 운영 중 | Basic: 월 100 크레딧 | Premium 1,200 크레딧 US$12/월(연간)·$20(월간), Advanced $70/$90, Max $160/$200(Advanced·Max는 fair-usage 무제한) |
| Consensus | Consensus (법인명은 확인되지 않음) | 운영 중 | Free: 월 Pro messages 10회, Deep Search 3회 | Pro / Deep / Team / Enterprise. 달러 금액은 동적 렌더링이라 확인되지 않음. 학생 12개월 40% 할인 |
| scite.ai | Scite LLC, "Part of the Research Solutions Family" | 운영 중 | 신규 개인 7일 체험. 무료 계정의 기능 범위는 확인되지 않음 | Basic $20/월 또는 $144/년, Pro $50/월 또는 $480/년(API 포함), Team $50/석/월, Enterprise 별도 |
| ORKG (+Ask) | TIB Hannover GitLab에서 개발. 파트너 로고는 TIB, Leibniz Universität Hannover, L3S, InfAI. EU Horizon 2020 공동 지원 | 운영 중(About v0.192.0) | 열람, REST, SPARQL, RDF 덤프 모두 무료 | 유료 플랜은 확인되지 않음 |
| Papers with Code (구) | 과거 핵심 팀은 Meta AI Research 소속 | **종료**. 2025-07-24 종료 보도 [2차]. 현재 모든 경로가 huggingface.co/papers/trending으로 302 (직접 확인) | 아카이브 데이터 무료(CC BY-SA 4.0) | — |
| HF Papers / Trending | Hugging Face | 운영 중 | 무료 열람. 업보트는 로그인 필요 | Papers 전용 유료 기능은 확인되지 않음 |
| paperswithcode.co | Hugging Face 오픈소스 팀 Niels Rogge 주도(HF 블로그 Community Article 기준) | 2026-05 공개, 운영 중. 별칭 도메인 paperswithco.de | 웹 접근 | 확인되지 않음 |
| alphaXiv | alphaXiv Inc. (약관 2026-04-17 개정) | 운영 중. arXiv 초록 페이지에 arXivLabs 토글로 연동 | 웹 열람·토론. Assistant와 MCP 검색·분석 도구는 쿼터 차감 | 약관에 "alphaXiv Pro" 등 유료 상품 가능성 명시. 금액은 확인되지 않음 |
| Ai2 Asta | Allen Institute for AI (Ai2) | 2025-08-26 발표. 운영 중(사이트 응답, GitHub 저장소 2026-10 갱신 확인) | 확인되지 않음 | 확인되지 않음 |

---

## 1. Elicit

**한 줄 설명**: 논문 검색, 스크리닝, 구조화 추출, 자동 리서치 리포트, 체계적 문헌고찰을 LLM으로 자동화하는 연구 어시스턴트입니다. 2026-09 이후 중심 인터페이스는 Research Agent입니다.

**운영 주체와 상태**
- "Elicit was born at Ought, a non-profit research organization, and is now an independent public benefit corporation."(2023-09-25 공식 블로그)
- 2026-09-30 변경: "Find Papers, Extract Data, and Chat with Papers were removed as separate tools and incorporated into the Research Agent workflow."
  - 기존 세션은 view-only로 남고, 2027년 중 정해질 날짜에 삭제됩니다.
  - Find Papers와 Extract Data는 Research Agent의 "skill"이 됐습니다.

**무료와 유료**
- Basic(무료) 항목: "Unlimited search across more than 138 million papers", "Unlimited summaries across as many papers as you want", "Unlimited chat with papers with full-text access", "View sources for answers", "Limited usage for Research Agent and Research Reports".
- Pro: "$49 … Per user/month, billed as $588 annually".
  - 표에 한 번에 20개 열 추가, 리포트당 최대 135개 출처, 5,000편까지 스크리닝하는 체계적 문헌고찰 워크플로, API를 포함합니다.
- Scale: "$169 … Per user/month, billed as $2,028 annually".
  - 30개 열, 그림에서 추출, 최대 200개 출처, 5배 사용량을 포함합니다.
- Enterprise: 별도 견적입니다.
- 월간 결제 금액은 요금 페이지에 표시되지 않아 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "Elicit searches across over 138 million academic papers from Semantic Scholar, PubMed, and OpenAlex … The corpus is updated weekly." 검색은 임베딩 검색 → 트랜스포머 관련도 순위화 → 상위 500편 → 포함·제외 기준 스크리닝의 4단계입니다. | [source-for-papers](https://support.elicit.com/en/articles/14758040-elicit-s-source-for-papers), [search methodology](https://support.elicit.com/en/articles/14757952-citing-elicit-search-methodology-and-using-elicit-s-content-in-your-own-work) |
| 2 | Citation & Relationship Visualization | 확인되지 않음 | Research Agent 산출물은 표, 그림, 슬라이드, 요약입니다. 인용 그래프나 관계 시각화는 공식 문서에서 확인되지 않았습니다. | [research-agent](https://support.elicit.com/en/articles/14756886-elicit-s-research-agent) |
| 3 | Research Evolution | 확인되지 않음 | — | — |
| 4 | Concept Knowledge Graph | 확인되지 않음 | — | — |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | Library와 공유 collection, Projects(연결 collection 우선 사용), Session History가 영속됩니다. 지식·숙달 모델은 확인되지 않았습니다. | [research-agent](https://support.elicit.com/en/articles/14756886-elicit-s-research-agent), [getting-started 목록](https://support.elicit.com/en/collections/19561689-getting-started) |
| 8 | Evidence & Provenance | **지원** | 리포트에서 "Click within the report to review supporting quotes and reasoning." 스크리닝 기준과 추출 지시를 단계별로 되짚어 볼 수 있습니다. Research Agent는 "separates those sources from ones it found through a broader search."(서재 출처와 외부 검색 출처 구분) | [research-report](https://support.elicit.com/en/articles/14756862-get-a-research-report-to-generate-in-depth-answers-automatically-in-elicit), [research-agent](https://support.elicit.com/en/articles/14756886-elicit-s-research-agent) |
| 9 | Interactive Learning | 부분 지원 | 무료 플랜에 "Unlimited chat with papers with full-text access"가 있습니다. 2026-09-30 이후에는 Research Agent 세션에서 논문을 올리거나 골라 질문합니다. 연습·피드백 같은 학습 기능은 확인되지 않았습니다. | [pricing](https://elicit.com/pricing), [tools 통합 안내](https://support.elicit.com/en/articles/17220397-where-did-find-papers-extract-data-and-chat-with-papers-go) |
| 10 | API / OSS / Data reuse | **지원**(유료) | API v2(OpenAPI 3.1) 엔드포인트: `/search/papers`, `/search/trials`, `/sessions/reports`, `/sessions/systematic-reviews`, `/sessions/agents`, library, projects, routines, usage. "API access requires a Pro plan or above." "burst limit of 100 requests per minute per IP address". MCP 서버도 있습니다. bulk 데이터와 OSS는 확인되지 않았습니다. | [docs.elicit.com](https://docs.elicit.com/), [API 안내](https://support.elicit.com/en/articles/14757400-elicit-s-api) |

### 지정 검증: LLM 추출·요약, 근거 연결, 환각 대응, 학습 기능
- **추출·요약**
  - 리포트를 만들 때 Elicit가 스크리닝 기준과 추출할 데이터 항목을 스스로 정합니다.
  - Pro 이상에서는 이전 단계 전부(스크리닝 기준, 포함·제외, 추출 열과 지시)를 편집해 다시 만들 수 있고, 이전 버전이 남습니다.
  - 각 단계 결과 표를 CSV로 내보낼 수 있습니다.
- **본문 접근 한계**: "If Elicit does not have access to the PDF for the paper, Elicit can only pull information from the abstract." 보통 오픈액세스 논문에 접근합니다. 브라우저 확장, PDF 업로드, Zotero로 전문을 보충합니다.
- **환각 대응(공식 설명)**
  - "We ensure that the info we use is extracted directly from papers … We then highlight the source of the content within the relevant papers."
  - 기법: "process supervision, prompt engineering, ensembling multiple models, double-checking our results with custom models and internal evaluations".
- **한계(공식 자인)**
  - "try hard to err on the side of Elicit saying nothing rather than saying something wrong", 그래도 "can miss the nuance of a paper or misunderstand what a number refers to".
  - "Elicit summarizes the findings of a bad study just like it summarizes the findings of a good study."
  - 실증 연구(RCT 등) 위주로 최적화돼 있습니다.
- **정확도 주장**: "In our testing, Elicit is often more accurate than humans."는 벤더 주장입니다. 독립 검증은 이번 조사에서 확인하지 않았습니다.
- **학습·튜터링 기능**: 확인되지 않았습니다.

### 이미 잘 해결한 것 (AIXON이 차별점으로 주장하면 안 됨)
- 연구 질문에서 시작하는 자동 검색, 스크리닝, 추출, 리포트 파이프라인과 단계별 재현·편집.
- 추출 값과 리포트 문장에 붙는 원문 인용(supporting quotes).
- 서재 출처와 외부 출처의 구분 표시.
- 반복 실행(Routines)과 API·MCP 연동.

### AIXON 목표 대비 공백
- 개념 그래프, 선수지식, 학습 경로, 학습자 모델, 실습이 확인되지 않았습니다.
- 연구 흐름 시각화와 인용 관계 시각화가 확인되지 않았습니다.
- 클라우드 SaaS이고, API가 유료(Pro 이상)입니다. 로컬 우선 설계와는 결이 다릅니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://elicit.com/pricing — 확인 2026-10-15
- https://elicit.com/blog/elicit-raises-9-million-and-becomes-a-public-benefit-corporation — 확인 2026-10-15
- https://support.elicit.com/en/articles/14758040-elicit-s-source-for-papers — 확인 2026-10-15
- https://support.elicit.com/en/articles/14757952-citing-elicit-search-methodology-and-using-elicit-s-content-in-your-own-work — 확인 2026-10-15
- https://support.elicit.com/en/articles/14757979-elicit-s-reliability-does-elicit-run-the-same-risk-of-hallucination-as-other-ai-tools — 확인 2026-10-15
- https://support.elicit.com/en/articles/14757928-elicit-s-limitations — 확인 2026-10-15
- https://support.elicit.com/en/articles/14756862-get-a-research-report-to-generate-in-depth-answers-automatically-in-elicit — 확인 2026-10-15
- https://support.elicit.com/en/articles/14756886-elicit-s-research-agent — 확인 2026-10-15
- https://support.elicit.com/en/articles/17220397-where-did-find-papers-extract-data-and-chat-with-papers-go — 확인 2026-10-15
- https://support.elicit.com/en/articles/14758163-improve-column-results — 확인 2026-10-15
- https://support.elicit.com/en/articles/14758226-evaluating-elicit — 확인 2026-10-15
- https://support.elicit.com/en/articles/14757400-elicit-s-api — 확인 2026-10-15
- https://support.elicit.com/en/collections/19561689-getting-started — 확인 2026-10-15
- https://docs.elicit.com/ , https://docs.elicit.com/llms.txt — 확인 2026-10-15

---

## 2. SciSpace

**한 줄 설명**: PDF 읽기 코파일럿(Chat with PDF), 문헌 검색·리뷰, 다중 PDF 데이터 추출, 글쓰기 도구, SciSpace Agent를 묶은 연구 워크스페이스입니다.

**운영 주체와 상태**
- 사이트 하단 표기: "© 2026 | PubGenius Inc. | … Milpitas CA 95035, USA". 운영 중입니다.
- 내비게이션에 SciSpace Agent, Biomedical Agent, Chat with PDF, Literature Review, AI Writer, Find Topics, Extract Data, AI Detector, AI Humanizer가 있습니다.

**무료와 유료** (공식 크레딧 가이드)

| 플랜 | 월 크레딧 | 가격 | 동시 작업 |
|---|---|---|---|
| Basic | 100 | $0 | 4 |
| Premium | 1,200 | $12/월(연간 결제) / $20/월(월간 결제) | 4 |
| Advanced | "Unlimited monthly credits with fair usage limits" | $70/월(연간) / $90/월(월간) | 8 |
| Max | 같은 표현 | $160/월(연간) / $200/월(월간) | 16 |

- llms.txt의 무료 설명은 "Limited access to tools, 2 chats/day, basic citation generator"로, 크레딧 가이드와 표현이 다릅니다. 작성 시점 차이로 보입니다(추론).
- 크레딧은 이월되지 않습니다. 긴 작업 중 크레딧이 떨어지면 작업이 멈추고 업그레이드를 요청합니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "Run an AI-powered literature search over 280M+ papers." | [llms.txt](https://scispace.com/llms.txt) |
| 2 | Citation & Relationship Visualization | 확인되지 않음 | 관계 그래프 기능은 공식 문서에서 확인되지 않았습니다. 자사 비교 글은 시각 그래프 용도로 Connected Papers를 권합니다: "Connected Papers can provide a cleanest visual graph." | [SciSpace vs Connected Papers](https://scispace.com/resources/connected-papers-or-scispace/) |
| 3 | Research Evolution | 확인되지 않음 | — | — |
| 4 | Concept Knowledge Graph | 부분 지원 | Find Topics가 "Definition & Overview", "Related Concepts – Other academic terms and ideas linked to your search", "Relevant Research Papers", "Common Applications"를 생성합니다. 영속적인 개념 그래프와 관계 유형은 확인되지 않았습니다. | [Find Topics 도움말](https://scispace.com/help/en/articles/10680624-find-topics-on-scispace-exploring-research-concepts-with-ai), [llms.txt](https://scispace.com/llms.txt) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | "Related Concepts"가 선수 관계라는 설명은 없습니다. | [Find Topics 도움말](https://scispace.com/help/en/articles/10680624-find-topics-on-scispace-exploring-research-concepts-with-ai) |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | Chat with PDF 기능 목록에 "Note taking"이 있습니다. 지식 모델은 확인되지 않았습니다. | [chat-pdf](https://scispace.com/chat-pdf) |
| 8 | Evidence & Provenance | **지원**(벤더 설명 기준) | "Get AI-generated, citation-linked answers with references to specific paragraphs and sections." 환각 처리 방식을 공식으로 설명한 문서는 확인되지 않았습니다. | [llms.txt](https://scispace.com/llms.txt) |
| 9 | Interactive Learning | 부분 지원 | "Explanations for maths, equations, tables and figures", "Text selection for Summarization", "Sectionwise PDF Summary", "Multilingual Support". 연습문제·퀴즈·피드백은 확인되지 않았습니다. | [chat-pdf](https://scispace.com/chat-pdf) |
| 10 | API / OSS / Data reuse | 확인되지 않음 | llms.txt와 요금 가이드에 공개 API, MCP, 데이터 라이선스 언급이 없습니다. | [llms.txt](https://scispace.com/llms.txt), [credits guide](https://scispace.com/guides/credits-pricing-guide) |

### 지정 검증: LLM 추출·요약, 근거 연결, 환각 대응, 학습 기능
- **추출·요약**
  - Extract Data: "Upload multiple PDFs and extract findings, tables, and data points across them".
  - Advanced 플랜: "Deep Literature Review (RAG), AI Gaps Finder, and PDF to Video".
- **근거 연결**: 단락·섹션을 가리키는 인용 링크입니다(위 (8)).
- **환각 대응**: 공식 도움말 문서는 확인되지 않았습니다. 자사 블로그 글은 마케팅 성격이라 판정 근거로 쓰지 않았습니다.
- **학습 기능**
  - 수식·방정식·표·그림 설명과 선택 텍스트 요약이 핵심입니다. 이용자 후기(공식 페이지 게재)도 "simplify and explain any text you highlight"를 강조합니다.
  - 개념 수준 보조는 Find Topics의 정의·관련 개념입니다.
  - 학습자 상태 추적과 연습 기능은 확인되지 않았습니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- PDF 안에서 하이라이트한 문장·수식·표·그림을 설명하는 기능.
- 단락·섹션 단위 인용이 붙은 PDF 질의응답.
- 다중 PDF 비교 추출.
- 주제 정의, 관련 개념, 대표 논문을 한 번에 보여 주는 개념 탐색(Find Topics).

### AIXON 목표 대비 공백
- 개념 간 관계 유형과 선수관계, 학습 경로, 학습자 모델, 실습형 랩이 확인되지 않았습니다.
- 공개 API와 데이터 재사용 경로가 확인되지 않았습니다.
- 관계·연구 흐름 시각화는 자사 문서조차 다른 도구를 권합니다.

### 출처 (모두 확인 2026-10-15)
- https://scispace.com/llms.txt — 확인 2026-10-15
- https://scispace.com/guides/credits-pricing-guide — 확인 2026-10-15
- https://scispace.com/pricing (하단 법인 표기. 플랜 금액은 JS 렌더링이라 크레딧 가이드로 확인) — 확인 2026-10-15
- https://scispace.com/chat-pdf — 확인 2026-10-15
- https://scispace.com/help/en/articles/10680624-find-topics-on-scispace-exploring-research-concepts-with-ai — 확인 2026-10-15
- https://scispace.com/resources/connected-papers-or-scispace/ — 확인 2026-10-15

---

## 3. Consensus

**한 줄 설명**: 동료심사 논문만으로 연구 질문에 답하는 AI 학술 검색엔진입니다. 답변 문장마다 논문 인용을 달고, 예/아니오형 질문에는 논문별 판정 분포인 Consensus Meter를 보여 줍니다.

**운영 주체와 상태**: consensus.app이며 운영 중입니다. 법인명은 확인되지 않았습니다(약관 페이지가 JS 렌더링).

**무료와 유료** (기계 판독용 공식 요금 파일)
- Free $0: "10 Pro messages per month", "3 Deep Searches per month".
- Pro: "Unlimited Pro messages per month", "15 Deep Searches per month". "Student discount: 40% off for 12 months".
- Deep: Deep Search 월 200회.
- Team: 석당 Deep Search 월 50회. "Optional access to the Consensus Search API (available upon approval, rate limited …)".
- Enterprise: 별도 계약입니다.
- 달러 금액: 공식 파일이 "intentionally omits hard coded dollar amounts for paid tiers"라고 밝힙니다. 사람용 요금 페이지도 정적으로 렌더링되지 않아 **유료 금액은 확인되지 않았습니다**.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "We index over 400 million peer-reviewed papers from Semantic Scholar, OpenAlex, PubMed, and publisher feeds". 벡터와 lexical을 섞은 하이브리드 검색입니다. 연구 유형, 연도, 저널, OA, 분야 필터가 있습니다. | [llms.txt](https://consensus.app/llms.txt), [llms-full.txt](https://consensus.app/llms-full.txt) |
| 2 | Citation & Relationship Visualization | 부분 지원 | Pro 기능 목록에 "Unlimited access to every research tool (search, analysis, citation graph, and more)"가 있고, 기능 페이지 `features/citation-graph`가 있습니다. 페이지가 JS 렌더링이라 표시 형태(그래프 여부)는 확인되지 않았습니다. | [pricing.md](https://consensus.app/.well-known/pricing.md), [citation-graph](https://consensus.app/home/features/citation-graph/) |
| 3 | Research Evolution | 부분 지원 | 논문별 "Citation counts and citation velocity"를 보여 줍니다(시간 지표 수준). 연구 흐름 시각화는 확인되지 않았습니다. | [llms-full.txt](https://consensus.app/llms-full.txt) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | 연구 설계 분류와 PICO 추출은 있지만 개념 엔티티·관계는 확인되지 않았습니다. | [llms-full.txt](https://consensus.app/llms-full.txt) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | 웹앱에 "account management, citation export, and library tooling"이 있습니다. | [llms-full.txt](https://consensus.app/llms-full.txt) |
| 8 | Evidence & Provenance | **지원** | "a synthesis across the top results, with every sentence linked back to the supporting paper(s)". Meter는 논문마다 supporting / refuting / mixed를 분류하고, 사용자가 해당 논문을 열어 분류를 확인할 수 있습니다. | [llms-full.txt](https://consensus.app/llms-full.txt) |
| 9 | Interactive Learning | 부분 지원 | Pro messages("dynamic AI powered search and analysis")로 문헌 Q&A를 합니다. 학습 기능은 확인되지 않았습니다. | [pricing.md](https://consensus.app/.well-known/pricing.md) |
| 10 | API / OSS / Data reuse | 부분 지원 | REST API가 검색, 논문 상세, 합성, Meter를 bearer token으로 제공합니다. 다만 Team은 "available upon approval", Enterprise는 맞춤 계약입니다. MCP 서버(OAuth 2.1)가 있습니다. bulk 데이터와 OSS는 확인되지 않았습니다. | [llms-full.txt](https://consensus.app/llms-full.txt), [pricing.md](https://consensus.app/.well-known/pricing.md), [API](https://consensus.app/home/api/) |

### 지정 검증: LLM 추출·요약, 근거 연결, 환각 대응, 학습 기능
- **논문별 AI 요약**: 한 문장 요약, 방법·표본·결과·한계 구조화 요약, PICO 추출(해당 시), "A confidence indicator based on study design and reproducibility signals".
- **품질 신호와 순위**
  - 연구 설계 분류(RCT, cohort, in vitro 등), 표본 크기, 자금·이해상충(가능 시), 인용 수와 인용 속도.
  - 순위 기준: "study design (RCT > systematic review > observational), citation count, journal quality (SJR), and recency".
- **근거 연결**: 합성 답변의 모든 문장이 논문에 연결되고, DOI·저널·연도·저자를 제공합니다.
- **환각 대응(공식 자인)**
  - "AI summaries are summaries. They are designed to be faithful to the source paper, but they are still LLM outputs."
  - "The Consensus Meter is a heuristic. It is not a formal meta-analysis".
- **공식 문서 간 불일치(주의)**
  - llms.txt: "Preprints are included by default and tagged in results".
  - llms-full.txt: "The default index excludes preprints".
- **학습·튜터링 기능**: 확인되지 않았습니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- 예/아니오형 연구 질문의 증거 분포 집계(Consensus Meter).
- 연구 설계에 따른 근거 품질 순위화.
- 문장 단위 인용이 달린 합성 답변.
- 인용 그래프 도구와 MCP·REST 연동.

### AIXON 목표 대비 공백
- 개념 그래프, 선수지식, 학습 경로, 학습자 모델, 실습이 확인되지 않았습니다.
- 의생명·실증 연구 질문형에 최적화돼 있습니다. "method A가 어떻게 B로 발전했나" 같은 AI 분야 계보 질문의 구조화 지원은 확인되지 않았습니다.

### 출처 (모두 확인 2026-10-15)
- https://consensus.app/llms.txt — 확인 2026-10-15
- https://consensus.app/llms-full.txt — 확인 2026-10-15
- https://consensus.app/.well-known/pricing.md — 확인 2026-10-15
- https://consensus.app/pricing/ (금액 미렌더링 확인) — 확인 2026-10-15
- https://consensus.app/home/api/ — 확인 2026-10-15
- https://consensus.app/home/features/citation-graph/ (JS 렌더링, 본문 미확인) — 확인 2026-10-15

---

## 4. scite.ai

**한 줄 설명**: 전문(full text)에서 인용 문장(citation statement)을 추출하고, 그 인용이 피인용 논문을 지지(supporting)·반박(contrasting)·언급(mentioning)하는지 분류해 보여 주는 "Smart Citations" 플랫폼입니다. 그 위에 Assistant, Search, Collections, Reference Check, API, MCP를 얹었습니다.

**운영 주체와 상태**: "Copyright © 2026 Scite LLC", "Part of the Research Solutions Family"이며 운영 중입니다. 도움말 센터는 help.researchsolutions.com으로 옮겨졌습니다(llms.txt 링크 기준). 옛 help.scite.ai는 2026-10-15 TLS 오류로 접속되지 않았습니다(직접 확인).

**무료와 유료** (pricing.md, "Last updated: October 5, 2026")

| 플랜 | 월간 결제 | 연간 결제 | MCP 크레딧 | API |
|---|---|---|---|---|
| Basic | $20/월 | $144/년($12/월) | 250/월 | 미포함 |
| Pro | $50/월 | $480/년($40/월) | 2,500/월 | 포함 |
| Team | $50/석/월 | $480/석/년 | 2,500/월/인 | 인당 포함 |
| Enterprise | 맞춤 | 맞춤 | pooled | 포함 |

- 체험: "New individual subscribers may be eligible for a seven-day free trial."
- 무료 계정: "Free Scite accounts and unauthenticated requests do not include MCP access." 무료 계정이 존재한다는 뜻이지만, 무료로 볼 수 있는 범위는 확인되지 않았습니다.
- 학생·학계 할인: 소속 기관에 scite를 추천하는 메일을 지원팀에 보내면 할인 코드를 줍니다.
- A 문서의 "$12/월(연간)", "$40/월(연간)"과 같은 값입니다. 이 문서는 월간 결제가와 Team 플랜을 추가로 확인했습니다.

### 10개 기준 판정 (A 문서와 같은 판정)

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "Search publication metadata and citation statements from full text to find relevant papers, findings, methods, and claims." | [llms.txt](https://scite.ai/llms.txt) |
| 2 | Citation & Relationship Visualization | 부분 지원 | Smart Citation 리포트가 인용 문맥과 3분류 집계를 목록·리포트로 보여 줍니다. 네트워크 그래프는 현행 공식 문서에서 확인되지 않았습니다. | [llms.txt](https://scite.ai/llms.txt) |
| 3 | Research Evolution | 확인되지 않음 | — | — |
| 4 | Concept Knowledge Graph | 확인되지 않음 | — | — |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | Collections: "Organize papers, monitor new citations, track supporting or contrasting evidence, and receive alerts about retractions and editorial notices." 플랜별 collection 상한은 1,000편, 10,000편, 50,000편입니다. | [llms.txt](https://scite.ai/llms.txt), [pricing.md](https://scite.ai/pricing.md) |
| 8 | Evidence & Provenance | **지원** | 인용별로 "the text surrounding a citation"과 분류를 보여 줍니다. Assistant: "Every claim Scite's AI makes links back to the specific sentence in the specific paper it came from."(벤더 주장) Reference Check는 원고 참고문헌의 철회, 편집 공지, 반박 증거를 점검합니다. 독립 평가는 분류 정확도가 낮다고 보고했습니다(아래). | [llms.txt](https://scite.ai/llms.txt), [홈](https://scite.ai/), [Bakker et al. 2023](https://journals.indianapolis.iu.edu/index.php/hypothesis/article/view/26528) |
| 9 | Interactive Learning | 부분 지원 | Scite Assistant: "Ask research questions and receive answers grounded in scholarly literature, with citations linked to their sources."(문헌 Q&A) | [llms.txt](https://scite.ai/llms.txt) |
| 10 | API / OSS / Data reuse | **지원**(유료) | API가 메타데이터, 검색, Smart Citation 집계·문장, collections, reference checking, Assistant, 연구 지표, evidence 데이터셋을 제공합니다. Pro 이상이며, bulk 데이터와 맞춤 라이선스는 영업 문의입니다. 원격 MCP는 `https://api.scite.ai/mcp`입니다. | [llms.txt](https://scite.ai/llms.txt), [pricing.md](https://scite.ai/pricing.md) |

### 지정 검증

**(a) Smart Citations의 세 분류**
- 현행 공식 정의: "classify the citation as supporting, contrasting, or mentioning, so researchers can understand how later work has evaluated a publication rather than relying on a citation count alone."
- 2021 논문은 반박 범주를 "disputing"이라 불렀습니다. 현행 "contrasting"과 같은 범주로 보입니다(추론).

**(b) 분류 생성 방식** (Nicholson et al., bioRxiv 2021 전문 기준. QSS 2(3) 게재본도 있음 [검색 결과 기준])
- 전문 수집
  - 오픈액세스: PubMed Central, Unpaywall이 찾은 OA 출처.
  - 구독 논문: 출판사 색인 협약(Wiley, BMJ, Karger, Sage, Europe PMC, Thieme, Cambridge UP 등).
- 처리 파이프라인
  - PDF는 GROBID로 변환하고, XML은 Pub2TEI로 표준화합니다.
  - 참고문헌은 biblio-glutton으로 Crossref에 매칭합니다.
  - 인용 문맥이 올바른 DOI에 연결되는 비율은 PDF 약 70%, PMC JATS XML 약 95%입니다.
- 분류 모델
  - 운영 모델은 fine-tuned SciBERT입니다. BiGRU, ELMo 앙상블, BERT를 거쳤습니다.
  - 학습·평가 데이터는 약 5만 건입니다(작업셋 38,925건, holdout 9,708건).
  - 최대 8명의 전문가 주석자가 건마다 최소 2인 블라인드로 주석하고 조정했습니다.
- 클래스 분포 추정: mentioning 약 92.6%, supporting 6.5%, disputing 0.8%. 반박 범주가 매우 희소합니다.
- 성능: disputing F-score가 초기 약 20%에서 58.97%로 올랐습니다. disputing precision은 85.19%입니다.
- 논문이 밝힌 한계
  - 세 범주는 뉘앙스를 놓칩니다.
  - disputing은 새 증거를 제시하는 경우로 한정돼, 개념적·논리적 비판은 빠집니다.
  - 당시 규모는 약 2,300만 편 전문에서 8억 건 이상의 분류된 인용 문장이었습니다.
- 출처: [bioRxiv 전문](https://www.biorxiv.org/content/10.1101/2021.03.15.435418v1.full), [DOAJ 서지](https://doaj.org/article/81fa50fb3c294f6ba01cc597d41a974e)

**(c) 독립 평가**
- Bakker, Theis-Mahon, Brown(2023, *Hypothesis*): 철회 논문을 인용한 체계적 문헌고찰의 인용 324건 중 scite에서 분류 가능한 것은 98건이었습니다.
  - supporting: scite는 2건, 사람은 42건으로 판정했습니다.
  - mentioning: scite는 96건, 사람은 39건으로 판정했습니다.
  - F-measure는 0.0–0.58이었고, 결론은 "the overall accuracy of scite's assessments was low"입니다.
- 출처: [Hypothesis 논문](https://journals.indianapolis.iu.edu/index.php/hypothesis/article/view/26528)

**(d) 커버리지** (공식 페이지끼리 수치가 다름)
- llms.txt: "more than 315 million scholarly articles from more than 41 million full-text sources", "more than 30 publisher partners".
- 홈페이지: "1.6B+ citations", "317M+ full-text scholarly articles", 출판사 "42+"와 "44+"가 함께 표기돼 있습니다.

**(e) 생태계**: arXiv 초록 페이지에 "scite.ai Toggle"(arXivLabs)이 있습니다(직접 확인).

### 이미 잘 해결한 것 (차별점 주장 금지)
- 인용 문장 단위 근거와 지지·반박·언급 분류.
- 반박 증거와 철회·편집 공지 모니터링(Collections 알림, Reference Check).
- 답변 문장을 원문 문장에 연결하는 Assistant.
- 출판사 협약에 기반한 대규모 전문 인용 색인.

### AIXON 목표 대비 공백
- 분류 축이 "주장에 대한 지지·반박"입니다. 연구 계보 타입(확장, 개선, 적용)은 확인되지 않았습니다. 독립 평가에서 정확도 한계도 드러났습니다.
- 개념, 선수지식, 학습자 모델, 실습이 확인되지 않았습니다.
- 모든 핵심 기능이 유료입니다. 데이터는 맞춤 라이선스입니다.

### 출처 (모두 확인 2026-10-15)
- https://scite.ai/llms.txt — 확인 2026-10-15
- https://scite.ai/pricing.md — 확인 2026-10-15
- https://scite.ai/pricing — 확인 2026-10-15
- https://scite.ai/ — 확인 2026-10-15
- https://www.biorxiv.org/content/10.1101/2021.03.15.435418v1.full — 확인 2026-10-15
- https://doaj.org/article/81fa50fb3c294f6ba01cc597d41a974e (검색 결과로 서지만 확인) — 확인 2026-10-15
- https://journals.indianapolis.iu.edu/index.php/hypothesis/article/view/26528 — 확인 2026-10-15
- https://arxiv.org/abs/1706.03762 (arXivLabs 토글 목록, 직접 확인) — 확인 2026-10-15

---

## 5. ORKG (Open Research Knowledge Graph) + ORKG Ask

**한 줄 설명**: 논문을 PDF 텍스트가 아니라 기계가 읽을 수 있는 "연구 기여(contribution)" 그래프로 기술하는 오픈 학술 지식그래프입니다. 공식 문구: "The Open Research Knowledge Graph aims to describe research papers in a structured manner". 자매 서비스 ORKG Ask는 LLM 기반 학술 검색·추출 도구입니다.

**운영 주체와 상태**
- About 페이지에 TIB, Leibniz Universität Hannover, L3S Research Center, InfAI 로고와 "Co-funded by the Horizon 2020 programme of the European Union"이 있습니다. 앱 버전은 0.192.0입니다.
- 소스 저장소는 gitlab.com/TIBHannover입니다.
- 운영 중입니다. RDF 덤프의 Last-Modified가 2026-10-13입니다(직접 확인).

**무료와 유료**: 열람, REST API, SPARQL, RDF 덤프 모두 무료로 접근됩니다(직접 확인). 유료 플랜은 확인되지 않았습니다. ORKG Ask의 무료 여부는 공식 페이지에 명시되지 않아 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | ORKG Ask는 "currently uses the CORE dataset"이며, 제목 없는 항목을 거른 뒤 "approximately +220 million"이 남습니다. 의미 검색으로 "semantically similar research articles"를 반환합니다. | [ORKG Ask About](https://ask.orkg.org/pages/about) |
| 2 | Citation & Relationship Visualization | 부분 지원 | 여러 논문의 기여를 나란히 놓는 Comparisons(4,255건)와 Visualizations(811건)가 있습니다(표·차트). 인용 네트워크 시각화는 확인되지 않았습니다. | [API 문서](https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/), [통계 API](https://orkg.org/api/statistics/content-types) |
| 3 | Research Evolution | 확인되지 않음 | Benchmarks(연구 문제 1,706개)와 발행본 버전 관리는 있지만, 시간축 진화 뷰는 확인되지 않았습니다. 문서화된 Benchmarks API에도 시간 필드가 없습니다. | [benchmarks summary](https://orkg.org/api/benchmarks/summary?size=2), [API 문서](https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/) |
| 4 | Concept Knowledge Graph | **지원** | "A statement represents a kind of sentence in the knowledge graph, similar to RDF triples … a tuple of a subject, a predicate, and an object." 그 위에 Research Problems, Research Fields 분류 체계, Templates, Rosetta Stone 문장 템플릿이 있습니다. | [API 문서](https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/), [help center](https://orkg.org/help-center) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | 선수관계 술어나 기능 설명은 확인되지 않았습니다. | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | 등록 사용자와 observatory 멤버십은 있지만, 개인 학습·연구 상태 저장은 확인되지 않았습니다. | [FAQ](https://orkg.org/help-center/article/19/Frequently_Asked_Questions_(FAQ)) |
| 8 | Evidence & Provenance | 부분 지원 | 모든 엔티티에 `created_at`, `created_by`("The UUID of the user or service who created"), `extraction_method`(AUTOMATIC / MANUAL / UNKNOWN / AI_GENERATED / AI_GENERATED_WITH_MANUAL_REVIEW), `verified`, `observatory_id`가 있습니다. 값마다 원문 인용문을 연결하는 기능은 확인되지 않았습니다. | [API 문서](https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/) |
| 9 | Interactive Learning | 부분 지원 | ORKG Ask에서 질문하면 LLM이 기사에서 정보를 추출하고, 사용자가 추출 속성을 지정할 수 있습니다(문헌 Q&A). 학습 기능은 확인되지 않았습니다. | [ORKG Ask About](https://ask.orkg.org/pages/about), [ORKG ASK 논문](https://arxiv.org/abs/2412.04977) |
| 10 | API / OSS / Data reuse | **지원** | "The published data is licensed under CC0 1.0 Universal". 예외로 "Data sourced from Papers With Code licensed CC BY-SA"가 있습니다. 코드는 MIT입니다. REST, SPARQL, RDF 덤프, Python 패키지 `orkg`를 제공합니다. ORKG Ask는 "fully open source"입니다. | [license](https://orkg.org/page/license), [data](https://orkg.org/data), [ORKG Ask About](https://ask.orkg.org/pages/about) |

### 지정 검증

**(a) 데이터 모델** (REST API 문서의 정의와 2026-10-15 통계 API 값)

| 엔티티 | 공식 정의(발췌) | 건수 |
|---|---|---|
| Statement / Resource / Predicate / Literal / Class | 주어–술어–목적어 튜플. 자원과 술어는 ID가 있고, 리터럴은 값입니다. "Statements can also be referenced by their IDs. This allows storing and retrieving provenance information about them." | rdfs:label 트리플 1,139,951개(SPARQL 직접 질의) |
| Paper | "Papers represent a collection of concepts … aggregate these concepts into a paper representation" | 68,795 |
| Contribution | "Contributions represent a collection of concepts in the knowledge graph … a collection of resources, literals and predicates" | 102,576 |
| Comparison | 기여들을 비교표로 집계합니다. 발행된 비교는 수정할 수 없고 새 버전을 만듭니다. "should be citable and referenceable"(FAQ) | 4,255 |
| Research Problem | "meta objects that help better classify the content within the ORKG" | 8,969 |
| Template / Template Property / Template Instance | "define structures to research contribution data and can help illustrate what kind of data is needed to make the paper comparable" | 1,500 |
| Rosetta Stone Template / Statement | "model the structure of statements following the rosetta stone approach". 문장은 "a semantically meaningful statement to a human reader"입니다. | (통계 항목 존재) |
| Smart Review / Literature List / Visualization | 각각 리뷰, 문헌 목록, 시각화 콘텐츠 타입입니다. | 250 / 253 / 811 |
| Benchmark | "Some benchmarks are imported into the ORKG". ID가 `PWC_…` 형식입니다(예: `PWC_OBJECT_DETECTION_PROBLEM`). | 1,706(연구 문제 단위 요약) |
| Observatory | "groups of experts affiliated with different institutions that curates and organize ORKG content for a specific discipline" | — |

- 출처: [API 문서](https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/), [통계](https://orkg.org/api/statistics/content-types), [benchmarks](https://orkg.org/api/benchmarks/summary?size=2), [FAQ](https://orkg.org/help-center/article/19/Frequently_Asked_Questions_(FAQ))

**(b) API·SPARQL·덤프**
- REST: 문서는 tibhannover.gitlab.io/orkg/orkg-backend/api-doc/입니다. 경고 문구: "This API is still in development and therefore unstable and subject to change! Be aware that the API can (and will) break without notice".
- SPARQL: Virtuoso Query Editor `https://orkg.org/triplestore`(GET `query=`로 SPARQL JSON 응답, 직접 확인)와 Visual SPARQL Editor `https://orkg.org/sparql`.
- RDF 덤프: `https://orkg.org/files/rdf-dumps/rdf-export-orkg.nt`(N-Triples, 약 938 MB, Last-Modified 2026-10-13, 직접 확인). 갱신 주기는 공식 명시가 확인되지 않았습니다.
- 그 밖에 PyPI `orkg` 패키지, CSV 가져오기, GraphQL 연합 질의 도움말, 위젯이 있습니다.

**(c) 라이선스**
- 데이터: CC0 1.0. 단 Papers with Code에서 온 데이터는 CC BY-SA입니다.
- 코드: MIT.

**(d) 큐레이션과 provenance** (사람과 자동화 혼합)
- 설계 원칙(2019 논문 초록): "multi-modal scholarly knowledge acquisition, combining crowdsourced and automated techniques".
- Benchmarks: "powered in part by automated information extraction within a human-in-the-loop curation model". 데이터는 "originally imported from" Papers with Code입니다.
- AI comparison creator
  - PDF를 올리면 LLM이 추출 계획에 따라 값을 뽑습니다(최대 10분).
  - 발행 전에 사용자가 "manually review all the values" 해야 합니다.
  - 경고: AI는 "can be imprecise, miss context, or simply get something wrong".
  - AI 값에 별도 라벨이 붙는지, 원문 구절에 연결되는지는 도움말에 없습니다.
- Smart suggestions(ChatGPT)
  - 제목·초록에서 research problem, method, material 값과 속성을 제안합니다.
  - 공식 안내: "use the suggestions from ChatGPT as inspiration, and not as facts".
- 엔티티 메타데이터: `extraction_method`에 AI_GENERATED와 AI_GENERATED_WITH_MANUAL_REVIEW가 따로 있습니다. 생성 주체(사용자 또는 서비스)는 `created_by`에 남습니다.
- 운영 장치: 분야별 전문가 그룹 Observatory, Curation 엔드포인트(예: 설명 없는 술어 목록), Curation Grants 프로그램.

**(e) ORKG Ask**
- 코퍼스: CORE의 제목·초록입니다.
- 모델과 저장소: 추출은 "Mistral Instruct 7B v0.2", 임베딩은 JinaAI, 벡터 저장은 Postgres pgvectorscale입니다.
- 투명성: "We provide the traces of how information were generated". 프롬프트와 파라미터를 공개합니다.
- 공개 범위: "ORKG Ask is fully open source"(GitLab).
- 2024 논문(Oelen, Jaradeh, Auer)은 이를 "a neuro-symbolic approach to scholarly search and exploration"으로 설명합니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- 연구 기여를 트리플로 구조화하는 일과 논문 간 비교표.
- 연구 문제 분류와 분야 분류 체계.
- 엔티티 단위 생성 방식 기록(사람/자동/AI/AI+검토).
- CC0 공개 데이터, SPARQL, 덤프.
- 발행본 불변과 버전 관리.

### AIXON 목표 대비 공백
- 연구 기여(문제–방법–결과) 중심입니다. 개념 학습용 선수관계, 학습 경로, 학습자 상태가 확인되지 않았습니다.
- 값마다 원문 인용문을 붙이는 기능이 확인되지 않았습니다. AIXON이 간선별 근거 문장을 요구한다면 ORKG 데이터에 근거를 보강해야 합니다(추론).
- REST API는 공식적으로 불안정합니다. 재사용한다면 덤프·SPARQL 스냅샷 기반이 안전합니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://orkg.org/about — 확인 2026-10-15
- https://orkg.org/data — 확인 2026-10-15
- https://orkg.org/page/license — 확인 2026-10-15
- https://orkg.org/help-center — 확인 2026-10-15
- https://orkg.org/help-center/article/19/Frequently_Asked_Questions_(FAQ) — 확인 2026-10-15
- https://orkg.org/help-center/article/65/AI_comparison_creator — 확인 2026-10-15
- https://orkg.org/help-center/article/53/Using_ChatGPT_in_the_ORKG_with_Smart_suggestions — 확인 2026-10-15
- https://orkg.org/benchmarks — 확인 2026-10-15
- https://tibhannover.gitlab.io/orkg/orkg-backend/api-doc/ — 확인 2026-10-15
- https://orkg.org/api/statistics/content-types (각 metric 하위 경로 포함, 직접 확인) — 확인 2026-10-15
- https://orkg.org/api/benchmarks/summary?size=2 (직접 확인) — 확인 2026-10-15
- https://orkg.org/triplestore (SPARQL 직접 질의) — 확인 2026-10-15
- https://orkg.org/files/rdf-dumps/rdf-export-orkg.nt (HEAD 응답 직접 확인) — 확인 2026-10-15
- https://arxiv.org/abs/1901.10816 — 확인 2026-10-15
- https://ask.orkg.org/pages/about — 확인 2026-10-15
- https://arxiv.org/abs/2412.04977 — 확인 2026-10-15

---

## 6. Papers with Code (구 paperswithcode.com): 종료와 데이터 아카이브

**한 줄 설명**: ML 논문을 task, dataset, method, 평가표(SOTA 리더보드), 코드 구현에 연결하던 커뮤니티 편집형 사이트입니다. 공식 사명: "to create a free and open resource with Machine Learning papers, code, datasets, methods and evaluation tables". 아래 10개 기준은 † 과거 기능 기준입니다.

**운영 주체**: "The core Papers with Code team is based in Meta AI Research. Papers with Code is a community project."(2024-12-16 보관본 About)

### 지정 검증 (a): 종료 여부와 시점

| 시점 | 관측 내용 | 근거 |
|---|---|---|
| 2025-07-22 | 홈페이지 HTTP 200(정상 서비스) | Wayback CDX (직접 확인) |
| 2025-07-24 | 공식 종료일로 보도됨. HF CTO Julien Chaumond가 2025-07-25 개인 계정에서 "Trending Papers"를 발표하며 "officially sunsetted the previous day"라고 했다고 전함 | [2차] hyper.ai |
| 2025-07-25 ~ 08-12 | 홈페이지가 302로 `github.com/paperswithcode`에 리다이렉트 | Wayback CDX와 보관본 Location 헤더 (직접 확인) |
| 2025-08-19 ~ | 301로 `huggingface.co/papers/trending`에 리다이렉트 | Wayback 보관본 Location 헤더 (직접 확인) |
| 2026-10-15 | `/`, `/methods`, `/sota`, `/about`, `/api/v1/papers/`가 모두 **HTTP 302 → https://huggingface.co/papers/trending** | curl (직접 확인) |

- Meta나 Hugging Face의 공식 종료 공지문 원문은 확인되지 않았습니다. 날짜는 2차 보도와 Wayback 관측으로만 뒷받침됩니다.
- 커뮤니티 보고: 이용자가 올린 데이터셋이 이전 후 보이지 않고 종료 통보도 받지 못했다는 포럼 글이 있습니다. HF 직원 답변은 없습니다 [2차].

### 지정 검증 (b): 데이터 덤프는 아직 받을 수 있는가

- 받을 수 있습니다. 다만 **고정 스냅샷**이고 갱신되지 않습니다.
- 위치: Hugging Face `pwc-archive` 조직의 데이터셋 5종입니다.

| 데이터셋 | 행 수 | 스냅샷 | 라이선스 |
|---|---|---|---|
| papers-with-abstracts | 576,261 | 2025-07-29 | cc-by-sa-4.0 (라이선스 선언 커밋 2026-08-17) |
| links-between-paper-and-code | 300,161 | 2025-07-28 | cc-by-sa-4.0 |
| datasets | 15,008 | 2025-07-28 | cc-by-sa-4.0 |
| methods | 8,725 | 2025-07-28 | cc-by-sa-4.0 |
| evaluation-tables | (parquet 4개, 약 138 MB) | 2025-07-28 | cc-by-sa-4.0 |

- 각 데이터셋 카드: "This dataset will not be updated. It corresponds to the last available public snapshot of the data, retrieved on July 28th, 2025."(papers-with-abstracts만 July 29th)
- GitHub `paperswithcode/paperswithcode-data`
  - 2025-09-08 PR #119로 다운로드 링크가 HF 데이터셋으로 바뀌었습니다.
  - README는 여전히 "At the moment, data is regenerated daily."라고 적혀 있습니다(사실과 다름).
  - 이를 고치려는 PR #120(2025-09-10)은 2026-10-15 현재 미병합(open)입니다.
  - README 라이선스: "All data is licenced under CC-BY-SA."
- 일부 데이터는 NLP-progress, EFF AI metrics, SQuAD, RedditSota처럼 호환 라이선스 출처에서 왔습니다(보관본 About).

### 지정 검증 (c): "Methods" 분류 체계와 카테고리가 있었는가

- 있었습니다.
- 보관본 메서드 페이지(Transformer, 2024-12-19)
  - **Categories**: "Transformers", "Autoregressive Transformers".
  - **Components**: Absolute Position Encodings, Adam, BPE, Dense Connections, Dropout, GELU, Label Smoothing, Layer Normalization, Multi-Head Attention, Position-Wise FFN, ReLU, Residual Connection, Scaled Dot-Product Attention, Softmax. 각 구성요소가 자기 카테고리와 함께 표시됩니다.
  - **Usage Over Time**: "This feature is experimental; we are continuously improving our matching algorithm."
  - 메서드별 Task 점유율도 있습니다.
- 덤프 구조
  - `methods`: `collections: [{area, area_id, collection}]`, `paper`(도입 논문), `introduced_year`, `num_papers`, `code_snippet_url`.
  - `papers-with-abstracts`: 논문별 `tasks`와 `methods[].main_collection{area, description, name, parent}`. `parent`로 컬렉션 계층을 표현합니다.
- (직접 분석) `methods` parquet을 집계한 결과
  - area는 7개입니다: General, Computer Vision, Natural Language Processing, Graphs, Reinforcement Learning, Sequential, Audio.
  - (area, collection) 고유 쌍은 334개입니다. 스팸 행이 포함된 수치입니다.
- **덤프에는 Components(메서드 간 구성 관계) 필드가 없습니다**(직접 분석: 11개 컬럼 확인). 메서드 설명문 안의 마크다운 링크로 다른 메서드·카테고리를 가리킬 뿐입니다.

### 지정 검증 (d): 아카이브 데이터 품질 (직접 분석)

- 방법: `pwc-archive/methods` parquet(6.2 MB)을 내려받아 pandas로 집계했습니다.
- **스팸 오염이 심합니다.**
  - 8,725행 중 6,043행의 이름에 "?"나 전화번호 패턴이 들어 있습니다(휴리스틱).
  - 예: "How do I contact Hulu customer service? Via Chat, Phone And More!"
  - 남은 2,682행에도 스팸이 섞여 있습니다. 예: "30 Ways to Speak Princess cruise Customer Service by Phone…".
- **`introduced_year`를 믿을 수 없습니다.**
  - 남은 2,682행 중 2,640행이 2000입니다.
  - 예: Transformer(도입 논문 "Attention Is All You Need", arXiv 1706.03762)와 Dropout이 모두 2000입니다. 자리표시 값으로 보입니다(추론).
- evaluation-tables 스키마의 metric 키에 SQL 인젝션 시도로 보이는 문자열(`-1' OR 3*2<(0+5+964-964) or '37tbCgjV'='`)이 있습니다. 편집 검수가 뚫린 흔적입니다(추론).
- 반면 evaluation-tables의 구조는 쓸모 있습니다.
  - task → categories / description / subtasks(재귀) → datasets → sota.rows{`paper_title`, `paper_url`, **`paper_date`**, `model_name`, `metrics`, `code_links`, `uses_additional_data`}.
  - 따라서 2025-07까지의 벤치마크별 SOTA 타임라인을 다시 만들 수 있습니다(추론).
- A 문서도 methods 첫 행들의 스팸을 지적했습니다. 이 문서는 그 규모와 연도 필드 문제를 정량으로 보탰습니다.

### 10개 기준 판정 († 과거 기능 기준. (10)만 현재 유효)

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원† | task, method, dataset별 논문·코드 탐색 사이트였습니다. 현재는 HF Trending으로 리다이렉트됩니다. | [보관본 About](https://web.archive.org/web/20241216214350/https://paperswithcode.com/about) |
| 2 | Citation & Relationship Visualization | 부분 지원† | 논문, 코드, task, method, 결과를 목록·표로 연결했습니다. 그래프 시각화는 확인되지 않았습니다. | [보관본 method](https://web.archive.org/web/20241219214701/https://paperswithcode.com/method/transformer) |
| 3 | Research Evolution | **지원**† | SOTA 페이지 차트에 "State-of-the-art methods" 추세선이 있고 x축이 날짜였습니다(예: FireCaffe 2015-10-31 → ResNet-152 2015-12-10 → …). 메서드 페이지에 "Usage Over Time"(실험적)도 있었습니다. | [보관본 SOTA](https://web.archive.org/web/20241227202530/https://paperswithcode.com/sota/image-classification-on-imagenet), [보관본 method](https://web.archive.org/web/20241219214701/https://paperswithcode.com/method/transformer) |
| 4 | Concept Knowledge Graph | **지원**† | 메서드 엔티티 사이에 Components(구성) 관계가 있었고, 카테고리 계층도 있었습니다. 단 덤프에는 계층만 있고 Components는 없습니다. | 위와 같음, [methods 카드](https://huggingface.co/datasets/pwc-archive/methods) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | Components는 구성(has-part) 관계로 표시됐고, 선수관계로 정의되지 않았습니다. 선수관계 후보로 바꿔 쓸 수는 있습니다(추론). | [보관본 method](https://web.archive.org/web/20241219214701/https://paperswithcode.com/method/transformer) |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | 계정은 편집용이었습니다. | [보관본 About](https://web.archive.org/web/20241216214350/https://paperswithcode.com/about) |
| 8 | Evidence & Provenance | 부분 지원† | 결과는 논문에 연결했고 "we require that the paper is published as pre-print, in a conference or a journal". 편집은 "monitored on Slack on the #recentchanges channel". 값마다 원문 인용문은 없었습니다. 최종 스냅샷의 스팸은 검수 한계를 보여 줍니다. | [보관본 About](https://web.archive.org/web/20241216214350/https://paperswithcode.com/about) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | **지원**(현재 유효) | 5종 덤프가 CC BY-SA 4.0으로 공개돼 있습니다. 과거 `/api/v1/`은 지금 리다이렉트됩니다(직접 확인). | [pwc-archive](https://huggingface.co/datasets/pwc-archive/methods), [GitHub](https://github.com/paperswithcode/paperswithcode-data) |

### 이미 잘 해결했던 것 (차별점 주장 금지)
- task, dataset, method, 결과, 코드의 연결.
- 날짜 축 SOTA 추세 차트.
- 메서드 분류 체계와 구성요소 관계.
- CC BY-SA 공개 데이터.
- "AI 분야 방법론 지도" 자체는 이미 있던 개념입니다. AIXON은 선수관계·근거·학습 측면으로 차별화해야 합니다(추론).

### AIXON 관점의 공백과 교훈
- 공개 편집과 Slack 모니터링만으로는 스팸을 막지 못했습니다. 운영 주체가 바뀌자 서비스가 사전 공지 없이 끊겼습니다(2차 보도, Wayback 관측).
- 선수관계, 학습자 모델, 실습은 처음부터 없었습니다(확인되지 않음).

### 출처 (모두 확인 2026-10-15)
- https://paperswithcode.com/ 및 /methods, /sota, /about, /api/v1/papers/ (curl로 302 → https://huggingface.co/papers/trending 직접 확인) — 확인 2026-10-15
- https://web.archive.org/cdx/search/cdx?url=paperswithcode.com/&from=20250715&to=20250805 (직접 확인) — 확인 2026-10-15
- https://web.archive.org/web/20250722220213/https://paperswithcode.com/ — 확인 2026-10-15
- https://web.archive.org/web/20250725094358/https://paperswithcode.com/ (Location: github.com/paperswithcode) — 확인 2026-10-15
- https://web.archive.org/web/20250819021752/https://paperswithcode.com/ (Location: huggingface.co/papers/trending) — 확인 2026-10-15
- https://web.archive.org/web/20241216214350/https://paperswithcode.com/about — 확인 2026-10-15
- https://web.archive.org/web/20241227202530/https://paperswithcode.com/sota/image-classification-on-imagenet — 확인 2026-10-15
- https://web.archive.org/web/20241219214701/https://paperswithcode.com/method/transformer — 확인 2026-10-15
- https://github.com/paperswithcode/paperswithcode-data , https://raw.githubusercontent.com/paperswithcode/paperswithcode-data/master/README.md — 확인 2026-10-15
- https://github.com/paperswithcode/paperswithcode-data/pull/119 , https://github.com/paperswithcode/paperswithcode-data/pull/120 (GitHub API로 상태 확인) — 확인 2026-10-15
- https://huggingface.co/datasets/pwc-archive/methods , /evaluation-tables , /papers-with-abstracts , /links-between-paper-and-code , /datasets (카드와 API 메타데이터) — 확인 2026-10-15
- https://huggingface.co/api/datasets/pwc-archive/papers-with-abstracts/commits/main — 확인 2026-10-15
- https://huggingface.co/api/datasets/pwc-archive/methods/parquet/default/train/0.parquet (직접 분석 원자료) — 확인 2026-10-15
- https://datasets-server.huggingface.co/info?dataset=pwc-archive/evaluation-tables — 확인 2026-10-15
- [2차] https://hyper.ai/en/news/42900 — 확인 2026-10-15
- [2차] https://discuss.huggingface.co/t/missing-dataset-after-paperswithcode-migration/167174 — 확인 2026-10-15

---

## 7. Hugging Face Papers / Trending Papers (구 PwC 리다이렉트 대상)

**한 줄 설명**: arXiv 논문마다 페이지를 만들어 관련 모델·데이터셋·Space, GitHub 저장소, 커뮤니티 토론, AI 요약을 붙이는 Hugging Face Hub 기능입니다. Daily Papers와 Trending Papers 피드가 있습니다.

**상태**
- 운영 중입니다. 구 paperswithcode.com의 현재 리다이렉트 대상이 `/papers/trending`입니다(6절).
- Trending 페이지는 "AK and the research community"를 크레딧으로 표기하고 Daily / Weekly / Monthly 탭을 둡니다. 순위 산정 방식은 페이지에 설명이 없어 확인되지 않았습니다.

**무료와 유료**: 열람은 무료입니다. 업보트는 로그인이 필요하고, 트렌딩 논문 일일 이메일 구독을 제공합니다. Papers 전용 유료 기능은 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Daily Papers, Trending(일·주·월), 제목·arXiv ID 검색, 미색인 논문 색인 요청이 있습니다. 공식 문서: "We're starting with Arxiv as it accounts for 95% of the paper URLs Hugging Face users have linked in their repos organically." | [trending](https://huggingface.co/papers/trending), [paper-pages docs](https://huggingface.co/docs/hub/paper-pages) |
| 2 | Citation & Relationship Visualization | 부분 지원 | "Paper pages allow people to find artifacts related to a paper such as models, datasets and apps/demos (Spaces)". API에 `linkedModels`, `linkedDatasets`, `linkedSpaces`가 있고 `/api/arxiv/{id}/repos`도 있습니다. 목록형이며 그래프는 확인되지 않았습니다. | [paper-pages docs](https://huggingface.co/docs/hub/paper-pages), [API 예](https://huggingface.co/api/papers/2501.12948) |
| 3 | Research Evolution | 부분 지원 | `list_daily_papers(date, week, month, sort="trending")`로 시간창별 조회가 됩니다(인기도 시간창 수준). 연구 흐름 시각화는 확인되지 않았습니다. | [huggingface_hub HfApi](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) |
| 4 | Concept Knowledge Graph | 부분 지원 | 논문마다 `ai_keywords`가 있습니다(예: "reinforcement learning", "multi-stage training", "cold-start data"). 개념 간 관계는 확인되지 않았습니다. | [API 예](https://huggingface.co/api/papers/2501.12948) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | 로그인 업보트, 일일 이메일 구독, 저자 claim과 프로필 노출 설정이 있습니다. | [trending](https://huggingface.co/papers/trending), [paper-pages docs](https://huggingface.co/docs/hub/paper-pages) |
| 8 | Evidence & Provenance | 부분 지원 | API가 `ai_summary`와 함께 생성 모델을 밝힙니다(조회한 2501.12948 레코드에서 `ai_summary_model: "Qwen/Qwen2.5-Coder-32B-Instruct"`). GitHub 링크 출처는 `githubRepoAddedBy: "auto"`로 표기됩니다. 요약 문장과 원문 구절의 연결은 확인되지 않았습니다. | [API 예](https://huggingface.co/api/papers/2501.12948) |
| 9 | Interactive Learning | 확인되지 않음 | 커뮤니티 토론("enable the community to discuss about the paper")은 있습니다. AI Q&A나 학습 기능은 확인되지 않았습니다. | [paper-pages docs](https://huggingface.co/docs/hub/paper-pages) |
| 10 | API / OSS / Data reuse | **지원** | `huggingface_hub`에 `list_papers(query, limit)`, `paper_info(id)`, `list_daily_papers(date, week, month, submitter, sort ∈ {publishedAt, trending}, p, limit)`가 문서화돼 있습니다. 무인증 JSON 응답도 직접 확인했습니다. **논문 메타데이터·AI 요약의 재사용 라이선스는 확인되지 않았습니다.** | [huggingface_hub HfApi](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api), [daily_papers](https://huggingface.co/api/daily_papers?limit=1) |

### PwC 후속으로서 무엇이 남고 무엇이 빠졌나
- 남은 것: 트렌딩 논문 피드, GitHub 저장소와 스타 수(`githubStars`), 관련 HF 아티팩트, 공개 API.
- 빠진 것
  - HF Papers 자체에는 task·method 분류 체계, 벤치마크 리더보드, SOTA 추세 차트가 확인되지 않았습니다.
  - 이 공백은 HF 오픈소스 팀원이 별도로 띄운 paperswithcode.co(8절)가 일부 메웁니다.
- 2025-07-25 Julien Chaumond가 Trending Papers를 PwC 후속으로 발표했다는 내용은 2차 보도입니다 [2차: hyper.ai].

### 이미 잘 해결한 것 (차별점 주장 금지)
- AI 논문 트렌딩 피드와 코드·모델·데이터셋 링크.
- 논문별 AI 요약과 키워드.
- 무료 공개 API.

### AIXON 목표 대비 공백
- 개념 관계, 선수관계, 학습 경로, 학습자 모델, 근거 문장 연결이 확인되지 않았습니다.
- 메타데이터 라이선스가 불명확합니다. 로컬에 대량 저장하기보다 ID와 링크 위주로 참조하는 편이 안전합니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://huggingface.co/papers/trending — 확인 2026-10-15
- https://huggingface.co/docs/hub/paper-pages — 확인 2026-10-15
- https://huggingface.co/docs/huggingface_hub/package_reference/hf_api — 확인 2026-10-15
- https://huggingface.co/api/papers/2501.12948 , https://huggingface.co/api/papers/1706.03762 , https://huggingface.co/api/daily_papers?limit=1 , https://huggingface.co/api/papers/search?q=attention%20is%20all%20you%20need&limit=1 , https://huggingface.co/api/arxiv/1706.03762/repos (직접 확인) — 확인 2026-10-15
- [2차] https://hyper.ai/en/news/42900 — 확인 2026-10-15

---

## 8. paperswithcode.co (2026 재개판)

**한 줄 설명**: 구 Papers with Code의 리더보드, task, method 페이지를 되살린 사이트입니다. 홈페이지 설명: "Discover trending machine-learning papers, methods, benchmarks, datasets, and open-source implementations."

**운영 주체와 상태**
- 2026-05-24 HF 블로그 Community Article: "Hi, Niels here from the open-source team at Hugging Face. It's been one week since I launched paperswithcode.co, a revival of the website we all loved." 따라서 공개 시점은 2026-05 중순입니다.
- 2026-06-22 후속 글: "At Hugging Face we continue working on a revival of Papers with Code". 별칭 도메인 paperswithco.de를 추가했습니다.
- 구 도메인 paperswithcode.com은 여전히 HF Trending으로 리다이렉트됩니다. 재개판으로 가지 않습니다(직접 확인).

**무료와 유료**: 웹 접근이 가능합니다. 요금과 계정 기능은 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Trending research, Recent papers, Paper archive, Research tasks, Methods가 있습니다. arXiv 밖 자료(GitHub, 블로그, bioRxiv)도 제출할 수 있고 "AI will automatically enrich it with task and method tags, the GitHub repo, evals, and more." | [홈](https://paperswithcode.co/), [재개 글](https://huggingface.co/blog/nielsr/paperswithcode-launch) |
| 2 | Citation & Relationship Visualization | 부분 지원 | "Support for paper lineage: whenever a paper has a follow-up or predecessor, this will be displayed with a small banner above the abstract." "Each method also lists all papers that cite it." 그래프는 확인되지 않았습니다. | [재개 글](https://huggingface.co/blog/nielsr/paperswithcode-launch) |
| 3 | Research Evolution | 부분 지원 | lineage 배너가 있습니다. 트렌딩 점수는 "a combination of the GitHub star velocity and the trending score of the linked Hugging Face artifacts"입니다. 비문서화 JSON에 task `research_trends`, method `trend_score`·`rate_change` 필드가 있습니다(직접 확인). 시간축 진화 뷰는 확인되지 않았습니다. | [업데이트 글](https://huggingface.co/blog/nielsr/updates-to-pwc), [methods JSON](https://paperswithcode.co/api/v1/methods) |
| 4 | Concept Knowledge Graph | 부분 지원 | task에 `parent_id`·`level` 계층이 있고, method에 `collection_parent`, `introduced_year`, `source_title`이 있습니다. 2026-10-15 응답 기준 count는 method 239개, task 143개입니다(직접 확인). 개념 간 관계 유형은 확인되지 않았습니다. | [methods JSON](https://paperswithcode.co/api/v1/methods), [tasks JSON](https://paperswithcode.co/api/v1/tasks) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | — | — |
| 8 | Evidence & Provenance | 부분 지원 | 관계 방향(선행/후속)과 점수(top-3 SOTA 배지: "displayed whenever a paper gets a score within the top 3 of a given benchmark")를 표시합니다. 외부 평가는 출처 이름과 함께 보여 줍니다(예: FrontierSWE, PostTrainBench, Artificial Analysis). lineage 판정 근거와 AI 자동 보강 값의 표기는 공개되지 않았습니다. | [업데이트 글](https://huggingface.co/blog/nielsr/updates-to-pwc) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | 확인되지 않음 | 공식 API 문서와 데이터 라이선스는 확인되지 않았습니다. `/api/v1/papers`, `/api/v1/methods`, `/api/v1/tasks`가 JSON으로 응답하지만 비문서화입니다(직접 확인). 데이터는 "based on the legacy PwC data available on the hub"이므로 CC BY-SA 승계 대상일 가능성이 큽니다(추론). | [업데이트 글](https://huggingface.co/blog/nielsr/updates-to-pwc) |

- A 문서와의 판정 차이
  - (8): A는 "확인되지 않음"입니다. 이 문서는 기준표의 "관계 방향·점수만 표시" 조항에 따라 부분 지원으로 봤습니다.
  - (10): A는 레거시 데이터를 합쳐 "지원"으로 봤습니다. 이 문서는 레거시를 6절로 분리했기 때문에 재개판 자체는 "확인되지 않음"입니다.
- 규모 비교: 재개판은 method 239개, task 143개입니다. 구 덤프는 method 8,725행(스팸 포함)이었습니다. 큐레이션 범위가 훨씬 좁습니다. 평가 수치는 2026-05-24 기준 "about 3k evals"입니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- AI 분야 task·method·benchmark 리더보드(다중 지표, scatter plot과 표).
- SOTA 배지와 트렌딩 점수.
- **선행/후속 논문 lineage 표시**.
- 외부 평가 수치 집계.

### AIXON 목표 대비 공백
- lineage가 방향 수준이고 근거가 공개되지 않았습니다. 관계 타입(확장, 개선, 적용)이 확인되지 않았습니다.
- 선수지식, 학습 경로, 학습자 모델, 실습이 확인되지 않았습니다.
- 1인 주도 Community Article 기반이라 지속성이 불확실합니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://paperswithcode.co/ — 확인 2026-10-15
- https://huggingface.co/blog/nielsr/paperswithcode-launch — 확인 2026-10-15
- https://huggingface.co/blog/nielsr/updates-to-pwc — 확인 2026-10-15
- https://paperswithcode.co/api/v1/methods , https://paperswithcode.co/api/v1/tasks , https://paperswithcode.co/api/v1/papers (비문서화, 직접 확인) — 확인 2026-10-15

---

## 9. alphaXiv

**한 줄 설명**: arXiv 논문 위에서 토론하고, AI 개요·어시스턴트·오디오로 읽게 해 주는 논문 읽기·토론 플랫폼입니다. 공식 설명: "Discuss, discover, and read arXiv papers. Explore trending papers, see recent activity and discussions, and follow authors of arXiv papers on alphaXiv." About: "Open discussion directly on arXiv papers."

**운영 주체와 상태**
- "alphaXiv Inc."이며 약관은 2026-04-17에 개정됐습니다. 운영 중이고 블로그 최신 글은 2026-09-09입니다.
- arXiv 초록 페이지의 "Code, Data, Media" 탭에 "alphaXiv Toggle"(arXivLabs)이 있습니다(직접 확인).

**무료와 유료**
- 웹 열람과 토론이 가능합니다.
- MCP 문서: "Feed retrieval is free of assistant quota; the search and analysis tools count against it." Assistant 쿼터가 있다는 뜻입니다.
- 약관: "alphaXiv may offer paid subscription plans, including alphaXiv Pro and other premium features". 가격은 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Explore(트렌딩, 최근 활동), 연구자 팔로우가 있습니다. MCP `discover_papers`는 "an agentic retrieval loop that combines keyword search, embedding search, and optional multi-round follow-up searches"입니다. | [홈](https://www.alphaxiv.org/), [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 2 | Citation & Relationship Visualization | 부분 지원 | 논문 페이지에 "Similar papers"·"Related papers" 목록이 있습니다. 인용 그래프 시각화는 확인되지 않았습니다. | [논문 페이지 예](https://www.alphaxiv.org/abs/1706.03762) |
| 3 | Research Evolution | 부분 지원 | "Hot feed over 30 Days"가 있습니다(인기도 시간창 수준). 연구 흐름 시각화는 확인되지 않았습니다. | [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | 논문, 연구자, 기관 엔티티는 있지만 개념 엔티티는 확인되지 않았습니다. | [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | 개인화 "For You" 피드(추천)는 있지만 학습 경로는 확인되지 않았습니다. | [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 7 | Persistent Learner State | 부분 지원 | "The default 'Want to read', 'Reading', and 'Completed' folders represent reading status". 연구자 팔로우와 개인화 피드도 있습니다. 지식·숙달 모델은 확인되지 않았습니다. | [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 8 | Evidence & Provenance | **지원** | AI Overview 문장에 페이지 앵커가 붙습니다(예: "[p 2]", "[p 8]"). MCP `answer_pdf_queries`는 페이지 단위 XML을 돌려주며 "so you can construct citations directly from the returned page text"입니다. | [논문 페이지 예](https://www.alphaxiv.org/abs/1706.03762), [MCP 문서](https://www.alphaxiv.org/docs/mcp) |
| 9 | Interactive Learning | 부분 지원 | 논문 페이지에 AI Overview, Assistant(로그인), Audio와 Transcript, 구절에 붙는 토론 스레드가 있습니다. 연습·퀴즈·피드백 루프는 확인되지 않았습니다. | [논문 페이지 예](https://www.alphaxiv.org/abs/1706.03762) |
| 10 | API / OSS / Data reuse | 부분 지원 | MCP 서버 `https://api.alphaxiv.org/mcp/v1`이 21개 도구를 제공하고, OAuth 2.1이나 API 키로 인증합니다. 약관은 "The Service is for your personal use"이며 상업적 이용과 "data mining, robots, scraping, or similar data gathering or extraction methods"를 금지합니다. 공개 데이터와 OSS는 확인되지 않았습니다. | [MCP 문서](https://www.alphaxiv.org/docs/mcp), [약관](https://www.alphaxiv.org/terms) |

### 지정 검증: 기능 목록 (공식 페이지·문서 기준)
- **토론**: 논문 구절에 붙는 댓글·답글 스레드입니다. 예시 논문 페이지에 Discussion 30건이 있었습니다.
- **AI 설명**
  - 논문별 "AI Overview"는 페이지 앵커가 달린 해설입니다. 표 해설도 포함합니다.
  - 로그인 후 Assistant를 쓸 수 있습니다.
  - Audio(재생기와 Transcript)가 있습니다.
- **그 밖의 페이지 요소**: 연결 GitHub 저장소, BibTeX, "AI detection Analyze", "Autoresearch", Similar/Related papers.
- **MCP 도구(21개)**
  - 피드: `get_for_you_feed`, `get_hot_feed`.
  - 검색·읽기: `discover_papers`, `get_paper_content`(기본값은 "a structured AI-generated intermediate report", 옵션으로 전문), `answer_pdf_queries`.
  - 코드: `read_files_from_github_repository`.
  - 연구자: `find_researchers`, `related_researchers` 등.
  - 서재: 폴더 관리.
  - 제약: "Browser-hosted MCP integrations (e.g. adding this server directly inside claude.ai or chatgpt.com) are not supported".
- **기타**: Chrome 확장, 중국어 인터페이스(`/zh`)가 있습니다. 블로그에는 arXiv 검색 에이전트 학습(ArxivQA) 같은 자체 연구 글이 있습니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- 논문 구절 단위 커뮤니티 토론.
- 페이지 앵커가 달린 AI 개요와 오디오 요약.
- 읽기 상태 폴더(Want to read / Reading / Completed).
- 논문 코드 저장소까지 읽는 에이전트 도구(MCP).

### AIXON 목표 대비 공백
- 개념 그래프, 선수관계, 학습 경로, 지식 상태 모델, 실습이 확인되지 않았습니다.
- 약관이 스크래핑과 데이터 수집을 금지합니다. AIXON의 데이터 소스로 쓰기는 어렵고, 개인 MCP 사용 정도가 한계입니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://www.alphaxiv.org/ — 확인 2026-10-15
- https://www.alphaxiv.org/about — 확인 2026-10-15
- https://www.alphaxiv.org/docs/mcp — 확인 2026-10-15
- https://www.alphaxiv.org/abs/1706.03762 — 확인 2026-10-15
- https://www.alphaxiv.org/terms — 확인 2026-10-15
- https://www.alphaxiv.org/blog — 확인 2026-10-15
- https://arxiv.org/abs/1706.03762 (alphaXiv Toggle 직접 확인) — 확인 2026-10-15

---

## 10. Ai2 Asta (추가 경쟁자)

**한 줄 설명**: Ai2가 Semantic Scholar 코퍼스 위에 만든 에이전트형 연구 보조 생태계입니다. 구성은 Asta agents(Find papers, Summarize literature, Analyze data), AstaBench, Asta resources입니다.

**운영 주체와 상태**
- Allen Institute for AI이며, 2025-08-26 공식 블로그로 발표했습니다.
- Analyze data는 일부 파트너 대상 베타입니다.
- Paper Finder는 Asta에 통합됐습니다("Paper Finder is now part of Asta" 리다이렉트 페이지).
- 공개 저장소가 2026-10에도 갱신되고 있습니다(GitHub API 직접 확인).

**무료와 유료**: 공식 페이지에서 요금 정보는 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Find papers가 질의에 대해 각 논문이 왜 관련 있는지 설명하며 논문을 찾습니다. | [Asta 블로그](https://allenai.org/blog/asta) |
| 2 | Citation & Relationship Visualization | 확인되지 않음 | — | — |
| 3 | Research Evolution | 확인되지 않음 | — | — |
| 4 | Concept Knowledge Graph | 확인되지 않음 | — | — |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | — | — |
| 8 | Evidence & Provenance | **지원** | 모든 출력이 "cited and traceable to its sources"이고, 요약의 주장마다 "a clickable citation and often an inline excerpt"가 붙습니다. MCP `snippet_search`는 본문 발췌(약 500단어)를 돌려줍니다. 독립 연구는 같은 질의에서도 인용 구성이 흔들린다고 보고했습니다(아래). | [Asta 블로그](https://allenai.org/blog/asta), [Corpus Tool](https://allenai.org/asta/resources/mcp), [Orduña-Malea & Lopezosa 2026](https://arxiv.org/abs/2606.08301) |
| 9 | Interactive Learning | 부분 지원 | Summarize literature는 연구 질문에 대한 구조화 요약(문헌 Q&A)입니다. 학습 기능은 블로그에 언급이 없습니다. | [Asta 블로그](https://allenai.org/blog/asta) |
| 10 | API / OSS / Data reuse | **지원** | `allenai/asta-paper-finder`, `allenai/ai2-scholarqa-lib`, `allenai/asta-bench`가 모두 Apache-2.0입니다. 단 "There are some proprietary artifacts, including artifacts tied to our UI infrastructure". Scientific Corpus Tool(MCP `https://asta-tools.allen.ai/mcp/v1`)은 별도 라이선스가 걸린 키 발급형입니다(아래). | [GitHub paper-finder](https://github.com/allenai/asta-paper-finder), [scholarqa-lib](https://github.com/allenai/ai2-scholarqa-lib), [asta-bench](https://github.com/allenai/asta-bench), [Corpus License](https://allenai.org/asta-corpus-license) |

### 지정 검증 성격의 보충
- **Scientific Corpus Tool 라이선스**
  - 이용 목적: "solely for academic and non-commercial research and benchmarking purposes".
  - 금지: 상업적 이용, 그리고 "the Tools or Asta, including its corpus"의 복사·수정.
  - 의무: 출판물에 Ai2 attribution을 넣어야 합니다.
  - 출력: 출력물 소유권은 이용자에게 있습니다. Ai2도 입력·출력을 서비스 개선에 쓸 수 있습니다.
- **독립 평가**(Orduña-Malea & Lopezosa, arXiv 2606.08301, 2026-06-06)
  - Summarize literature를 10개 질의로 두 차례 수집했습니다.
  - 결과: "notable instability is observed in the composition of cited references across identical queries", "a lack of concordance between retrieved documents and those ultimately cited".
- **학습 기능**: 공식 블로그는 향후 기술로 실험 재현, 가설 생성, 과학 프로그래밍만 언급합니다.

### 이미 잘 해결한 것 (차별점 주장 금지)
- 주장마다 클릭 가능한 인용과 원문 발췌를 붙인 문헌 요약.
- 근거 기반 에이전트의 오픈소스 구현과 벤치마크(AstaBench).
- 논문 발췌 검색 MCP.

### AIXON 목표 대비 공백
- 개념 그래프, 선수관계, 학습 경로, 학습자 모델, 실습이 확인되지 않았습니다.
- 코퍼스 도구 약관이 코퍼스 복사를 금지합니다. 로컬 지식베이스에 대량 적재하는 용도로는 맞지 않습니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://allenai.org/blog/asta — 확인 2026-10-15
- https://allenai.org/asta — 확인 2026-10-15
- https://allenai.org/asta/resources/mcp — 확인 2026-10-15
- https://allenai.org/asta-corpus-license — 확인 2026-10-15
- https://asta.allen.ai/discover?redirect_from=paper-finder — 확인 2026-10-15
- https://github.com/allenai/asta-paper-finder , https://github.com/allenai/ai2-scholarqa-lib , https://github.com/allenai/asta-bench (GitHub API로 라이선스 확인) — 확인 2026-10-15
- https://arxiv.org/abs/2606.08301 — 확인 2026-10-15

---

## 11. Gaps & implications for AIXON

### 11.1 이미 시장에 있는 것: AIXON이 차별점으로 주장하면 안 되는 목록

| 기능 | 이미 제공하는 곳 (근거 절) |
|---|---|
| 논문 PDF를 대상으로 한 LLM 요약과 질의응답 | Elicit, SciSpace, Consensus, scite Assistant, alphaXiv, ORKG Ask, Asta (1–5, 9, 10절). HF는 논문별 AI 요약 (7절) |
| 답변 문장·추출 값과 원문 인용문·페이지·스니펫의 연결 | Elicit supporting quotes, Consensus 문장별 인용, scite 문장 연결, SciSpace 단락·섹션 인용, alphaXiv `[p N]`, Asta inline excerpt (1–4, 9, 10절) |
| 여러 논문을 구조화된 표로 비교·추출 | Elicit 열 추출, SciSpace Extract Data, ORKG Comparisons와 AI comparison creator, Consensus PICO (1–3, 5절) |
| 연구 질문에 대한 증거 분포 집계 | Consensus Meter, scite supporting/contrasting 집계 (3, 4절) |
| 인용 성격 분류, 철회·편집 공지 점검 | scite (4절). 인용 의도 분류는 Semantic Scholar(A 문서 1절) |
| 수식·방정식·표·그림 설명 | SciSpace (2절) |
| 개념 정의, 관련 개념, 대표 논문 개요 | SciSpace Find Topics (2절). Semantic Scholar Topic pages(A 문서) |
| 연구 기여 트리플 KG, 생성 방식(AI 여부) provenance, CC0 공개 데이터 | ORKG (5절) |
| AI 분야 task·method·benchmark 분류와 SOTA 리더보드 | 구 PwC†, paperswithcode.co (6, 8절) |
| 날짜 축 SOTA 추세 차트 | 구 PwC† (6절) |
| 선행/후속 논문 lineage 표시 | paperswithcode.co (8절) |
| 트렌딩 논문 피드와 코드·모델 링크 | HF Papers, paperswithcode.co, alphaXiv (7–9절) |
| 논문 구절 단위 토론, 오디오 요약, 읽기 상태 폴더 | alphaXiv (9절) |
| 정기 실행 리서치와 에이전트(MCP/API) 연동 | Elicit Routines·API·MCP, Consensus, scite, alphaXiv, Asta, HF (1, 3, 4, 7, 9, 10절) |

### 11.2 비어 있는 영역 (10개 행 전체에서 확인되지 않은 것)
- **(5) 명시적 선수관계 그래프**: 10/10 확인되지 않음입니다.
  - 가장 가까운 것은 구 PwC의 메서드 Components 관계입니다. 구성(has-part)이지 선수관계가 아니고, 공개 덤프에는 빠져 있습니다(6절).
- **(6) 학습자 상태에 따른 학습 경로 계획**: 10/10 확인되지 않음입니다. 개인화는 추천 피드(alphaXiv For You 등)까지만 있습니다.
- **(7) 지식·숙달 모델**: 확인되지 않았습니다. 최고 수준이 서재, 노트, 읽기 상태입니다.
- **(9) 실습·연습·피드백 루프(수학·알고리즘 랩)**: 확인되지 않았습니다. 최고 수준이 수식 설명(SciSpace)과 논문 Q&A입니다.
- **개념 단위 근거 사슬**: "개념 X는 논문 P에서 도입, Q에서 개선"을 인용문과 함께 보여 주는 구조는 확인되지 않았습니다.
  - 조각만 있습니다. 구 PwC 메서드 덤프는 도입 논문은 있지만 도입 연도(`introduced_year`)가 깨져 있고, 재개판 lineage는 근거가 비공개이며, ORKG는 값별 인용문이 없습니다.
- **로컬 우선**: 10개 모두 클라우드 서비스입니다. ORKG만 데이터(CC0)와 코드(MIT)를 공개해 자체 구축이 가능합니다(추론).

### 11.3 데이터 재사용 가능성과 제약

| 소스 | 얻을 수 있는 것 | 라이선스·약관 | AIXON 활용안 (추론) | 주의 |
|---|---|---|---|---|
| PwC 아카이브 (HF `pwc-archive`) | 논문 576,261, 논문–코드 링크 300,161, 데이터셋 15,008, 메서드 8,725행, 평가표(`paper_date` 포함) | CC BY-SA 4.0. 2025-07-28/29 고정 스냅샷 | 메서드 분류(area→collection) 시드, 2025-07까지의 벤치마크별 SOTA 타임라인 재구성 | ShareAlike 의무(파생 DB 배포 시). 스팸 대량 정제 필요. `introduced_year` 불신. Components 없음 |
| ORKG | 연구 문제 8,969, 기여 102,576, 비교 4,255, 템플릿 1,500, 벤치마크 1,706 | CC0 1.0(PwC 유래분은 CC BY-SA), 코드 MIT | 연구 문제–방법–벤치마크 연결 시드. `extraction_method` 같은 provenance 스키마 참고 | REST는 공식적으로 불안정 → 덤프·SPARQL 스냅샷 사용. 값별 인용문 없음 |
| HF Papers API | 일·주·월 트렌딩, 논문 메타, GitHub 저장소·스타, AI 키워드 | 공개 API이나 메타데이터 라이선스는 확인되지 않음 | 최신 트렌드 피드와 "코드 있음" 신호 | ID·링크 위주로 최소 저장 |
| paperswithcode.co | 리더보드, lineage, task·method(239/143) | 비문서화. 라이선스 확인되지 않음 | 링크로만 참조 | 의존 금지(지속성 불확실) |
| Asta Scientific Corpus Tool | 논문 검색, 발췌 스니펫, 인용 정보 | 비상업 연구용. 코퍼스 복사·수정 금지. attribution 의무 | 개인 연구 중 실시간 근거 조회 | 로컬 캐시·적재는 약관 위험 |
| Elicit / scite / Consensus API | 근거 달린 답변, 인용 문장, Meter | 유료(Elicit Pro+, scite Pro+), Consensus는 Team/Enterprise 승인제 | 선택형 외부 근거 공급자(커넥터) | 비용, 약관, 벤더 종속 |
| alphaXiv MCP | 논문 읽기, 페이지 단위 발췌, 코드 읽기 | 개인 사용. 스크래핑·데이터 수집 금지 | 개인 MCP 보조 도구 | 데이터 소스로 사용 불가 |
| Semantic Scholar | (A 문서 1절 참조) | 데이터셋별 라이선스(A 문서) | (A 문서) | (A 문서) |

### 11.4 데이터 품질과 지속성 리스크 (관측 사실)
- **서비스 급변**
  - PwC는 사전 공식 공지 없이 종료됐습니다(2차 보도, Wayback 관측).
  - Elicit은 2026-09-30에 핵심 도구 3종을 통합했습니다.
  - scite 도움말 센터는 도메인을 옮겼습니다.
- **문서 부패**: PwC 데이터 README는 아직도 "regenerated daily"라고 씁니다.
- **벤더 주장과 독립 평가의 간극**
  - scite 분류 정확도에 대한 독립 평가는 낮은 정확도를 보고했습니다(4절).
  - Asta 인용 구성은 같은 질의에서도 불안정했습니다(10절).
  - Elicit의 "often more accurate than humans"는 독립 검증되지 않았습니다.
- **공식 문서끼리의 불일치**: Consensus 프리프린트 기본 포함 여부, scite 커버리지 수치, SciSpace 무료 플랜 설명이 서로 다릅니다.

### 11.5 설계 시사점 (모두 추론)
1. **차별화 축을 좁힐 것**
   - 근거 달린 선수관계 DAG, 근거 달린 학습자 숙달 모델, 경로 계획, 개념 노드에 묶인 인터랙티브 랩, 로컬 우선. 이 다섯 가지가 이번 10개 행 어디에서도 확인되지 않은 영역입니다.
   - "근거 인용 답변", "논문 요약", "SOTA 추적", "트렌딩 피드"는 차별점으로 주장하지 않는 것이 맞습니다.
2. **간선 provenance 스키마는 ORKG를 참고할 것**: `extraction_method`(MANUAL / AUTOMATIC / AI_GENERATED / AI_GENERATED_WITH_MANUAL_REVIEW)와 `created_by`(사람 또는 서비스)를 두고, 여기에 Elicit·alphaXiv식 원문 앵커(인용문·페이지)를 더하면 ORKG의 빈칸(값별 인용문)까지 채우는 구조가 됩니다.
3. **시드 데이터 전략**
   - 메서드·task 분류: PwC 아카이브(정제 후) + ORKG 연구 문제.
   - 노드마다 라이선스(CC BY-SA / CC0)를 기록해 ShareAlike 범위를 관리합니다.
   - 2025-07 이후는 HF Papers나 paperswithcode.co를 링크로만 참조합니다.
4. **PwC Components는 선수관계 "후보"로만 쓸 것**: has-part를 prerequisite로 자동 변환하면 오류가 생깁니다. 사람 검토 상태(예: AI_GENERATED_WITH_MANUAL_REVIEW)를 거치도록 하는 편이 안전합니다. 다만 Components는 덤프에 없으므로 보관 페이지에서 얻어야 하는데, 이는 스크래핑 성격이라 별도 판단이 필요합니다.
5. **연구 진화 뷰**: 평가표의 `paper_date`로 벤치마크 SOTA 계단 그래프는 즉시 만들 수 있습니다. AIXON 고유 가치는 그 위에 "개념·방법 계보 간선 + 근거"를 얹는 데 있습니다.
6. **외부 유료 API는 선택형 커넥터로**: 핵심 데이터 경로는 CC0·CC BY-SA 스냅샷과 로컬 저장으로 두고, Elicit·scite·Consensus·Asta·alphaXiv는 MCP 커넥터 수준에 머무는 편이 로컬 우선 원칙과 약관 리스크 모두에 맞습니다.
7. **스냅샷 규율**: 외부 출처는 조회일, 버전, 원본 URL과 함께 저장합니다. PwC 종료와 Elicit 도구 통합처럼 출처가 사라지는 일이 실제로 있었습니다.

### 11.6 미확인 항목과 범위 메모
- 확인되지 않은 항목
  - Consensus 유료 금액과 법인명.
  - SciSpace API·데이터 라이선스.
  - alphaXiv Pro 가격.
  - Asta 요금.
  - HF Papers 메타데이터 라이선스와 Trending 산정식.
  - PwC 종료에 대한 Meta·HF 공식 공지 원문.
  - ORKG Ask 무료·로그인 요건.
  - scite 무료 계정의 기능 범위.
  - paperswithcode.co의 공식 API·라이선스.
- 범위 밖: 범용 소스 기반 학습 도구(예: NotebookLM 계열)는 이 문서에서 검증하지 않았습니다. 학습 기능(퀴즈 등) 비교가 필요하면 별도 조사가 필요합니다.
- A 문서와 판정이 다른 곳은 8절 paperswithcode.co의 (8)과 (10)입니다. 이유는 8절에 적었습니다. scite 판정은 A와 같습니다.

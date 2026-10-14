# A. 문헌 탐색·인용 그래프 도구 경쟁 분석 (AIXON 설계 문서용)

- 조사 기준일: 2026-10-15. 본문 모든 출처는 "확인 2026-10-15".
- 대상: Semantic Scholar, Connected Papers, ResearchRabbit, Litmaps, Inciteful, Open Knowledge Maps(OKM). 추가 2종은 scite, Papers with Code(2026년 재개판).
  - scite를 넣은 이유: 인용 문맥과 인용 성격(supporting/contrasting/mentioning)을 분류합니다. 기준 (8)의 직접 경쟁자입니다.
  - Papers with Code를 넣은 이유: AI 분야 전용 task/method/benchmark 구조를 갖췄고, 2026-05 재개판이 "paper lineage"(선행/후속 논문)를 표시합니다. AIXON의 AI 연구 계보 목표와 직접 겹칩니다.
- 판정 원칙
  - 공식 문서로 확인한 기능만 "지원" 또는 "부분 지원"으로 판정했습니다.
  - 공식 근거가 없으면 "확인되지 않음"입니다.
  - "미지원(공식 근거 있음)"은 공식 문서가 명시적으로 부정할 때만 씁니다. 이번 조사에서는 해당 셀이 없습니다.
- 표기
  - 2차 출처(대학 도서관 가이드, 블로그, 뉴스)는 **[2차]**로 표시했습니다.
  - 내 판단은 **(추론)**으로 표시했습니다.
  - JS로 렌더링되는 페이지(Connected Papers, Inciteful 앱)는 해당 사이트가 배포한 JS 번들 안의 문구로 확인했습니다. 각 절에 따로 적었습니다.

### 기준별 판정 규칙

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

---

## 0. 요약 표

| 제품 | (1) Literature Discovery | (2) Citation & Relationship Visualization | (3) Research Evolution | (4) Concept KG | (5) Prerequisite Graph | (6) Personalized Paths | (7) Persistent Learner State | (8) Evidence & Provenance | (9) Interactive Learning | (10) API/OSS/Data Reuse |
|---|---|---|---|---|---|---|---|---|---|---|
| Semantic Scholar | 지원 | 부분 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | **지원** |
| Connected Papers | 지원 | **지원** | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 확인되지 않음 | 부분 지원 |
| ResearchRabbit | 지원 | **지원** | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 확인되지 않음 | 부분 지원 |
| Litmaps | 지원 | **지원** | **지원** | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 확인되지 않음 | 부분 지원 |
| Inciteful | 지원 | **지원** | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 부분 지원 |
| Open Knowledge Maps | 지원 | 부분 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | **지원** |
| scite (추가) | 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | **지원** | 부분 지원 | **지원**(유료) |
| Papers with Code 재개판 (추가) | 지원 | 부분 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | **지원**(레거시 데이터) |

이 표에서 바로 보이는 점:
- (5) Prerequisite Graph, (6) Personalized Paths는 8개 제품 모두 "확인되지 않음"입니다.
- (7) Persistent Learner State는 "부분 지원"이 최고 판정입니다. 서재·평가 같은 활동 상태만 저장되고, 지식 숙달 모델을 갖춘 제품은 확인되지 않았습니다.
- (9) Interactive Learning도 "부분 지원"이 최고 판정입니다. 읽기 보조와 Q&A까지만 있고, 실습 랩은 확인되지 않았습니다.
- 반면 관계 시각화, 인용 근거 문장, 인용 의도 분류, 시간축 지도, 선행/후속 논문 구분은 이미 시장에 있습니다(9장 참조).

### 운영 주체·상태·요금 요약

| 제품 | 운영 주체 | 상태 (2026-10-15) | 개인 무료 | 개인 유료 |
|---|---|---|---|---|
| Semantic Scholar | Allen Institute for AI (Ai2) | 운영 중. 데이터셋 최신 릴리스 2026-10-06 | 웹 무료. 무료 계정으로 Library·Feeds·Alerts 사용. API는 무인증·무료 사용 가능(레이트 제한) | 유료 요금제는 확인되지 않음 |
| Connected Papers | Alex Tarnavsky Eitan, Eddie Smolyansky 등 창업자 팀(About 페이지 기준) | 운영 중. 공식 Python 클라이언트 2025-11-11 갱신 | 월 5개 그래프, 모든 기능 포함 | Academic / Business 플랜(그래프 무제한), 연간·분기 결제. 금액은 통화·지역별로 동적 표시돼 정적 확인 불가 |
| ResearchRabbit | Litmap Limited(사이트 저작권 표기). 2025-05 Litmaps가 인수했다는 보도 [2차] | 2025-10-20 대규모 개편. 프리미엄 RR+ 도입 | 시드 최대 50편, 인용 맵, 컬렉션, 공유, BibTeX 입출력 | RR+ US$12.50/월 또는 US$120/년. 국가별 할인 |
| Litmaps | Litmap Limited (뉴질랜드) | 운영 중. MCP(beta) 제공 | Basic search, 입력 최대 20편, 맵당 100편, Litmap 1–2개(페이지 내 표기 혼재), 월간 알림 | Pro: US$10/월(교육 라이선스·연간 결제, 학교 이메일 필요) 또는 US$120/년. 국가별 가격 |
| Inciteful | 개발자 M. Weishuhn의 개인 프로젝트(사이트 인용 안내 "Weishuhn, M." 기준) | 운영 중("still under active development") | 전부 무료("intend to keep free forever") | 없음(공식 About 기준) |
| Open Knowledge Maps | Open Knowledge Maps(빈 소재 비영리 단체. 2015년 Peter Kraker 창립, 2016년부터 등록 비영리) | 운영 중. 2026년 빈 시 기본 지원금 확보 | 공개 검색·지도 생성 | 개인 유료 요금제는 확인되지 않음. 기관 대상 Custom Services와 후원 회원 제도 있음 |
| scite | Scite LLC. Research Solutions 산하(인수 발표 2023-11-27) | 운영 중 | 7일 무료 체험(무료 플랜은 확인되지 않음) | Basic US$12/월(연간 결제), Pro US$40/월(연간 결제, API 포함) |
| Papers with Code | 구 paperswithcode.com은 Meta와 연계(보도 기준) [2차]. 재개판 paperswithcode.co는 Hugging Face 오픈소스 팀 Niels Rogge | 구 사이트는 2025-07 종료 [2차]. 현재 huggingface.co/papers/trending으로 302 리다이렉트(직접 확인). 재개판은 2026-05 공개 | 웹 접근 가능 | 요금 정보 확인되지 않음 |

---

## 1. Semantic Scholar (S2)

**한 줄 설명**: Ai2가 운영하는 무료 AI 기반 학술 검색 엔진입니다. 학술 그래프(S2AG) 위에서 TLDR, 인용 의도 분류, Highly Influential Citations, 개인화 피드, Semantic Reader, 공개 API·데이터셋을 제공합니다. 공식 문구: "Semantic Scholar is a free, AI-powered research tool for scientific literature, based at Ai2."

**운영 주체와 상태**
- 운영 주체는 The Allen Institute for Artificial Intelligence입니다. API License 계약 당사자 표기도 같습니다.
- 규모는 214 Million Papers, 2.49 Billion Citations, 79 Million Authors입니다(API 페이지).
- 데이터셋 최신 릴리스는 `2026-10-06`입니다.
- 관련 동향: Ai2는 2025-08-26 에이전트 플랫폼 Asta를 발표했습니다. 그 구성 요소인 Scientific Corpus Tool은 "MCP extension of the Semantic Scholar API"이며, 200M+ 논문 인덱스에 무료로 접근할 수 있습니다.

**무료와 유료**
- 웹 서비스는 무료이며 "Create Free Account"를 제공합니다.
- API는 무인증으로 쓸 수 있지만 "rate-limited to 1000 requests per second shared among all unauthenticated users"입니다.
- API 키를 받으면 "The introductory rate limit for an API key is 1 RPS on all endpoints"입니다.
- 유료 요금제는 확인되지 않았습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "Search over 214 million papers from all fields of science, with filters such as journals and conferences, authors, publication types, and date range." 서재 폴더 기반 Research Feeds와 Recommendations API도 제공합니다. | [product](https://www.semanticscholar.org/product), [api](https://www.semanticscholar.org/product/api) |
| 2 | Citation & Relationship Visualization | 부분 지원 | 논문 페이지에서 인용·참고문헌 목록을 볼 수 있고, 'Cites Results/Methods/Background' 필터와 Highly Influential 배지로 탐색합니다. 그래프 형태의 시각화는 공식 문서에서 확인되지 않았습니다. | [tutorials](https://www.semanticscholar.org/product/tutorials) |
| 3 | Research Evolution | 부분 지원 | Citation Velocity(최근 3년 인용의 가중 평균)와 Citation Acceleration(velocity의 변화) 지표가 있습니다. Research Feed는 최근 3개월 논문을 추천합니다. 시간축 계보 뷰는 확인되지 않았습니다. | [citation-velocity](https://www.semanticscholar.org/faq/citation-velocity), [citation-acceleration](https://www.semanticscholar.org/faq/citation-acceleration), [research-feeds-sources](https://www.semanticscholar.org/faq/research-feeds-sources) |
| 4 | Concept Knowledge Graph | 부분 지원 | Topic pages는 "Definition of the topic / Related topics / Papers often cited for this topic / Recent papers that mention this topic"를 보여 주며, "only topics in the Computer Science field are available"입니다. Field of Study 분류도 있습니다(논문당 최대 3개). 개념 간 관계는 "Related topics" 외에 유형화가 확인되지 않았습니다. | [what-are-topic-pages](https://www.semanticscholar.org/faq/what-are-topic-pages), [why-dont-i-see-topics…](https://www.semanticscholar.org/faq/why-dont-i-see-topics-for-a-paper-im-interested-in), [field-of-study](https://www.semanticscholar.org/faq/how-does-semantic-scholar-determine-a-papers-field-of-study) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | "Related topics"가 선수 관계라는 설명은 없습니다. | [what-are-topic-pages](https://www.semanticscholar.org/faq/what-are-topic-pages) |
| 6 | Personalized Learning Paths | 확인되지 않음 | 공식 FAQ·제품 페이지에 학습 경로 기능이 없습니다. | [faq](https://www.semanticscholar.org/faq) |
| 7 | Persistent Learner State | 부분 지원 | 계정에 영속 저장되는 활동 상태는 많습니다. Library 폴더, Research Feeds(서재 저장과 "not relevant" 평가를 신호로 학습), 4종 알림, Research Dashboard가 있습니다. Semantic Reader는 서재 논문을 주황, 서재 논문이 인용한 논문을 분홍으로 표시합니다. 학습자 지식·숙달 모델은 확인되지 않았습니다. | [what-are-research-feeds](https://www.semanticscholar.org/faq/what-are-research-feeds), [alert-types](https://www.semanticscholar.org/faq/alert-types), [what-are-personalized-citations](https://www.semanticscholar.org/faq/what-are-personalized-citations) |
| 8 | Evidence & Provenance | **지원** | 인용마다 `contexts`(인용 문장 스니펫), `intents`, `contextsWithIntent`, `isInfluential`을 API(`/paper/{id}/citations`)와 citations 데이터셋으로 제공합니다. 제약: "citation intent data is limited to papers for which we have access to the full text". | [graph swagger](https://api.semanticscholar.org/graph/v1/swagger.json), [citation-intent](https://www.semanticscholar.org/faq/citation-intent), [datasets release](https://api.semanticscholar.org/datasets/v1/release/latest) |
| 9 | Interactive Learning | 부분 지원 | Semantic Reader에 "Citations Cards … including TLDR summaries", "Definitions On-Demand"(용어 클릭 시 정의), Skimming(Goal/Method/Result 하이라이트), Hypothesis 주석이 있습니다. Ask This Paper는 논문 Q&A입니다. 연습문제나 실습 랩은 확인되지 않았습니다. | [semantic-reader](https://www.semanticscholar.org/product/semantic-reader), [product](https://www.semanticscholar.org/product) |
| 10 | API / OSS / Data reuse | **지원** | Academic Graph, Recommendations, Datasets API가 있습니다. 데이터셋 대부분은 ODC-BY이고 SPECTER 임베딩은 Apache 2.0입니다. API License에는 재판매·재배포 금지, attribution 의무, at-will 종료 조항이 있습니다(아래 상세). | [api](https://www.semanticscholar.org/product/api), [license](https://www.semanticscholar.org/product/api/license), [datasets release](https://api.semanticscholar.org/datasets/v1/release/latest) |

### 지정 검증 항목 상세

**TLDR**
- FAQ: "A TLDR is an AI-generated summarization for a scientific paper." "TLDRs are currently limited to the computer science and biomedical domains."
- 제품 페이지는 "available for nearly 60 million papers in computer science, biology, and medicine"이라고 합니다.
- 데이터셋 `tldrs`는 58M records이며 README에 "The model is based on the SciTLDR model"이라고 적혀 있습니다.
- 출처: [faq/tldr](https://www.semanticscholar.org/faq/tldr), [product](https://www.semanticscholar.org/product), [datasets release](https://api.semanticscholar.org/datasets/v1/release/latest)

**Semantic Reader**
- 제품 페이지 문구:
  - "Citations Cards that show details of a cited paper in-line where you're reading, including TLDR summaries"
  - "Table of Contents", "Save to Library"
  - Personalized In-line Citations
  - Skimming: "AI-generated highlighted overlays with 3 category labels: Goal, Method, and Result", "most English-language arXiv papers in computer science fields"
  - Definitions On-Demand: "click any term with a dotted underline and get an AI-generated definition based on its context in the paper"
  - Hypothesis 기반 하이라이트·노트
- 정의 생성 방식(FAQ): "we ask ChatGPT to provide a definition for the given term in the context it appears in". 정의 가능한 용어는 명사구를 추출한 뒤 규칙으로 필터링합니다.
- **상충**: 제품 페이지는 "now available for most arXiv papers"라고 하지만, FAQ는 "only available for papers that are published on ArXiv … 250k+ … papers"라고 합니다.
- 출처: [semantic-reader](https://www.semanticscholar.org/product/semantic-reader), [how-are-terms-defined…](https://www.semanticscholar.org/faq/how-are-terms-defined-in-the-semantic-reader), [which-terms-are-definable…](https://www.semanticscholar.org/faq/which-terms-are-definable-in-the-semantic-reader), [what-are-skimming-highlights](https://www.semanticscholar.org/faq/what-are-skimming-highlights), [reader availability FAQ](https://www.semanticscholar.org/faq/why-dont-i-see-an-option-to-read-this-paper-with-semantic-reader)

**Citation intent (인용 의도)**
- FAQ: "We categorize citation intents into three different types; Background, Method and Result Extension."
  - Background: "historical context, justification of importance, and/or additional information"
  - Method: "use the previously established procedures or experiments"
  - Result: "extend on findings from research that was previously conducted"
- 방법론 논문: "Structural Scaffolds for Citation Intent Classification in Scientific Publications".
- 전문(full text)이 있는 논문에만 적용됩니다.
- UI 표기는 'Cites Background / Cites Methods / Cites Results'입니다.
- API 예시 값은 `"methodology"`입니다(swagger).
- 출처: [citation-intent](https://www.semanticscholar.org/faq/citation-intent), [tutorials](https://www.semanticscholar.org/product/tutorials), [graph swagger](https://api.semanticscholar.org/graph/v1/swagger.json)

**Highly Influential Citations**
- FAQ: "Influential citations are determined utilizing a machine-learning model analyzing a number of factors including the number of citations to a publication, and the surrounding context for each."
- 참고 논문: "Identifying Meaningful Citations".
- 제약: "Identification as highly influential relies on our access to the full-text of the citing paper."
- API 필드는 `influentialCitationCount`와 `isInfluential`입니다.
- 출처: [influential-citations](https://www.semanticscholar.org/faq/influential-citations), [graph swagger](https://api.semanticscholar.org/graph/v1/swagger.json)

**Research Feeds**
- "adaptive research recommender". "We use a state-of-the-art paper embedding model trained using contrastive learning to find papers similar to those in each Library folder."
- 서재 저장이 positive 신호이고, "not relevant" 평가가 negative 신호입니다.
- 추천 대상은 최근 3개월 논문이며 매일 갱신됩니다.
- 출처: [what-are-research-feeds](https://www.semanticscholar.org/faq/what-are-research-feeds), [fine-tune-research-feeds](https://www.semanticscholar.org/faq/fine-tune-research-feeds), [feed-refresh](https://www.semanticscholar.org/faq/feed-refresh)

**Library와 Alerts**
- Library: 폴더 정리, bulk export, 공유 폴더(복사 가능), 폴더별 Research Feed.
- Alerts 4종: Author Alerts, Paper Alerts, Topic Alerts, Research Feed Alerts.
- 출처: [library-benefit](https://www.semanticscholar.org/faq/library-benefit), [alert-types](https://www.semanticscholar.org/faq/alert-types), [product](https://www.semanticscholar.org/product)

**Academic Graph API와 Datasets API**
- 서비스 구성
  - Academic Graph: authors, papers, citations, venues, SPECTER2 embeddings.
  - Recommendations.
  - Datasets: 다운로드 링크 제공.
- `/snippet/search`: 제목·초록·본문에서 약 500단어 발췌를 검색합니다. 그림 캡션과 참고문헌은 제외됩니다.
- Datasets 릴리스 README:
  - "Downloading the full data requires an API key."
  - 데이터셋 목록: `papers`(200M), `abstracts`(100M), `citations`(2.4B, "influential classification, intent classification, and citation context" 포함), `tldrs`(58M), `s2orc`/`s2orc_v2`(전문), `embeddings-specter_v1/v2`, `authors`, `publication-venues`, `paper-ids`.
- 출처: [api](https://www.semanticscholar.org/product/api), [graph swagger](https://api.semanticscholar.org/graph/v1/swagger.json), [datasets release](https://api.semanticscholar.org/datasets/v1/release/latest)

**라이선스와 약관**
- 데이터셋별 README
  - papers/abstracts/citations/tldrs/s2orc/authors/venues/paper-ids: "This collection is licensed under ODC-BY."
  - SPECTER v1/v2 임베딩: "released under the Apache 2.0 license"
  - 사용 시 "The Semantic Scholar Open Data Platform" 등 해당 논문 인용을 요청합니다.
- API License Agreement("Last updated: May 17, 2023")
  - API 이용권은 "limited, non-exclusive, non-transferable, non-sublicensable and terminable"입니다.
  - S2 Data는 "separately governed by the licenses that accompany such S2 Data, such as CC BY-NC or ODC-BY"입니다.
  - "Semantic Scholar" attribution과 Open Data Platform 논문 인용이 의무입니다.
  - 금지 조항에 "repackage, sell, rent, lease, lend, distribute, or sublicense the API"가 포함됩니다.
  - 이용은 "at will"이라 AI2가 언제든 종료할 수 있습니다.
  - API 전체 종료 시에는 대체 제공 또는 60일 전 고지를 약속합니다.
- 출처: [datasets release](https://api.semanticscholar.org/datasets/v1/release/latest), [license](https://www.semanticscholar.org/product/api/license)

### 관계 산출 방식 (공식 설명 그대로)
- 인용 관계: 논문 bibliography에서 citingPaper→citedPaper를 연결합니다(citations 데이터셋 정의).
- Influential 판정: ML 모델이 인용 수와 각 인용의 주변 문맥을 분석합니다(위 FAQ).
- 인용 의도: Background / Method / Result Extension 3범주(Structural Scaffolds 논문).
- 유사 논문: contrastive learning 기반 논문 임베딩(Research Feeds). Recommendations API.
- Topic pages: "We use large language models (LLMs) to extract a list of topics from the title and abstract of a paper." 정의는 "the single most cited paper for a topic"의 스니펫으로 생성합니다([how-are-topic-pages-generated](https://www.semanticscholar.org/faq/how-are-topic-pages-generated)).
- Ask This Paper: "We query OpenAI's gpt3.5-turbo-16k with the content of the current paper alongside your question." 답변과 함께 근거 문장을 표시합니다([how-are-questions-answered…](https://www.semanticscholar.org/faq/how-are-questions-answered-by-paper-question-answering)).

### 이미 잘 해결한 것 (AIXON이 차별점으로 주장하면 안 됨)
- 대규모 무료 코퍼스 검색, TLDR 요약(약 60M 편).
- 인용 문맥 문장 + 인용 의도 3범주 + 영향력 인용 판별. UI, API, bulk 데이터(ODC-BY)로 모두 제공됩니다.
- 서재 기반 개인화 피드, 4종 알림, 대시보드.
- 읽는 중 인용 카드, 용어 정의, 스키밍 하이라이트, 논문 Q&A.
- CS 분야 토픽 페이지(정의, 관련 토픽, 자주 인용된 논문).
- 공개 API와 MCP 확장(Asta).

### AIXON 목표 대비 공백
- 인용 의도가 3범주로 거칩니다. EXTENDS / ADAPTS / IMPROVES_ON 같은 계보 타입은 확인되지 않았습니다. 의도·영향 라벨은 전문 접근이 가능한 논문에만 있습니다.
- 그래프 시각화와 시간축 계보 뷰가 확인되지 않았습니다.
- Topic pages는 CS 한정이고 개념 간 선수 관계가 없습니다(확인되지 않음).
- 학습자 지식 상태, 학습 경로, 실습 랩이 확인되지 않았습니다.
- API 재배포 금지와 at-will 종료 조항 때문에, AIXON이 S2 데이터를 캐시하거나 배포할 때 데이터 라이선스(ODC-BY 등)와 API 약관을 따로 검토해야 합니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://www.semanticscholar.org/product
- https://www.semanticscholar.org/product/api
- https://www.semanticscholar.org/product/api/license
- https://www.semanticscholar.org/product/semantic-reader
- https://www.semanticscholar.org/product/tutorials
- https://www.semanticscholar.org/faq (및 하위 faq/tldr, faq/citation-intent, faq/influential-citations, faq/citation-velocity, faq/citation-acceleration, faq/what-are-research-feeds, faq/fine-tune-research-feeds, faq/research-feeds-sources, faq/feed-refresh, faq/alert-types, faq/library-benefit, faq/research-dashboard, faq/what-are-topic-pages, faq/how-are-topic-pages-generated, faq/why-dont-i-see-topics-for-a-paper-im-interested-in, faq/how-are-terms-defined-in-the-semantic-reader, faq/which-terms-are-definable-in-the-semantic-reader, faq/what-are-skimming-highlights, faq/what-are-personalized-citations, faq/why-dont-i-see-an-option-to-read-this-paper-with-semantic-reader, faq/how-are-questions-answered-by-paper-question-answering, faq/how-does-semantic-scholar-determine-a-papers-field-of-study, faq/open-data)
- https://api.semanticscholar.org/graph/v1/swagger.json
- https://api.semanticscholar.org/recommendations/v1/swagger.json
- https://api.semanticscholar.org/datasets/v1/release/latest
- https://allenai.org/blog/asta

---

## 2. Connected Papers

**한 줄 설명**: origin 논문 하나(또는 여러 개)를 넣으면 유사도 기반의 시각적 논문 그래프를 만들어 주는 도구입니다. 공식 문구: "a unique, visual tool to help researchers and applied scientists find and explore papers relevant to their field of work".

**운영 주체와 상태**
- About 페이지에 창업자 Alex Tarnavsky Eitan, Eddie Smolyansky, Itay Knaan Harpaz, Sahar Perets가 소개돼 있습니다.
- 운영 중입니다. 공식 Python 클라이언트가 2025-11-11 v0.2.5로 갱신됐습니다.
- 2021-02 뉴스레터에서 arXiv 연동(arXiv 논문 페이지에서 그래프 링크)을 발표했습니다.
- 2022-08-01부터 Free/Premium 계정 체계를 시행했습니다.

**무료와 유료**
- FAQ: "Our free tier includes all of the features and provides you with 5 Connected Papers graphs for free, every month."
- Premium은 "unlimited amount of Connected Papers graphs every month"입니다.
- Academic 플랜은 "For academics, non-profits and personal use", Business 플랜은 "For business and industry"입니다.
- 결제는 연간 또는 분기 단위입니다. 금액은 통화별로 동적으로 로드돼 정적 확인이 불가능합니다.
- 모든 플랜에 "Connected Papers similarity graphs, Prior and derivative works, Multi-origin graphs, Saved papers, Graph history"가 포함됩니다.

> 확인 방법: connectedpapers.com의 About·Pricing·그래프 안내 문구는 JS 렌더링이라, 사이트가 배포한 JS 번들(`/assets/index-*.js`)에 들어 있는 원문으로 확인했습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "To create each graph, we analyze an order of ~50,000 papers and select the few dozen with the strongest connections to the origin paper." | [about](https://www.connectedpapers.com/about) |
| 2 | Citation & Relationship Visualization | **지원** | Force Directed Graph로 유사 논문을 군집화합니다. "Node size is the number of citations", "Node color is the publishing year". 공식 문구로 "Connected Papers is not a citation tree"입니다. 즉 인용 트리가 아니라 유사도 그래프입니다. | [about](https://www.connectedpapers.com/about), [그래프 안내 문구](https://www.connectedpapers.com/) |
| 3 | Research Evolution | 부분 지원 | 노드 색이 출판연도입니다. Prior works(고전)와 Derivative works(서베이·최신 후속)로 시간 방향을 구분합니다. Graph history는 "the graphs for each paper change and evolve over time"이라 이전 버전 그래프를 보여 줍니다. 시간축 배치는 확인되지 않았습니다. | [about](https://www.connectedpapers.com/about), [newsletter #2](https://connectedpapers.substack.com/p/connected-papers-newsletter-2-21-02-10) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | 공식 설명은 논문 간 유사도뿐입니다. | [about](https://www.connectedpapers.com/about) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | Prior works에 "it could be a good idea to get familiar with them"이라는 읽기 권고가 있을 뿐, 명시적 선수 간선은 없습니다. | [about](https://www.connectedpapers.com/about) |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | [pricing](https://www.connectedpapers.com/pricing) |
| 7 | Persistent Learner State | 부분 지원 | 2022년 User Accounts와 함께 저장 논문 목록과 그래프 히스토리가 추가됐습니다. 학습자 모델은 확인되지 않았습니다. | [premium 발표](https://connectedpapers.substack.com/p/announcing-premium-accounts-multi-22-07-28) |
| 8 | Evidence & Provenance | 부분 지원 | 유사도 산출 원리(Co-citation, Bibliographic Coupling)를 공개합니다. Prior works에서 하나를 선택하면 "highlight all graph papers referencing it"입니다. 두 논문 간 공유 참고문헌 목록이나 인용 문맥 표시는 확인되지 않았습니다. | [about](https://www.connectedpapers.com/about) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | 부분 지원 | 공식 Python 클라이언트 `connectedpapers-py`(MIT)가 있습니다. "Contact us at hello@connectedpapers.com to get an early-access access token". 그래프 데이터 재배포 조건은 확인되지 않았습니다. 기반 데이터는 "Semantic Scholar Paper Corpus (licensed under ODC-BY)"입니다. | [PyPI](https://pypi.org/project/connectedpapers-py/), [GitHub](https://github.com/ConnectedPapers/connectedpapers-py/), [about](https://www.connectedpapers.com/about) |

### 그래프 구성 방법과 Prior/Derivative works (공식)
- 후보와 선택: 그래프마다 약 50,000편을 분석해 origin과 연결이 가장 강한 수십 편을 고릅니다.
- 유사도: "Our similarity metric is based on the concepts of Co-citation and Bibliographic Coupling. According to this measure, two papers that have highly overlapping citations and references are presumed to have a higher chance of treating a related subject matter."
- 직접 인용이 없어도 연결됩니다: "even papers that do not directly cite each other can be strongly connected".
- 배치: Force Directed Graph. 노드를 선택하면 "highlight the shortest path from each node to the origin paper in similarity space".
- **Prior works**: "These are papers that were most commonly cited by the papers in the graph. This usually means that they are important seminal works for this field…"
- **Derivative works**: "These are papers that cited many of the papers in the graph. This usually means that they are either surveys of the field or recent relevant works which were inspired by many papers in the graph."
- Multi-origin graphs(2022-07 발표): 노드를 두 번째 origin으로 추가하면 모든 origin과 유사한 논문 쪽으로 결과가 좁혀집니다.
- API 그래프 캐시: 그래프가 1개월보다 오래되면 재빌드됩니다("A graph build can take up to 1 minute").
- 데이터 출처: S2 API 페이지에 공동창업자 증언 "Since day 1 Connected Papers has been built on top of the Semantic Scholar Open Corpus and APIs"가 있습니다([S2 api](https://www.semanticscholar.org/product/api)).

### 이미 잘 해결한 것 (차별점으로 주장 금지)
- 직접 인용이 없는 논문까지 잇는 유사도 그래프의 즉시 생성.
- "먼저 익힐 고전(Prior)"과 "후속·서베이(Derivative)" 구분 목록.
- 다중 origin.
- 그래프 버전 히스토리.
- arXiv 연동.

### AIXON 목표 대비 공백
- 간선이 유사도 하나뿐이고 타입이 없습니다. 개별 간선의 근거(공유 참고문헌, 인용 문장)는 확인되지 않았습니다.
- 개념, 선수지식, 학습자 모델, 실습이 확인되지 않았습니다.
- 무료는 월 5개 그래프로 제한되고, API는 early access입니다.

### 출처 (모두 확인 2026-10-15)
- https://www.connectedpapers.com/about (JS 번들 원문으로 확인)
- https://www.connectedpapers.com/pricing (JS 번들 원문으로 확인)
- https://www.connectedpapers.com/
- https://connectedpapers.substack.com/p/announcing-premium-accounts-multi-22-07-28
- https://connectedpapers.substack.com/p/connected-papers-newsletter-2-21-02-10
- https://pypi.org/project/connectedpapers-py/ (메타데이터: https://pypi.org/pypi/connectedpapers-py/json)
- https://github.com/ConnectedPapers/connectedpapers-py/
- https://www.semanticscholar.org/product/api

---

## 3. ResearchRabbit

**한 줄 설명**: 시드 논문에서 Similar / Earlier / Later Work를 반복적으로 따라가는("rabbit hole") 인용 네트워크 기반 탐색 도구입니다. 컬렉션, 저자 네트워크, 인용 맵을 제공합니다.

**운영 주체와 상태 (2024–2026 변화)**
- **소유권**
  - 2025-05-08 보도: "New Zealand-based Litmaps has acquired US research tool ResearchRabbit" [2차: IT Brief NZ].
  - 현재 researchrabbit.ai 하단 표기는 "Copyright © Litmap Limited. 2016-2026."입니다.
  - 공식 도움말은 관계를 "partnership with Litmaps"로 표현합니다.
- **개편**
  - 공식 도움말 "Welcome to the new ResearchRabbit!"(2025-10-17 작성): "The update rolled out on October 20, 2025 (EST)."
  - 변경 내용: 새 검색바, 반복 검색, 컬렉션과 분리된 검색, DB 확장("over 280 million … SemanticScholar, Crossref, and OpenAlex"), 내장 노트, 프리미엄 RR+.
  - 2026-06 기준 DB는 "310+ million"입니다.
  - Aaron Tay 블로그는 출시를 2025-10-30으로 적어 공식 날짜와 상충합니다 [2차].
- 사용자 규모: "Trusted by 1,000,000+ researchers worldwide"(홈페이지).

**무료와 유료**
- Free Tier: "with up to 50 starting articles", 인용·참고·유사 논문 탐색, "Visualisation of how articles connect using citation maps", 컬렉션·하위 컬렉션, Zotero Importer, 공유, BibTeX 입출력, 노트·스티커·색상.
- RR+: Advanced Search 필터(키워드, 출판일, SJR 분위, 저널 h-index, OA, 철회 여부), 최대 300편 시드, 다중 프로젝트.
- RR+ 가격: "$12.50 USD / month; or $120 USD / year". 국가별 할인이 있습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | 시드(키워드·DOI·제목·가져오기)에서 "Find Related Articles"(Similar Work)를 찾고, 결과를 다시 시드로 넣는 반복 탐색을 지원합니다. | [similar work](https://learn.researchrabbit.ai/en/articles/12454538-how-do-i-search-similar-work-in-the-new-researchrabbit) |
| 2 | Citation & Relationship Visualization | **지원** | "Visualize networks of research and authors."라고 설명합니다. 인용·참고문헌을 "as a list and visualization"으로 보여 줍니다. | [welcome](https://learn.researchrabbit.ai/en/articles/12440130-welcome-to-the-new-researchrabbit), [citations & references](https://learn.researchrabbit.ai/en/articles/12454564-how-do-i-see-citations-and-references-in-the-new-researchrabbit) |
| 3 | Research Evolution | 부분 지원 | 공식 기능은 "Earlier Work"(참고문헌, 더 이전)와 "Later Work"(인용, 더 이후), 그리고 RR+ 출판일 필터입니다. 신규 그래프의 기본 축이 x=출판연도, y=인용수라는 설명은 2차 출처뿐입니다 [2차: Aaron Tay]. | [earlier work](https://learn.researchrabbit.ai/en/articles/12454543-how-do-i-search-earlier-work-in-the-new-researchrabbit), [later work](https://learn.researchrabbit.ai/en/articles/12454547-how-do-i-search-later-work-in-the-new-researchrabbit), [Aaron Tay](https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | 공식 알고리즘 설명은 논문·저자 연결뿐입니다. | [algorithm](https://learn.researchrabbit.ai/en/articles/12875619-what-s-behind-researchrabbit-s-search-algorithm) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | RR+ 마케팅 문구 "Target foundational articles to develop an understanding of your field"는 필터 활용법이지 선수 그래프가 아닙니다. | [what is RR+](https://learn.researchrabbit.ai/en/articles/12454495-what-is-researchrabbit) |
| 6 | Personalized Learning Paths | 확인되지 않음 | 교육용 안내 문서는 있으나 개인화 경로는 없습니다. | [teaching](https://learn.researchrabbit.ai/en/articles/16424258-using-researchrabbit-in-your-teaching-and-supervision) |
| 7 | Persistent Learner State | 부분 지원 | 컬렉션, 노트, 스티커, 프로젝트가 계정에 저장됩니다. 홈페이지는 "With every search, ResearchRabbit learns"라고 주장합니다. 지식 상태 모델은 확인되지 않았습니다. | [free tier](https://learn.researchrabbit.ai/en/articles/12865509-researchrabbit-free-tier), [home](https://www.researchrabbit.ai/) |
| 8 | Evidence & Provenance | 부분 지원 | 연결 유형(인용, 공유 참고·인용, 공저, 의미 유사도)과 랭킹 원리를 공개합니다. 인용 문맥이나 의도 표시는 확인되지 않았습니다. 랭킹은 "currently fixed and cannot be fine-tuned"입니다. | [algorithm](https://learn.researchrabbit.ai/en/articles/12875619-what-s-behind-researchrabbit-s-search-algorithm) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | 부분 지원 | BibTeX / RIS / CSV 가져오기, BibTeX 내보내기, Zotero Importer를 제공합니다. 공개 API는 확인되지 않았습니다. "We don't train AI models using your articles or notes." | [similar work](https://learn.researchrabbit.ai/en/articles/12454538-how-do-i-search-similar-work-in-the-new-researchrabbit), [free tier](https://learn.researchrabbit.ai/en/articles/12865509-researchrabbit-free-tier), [data](https://learn.researchrabbit.ai/en/articles/12796770-data-responsibility-tldr) |

### 관계 산출 방식 (공식)
- 후보 선정에서 "connected"의 의미:
  - "Most commonly … one cites the other"
  - "share a reference or citation"
  - "shared authors, or co-authorships"
  - "Sometimes … semantic similarity of their titles and/or abstracts"
- 랭킹: "Relevance is measured in connectedness"입니다. 공유 인용·참고, 공저, 의미 유사도를 섞어 점수를 매기며 사용자가 조정할 수 없습니다.
- 네트워크 범위: "first-degree and second-degree connections". "ResearchRabbit does not use large language models to power its core recommendation algorithms."
- 영향력: "influence comes from both the number and quality of citations"([how it works](https://learn.researchrabbit.ai/en/articles/12454660-how-does-researchrabbit-work)).
- 출처: [algorithm](https://learn.researchrabbit.ai/en/articles/12875619-what-s-behind-researchrabbit-s-search-algorithm), [AI 사용](https://learn.researchrabbit.ai/en/articles/13545485-how-researchrabbit-uses-ai-and-where-we-don-t)

### 이미 잘 해결한 것 (차별점으로 주장 금지)
- 반복 시드 확장 탐색.
- Earlier / Later / Similar 구분.
- 저자 네트워크.
- 컬렉션 공유와 노트.
- 투명한 비-LLM 알고리즘 설명.
- 넉넉한 무료 티어.

### AIXON 목표 대비 공백
- 간선 타입과 근거 텍스트가 확인되지 않았습니다.
- 개념·선수지식·학습 기능이 확인되지 않았습니다.
- API가 확인되지 않았습니다.
- Litmaps와 같은 법인, 같은 데이터 공급원(S2/Crossref/OpenAlex)이라 두 제품의 기능이 수렴할 가능성이 큽니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://learn.researchrabbit.ai/en/articles/12440130-welcome-to-the-new-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12454605-the-researchrabbit-database
- https://learn.researchrabbit.ai/en/articles/12865509-researchrabbit-free-tier
- https://learn.researchrabbit.ai/en/articles/12454495-what-is-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12875619-what-s-behind-researchrabbit-s-search-algorithm
- https://learn.researchrabbit.ai/en/articles/12454660-how-does-researchrabbit-work
- https://learn.researchrabbit.ai/en/articles/13545485-how-researchrabbit-uses-ai-and-where-we-don-t
- https://learn.researchrabbit.ai/en/articles/12454538-how-do-i-search-similar-work-in-the-new-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12454543-how-do-i-search-earlier-work-in-the-new-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12454547-how-do-i-search-later-work-in-the-new-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12454564-how-do-i-see-citations-and-references-in-the-new-researchrabbit
- https://learn.researchrabbit.ai/en/articles/12796770-data-responsibility-tldr
- https://learn.researchrabbit.ai/en/articles/16424258-using-researchrabbit-in-your-teaching-and-supervision
- https://www.researchrabbit.ai/ , https://www.researchrabbit.ai/privacy-policy (하단 "Copyright © Litmap Limited")
- [2차] https://itbrief.co.nz/story/litmaps-acquires-researchrabbit-raises-1-million-for-ai (2025-05-08)
- [2차] https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative (2025-11-02)

---

## 4. Litmaps

**한 줄 설명**: 인용·참고 관계로 연결된 문헌 지도("Litmap")를 축 선택형 2D 지도로 보여 주는 탐색·모니터링 도구입니다. 공식 문구: "A Litmap … visualizes scientific articles based on how they connect via citations and references."

**운영 주체와 상태**
- 운영 주체는 Litmap Limited입니다(가격 페이지 하단 표기). 뉴질랜드 기업입니다 [2차: IT Brief].
- 2025년 ResearchRabbit를 인수했습니다(위 3절).
- DB는 "270+ million"이고, Crossref·Semantic Scholar·OpenAlex에서 가져오며 매주 갱신합니다.
- MCP(beta)를 제공합니다. 문서 표기가 "Updated this week"이므로 2026-10 기준 최신 갱신입니다. 최초 공개일은 확인되지 않았습니다.
- S2 API 페이지에 Litmaps CTO의 S2 API·bulk data 사용 증언이 있습니다.

**무료와 유료**
- 가격 페이지 Free: "Basic Search", "Up to 20 inputs", "100 articles per Map", Litmap 수는 "2 Litmaps"와 "1 Litmap" 표기가 혼재합니다. 알림은 "Monthly (summary)"입니다.
- Pro: "$10 / month"(연간 결제, "*requires academic email address"), "$120 / year - save 20%". 무제한이며 Advanced Search와 Daily·Weekly 알림이 포함됩니다.
- Pro 문서: 교육 라이선스는 상용가 대비 75% 할인입니다. 국가별 parity pricing을 적용합니다. Team 플랜이 있습니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | 시작 논문으로 "Explore Related Articles"를 실행합니다. 알고리즘 3종과 필터를 제공합니다. | [create](https://docs.litmaps.com/en/articles/9057179-create-a-litmap), [algorithms](https://docs.litmaps.com/en/articles/9029858-search-algorithms-in-litmaps) |
| 2 | Citation & Relationship Visualization | **지원** | "Dots represent articles, and lines represent connection." 표시 방식은 Standard / Ring / Side by Side / By Author 네 가지입니다. | [visualization](https://docs.litmaps.com/en/articles/9181490-use-and-edit-litmaps-visualization) |
| 3 | Research Evolution | **지원** | X·Y축을 Cite Count, Ref Count, **Publication Date**, Momentum, Map Connectivity 중에서 고릅니다. 공식 활용표: "High-impact work: X-axis Date / Y-axis Citation Count", "Review papers: Date / Reference Count". 계보 타입은 없습니다(아래 공백 참조). | [visualization](https://docs.litmaps.com/en/articles/9181490-use-and-edit-litmaps-visualization) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | Tags는 사용자 정리용 컬렉션이지 개념 그래프가 아닙니다. | [tags](https://docs.litmaps.com/en/articles/9029278-save-articles-with-tags-in-litmaps) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | "Literature Review Course with Litmaps" 같은 교육 자료는 있으나 개인화 경로는 확인되지 않았습니다. | [intro](https://docs.litmaps.com/en/articles/7240465-introduction-to-litmaps) |
| 7 | Persistent Learner State | 부분 지원 | Workspaces, Tags, Monitor(저장된 검색으로 신규 논문 알림. 무료 사용자도 이용 가능, 설정 변경은 Pro), Zotero Sync가 있습니다. 학습자 모델은 확인되지 않았습니다. | [monitor](https://docs.litmaps.com/en/articles/9126249-monitor-get-alerts-for-important-research), [pro](https://docs.litmaps.com/en/articles/8115278-litmaps-pro) |
| 8 | Evidence & Provenance | 부분 지원 | 선은 인용·참고 연결이고, Map Connectivity는 "number of citations within this map"입니다. 사용자가 "add or remove citations" 할 수 있습니다. 인용 문맥·의도 표시는 확인되지 않았습니다. | [visualization](https://docs.litmaps.com/en/articles/9181490-use-and-edit-litmaps-visualization) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | 부분 지원 | MCP(beta) `https://mcp.litmaps.com/mcp`로 AI 어시스턴트가 Litmap·Tag를 만들고 논문을 추가·삭제할 수 있습니다. BibTeX 내보내기와 Zotero Sync를 제공합니다. 공개 개발자 API와 데이터 라이선스는 확인되지 않았습니다. | [MCP](https://docs.litmaps.com/en/articles/17508256-use-litmaps-with-your-ai-assistant-mcp), [export](https://docs.litmaps.com/en/articles/9092828-export-articles-from-litmaps) |

### 지정 검증: 시간축과 y축
- 공식 문서는 축을 고정하지 않고 선택형으로 둡니다.
  - Publication Date: "The date the article was published."
  - Cite Count: "The article's number of citations."
  - Ref Count: "The article's number of references"
  - Momentum: "Cited Count adjusted for recency of publication"
  - Map Connectivity: "The article's number of citations within this map … used to be called Map Relevance"
- 공식 활용표가 x=Date와 y=Citation Count, Reference Count, Map Connectivity를 짝지어 권장합니다. 따라서 **x축을 출판일 시간축으로 쓰는 것은 공식 기능**입니다.
- **기본값**(x=publication date, y=no. of citations)은 공식 문서에 명시돼 있지 않습니다. HKUST 도서관 가이드(2026-01-08 갱신)에는 "default: x: publication date, y: no. of citations"로 적혀 있습니다 [2차].
  - 같은 가이드는 기본 노드 크기를 "no. of references"라고 하지만, 다른 2차 자료는 인용수라고 해 상충합니다.
  - Litmaps 홈페이지에 게재된 사용자 후기에도 "date vs cite graph format"이라는 표현이 있습니다.
- 출처: [visualization](https://docs.litmaps.com/en/articles/9181490-use-and-edit-litmaps-visualization), [HKUST guide](https://libguides.hkust.edu.hk/citation-chaining/litmaps), [home](https://www.litmaps.com/)

### 관계 산출 방식 (공식)
- **Shared Citations & References** (기본값): "For a single input article, Litmaps returns the most interconnected articles from among your paper's citations, references and co-citations (co-citations are all the citations of the references)." 입력이 여러 편이면 전체 입력의 인용·참고 중 가장 상호연결된 논문을 고릅니다.
- **Common Authors**: 입력 논문들의 공저 그룹이 낸 다른 논문을 찾습니다.
- **Similar Text**: "AI-driven semantic analysis on the titles and abstracts". "the only algorithm that does not use citations/references".
- 출처: [algorithms](https://docs.litmaps.com/en/articles/9029858-search-algorithms-in-litmaps)

### 이미 잘 해결한 것 (차별점으로 주장 금지)
- 출판일 시간축 위의 인용 지도. "연구 흐름을 시간에 따라 본다"는 시각화 자체는 이미 있습니다.
- Momentum(최신성 보정 인용).
- 알고리즘 3종 선택.
- 지도 주석·사용자 편집.
- 저장 검색 기반 모니터링 알림.
- MCP를 통한 AI 어시스턴트 연동.

### AIXON 목표 대비 공백
- 간선은 인용 연결 하나뿐이고 타입·근거 문장이 없습니다(확인되지 않음).
- 개념 그래프, 선수지식, 학습자 모델, 실습이 확인되지 않았습니다.

### 출처 (모두 확인 2026-10-15)
- https://docs.litmaps.com/en/articles/9181490-use-and-edit-litmaps-visualization
- https://docs.litmaps.com/en/articles/9029858-search-algorithms-in-litmaps
- https://docs.litmaps.com/en/articles/7240465-introduction-to-litmaps
- https://docs.litmaps.com/en/articles/9057179-create-a-litmap
- https://docs.litmaps.com/en/articles/7212085-litmaps-database-coverage-open-access-and-article-indexing
- https://docs.litmaps.com/en/articles/9126249-monitor-get-alerts-for-important-research
- https://docs.litmaps.com/en/articles/8115278-litmaps-pro
- https://docs.litmaps.com/en/articles/17508256-use-litmaps-with-your-ai-assistant-mcp
- https://docs.litmaps.com/en/articles/9029278-save-articles-with-tags-in-litmaps
- https://docs.litmaps.com/en/articles/9092828-export-articles-from-litmaps
- https://www.litmaps.com/pricing , https://www.litmaps.com/
- https://www.semanticscholar.org/product/api
- [2차] https://libguides.hkust.edu.hk/citation-chaining/litmaps
- [2차] https://itbrief.co.nz/story/litmaps-acquires-researchrabbit-raises-1-million-for-ai

---

## 5. Inciteful

**한 줄 설명**: 시드 논문 주변의 깊이 2 인용 네트워크를 즉석으로 만든 뒤 네트워크 분석(PageRank, link prediction)으로 중요·유사 논문을 찾아 주는 무료 도구입니다. 두 논문 사이 인용 경로를 찾는 Literature Connector도 있습니다.

**운영 주체와 상태**
- 개발자 개인 프로젝트입니다. 사이트 인용 안내 문구가 "Weishuhn, M. … Inciteful: Citation network exploration"입니다.
- About: "It's still under active development".
- GitHub README: "This is a personal project that I intend to keep free forever."
- 웹 프론트엔드 저장소는 "the front end of Academic version of IncitefulMed.com"이라고 적혀 있습니다. IncitefulMed는 환자 대상 의료 문헌 서비스입니다.

**무료와 유료**: 전부 무료입니다. About 원문: "As this is built upon the back of data that I received for free, it feels like bad karma to charge for the service."

> 확인 방법: inciteful.xyz 앱 페이지(`/about`, `/data`, `/beta`)는 JS 렌더링이라 사이트 JS 번들 원문으로 확인했습니다. 문서 사이트(incitefulmed.com/academic/help)는 정적 HTML입니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Paper Discovery는 "find the most similar papers, important papers as well as prolific authors and institutions"입니다. | [getting started](https://incitefulmed.com/academic/help/) |
| 2 | Citation & Relationship Visualization | **지원** | 인용 네트워크 그래프를 보여 줍니다. Literature Connector는 "an interactive visualization showing you how they are connected by the literature"입니다. | [getting started](https://incitefulmed.com/academic/help/), [connector](https://incitefulmed.com/academic/help/literature-connector-explained.html) |
| 3 | Research Evolution | 부분 지원 | 연도 필터가 있습니다. 문서는 Important(PageRank)가 오래된 논문 쪽으로, Similarity가 최신 논문 쪽으로 기운다고 공식 설명합니다. 시간축 시각화는 확인되지 않았습니다. | [paper discovery](https://incitefulmed.com/academic/help/paper-disovery-explained.html), [power users](https://incitefulmed.com/academic/help/power-users.html) |
| 4 | Concept Knowledge Graph | 확인되지 않음 | 제목 키워드 클라우드와 `title_terms` 테이블만 있습니다. 문서: "we do not have access to abstracts at this point". | [power users](https://incitefulmed.com/academic/help/power-users.html) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | "Important Papers"는 "a good place to start when trying to understand the foundations of a topic"이라는 휴리스틱일 뿐 명시적 선수 간선이 아닙니다. | [paper discovery](https://incitefulmed.com/academic/help/paper-disovery-explained.html) |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | 계정 기반 저장은 확인되지 않았습니다. 상태는 URL에 보존됩니다: "I try to ensure that state is preserved in the url for a page". | [beta](https://inciteful.xyz/beta) |
| 8 | Evidence & Provenance | 부분 지원 | 그래프마다 SQL DB를 노출해 `page_rank`, `adamic_adar`, `cocite`(Salton), `distance` 점수와 그 쿼리를 그대로 보여 줍니다. Connector는 실제 인용 경로를 표시합니다. 인용 문맥 텍스트는 확인되지 않았습니다. | [power users](https://incitefulmed.com/academic/help/power-users.html), [paper discovery](https://incitefulmed.com/academic/help/paper-disovery-explained.html) |
| 9 | Interactive Learning | 확인되지 않음 | SQL 쿼리 패널은 분석 도구이지 학습 기능이 아닙니다. | [power users](https://incitefulmed.com/academic/help/power-users.html) |
| 10 | API / OSS / Data reuse | 부분 지원 | 웹 프론트엔드는 AGPL-3.0입니다. MCP 서버 `inciteful-mcp`는 MIT이며 OpenAlex 검색과 Inciteful 그래프 서버를 결합합니다. Zotero 플러그인도 있습니다. 백엔드 그래프 엔진 공개 여부와 API 약관은 확인되지 않았습니다. | [inciteful-web](https://github.com/inciteful-xyz/inciteful-web), [inciteful-mcp](https://github.com/inciteful-xyz/inciteful-mcp), [org](https://github.com/inciteful-xyz) |

### 관계 산출 방식 (공식)
- **로컬 그래프 구성**
  - 시드가 인용한 논문과 시드를 인용한 논문을 모읍니다. 그 결과에 같은 과정을 한 번 더 반복합니다(깊이 2).
  - 보통 "10-20,000 papers and 50-100,000 citations" 규모입니다.
  - 깊이 2 그래프가 150,000편을 넘으면 1단계에서 멈춥니다.
  - 시드가 여러 편이면 그 시드들을 인용하는 가상 노드("fake node")를 만듭니다.
- **Importance**: PageRank("cited by papers which do"까지 반영).
- **Similarity** ("link prediction")
  - 서지결합에는 Adamic/Adar를 씁니다. 공통 참고문헌마다 1/log(그 문헌의 피인용수)를 더하며, "doesn't overly penalize a mutual paper for being popular"라고 설명합니다.
  - 공인용에는 Salton Index를 씁니다(피인용수 차이 보정).
- **Literature Connector**: 인용을 무방향 간선으로 보고 bidirectional search로 최단 경로를 찾습니다. "Extended Graphs"는 한 홉을 더 포함합니다.
- **데이터**: OpenAlex API를 사용합니다(앱 코드). 감사 대상으로 OpenAlex, Semantic Scholar, Crossref, OpenCitations를 표기합니다([data](https://inciteful.xyz/data)).
- 출처: [paper discovery](https://incitefulmed.com/academic/help/paper-disovery-explained.html), [connector](https://incitefulmed.com/academic/help/literature-connector-explained.html)

### 이미 잘 해결한 것 (차별점으로 주장 금지)
- 완전 무료.
- 알고리즘 수식 수준의 공개와 SQL 재현성.
- 두 논문(분야) 사이 인용 경로 찾기.
- 다중 시드 맞춤 그래프.
- MCP 연동.

### AIXON 목표 대비 공백
- 근거 텍스트와 관계 타입이 없습니다(확인되지 않음).
- 초록과 개념을 쓰지 않습니다(문서상 제목만).
- 계정과 학습자 상태가 확인되지 않았습니다.
- 학습 기능이 확인되지 않았습니다.

### 출처 (모두 확인 2026-10-15)
- https://incitefulmed.com/academic/help/
- https://incitefulmed.com/academic/help/paper-disovery-explained.html
- https://incitefulmed.com/academic/help/literature-connector-explained.html
- https://incitefulmed.com/academic/help/power-users.html
- https://incitefulmed.com/academic/help/graphs-explained.html
- https://inciteful.xyz/about , https://inciteful.xyz/data , https://inciteful.xyz/beta (JS 번들 원문으로 확인)
- https://github.com/inciteful-xyz/inciteful-web
- https://github.com/inciteful-xyz/inciteful-mcp
- https://github.com/inciteful-xyz
- https://incitefulmed.com/

---

## 6. Open Knowledge Maps (OKM)

**한 줄 설명**: 검색어에 맞는 상위 100건 문헌을 AI 파이프라인으로 주제 군집화해 "knowledge map"으로 보여 주는 비영리 시각 검색 서비스입니다. 공식 문구: "the world's largest AI-based search engine for scientific knowledge".

**운영 주체와 상태**
- Peter Kraker가 2015년에 창립했고, "Since 2016 Open Knowledge Maps is a registered non-profit organization"입니다.
- 빈(Vienna)을 근거지로 합니다. 빈 시가 2026년 기본 지원금을 승인했고, 후원 회원 기관은 30곳입니다.
- 2025-07-01 연구자 프로필 서비스 VisConnect를 공개했습니다.
- 규모는 "400 Million outputs in 400+ languages from over 11.000 sources (via BASE)"이고, "more than one million users"를 표방합니다.

**무료와 유료**
- 개인 대상 유료 요금제는 확인되지 않았습니다. 운영 원칙은 "can be used by anyone"입니다.
- 운영 재원은 기관 후원 회원, 기부, 기관 대상 Custom Services입니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | BASE(전 분야) 또는 PubMed(생명과학)에서 검색합니다. 각 제공자의 relevance ranking 상위 100건으로 지도를 만듭니다. | [faq Q1–Q2](https://openknowledgemaps.org/faq), [home](https://openknowledgemaps.org/) |
| 2 | Citation & Relationship Visualization | 부분 지원 | 주제 영역(버블)과 문헌을 배치하는 지도입니다. "Closeness of areas implies subject similarity". 인용 관계는 표시하지 않고 텍스트 유사도 기반입니다. | [faq Q8.1](https://openknowledgemaps.org/faq) |
| 3 | Research Evolution | 부분 지원 | GoTriple 통합의 streamgraph는 "provides an overview of a given topic over time"입니다. 공개 검색(openknowledgemaps.org)의 시각화 유형은 "knowledge map"으로 설정돼 있고, 시간 범위 필터만 확인됩니다. | [GoTriple 뉴스](https://openknowledgemaps.org/news/2023/05/03/gotriple-platform), [home](https://openknowledgemaps.org/) |
| 4 | Concept Knowledge Graph | 부분 지원 | "labelling research areas with relevant concepts"라고 소개하며, 신규 연구자가 분야의 "language"를 익히도록 돕는다고 표방합니다. 개념 간 관계 유형은 확인되지 않았습니다. | [about](https://openknowledgemaps.org/about) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | 개인 계정 기능은 확인되지 않았습니다. 지도별 cite 버튼은 있습니다. | [faq Q10](https://openknowledgemaps.org/faq) |
| 8 | Evidence & Provenance | 부분 지원 | 군집 방법, 영역 제목 생성(TF-IDF 키워드), 배치의 의미를 FAQ로 공개합니다. "Resources are always assigned to a single area only." 개별 관계의 근거는 확인되지 않았습니다. | [faq Q6–Q8](https://openknowledgemaps.org/faq) |
| 9 | Interactive Learning | 확인되지 않음 | — | — |
| 10 | API / OSS / Data reuse | **지원** | Head Start는 "licensed under MIT"이고 지도 자동 생성 백엔드를 포함합니다. 사이트 콘텐츠는 CC BY 4.0입니다. 공개 API는 확인되지 않았고, 기관 통합은 Custom Services로 제공합니다. 원천 데이터(BASE/PubMed) 이용 조건은 각 제공자 약관을 따릅니다(추론). | [Headstart](https://github.com/OpenKnowledgeMaps/Headstart), [faq 하단](https://openknowledgemaps.org/faq) |

### 관계 산출 방식 (공식)
- 지도는 메타데이터 기반입니다: "Currently, we use titles, abstracts, authors, journals, and subject keywords to create a word co-occurrence matrix between articles. On top of this matrix, we perform clustering and ordination algorithms."
- 영역 제목 생성:
  - 3단어 이하 키워드·구를 모읍니다.
  - "bag-of-words TF-IDF"로 점수를 매깁니다.
  - 상위 3개를 고릅니다.
  - 키워드가 없으면 제목·초록에서 추론합니다.
- 크기
  - PubMed 통합: 논문 크기는 피인용수(Crossref 제공)입니다.
  - BASE 통합: 영역 크기는 문헌 수이고, 문헌 크기는 모두 같습니다.
- 출처: [faq](https://openknowledgemaps.org/faq)

### 이미 잘 해결한 것 (차별점으로 주장 금지)
- 키워드 하나로 분야의 하위 주제를 한눈에 보여 주는 지도.
- 하위 주제를 개념으로 라벨링하는 것. "분야의 언어 익히기"를 표방합니다.
- OA 문헌 강조.
- 완전 오픈소스(MIT)와 비영리 운영.
- 기관용 streamgraph, 저자 맵, 프로젝트 맵.

### AIXON 목표 대비 공백
- 인용·계보 관계를 쓰지 않습니다.
- 상위 100건으로 제한됩니다(FAQ Q2).
- 개념 간 관계와 선수지식이 없습니다(확인되지 않음).
- 개인 상태와 학습 기능이 확인되지 않았습니다.

### 출처 (모두 확인 2026-10-15)
- https://openknowledgemaps.org/faq
- https://openknowledgemaps.org/about
- https://openknowledgemaps.org/
- https://openknowledgemaps.org/news
- https://openknowledgemaps.org/news/2023/05/03/gotriple-platform
- https://github.com/OpenKnowledgeMaps/Headstart

---

## 7. scite (추가 경쟁자)

**한 줄 설명**: 인용 문장(citation statement)을 전문에서 추출하고, 그 인용이 피인용 논문을 지지(supporting)·반박(contrasting)·언급(mentioning)하는지 분류해 보여 주는 "Smart Citations" 플랫폼입니다. 공식 llms.txt: "They show the text surrounding a citation and classify the citation as supporting, contrasting, or mentioning".

**운영 주체와 상태**
- Scite LLC이며 "Now part of Research Solutions"입니다.
- Research Solutions가 2023-11-27 인수를 발표했습니다.
- 운영 중입니다. Assistant, Search, Collections, Reference Check, API, MCP를 제공합니다.

**무료와 유료**
- 7일 무료 체험이 있습니다. 무료 플랜은 확인되지 않았습니다.
- Basic: "$12 / month Billed yearly". Assistant, Search, Smart Citation 리포트, 최대 1,000편 Collections, 인용 알림을 포함합니다.
- Pro: "$40 / month Billed yearly". API 접근을 포함합니다.
- Enterprise는 별도 견적입니다.
- MCP는 유료 플랜, 체험, 또는 Enterprise가 있어야 씁니다.

### 10개 기준 판정

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | "Scite Search: Search publication metadata and citation statements from full text". | [llms.txt](https://scite.ai/llms.txt) |
| 2 | Citation & Relationship Visualization | 부분 지원 | Smart Citation 리포트로 인용 집계와 문맥을 보여 줍니다. 네트워크 시각화는 현행 공식 문서에서 확인되지 않았습니다(제3자 소개만 있음). | [llms.txt](https://scite.ai/llms.txt) |
| 3 | Research Evolution | 확인되지 않음 | — | — |
| 4 | Concept Knowledge Graph | 확인되지 않음 | — | — |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 부분 지원 | Collections는 "monitor new citations, track supporting or contrasting evidence, and receive alerts"를 제공합니다. 대시보드도 있습니다. | [llms.txt](https://scite.ai/llms.txt), [pricing](https://scite.ai/pricing) |
| 8 | Evidence & Provenance | **지원** | 인용별 주변 텍스트와 supporting / contrasting / mentioning 분류를 보여 줍니다. 논문 설명: "a classification from our deep learning model". | [llms.txt](https://scite.ai/llms.txt), [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.03.15.435418v1) |
| 9 | Interactive Learning | 부분 지원 | Scite Assistant는 "answers grounded in scholarly literature"를 주는 문헌 Q&A입니다. 실습형 학습은 확인되지 않았습니다. | [llms.txt](https://scite.ai/llms.txt) |
| 10 | API / OSS / Data reuse | **지원**(유료) | 문서화된 API가 메타데이터, Smart Citation 집계·문장, Assistant 등을 제공합니다. 원격 MCP `https://api.scite.ai/mcp`가 있습니다. Pro 이상에서 쓰며 데이터 라이선스는 영업 문의입니다. | [llms.txt](https://scite.ai/llms.txt), [pricing](https://scite.ai/pricing) |

### 관계 산출 방식 (공식)
- 전문에서 인용 문장을 추출하고 딥러닝 모델로 분류합니다: "whether the statement provides supporting or disputing evidence for a referenced work, or simply mentions it".
- 2021년 논문 기준 규모: "over 23 million full-text scientific articles", "more than 800 million classified citation statements".
- 출처: [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.03.15.435418v1)

### 이미 잘 해결한 것 / 공백
- 이미 해결: 인용 문장 단위 근거 제시, 지지·반박 판별, 반박 증거 모니터링, 참고문헌 점검(철회 등), API·MCP. **"관계별 근거 문장 제시" 자체는 차별점이 될 수 없습니다.**
- 공백
  - 분류 축이 "주장에 대한 지지·반박"입니다. 연구 계보 타입(확장·적용·개선)은 확인되지 않았습니다.
  - 개념, 선수지식, 학습자 모델, 실습이 확인되지 않았습니다.
  - 유료입니다.

### 출처 (모두 확인 2026-10-15)
- https://scite.ai/llms.txt
- https://scite.ai/pricing
- https://researchsolutions.investorroom.com/2023-11-27-Research-Solutions-Announces-Acquisition-of-scite
- https://www.biorxiv.org/content/10.1101/2021.03.15.435418v1

---

## 8. Papers with Code: 구 사이트 종료와 2026 재개판 (추가 경쟁자)

**한 줄 설명**: ML 논문을 task / method / dataset / benchmark(SOTA)와 코드 구현에 연결하는 AI 분야 전용 탐색 사이트입니다. 재개판 홈페이지 문구: "Discover trending machine-learning papers, methods, benchmarks, datasets, and open-source implementations."

**상태 (중요)**
- **구 paperswithcode.com**
  - 2025-07에 종료됐다는 보도가 있습니다. Hugging Face CTO Julien Chaumond가 2025-07-25 "Trending Papers"를 발표하면서 전날 종료됐다고 밝혔다고 전합니다 [2차: hyper.ai].
  - 2026-10-15 직접 확인 결과 `https://paperswithcode.com/` → **HTTP 302 → https://huggingface.co/papers/trending**입니다.
- **재개판 paperswithcode.co**
  - Hugging Face 블로그의 Community Article "Relaunching PapersWithCode with new features"(2026-05-24, Niels Rogge): "Niels here from the open-source team at Hugging Face. It's been one week since I launched paperswithcode.co, a revival of the website…"
  - 후속 글(2026-06-22): "At Hugging Face we continue working on a revival of Papers with Code". `paperswithco.de` 도메인을 추가했습니다.
- **레거시 데이터**
  - HF Hub `pwc-archive` 조직에 datasets / methods / evaluation-tables / links-between-paper-and-code / papers-with-abstracts 등이 있습니다.
  - 라이선스는 `cc-by-sa-4.0`입니다.
  - 설명: "This dataset will not be updated. It corresponds to the last available public snapshot of the data, retrieved on July 28th, 2025."
  - 구 GitHub 저장소: "All data is licenced under CC-BY-SA."

**무료와 유료**: 웹 접근이 가능합니다. 요금 정보는 확인되지 않았습니다.

### 10개 기준 판정 (재개판 paperswithcode.co 기준)

| # | 기준 | 판정 | 근거 | 출처 |
|---|---|---|---|---|
| 1 | Literature Discovery | 지원 | Trending research, Recent papers, Paper archive, Research tasks, Methods를 제공합니다. | [paperswithcode.co](https://paperswithcode.co/) |
| 2 | Citation & Relationship Visualization | 부분 지원 | "Support for paper lineage: whenever a paper has a follow-up or predecessor, this will be displayed with a small banner above the abstract." "Each method also lists all papers that cite it." 그래프 시각화는 확인되지 않았습니다. | [relaunch 글](https://huggingface.co/blog/nielsr/paperswithcode-launch) |
| 3 | Research Evolution | 부분 지원 | 선행·후속 lineage 배너, 벤치마크 리더보드(다중 지표, scatter plot과 table), top-3 SOTA 배지가 있습니다. 시간축 진화 뷰는 확인되지 않았습니다. | [relaunch 글](https://huggingface.co/blog/nielsr/paperswithcode-launch), [updates 글](https://huggingface.co/blog/nielsr/updates-to-pwc) |
| 4 | Concept Knowledge Graph | 부분 지원 | task / method / benchmark 엔티티와 논문 연결이 있고, 제출 논문은 "AI will automatically enrich it with task and method tags"입니다. 레거시 methods 데이터는 area → collection → method 계층을 가집니다(스키마 필드 `collections`). 개념 간 관계 유형은 확인되지 않았습니다. | [relaunch 글](https://huggingface.co/blog/nielsr/paperswithcode-launch), [methods first-rows](https://datasets-server.huggingface.co/first-rows?dataset=pwc-archive/methods&config=default&split=train) |
| 5 | Explicit Prerequisite Graph | 확인되지 않음 | — | — |
| 6 | Personalized Learning Paths | 확인되지 않음 | — | — |
| 7 | Persistent Learner State | 확인되지 않음 | 계정과 개인화 기능은 확인되지 않았습니다. | — |
| 8 | Evidence & Provenance | 확인되지 않음 | lineage(선행·후속)의 판정 근거와 방법이 공개되지 않았습니다. 외부 평가 수치(Artificial Analysis 등)는 출처를 표시하지만 이는 관계 근거가 아닙니다. | [updates 글](https://huggingface.co/blog/nielsr/updates-to-pwc) |
| 9 | Interactive Learning | 확인되지 않음 | 채팅 기능이 있다는 2차 보도가 있으나 공식 글에서는 확인되지 않았습니다. | — |
| 10 | API / OSS / Data reuse | **지원**(레거시 데이터) | `pwc-archive` 데이터셋은 CC-BY-SA-4.0이고 2025-07-28 스냅샷에서 고정됐습니다. 재개판 API는 확인되지 않았습니다. **주의**: `pwc-archive/methods` 첫 행들에 항공사·스트리밍 고객센터 스팸 항목이 섞여 있어 정제가 필요합니다(datasets-server 응답 직접 확인). | [HF API 목록](https://huggingface.co/api/datasets?author=pwc-archive&limit=50), [methods first-rows](https://datasets-server.huggingface.co/first-rows?dataset=pwc-archive/methods&config=default&split=train), [legacy GitHub](https://github.com/paperswithcode/paperswithcode-data) |

### 관계 산출 방식 (공식)
- SOTA 배지: "displayed whenever a paper gets a score within the top 3 of a given benchmark".
- Trending 점수: "a combination of the GitHub star velocity and the trending score of the linked Hugging Face artifacts (models, datasets, and Spaces)".
- lineage와 task·method 태깅: 제출 논문은 AI로 자동 보강합니다. lineage 판정 방법은 공개되지 않았습니다(확인되지 않음).
- 출처: [updates 글](https://huggingface.co/blog/nielsr/updates-to-pwc), [relaunch 글](https://huggingface.co/blog/nielsr/paperswithcode-launch)

### 이미 잘 해결한 것 / 공백
- 이미 해결
  - AI 분야 task / method / benchmark 분류와 SOTA 추적.
  - 논문–코드–평가 연결.
  - **선행/후속 논문 lineage 표시(2026-05~)**.
  - 방법별 인용 논문 목록.
- 공백
  - lineage가 방향(선행/후속) 수준이고 근거가 공개되지 않았습니다.
  - EXTENDS / ADAPTS / IMPROVES_ON 같은 타입이 확인되지 않았습니다.
  - 선수지식, 학습자 모델, 랩이 확인되지 않았습니다.
  - 1인 주도 커뮤니티 아티클 기반이라 지속성이 불확실합니다(추론).

### 출처 (모두 확인 2026-10-15)
- https://paperswithcode.com/ (302 → https://huggingface.co/papers/trending, curl로 직접 확인)
- https://paperswithcode.co/
- https://huggingface.co/blog/nielsr/paperswithcode-launch
- https://huggingface.co/blog/nielsr/updates-to-pwc
- https://huggingface.co/pwc-archive , https://huggingface.co/api/datasets?author=pwc-archive&limit=50
- https://datasets-server.huggingface.co/first-rows?dataset=pwc-archive/methods&config=default&split=train
- https://github.com/paperswithcode/paperswithcode-data
- [2차] https://hyper.ai/en/news/42900

---

## 9. Gaps & implications for AIXON

### 9.1 시장에서 이미 해결된 것: AIXON이 차별점으로 주장하면 안 되는 목록

| 기능 | 이미 제공하는 곳 (근거 절) |
|---|---|
| 시드 논문 기반 관련 논문 추천과 반복 확장 | 8개 제품 전부 (1–8절) |
| 인용 또는 유사도 그래프 시각화 | Connected Papers, ResearchRabbit, Litmaps, Inciteful (2–5절) |
| 출판일 시간축 위의 인용 지도 | Litmaps (공식 축 옵션), ResearchRabbit 신규 그래프 [2차] (3–4절) |
| "먼저 읽을 고전"과 "후속·최신 연구" 구분 | Connected Papers Prior/Derivative, ResearchRabbit Earlier/Later, Inciteful Important/Similar, Litmaps Momentum (2–5절) |
| 두 논문·분야 사이 연결 경로 | Inciteful Literature Connector, Connected Papers 유사도 공간 최단 경로 (2·5절) |
| 인용 문맥 문장 제시와 인용 의도·성격 분류 | Semantic Scholar(Background/Method/Result + contexts + isInfluential), scite(supporting/contrasting/mentioning) (1·7절) |
| 영향력 있는 인용 판별 | Semantic Scholar Highly Influential Citations (1절) |
| 요약·용어 정의·논문 Q&A | Semantic Scholar TLDR, Definitions On-Demand, Ask This Paper, scite Assistant (1·7절) |
| 토픽 페이지와 개념 라벨 | Semantic Scholar Topic pages(CS), OKM 영역 라벨 ("분야의 언어 익히기" 표방) (1·6절) |
| 신규 논문 알림과 개인화 피드 | Semantic Scholar, Litmaps Monitor, scite Collections (1·4·7절) |
| AI 어시스턴트(MCP) 연동 | Litmaps MCP(beta), scite MCP, inciteful-mcp, Ai2 Asta Scientific Corpus Tool (1·4·5·7절) |
| AI 분야 task / method / benchmark 분류, SOTA, 선행/후속 lineage 배너 | Papers with Code 재개판, 2026-05~ (8절) |

### 9.2 8개 제품 모두에서 "확인되지 않음"인 영역: AIXON의 실제 차별화 후보
1. **(5) 명시적 선수지식 그래프**: 개념 수준의 "A를 알아야 B" 간선. 현재 시장에는 논문 단위 휴리스틱(Prior works, PageRank Important papers, "foundational articles" 필터)만 있습니다.
2. **(6) 개인화 학습 경로**: 학습자 상태에 따른 읽기·학습 순서 계획.
3. **(7) 근거 기반 학습자 모델**: 지금 시장의 "영속 상태"는 서재, 평가, 노트, 알림 같은 연구 활동 상태뿐입니다. 숙달도 모델은 없습니다.
4. **(9) 실습형 인터랙티브 랩**: 수학·알고리즘 실습. 현재는 읽기 보조와 Q&A까지만 있습니다.
5. **타입화된 연구 계보와 간선별 근거**: EXTENDS / ADAPTS / IMPROVES_ON 같은 타입에 근거 문장과 출처를 붙인 것. 가장 근접한 것은 S2의 3범주 의도 + contexts, scite의 3범주 성격, PwC 재개판의 무타입 lineage 배너(근거 비공개)입니다. 이 결합을 공식 문서로 제공하는 곳은 확인되지 않았습니다.

### 9.3 데이터·라이선스 시사점 (추론 포함)
- **S2 citations 데이터셋**은 `contexts`, `intents`, `isinfluential`을 ODC-BY로 제공합니다. AIXON이 타입화된 계보를 분류할 때 근거 문장 공급원과 약지도(weak label) 출발점으로 쓰기에 가장 현실적입니다(추론).
  - 제약 1: 의도·영향 라벨은 전문 접근이 가능한 논문에만 있습니다.
  - 제약 2: full bulk 다운로드에는 API 키가 필요합니다.
  - 제약 3: API License에 API 재배포 금지, attribution 의무, at-will 종료 조항이 있습니다.
  - 무인증 API는 전체 사용자 공유 1000 RPS이고, 키는 1 RPS로 시작합니다. 개인 로컬 앱의 증분 수집은 가능하지만, 대량 시드는 bulk 데이터셋이 현실적입니다(추론).
- **PwC 레거시 아카이브**(CC-BY-SA-4.0, 2025-07-28 고정)는 AI method·task 분류 체계의 초기 시드로 유용합니다. 단, ShareAlike 조건 때문에 파생 데이터를 배포하면 같은 라이선스를 따라야 할 가능성이 큽니다(추론). 스팸 항목 정제도 필수입니다.
- **오픈소스 재사용**
  - Head Start(MIT)와 inciteful-mcp(MIT)는 코드 차용이 쉽습니다.
  - inciteful-web은 AGPL-3.0이라 코드를 차용하면 네트워크 제공 시 소스 공개 의무가 생길 수 있습니다(추론).
  - Inciteful의 PageRank, Adamic/Adar, Salton 공식은 문서화돼 있어 AIXON 탐색 기능의 기준선(baseline)으로 재현할 수 있습니다(추론).
- **Connected Papers API**는 early access입니다. 그래프 재배포 조건은 확인되지 않았습니다.

### 9.4 설계 시사점 (추론)
- 차별점 문구는 "관계를 시각화한다", "근거 문장을 보여 준다", "시간축으로 본다"가 되면 안 됩니다. 모두 이미 있는 기능입니다. **"개념 선수지식 구조 + 숙달 상태 + 경로 계획 + 실습 랩 + 타입화된 계보(간선별 근거·검증 상태)"의 결합**이어야 합니다.
- 계보 간선마다 다음을 provenance로 붙이면 S2·scite와 구분됩니다.
  - 근거 스팬(S2 `contexts`)
  - 출처 ID(S2 `corpusId`/`paperId`)
  - 분류 주체(모델 또는 사람)와 신뢰도
  - 사용자 검증 상태
- Papers with Code 재개판은 AI 분야 lineage, method, SOTA를 2026-05~06 사이 빠르게 늘리고 있습니다. **AI 특화 경쟁자 가운데 가장 가까워 지속 추적이 필요합니다.**
- Litmaps와 ResearchRabbit가 같은 법인으로 통합되면서 시간축 지도, 반복 탐색, MCP가 이 범주의 표준 기능이 됐습니다.

### 9.5 상충·불확실 정보 (설계 문서 인용 시 주의)
- Semantic Reader 커버리지: 제품 페이지는 "most arXiv papers", FAQ는 "only … ArXiv … 250k+"입니다.
- TLDR 범위: FAQ는 "computer science and biomedical", 제품 페이지는 "nearly 60 million papers in computer science, biology, and medicine"이고, 데이터셋은 58M records입니다.
- S2 데이터 라이선스: API License는 "such as CC BY-NC or ODC-BY"라고 예시하지만, 현행 데이터셋 README는 ODC-BY와 Apache-2.0(임베딩)입니다. 데이터셋별로 확인해야 합니다.
- ResearchRabbit
  - 출시일: 공식 2025-10-20 vs Aaron Tay 2025-10-30 [2차].
  - Litmaps와의 관계: 공식 도움말은 "partnership", 뉴스는 "acquired" [2차], 사이트 저작권 표기는 Litmap Limited.
- Litmaps
  - 무료 Litmap 수: 가격 페이지에 1개와 2개 표기가 섞여 있습니다.
  - 기본 축(x=출판일, y=인용수): 공식 문서에 명시가 없고 2차 출처에만 있습니다.
  - 기본 노드 크기: 2차 출처끼리 상충합니다.
- Connected Papers 가격: 지역·통화별로 동적 표시돼 금액을 확정하지 못했습니다.
- Papers with Code 구 사이트 종료일(2025-07-24 무렵)은 2차 보도에 기반합니다. 현재의 리다이렉트만 직접 확인했습니다.

# C. 학습 중심·인터랙티브 ML 학습 제품 및 선행 사례 분석 (AIXON 경쟁 분석용)

- 작성일: 2026-10-15 (조사 서브에이전트). **본문의 모든 URL은 2026-10-15에 확인함.** 출처 전체 목록은 문서 끝 「출처 목록」에 있음.
- 대상(12): Learn Anything, Metacademy, Math Academy, ALEKS, TensorFlow Playground, Distill, Transformer Explainer, CNN Explainer, NotebookLM(2026-07-16부터 **Gemini Notebook**), ChatGPT study mode, Claude learning mode, Anki + FSRS
- 판정 라벨: **지원** / **부분 지원** / **확인되지 않음** / **미지원(공식 근거 있음)**. 「확인되지 않음」은 공개된 공식 자료에서 확인하지 못했다는 뜻이며 기능이 없다는 뜻이 아님. 이번 조사에서 「미지원(공식 근거 있음)」 판정은 0건.
- 「추론」 표시는 조사자의 해석임. 표시가 없는 서술은 링크된 출처에 근거함.

**조사 방법과 한계**
- Internet Archive가 조사 시점에 "Temporarily Offline" 상태여서 과거 스냅샷을 확인할 수 없었음.
- metacademy.org는 이 조사 환경에서 접속되지 않았음(443 연결 거부, 80 타임아웃).
- openai.com과 help.openai.com은 직접 요청하면 봇 차단(403)이 걸려, 공식 URL 본문을 `r.jina.ai` 리더 프록시로 읽었음. Claude 도움말 일부도 같은 방식으로 읽었음.
- GitHub API는 호출 한도에 걸려 대부분 웹 페이지와 raw 파일로 확인했음.
- 로그인이 필요한 기능은 직접 써 보지 않았음(계정 생성 없음).
- Learn Anything은 공식 문서가 placeholder뿐이어서, 공개된 프런트엔드 번들(JS)의 UI 문자열과 코드를 직접 관찰했음(배포본은 바뀔 수 있음).
- Metacademy는 보관(archived)된 공식 GitHub 저장소의 소스와 공개 데이터 덤프를 직접 분석했음.

**기준 번호**
- (1) Literature Discovery
- (2) Citation & Research Relationship Visualization
- (3) Research Evolution over time
- (4) Concept Knowledge Graph
- (5) Explicit Prerequisite Graph
- (6) Personalized Learning Paths
- (7) Persistent Learner State
- (8) Evidence & Provenance
- (9) Interactive Learning
- (10) API / open-source / reuse potential

---

## 0. 요약 표

| 제품 | (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) | (9) | (10) |
|---|---|---|---|---|---|---|---|---|---|---|
| Learn Anything | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 |
| Metacademy | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 | 지원 | 부분 지원 | 부분 지원 | 확인되지 않음 | 지원 |
| Math Academy | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 | 지원 | 지원 | 확인되지 않음 | 부분 지원 | 확인되지 않음 |
| ALEKS | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 지원 | 지원 | 확인되지 않음 | 부분 지원 | 확인되지 않음 |
| TensorFlow Playground | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 |
| Distill | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 | 지원 |
| Transformer Explainer | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 |
| CNN Explainer | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 지원 | 지원 |
| NotebookLM / Gemini Notebook | 부분 지원 | 부분 지원 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 지원 | 부분 지원 | 부분 지원 |
| ChatGPT study mode (+학습 기능) | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 부분 지원 | 확인되지 않음 | 지원 | 확인되지 않음 |
| Claude learning mode | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 확인되지 않음 | 부분 지원 | 부분 지원 |
| Anki + FSRS | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 확인되지 않음 | 부분 지원 | 지원 | 확인되지 않음 | 부분 지원 | 지원 |

### 0.1 제품 개요 (운영·상태·오픈소스·개인 이용 조건)

| 제품 | 운영 주체 | 현재 상태 (2026-10-15 기준) | 오픈소스 | 개인 무료 / 유료 |
|---|---|---|---|---|
| Learn Anything | Nikita Voloboev 개인 프로젝트로 보도됨(2차 출처) | 사이트는 응답(HTTP 200)하며 로그인 기반 앱이 서빙됨. 공식 GitHub 저장소는 `linsa-io/linsa`로 리디렉션됨(커밋 1개, 2026-01-17) | 과거에는 MIT(2차 출처). 현재 앱 코드는 비공개로 보임 | "free" 표방. 유료 플랜은 확인되지 않음 |
| Metacademy | Roger Grosse, Colorado Reed | 앱 저장소 보관(archived) 2023-07-06. 사이트 접속 실패 | 코드 GPLv3, 콘텐츠 CC BY-SA 3.0 | 무료 공개 프로젝트. 유료 플랜은 확인되지 않음 |
| Math Academy | Math Academy, LLC | 운영 중("JOIN BETA" 표기) | 확인되지 않음(비공개로 보임) | $49/월(학생당). 무료 체험 없음, 30일 내 환불 |
| ALEKS | McGraw Hill(상표는 ALEKS Corporation) | 운영 중 | "proprietary" 명시 | 무료 체험 있음. 개인 구독 $19.95(1개월) ~ $179.95(12개월) |
| TensorFlow Playground | Daniel Smilkov, Shan Carter (tensorflow GitHub 조직) | 사이트 운영 중. 마지막 커밋 2022-06-06 | Apache-2.0 | 무료, 계정 없음 |
| Distill | Distill 편집팀 | 2021-07-02부터 휴간. "indefinite hiatus and no longer accepting submissions". 마지막 게재 2021-09-02 | 기사는 CC-BY 4.0, 소스는 GitHub | 무료 열람 |
| Transformer Explainer | Georgia Tech Polo Club | 데모 운영 중. 최근 커밋 2026-06-06. CHI 2026 논문 | MIT | 무료 |
| CNN Explainer | Georgia Tech Polo Club | 데모 운영 중. 마지막 커밋 2023-10-14. TVCG 2020 논문 | MIT | 무료 |
| NotebookLM / Gemini Notebook | Google | 운영 중. 2026-07-16에 Gemini Notebook으로 개명 | 비공개. Enterprise API(v1alpha) 있음 | Standard 무료(노트북 100개, 노트북당 소스 50개). Plus·Pro·Ultra는 한도 상향 |
| ChatGPT study mode | OpenAI | 2025-07-29 출시. 2026-03-10 인터랙티브 비주얼 추가 | 비공개 | 모든 플랜(무료 포함) |
| Claude learning mode | Anthropic | 2025-04-02 Claude for Education에서 시작. 2025-08 전체 사용자로 확대(보도 기준). Claude Code에 Learning output style | 비공개(output style은 사용자 정의 가능) | 보도 기준 전체 사용자 |
| Anki + FSRS | Anki: Ankitects Pty Ltd(상표)·커뮤니티. FSRS: open-spaced-repetition 커뮤니티 | Anki 데스크톱 현재 26.09.3. FSRS는 Anki 23.10+ 내장 옵션 | Anki AGPL-3.0+. FSRS 구현은 MIT/BSD-3 | 데스크톱·AnkiDroid·AnkiWeb 동기화 무료. AnkiMobile(iOS)은 유료(가격 미확인) |

---

## 0.2 핵심 질문에 대한 답

### Q1. 명시적 prerequisite 그래프를 제공하는 제품은?

**Metacademy (명확, 학습자에게 노출)**
- 공식 소개: "The concepts are arranged in a prerequisite graph, which is used to generate a learning plan for a concept." ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html))
- 공개 데이터 덤프 기준으로 dependency 1,208개 중 1,006개에 선수 이유(`reason`) 텍스트와 source/target learning goal 연결이 있음. 덤프 파일을 직접 집계한 결과임 ([graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json))

**Math Academy (명확, 시스템 내부 모델)**
- 공식 설명: "the objects are mathematical topics and the arrows between them represent relationships, such as one topic being a prerequisite for another topic". 선수 관계와 별도로 "encompassed" 관계도 모델링함 ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works))
- 학습자가 앱 안에서 그래프를 직접 탐색하는 UI가 있는지는 공개 페이지로 확인되지 않음. 공개 페이지에는 학생 knowledge graph 시각화 예시만 있음.

**ALEKS (부분)**
- Knowledge Space Theory의 "Knowledge Structure" 위에서 동작함 ([KST 페이지](https://www.aleks.com/about_aleks/knowledge_space_theory))
- 공개 문서가 이를 'prerequisite graph'로 학습자에게 노출하거나 설명하는지는 확인되지 않음. KST의 지식 구조가 선후 관계를 함축한다는 해석은 추론임.

**그 외**
- Learn Anything의 `connectedTopics`는 방향과 유형이 없는 연관 관계로 보임(번들 코드 관찰).
- NotebookLM의 Mind Map은 주제 계층을 보여 줌.
- 나머지 제품은 확인되지 않음.

### Q2. 학습자가 이미 아는 것에서 개인화 계획을 계산하는 제품은? 어떻게?

**Metacademy: 목표 개념 + 자기보고 "learned"**
1. 사용자가 목표 개념을 지정함. 덤프에는 개념별 `graph.targetgraph` 레코드(487개, depth와 dependency 목록 포함)가 있어, 목표 개념별 선수 하위그래프를 미리 계산해 두는 구조로 보임(추론) ([graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json))
2. 클라이언트가 목표(leaf)에서 dependency를 역방향으로 탐색함. 이때 사용자가 learned로 체크한 개념에서 탐색을 차단함(`dfsFromNode(leaf, doesLearnedBlock)`) ([aux-model.js](https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/aux-model.js))
3. 도달되지 않는 개념은 "implicitly learned"로 표시되어 학습 계획에서 숨겨짐(`showLearnedConcepts` 옵션) ([explore-graph-model.js](https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/explore-graph-model.js), [agfk-concept-list-view.js](https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/views/agfk-concept-list-view.js))
4. 남은 개념의 예상 소요시간("Completion Time")을 다시 계산함. 시간 추정이 없는 개념은 기본 1시간으로 계산함 ([aux-model.js](https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/aux-model.js))

**Math Academy: 적응형 진단 + knowledge graph**
- 진단이 "knowledge frontier"(아는 것과 모르는 것의 경계)를 추정함.
- 정답은 해당 토픽과 그 선수 토픽에 대한 양의 증거, 오답은 해당 토픽과 "postrequisites"에 대한 음의 증거로 쓰임. 응답 시간이 지나치게 길면 증거 가중치를 낮춤.
- 진단 결과로 결손된 하위 과정 기초를 포함한 custom course를 만듦.
- 이후 task-selection 알고리즘이 학습량 대비 시간을 최대화하도록 다음 과제를 고름(mastery learning, layering, interleaving, 연관 간섭 최소화).
- 레슨에서 반복 실패하면 지식 그래프에서 핵심 선수 토픽을 찾아 remediation을 줌. ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works))

**ALEKS: KST 적응형 평가**
- 약 25–30문항으로 지식 상태를 추정함(Markovian procedures) ([KST](https://www.aleks.com/about_aleks/knowledge_space_theory))
- 추정한 지식 상태에서 "topics that they are currently ready to learn"을 제시함 ([Overview](https://www.aleks.com/about_aleks/overview))

**LLM 튜터 (그래프 계산은 확인되지 않음)**
- ChatGPT study mode: "based on questions that assess skill level and memory from previous chats"로 수준을 맞춤 ([OpenAI](https://openai.com/index/chatgpt-study-mode/)). 요청하면 학습 계획을 텍스트로 생성함([FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq)).
- NotebookLM Learning Guide와 Claude learning mode는 대화형으로 적응함.

**Anki + FSRS**
- 학습 경로가 아니라 카드별 복습 일정만 개인화함 ([Anki manual](https://docs.ankiweb.net/deck-options.html))

### Q3. 학습자 모델을 저장하는 제품과 증거 유형은? (자기보고 vs 평가)

| 제품 | 저장되는 학습자 상태 | 증거 유형 | 출처 |
|---|---|---|---|
| Math Academy | knowledge profile: 토픽별 누적 "spaced repetitions", 학생-토픽별 "learning speed" | **평가**(정오답, 응답 시간, 퀴즈) | [How Our AI Works](https://www.mathacademy.com/how-our-ai-works) |
| ALEKS | 토픽별 숙달 여부와 ready-to-learn 여부("detailed map of each student's knowledge") | **평가**(적응형 평가, Knowledge Checks) | [Overview](https://www.aleks.com/about_aleks/overview) |
| Anki + FSRS | 카드별 리뷰 이력, 기억 상태(Difficulty/Stability/Retrievability), 개인 파라미터 | **자기평가된 회상 결과**(Again/Hard 등 버튼)와 시간 경과 | [Anki manual](https://docs.ankiweb.net/deck-options.html), [FSRS Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm) |
| Metacademy | 사용자별 learned/starred 개념 집합(서버 DB) | **자기보고**(체크). 이를 근거로 implicit learned를 추론함 | [models.py](https://github.com/metacademy/metacademy-application/blob/master/server/apps/user_management/models.py) |
| Learn Anything | 토픽별 "I want to learn / Learning / Learned", 개인 링크의 learning status | **자기보고** | [onboarding 번들](https://learn-anything.xyz/_build/assets/index-BIK8JTzQ.js) |
| Gemini Notebook | 플래시카드 "Got it!/Missed it!" 진도, 결과 리뷰·재시도 | **자기표시** + 퀴즈 응답 | [Help: Flashcards/Quizzes](https://support.google.com/gemininotebook/answer/16958963) |
| ChatGPT | Memory: 학습 목표, 선호 설명 방식, 공부한 주제 | **대화에서 추출**(자유 형식) | [FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq) |
| Claude | Memory: 주제(topic) 단위로 저장, 사용자가 열람·편집 가능 | **대화에서 추출**(학습 전용 아님) | [Claude memory](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context) |
| TF Playground, Distill, Transformer/CNN Explainer | 확인되지 않음(계정 기능 없음) | 해당 없음 | 각 제품 섹션 참조 |

### Q4. 인터랙티브 시뮬레이션과 평가를 연결하는 제품은?

조사한 12개 제품 중, 시뮬레이션 조작 결과를 평가나 학습자 모델의 증거로 쓴다고 공식 문서에서 확인된 제품은 **없음**(확인되지 않음).
- **시뮬레이션은 있지만 평가 연결은 확인되지 않음:** TF Playground, Transformer Explainer, CNN Explainer, Distill(기사 내 인터랙티브), ChatGPT(2026-03-10부터 70개 이상 수학·과학 개념의 인터랙티브 비주얼, [OpenAI](https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt)).
- ChatGPT는 같은 제품 안에 퀴즈와 비주얼을 모두 갖고 있지만, 둘이 연동된다는 공식 기술은 확인되지 않음.
- **평가는 있지만 시뮬레이션은 확인되지 않음:** Math Academy, ALEKS, Gemini Notebook(퀴즈), ChatGPT study mode(knowledge checks), Anki.
- 조사 범위 밖의 제품(예: Brilliant 등)은 확인하지 않았음. 별도 조사가 필요함.

### Q5. 간격 반복(spaced repetition)을 쓰는 제품과 알고리즘은?

- **Anki**
  - FSRS(Free Spaced Repetition Scheduler)를 선택해서 켤 수 있음. 지원 클라이언트: Anki 23.10, AnkiMobile 23.10, AnkiWeb, AnkiDroid 2.17+.
  - 켜지 않으면 legacy SM-2를 씀(매뉴얼은 FSRS를 "alternative to Anki's legacy SuperMemo 2 (SM-2) algorithm"으로 설명).
  - desired retention 기본값은 90%. "Optimize" 버튼이 리뷰 이력에 맞춰 파라미터를 학습함. ([Anki manual](https://docs.ankiweb.net/deck-options.html))
  - FSRS-6은 21개 파라미터를 씀. Stability는 "interval when R=90%", Difficulty는 [1, 10] 범위. ([The Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm))
- **Math Academy: FIRe (Fractional Implicit Repetition)**
  - 상위 토픽을 연습하면 그 반복 크레딧이 "encompassed" 하위 토픽으로 할인·분수 형태로 전파됨.
  - 여러 복습을 적은 과제로 압축함("repetition compression").
  - 학생-토픽별 learning speed가 반영됨.
  - 공식 페이지는 기존 알고리즘을 "limited to the context of independent flashcards"라고 명시함. ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works))
- **ALEKS:** "Knowledge Checks automatically confirm and enhance retention"(retrieval practice). 스케줄링 알고리즘의 공개 여부는 확인되지 않음. ([Overview](https://www.aleks.com/about_aleks/overview))
- **Gemini Notebook:** 플래시카드 진도와 "Only cards you missed" 재학습은 있음. 간격 반복 스케줄링은 확인되지 않음. ([Help](https://support.google.com/gemininotebook/answer/16958963))
- **ChatGPT, Claude, Metacademy, Learn Anything, TF Playground, Distill, Explainer류:** 간격 반복 스케줄러는 확인되지 않음.

---

## 1. Learn Anything (learn-anything.xyz)

**한 줄 설명**
토픽별 학습 리소스 링크 목록("study guide")과 개인 링크·페이지·태스크·학습 상태 추적을 묶은 웹앱(2026-10-15 배포본 기준).

**운영 주체**
- Nikita Voloboev로 보도됨([tproger](https://tproger.ru/news/learn-anything-search-engine), 2차 출처).
- 현재 저장소의 유일한 커밋 작성자는 `nikivdev`임([linsa commits](https://github.com/linsa-io/linsa/commits/main)).

**현재 상태**
- 사이트는 응답(HTTP 200)하며, meta description은 "Our free, comprehensive platform connects you to the best resources for every subject"임 ([learn-anything.xyz](https://learn-anything.xyz/))
- 빌드 manifest의 라우트: topics, links, pages, journals, tasks, community/$topicName, onboarding, search. Clerk 로그인을 씀. ([manifest](https://learn-anything.xyz/_build/.vite/manifest.json))
- 문서 사이트에는 "Future docs of learn-anything.xyz will be here."라는 한 줄뿐임 ([docs](https://docs.learn-anything.xyz/))
- GitHub 조직 페이지는 "This organization has no public repositories."라고 표시함 ([github.com/learn-anything](https://github.com/learn-anything))

**피벗 이력**

| 시점 | 무엇이었나 | 출처 |
|---|---|---|
| 2016-08-08 | 저장소 생성(repo id 65219131) | [API](https://api.github.com/repositories/65219131) |
| 2017-06 ~ 2017-07 | "Search Engine that searches Interactive Mind Maps to learn anything", "Open Source Search Engine to Learn Anything"(HN 145점). 토픽별 마인드맵 URL을 씀(예: /machine-learning/deep-learning) | [HN 14483578](https://news.ycombinator.com/item?id=14483578), [HN 14798336](https://news.ycombinator.com/item?id=14798336), [HN 14832129](https://news.ycombinator.com/item?id=14832129) |
| 2018-12-15 | "Platform for knowledge discovery" | [HN 18688902](https://news.ycombinator.com/item?id=18688902) |
| 2024-04-19 | "Organize knowledge, explore connections, curate learning paths". 당시 저장소 이름은 learn-anything/learn-anything.xyz | [HN 40088501](https://news.ycombinator.com/item?id=40088501) |
| 2026-10-15 | `github.com/learn-anything/learn-anything`과 `.../learn-anything.xyz`가 모두 301로 `github.com/linsa-io/linsa`로 리디렉션됨 | [linsa-io/linsa](https://github.com/linsa-io/linsa) |

- linsa 저장소 현재 상태: 설명 "Work. Save. Share. Privately.", 커밋 1개(2026-01-17), 라이선스 없음, 별 약 16.9k(이전 Learn Anything 별이 그대로 남은 것으로 보임, 추론). ([linsa-io/linsa](https://github.com/linsa-io/linsa))
- README에는 "Currently the author of this project does not have time to develop this in public"라고 적혀 있음.
- Linsa 자체는 "The Thinking Messenger"라는 AI 메신저 제품임 ([linsa.io](https://linsa.io)).
- 개발의 축이 Linsa로 옮겨 간 것으로 보임(추론).
- 원래 비전: "machine learning system that understands what you know and what you want to learn … craft the most optimized path". 이는 위키 사본에 실린 문구로 2차 출처이며, 실제 출시된 기능은 아님 ([wiki 사본](https://wiki.skiddle.id/ideas/learn-anything)).

**오픈소스**
- 과거에는 MIT였음([AlternativeTo](https://alternativeto.net/software/learn-anything/about), 2차 출처).
- 현재 앱 코드는 공개 저장소에 없음.
- curated-lists 저장소는 `linsa-io/curated-lists`로 옮겨진 상태로 남아 있음 ([raw readme](https://raw.githubusercontent.com/learn-anything/curated-lists/master/readme.md)).

**무료/유료:** "free"를 표방함. 유료 플랜은 확인되지 않음.

**명칭 혼동 주의:** Product Hunt의 "learn-anything-3"는 2026년에 나온 다른 제작자(yaqi Chen)의 AI 코딩 학습 도구로, 이 제품과 무관함 ([Product Hunt](https://www.producthunt.com/products/learn-anything-3)).

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 부분 지원 | 토픽마다 링크 목록이 붙고("This is the topic's study guide"), 검색 라우트도 있음. 논문 특화 검색은 확인되지 않음 ([onboarding 번들](https://learn-anything.xyz/_build/assets/index-BIK8JTzQ.js), [manifest](https://learn-anything.xyz/_build/.vite/manifest.json)) |
| (2) | 확인되지 않음 | 인용·연구 관계 시각화는 번들과 문서에서 확인되지 않음 |
| (3) | 확인되지 않음 | 시간축 기능은 확인되지 않음 |
| (4) | 부분 지원 | 랜딩 페이지가 토픽 노드와 `connectedTopics` 간선을 canvas force-directed 그래프로 렌더링함(코드 관찰). 관계 유형은 구분하지 않음 ([landing 번들](https://learn-anything.xyz/_build/assets/index-BXRjHR5G.js)) |
| (5) | 확인되지 않음 | `connectedTopics` 외의 선수 관계 표현은 확인되지 않음 |
| (6) | 확인되지 않음 | study guide는 토픽 공용 링크 목록이고, "will allow any user to edit these study guides too (Reddit style)"는 미래 계획으로만 언급됨. 개인화 계산은 확인되지 않음 ([onboarding 번들](https://learn-anything.xyz/_build/assets/index-BIK8JTzQ.js)) |
| (7) | 부분 지원 | "change the state of the topic to I want to learn, Learning or Learned". 사용자 데이터에 `topicsWantToLearn/Learning/Learned`가 저장됨. 증거는 자기보고 ([onboarding](https://learn-anything.xyz/_build/assets/index-BIK8JTzQ.js), [pages 번들](https://learn-anything.xyz/_build/assets/_pages-Dp1-g3JL.js)) |
| (8) | 확인되지 않음 | 링크 큐레이션 외의 근거·출처 추적은 확인되지 않음 |
| (9) | 확인되지 않음 | 연습·시뮬레이션은 확인되지 않음 |
| (10) | 부분 지원 | 과거 MIT 오픈소스(2차 출처). 현재 코드는 비공개 상태로 README에 "does not have time to develop this in public"라고 적힘. curated-lists는 남아 있음 ([linsa-io/linsa](https://github.com/linsa-io/linsa)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 토픽별 커뮤니티 리소스 큐레이션.
- 개인 지식관리(링크, 페이지)와 토픽 학습 상태 자기 추적의 결합.
- 토픽 연관 그래프 시각화.

**AIXON 대비 공백**
- 선수 관계, 평가 기반 학습자 모델, 출처 추적, 인터랙티브 랩이 모두 확인되지 않음.
- 반복된 피벗과 저장소 이전으로 제품이 계속 운영될지 불확실함(추론).

---

## 2. Metacademy (metacademy.org)

**한 줄 설명**
ML·확률적 AI 중심 개념을 prerequisite 그래프로 엮고, 목표 개념에서 학습 계획(learning plan)을 생성하는 오픈소스 "package manager for knowledge" ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html)).

**운영 주체**
- Roger Grosse, Colorado Reed. about 페이지에 "the two of us ( Roger Grosse and Colorado Reed ) have spent countless hours curating the content"라고 적혀 있음.
- Roger Grosse의 소개 글은 2014-02-16 게시 ([hunch.net](https://hunch.net/?p=2714)).

**현재 상태**
- 앱 저장소: "archived by the owner on Jul 6, 2023. It is now read-only." ([metacademy-application](https://github.com/metacademy/metacademy-application))
- 콘텐츠 저장소: "This content repository is deprecated. We now use a relational database for Metacademy's content." ([metacademy-content](https://github.com/metacademy/metacademy-content))
- 2026-10-15 이 조사 환경에서 metacademy.org 접속 실패(HTTPS 연결 거부, HTTP 타임아웃). 영구 폐쇄 여부는 확인되지 않음.
- 2024-01-15에 HN에 Metacademy 개념 페이지 링크가 제출된 기록이 있음 ([HN 39007587](https://news.ycombinator.com/item?id=39007587)). 그때까지는 접속 가능했던 것으로 보임(추론).

**오픈소스**
- 코드 GPLv3, 콘텐츠 CC BY-SA 3.0.
- Python 2.7 / Django 기반 ([README](https://github.com/metacademy/metacademy-application)).

**무료/유료:** 무료 공개 오픈소스 프로젝트로 소개됨 ([hunch.net](https://hunch.net/?p=2714)). 유료 플랜은 확인되지 않음.

**공개 데이터 덤프 정량 정보** ([graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json)를 직접 집계함. 운영 DB와 다를 수 있음)
- 개념 487개, dependency 1,208개(그중 `reason` 텍스트가 있는 것 1,006개), learning goal 1,352개, 개념-리소스 연결 1,442개.
- 수정 기록 범위: 2014-08-13 ~ 2015-03-31.
- 태그 상위: machinelearning 158, pgm 72, probability theory 56, linear algebra 43, bayesian stats 42.
- 제목에 transformer, attention, LSTM, dropout, autoencoder, GAN이 들어간 개념은 0개. "deep belief networks", "restricted Boltzmann machines", "convolutional neural nets"는 있음. 즉 2015년 이후 ML 발전은 반영되지 않았음(추론).

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 부분 지원 | 각 개념에 "pointers to learning resources"를 큐레이션해 둠. 검색형 문헌 발견은 아님 ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html)) |
| (2) | 확인되지 않음 | 개념 그래프 시각화는 있으나 인용·연구 관계 시각화는 아님 |
| (3) | 확인되지 않음 | 시간축 기능은 확인되지 않음 |
| (4) | 지원 | "an interconnected web of concepts, each one annotated with a short description, a set of learning goals, a (very rough) time estimate, and pointers to learning resources". roadmaps와 course guides도 있음 ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html)) |
| (5) | 지원 | "arranged in a prerequisite graph". 간선은 개념 단위와 goal 단위로 연결되고 선수 이유 텍스트가 붙음 ([graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json)) |
| (6) | 지원 | 목표 개념에서 learning plan을 만들고, learned 개념에서 탐색을 차단하며, 남은 개념의 예상 소요시간을 보여 줌(Q2 참조) ([aux-model.js](https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/aux-model.js)) |
| (7) | 부분 지원 | "Metacademy keeps track of what you've already learned". 사용자별 `learned`/`starred` 개념을 서버 DB에 저장함. 증거는 자기보고 체크 ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html), [models.py](https://github.com/metacademy/metacademy-application/blob/master/server/apps/user_management/models.py)) |
| (8) | 부분 지원 | 선수 간선에 큐레이터가 쓴 이유와 learning goal이 연결됨. 외부 문헌 인용으로 간선을 뒷받침하는 구조는 확인되지 않음 ([graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json)) |
| (9) | 확인되지 않음 | 데이터에 `exercises` 필드는 있으나(샘플 값은 null) 인터랙티브 연습은 확인되지 않음 |
| (10) | 지원 | GPLv3 코드, CC BY-SA 3.0 콘텐츠, 공개 그래프 덤프가 있음. 다만 보관 상태이고 Python 2.7임 ([repo](https://github.com/metacademy/metacademy-application), [content](https://github.com/metacademy/metacademy-content)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- ML 도메인 개념 prerequisite 그래프.
- 목표 개념에서 learning plan 자동 생성.
- 이미 학습한 개념 추적과 implicit learned 추론.
- 개념별 learning goal, 시간 추정, 리소스 포인터.
- 간선별 선수 이유 텍스트.
- 그래프 편집기와 roadmap.
- AIXON의 문제 정의("dependency hell … juggle all the prerequisites of prerequisites")와 거의 같은 문제를 2014년에 이미 다뤘음 ([about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html)).

**AIXON 대비 공백**
- 서비스가 휴면 상태이고 콘텐츠가 2014–2015년에 멈춰 있음.
- 학습자 상태가 자기보고 이진값이라 평가 증거가 없음.
- 논문·모델·연구 진화와 연결되지 않음.
- 인터랙티브 랩이 없음.
- 수작업 큐레이션 부담이 큼. 2014년 about 페이지에는 "doing it well enough that you can actually learn from it is still AI-complete"라고 적혀 있음.

---

## 3. Math Academy (mathacademy.com)

**한 줄 설명**
수천 개 수학 토픽의 knowledge graph 위에서 적응형 진단, 맞춤 코스, 숙달 학습, FIRe 간격 반복을 자동화하는 유료 수학 학습 플랫폼.

**운영 주체**
- Math Academy, LLC. 공동 창업자는 Jason Roberts, Sandy Durell Roberts ([About Us](https://www.mathacademy.com/about-us)).

**현재 상태**
- 운영 중이며, 사이트 전반에 "JOIN BETA"가 표기됨 ([홈](https://www.mathacademy.com/)).
- 카탈로그에 Mathematics for Machine Learning 과정이 있음 ([Courses](https://www.mathacademy.com/courses)).
- **Mathematics for Machine Learning** ([과정 페이지](https://www.mathacademy.com/courses/mathematics-for-machine-learning))
  - 12개 단원, 301개 토픽(단원별 토픽 수를 합산한 값): Set Theory 25, Logic 19, Vectors & Matrices 35, Vector Spaces 21, Diagonalization 13, Orthogonality & Projections 18, SVD 12, Applications of Linear Algebra 9, Multivariable Calculus 57, Probability & Random Variables 41, Combining Random Variables 29, Parametric Inference 22.
  - 목표: "well-prepared for a university-level machine learning course that tackles concepts such as gradient descent, neural networks, backpropagation…"
  - 별도의 ML 알고리즘 과정은 직원(Justin Skycak) 팟캐스트에서 "upcoming"으로 언급됨([justinmath.com](https://justinmath.com/golden-nuggets-podcast-39/)). 2026-10-15 공식 카탈로그에는 없음.

**오픈소스:** 오픈소스나 API는 확인되지 않음(비공개로 보임).

**무료/유료** ([홈](https://www.mathacademy.com/), [FAQ](https://www.mathacademy.com/faq))
- "Only $49/mo per student".
- "We do not offer a free trial".
- 30일 이내 취소하면 전액 환불.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 문헌 기능은 확인되지 않음 |
| (2) | 확인되지 않음 | 해당 없음으로 보임(확인되지 않음) |
| (3) | 확인되지 않음 | 해당 없음으로 보임(확인되지 않음) |
| (4) | 지원 | "multiple thousands of interlinked topics spanning 4th Grade through university-level math … connected up together in the knowledge graph" ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works)) |
| (5) | 지원 | prerequisite 관계와 "encompassed" 관계를 모델링함. 학습자가 그래프를 직접 탐색하는 UI는 확인되지 않음 ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works), [How It Works](https://www.mathacademy.com/how-it-works)) |
| (6) | 지원 | 진단으로 knowledge frontier를 추정하고, 결손 기초를 포함한 custom course를 만들며, task selection을 계속함(Q2 참조). 성인 대상 페이지: "a custom course will be created for you that includes any missing lower-course prerequistes" ([Adult Students](https://www.mathacademy.com/adult-students)) |
| (7) | 지원 | "Our student model uses a student's answer history to compute their knowledge profile". 토픽별 spaced repetition 수와 learning speed를 저장함. 증거는 평가 ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works)) |
| (8) | 확인되지 않음 | 콘텐츠·관계의 출처 표시는 확인되지 않음 |
| (9) | 부분 지원 | 레슨, 리뷰, 퀴즈에 해설과 정답률에 따라 바뀌는 문항 수가 있음(능동 연습). 시뮬레이션형 랩은 확인되지 않음 ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works)) |
| (10) | 확인되지 않음 | API, 데이터 내보내기, 오픈소스 모두 확인되지 않음 |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 평가 증거 기반 학습자 모델.
- 그래프를 이용해 문항 수를 줄이는 적응형 진단.
- knowledge frontier 기반 개인화 경로.
- 선수 토픽을 따라가는 remediation.
- 그래프 인지형 간격 반복(FIRe).
- 이 모든 것을 ML 수학 선수지식(301개 토픽)에 적용하는 것까지 이미 제공함.

**AIXON 대비 공백**
- 수학만 다룸(AI 연구 분야, 문제, 논문, 모델, 방법은 다루지 않음).
- 문헌과 출처 추적이 없음.
- 비공개 클라우드이고, 학습자 데이터 소유와 내보내기는 확인되지 않음.
- 그래프 탐색 UI는 확인되지 않음.

---

## 4. ALEKS (aleks.com)

**한 줄 설명**
Knowledge Space Theory(KST) 기반 적응형 평가로 학습자의 지식 상태를 추정하고 "ready to learn" 토픽을 제시하는 상용 학습·평가 시스템.

**운영 주체**
- McGraw Hill(©2026 McGraw Hill). ALEKS® 상표는 ALEKS Corporation 소유 ([Overview](https://www.aleks.com/about_aleks/overview)).

**현재 상태**
- 운영 중. "used by over 50 million students for Math, Chemistry, Statistics and Accounting".
- "billions of data points … accumulated over 26 years" ([Overview](https://www.aleks.com/about_aleks/overview)).

**오픈소스:** 비공개. 공식 문구: "ALEKS intelligence, content and software are unique and proprietary" ([Overview](https://www.aleks.com/about_aleks/overview)).

**무료/유료**
- 무료 체험이 있음. 개인 체험은 "Choose a course and complete an Initial Knowledge Check" ([Free Trial](https://www.aleks.com/free_trial)).
- 개인 구독: 1-Month $19.95 / 3-Months $49.95 / 6-Months $99.95 / 12-Months $179.95.
- 한 번에 한 과정만 수강할 수 있음. 자동 갱신되며, 남은 기간에 대한 부분 환불은 없음 ([Purchase](https://www.aleks.com/buy_aleks_now)).

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 문헌 기능은 확인되지 않음 |
| (2) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (3) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (4) | 부분 지원 | "discipline-specific knowledge structures (known as 'Knowledge Spaces')". Algebra 1은 약 350개 개념과 "millions of empirically feasible knowledge states"로 구성됨. 학습자에게는 그래프가 아니라 pie로 진도를 보여 줌 ([KST](https://www.aleks.com/about_aleks/knowledge_space_theory), [Overview](https://www.aleks.com/about_aleks/overview)) |
| (5) | 부분 지원 | KST 지식 구조가 선후 관계를 담는 것으로 보이나(추론), 공개 문서에서 prerequisite graph로 노출하거나 설명하는지는 확인되지 않음 |
| (6) | 지원 | "offering the student a selection of the topics that they are currently ready to learn". 그런 토픽을 "at least 90% of the time" 숙달한다고 밝힘 ([Overview](https://www.aleks.com/about_aleks/overview)) |
| (7) | 지원 | "develop and maintain a detailed map of each student's knowledge". 약 25–30문항의 적응형 평가와 Knowledge Checks를 씀. 증거는 평가 ([Overview](https://www.aleks.com/about_aleks/overview), [KST](https://www.aleks.com/about_aleks/knowledge_space_theory)) |
| (8) | 확인되지 않음 | 출처 표시는 확인되지 않음 |
| (9) | 부분 지원 | "replaces multiple guess with authentic problems". "Complete explanations and immediate feedback"을 줌. 시뮬레이션은 확인되지 않음 ([Overview](https://www.aleks.com/about_aleks/overview), [Independent](https://www.aleks.com/independent)) |
| (10) | 확인되지 않음 | 소스는 proprietary라고 명시됨. API는 확인되지 않음 |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 이론(KST)에 근거한 지식 상태 추정과 "ready to learn" 경계 제시.
- 대규모 실증.
- KST의 학술적 근거는 ALEKS 공식 페이지가 인용함: Falmagne 외 1990 *Psychological Review*, Doignon & Falmagne *Knowledge Spaces*(1999), *Learning Spaces*(2011) ([KST](https://www.aleks.com/about_aleks/knowledge_space_theory)).

**AIXON 대비 공백**
- 수학, 화학, 통계, 회계 위주이고 AI 연구는 다루지 않음.
- 비공개 상용 서비스임.
- 그래프와 근거를 학습자에게 보여 주는지는 확인되지 않음.

---

## 5. TensorFlow Playground (playground.tensorflow.org)

**한 줄 설명**
"Tinker With a Neural Network Right Here in Your Browser." 소형 신경망을 직접 조작하며 학습 과정을 시각화하는 도구 ([사이트](https://playground.tensorflow.org/)).

**운영 주체**
- "created by Daniel Smilkov and Shan Carter" ([사이트](https://playground.tensorflow.org/)).
- tensorflow GitHub 조직에 있으며 README에 "This is not an official Google product."라고 적혀 있음 ([repo](https://github.com/tensorflow/playground)).

**현재 상태**
- 사이트 운영 중.
- 마지막 커밋은 2022-06-06(의존성 업데이트 병합) ([commits](https://github.com/tensorflow/playground/commits/master)).

**오픈소스:** Apache License 2.0 ([LICENSE](https://github.com/tensorflow/playground/blob/master/LICENSE)). 별 약 13.1k.

**무료/유료:** 무료, 계정 없음.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 단일 시각화 도구라 범위 밖으로 보임(추론). 관련 기능은 확인되지 않음 |
| (2) | 확인되지 않음 | 위와 같음 |
| (3) | 확인되지 않음 | 위와 같음 |
| (4) | 확인되지 않음 | 위와 같음 |
| (5) | 확인되지 않음 | 위와 같음 |
| (6) | 확인되지 않음 | 위와 같음 |
| (7) | 확인되지 않음 | 계정이나 진도 저장은 언급되지 않음. 대신 수업용으로 보이는 컨트롤을 고른 링크를 저장할 수 있음 ([사이트](https://playground.tensorflow.org/)) |
| (8) | 확인되지 않음 | 출처 표시는 확인되지 않음 |
| (9) | 지원 | learning rate, activation, regularization, 문제 유형, 데이터셋, 노이즈, batch size, 입력 feature, hidden layer를 조작할 수 있고 학습 결과를 실시간으로 보여 줌 ([사이트](https://playground.tensorflow.org/)) |
| (10) | 지원 | "We've open sourced it on GitHub … You're free to use it in any way that follows our Apache License." 수업 주제에 맞게 컨트롤을 고를 수 있음 ([사이트](https://playground.tensorflow.org/)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 신경망 하이퍼파라미터의 직관을 브라우저 안에서, 설치 없이 탐구하게 해 줌.

**AIXON 대비 공백**
- 평가, 학습자 상태, 개념 그래프와 연결되지 않음.
- 2022년 이후 실질적인 개발이 없음.

---

## 6. Distill (distill.pub)

**한 줄 설명**
인터랙티브 다이어그램을 갖춘 동료심사 ML 설명 저널. "Distill is dedicated to clear explanations of machine learning." ([Journal](https://distill.pub/journal/))

**운영 주체**
- Distill 편집팀. 휴간 공지는 Chris Olah, Nick Cammarata, Sam Greydanus, Janelle Tam이 초안을 썼음 ([Hiatus](https://distill.pub/2021/distill-hiatus/)).

**현재 상태: 휴간**
- 2021-07-02 공지: "Starting today Distill will be taking a one year hiatus, which may be extended indefinitely." ([Hiatus](https://distill.pub/2021/distill-hiatus/))
- 현재 저널 페이지: "Distill is on an indefinite hiatus and no longer accepting submissions." 갱신 이력에도 "July 2, 2021 Distill went on hiatus and stopped accepting submissions for the indefinite future."라고 적혀 있음 ([Journal](https://distill.pub/journal/))
- 홈 기준 마지막 게재는 2021-09-02의 GNN 관련 2편 ([홈](https://distill.pub/)).

**오픈소스·라이선스**
- "Diagrams and text are licensed under Creative Commons Attribution CC-BY 4.0 with the source available on GitHub" ([GNN 글](https://distill.pub/2021/gnn-intro/)).
- Crossref에 등록되어 DOI를 발급함(10.23915/distill). ISSN 2476-0757 ([Journal](https://distill.pub/journal/)).

**무료/유료:** 무료 열람.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 저널 자체이며 문헌 탐색 도구는 확인되지 않음 |
| (2) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (3) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (4) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (5) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (6) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (7) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (8) | 지원 | "peer reviewed and appear in Google Scholar". DOI와 BibTeX 인용을 제공함. 게재 후에도 GitHub issue로 공개 리뷰와 정정("Updates and Corrections")을 받음 ([Journal](https://distill.pub/journal/), [GNN 글](https://distill.pub/2021/gnn-intro/)) |
| (9) | 지원 | 기사 안에 인터랙티브 다이어그램이 있음. 예: GNN 글의 GNN playground ([GNN 글](https://distill.pub/2021/gnn-intro/)) |
| (10) | 지원 | CC-BY 4.0이고 GitHub에 소스가 있음 ([GNN 글](https://distill.pub/2021/gnn-intro/)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 근거(동료심사, 인용, DOI)를 갖춘 인터랙티브 설명이라는 형식 자체.

**AIXON 대비 공백**
- 신규 콘텐츠가 2021년에 멈춤.
- 학습자 모델, 경로, 평가가 없음.
- 재사용할 수 있는 고품질 설명 자산으로는 가치가 있음(추론).

---

## 7. Transformer Explainer (Georgia Tech Polo Club)

**한 줄 설명**
"runs a live GPT-2 model right in your browser". 사용자가 입력한 텍스트로 Transformer 내부 연산을 실시간으로 시각화함 ([README](https://github.com/poloclub/transformer-explainer)).

**운영 주체**
- Georgia Institute of Technology의 Aeree Cho 외. Polo Chau 연구실 ([README](https://github.com/poloclub/transformer-explainer)).

**현재 상태**
- 데모 운영 중 ([데모](https://poloclub.github.io/transformer-explainer/)).
- 최근 커밋 2026-06-06("update cite info") ([commits](https://github.com/poloclub/transformer-explainer/commits/main)).
- 논문: *Proceedings of the 2026 CHI Conference on Human Factors in Computing Systems* (DOI 10.1145/3772318.3791725, [ACM](https://dl.acm.org/doi/10.1145/3772318.3791725)). arXiv 2408.04619 ([arXiv](https://arxiv.org/abs/2408.04619)).

**오픈소스:** MIT. 별 약 9.0k.

**무료/유료:** 무료.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 단일 개념 시각화 도구라 범위 밖으로 보임(추론). 관련 기능은 확인되지 않음 ([README](https://github.com/poloclub/transformer-explainer)) |
| (2) | 확인되지 않음 | 위와 같음 |
| (3) | 확인되지 않음 | 위와 같음 |
| (4) | 확인되지 않음 | 위와 같음 |
| (5) | 확인되지 않음 | 위와 같음 |
| (6) | 확인되지 않음 | 위와 같음 |
| (7) | 확인되지 않음 | 위와 같음 |
| (8) | 확인되지 않음 | 도구 안에서 주장별 출처를 표시하는지는 확인되지 않음. 도구 자체는 동료심사 논문(CHI 2026)으로 출판됨 |
| (9) | 지원 | 사용자가 넣은 텍스트로 실제 GPT-2 내부 구성요소를 실시간으로 관찰함 ([README](https://github.com/poloclub/transformer-explainer)) |
| (10) | 지원 | MIT 라이선스이고 로컬에서 실행할 수 있음(`npm run dev`) ([README](https://github.com/poloclub/transformer-explainer)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 실제 모델 연산에 근거한 Transformer 인터랙티브 설명.

**AIXON 대비 공백**
- 평가, 학습자 상태, 경로, 개념 그래프와 연결되지 않음(확인되지 않음).

---

## 8. CNN Explainer (Georgia Tech Polo Club)

**한 줄 설명**
"An interactive visualization system designed to help non-experts learn about Convolutional Neural Networks (CNNs)" ([README](https://github.com/poloclub/cnn-explainer)). 학습에 쓴 CNN 코드는 `tiny-vgg/` 디렉터리에 있음.

**운영 주체**
- Zijie J. Wang 외, Georgia Tech Polo Club.

**현재 상태**
- 데모 운영 중 ([데모](https://poloclub.github.io/cnn-explainer/)).
- 마지막 커밋 2023-10-14 ([commits](https://github.com/poloclub/cnn-explainer/commits/master)).
- 논문: IEEE TVCG 2020 (DOI 10.1109/TVCG.2020.3030418, [DOI](https://doi.org/10.1109/TVCG.2020.3030418)).

**오픈소스:** MIT. 별 약 9.1k.

**무료/유료:** 무료.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 단일 개념 시각화 도구라 범위 밖으로 보임(추론). 관련 기능은 확인되지 않음 ([README](https://github.com/poloclub/cnn-explainer)) |
| (2) | 확인되지 않음 | 위와 같음 |
| (3) | 확인되지 않음 | 위와 같음 |
| (4) | 확인되지 않음 | 위와 같음 |
| (5) | 확인되지 않음 | 위와 같음 |
| (6) | 확인되지 않음 | 위와 같음 |
| (7) | 확인되지 않음 | 위와 같음 |
| (8) | 확인되지 않음 | 도구 안의 출처 표시는 확인되지 않음. 도구는 TVCG 논문으로 출판됨 |
| (9) | 지원 | 인터랙티브 시각화로 CNN 연산을 학습함 ([README](https://github.com/poloclub/cnn-explainer)) |
| (10) | 지원 | MIT 라이선스. README가 "use CNN Explainer with your own CNN model or image classes" 방법을 이슈로 안내함 ([README](https://github.com/poloclub/cnn-explainer)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 비전문가 대상 CNN 연산 시각화.

**AIXON 대비 공백**
- Transformer Explainer와 같음. 2023년 이후 업데이트가 없음.

---

## 9. NotebookLM → Gemini Notebook (Google)

**한 줄 설명**
사용자가 올린 소스에 근거해(인용과 함께) 답변과 학습 자료를 만드는 AI 리서치·노트 도구. 학습 자료로는 플래시카드, 퀴즈, 마인드맵, Audio/Video Overview, 리포트가 있음.

**운영 주체:** Google.

**현재 상태**
- 2026-07-16 "We're renaming NotebookLM to Gemini Notebook." 같은 단독 제품이며, 노트북마다 "a secure cloud computer"가 생겨 코드 실행이 가능해짐 ([Google blog](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/), [Workspace Updates](https://workspaceupdates.googleblog.com/2026/07/notebooklm-now-gemini-notebook.html)).
- notebooklm.google.com은 notebook.google.com으로 리디렉션됨(관찰).
- 학습 기능 발표(2025-09-08): 플래시카드와 퀴즈, 그리고 "Learning Guide" 채팅 설정 — "encourages participation with probing, open-ended questions" ([Google blog](https://blog.google/technology/google-labs/notebooklm-student-features/)).
- Workspace 교육 고객 대상 출시는 2025-09-11 ([Workspace Updates](https://workspaceupdates.googleblog.com/2025/09/flashcards-quizzes-reports-notebook-lm-google-education.html)).

**오픈소스:** 비공개. Enterprise용 REST API(`v1alpha`, `notebooks.create` 등)가 Google Cloud에 있음 ([Cloud docs](https://docs.cloud.google.com/agentspace/notebooklm-enterprise/docs/api-notebooks)).

**무료/유료** ([Plans](https://support.google.com/notebooklm/answer/16213268), [Usage limits](https://support.google.com/gemininotebook/answer/17670842))
- Standard(무료, Gmail 계정): 노트북 100개, 노트북당 소스 50개.
- Plus: 200개 / 100개. Pro: 500개 / 300개. Ultra: 500개 / 500개 또는 600개.
- 사용량 한도는 연산량 기준임. 5시간마다 회복되며 주간 한도가 있음.
- AI Plus는 표준 한도의 2배, AI Pro는 4배, AI Ultra는 Pro의 5배 또는 20배.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 부분 지원 | "To find sources from the web or files from Workspace, type a research question in the search box". 채팅에서 리서치를 수행하고 보고서와 소스를 노트북으로 가져올 수 있음. 학술 DB에 특화되어 있는지는 확인되지 않음 ([Sources](https://support.google.com/gemininotebook/answer/16215270), [Chat](https://support.google.com/gemininotebook/answer/16179559)) |
| (2) | 부분 지원 | Mind Maps가 "main topics and related ideas as a branching diagram"을 보여 줌. 인용 관계 시각화는 확인되지 않음 ([Mind Maps](https://support.google.com/gemininotebook/answer/16212283)) |
| (3) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (4) | 부분 지원 | 노트북 단위로 AI가 생성하는 마인드맵이 있고, 노드를 선택해 질문할 수 있음. 지속적이고 전역적인 개념 그래프는 확인되지 않음 ([Mind Maps](https://support.google.com/gemininotebook/answer/16212283)) |
| (5) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (6) | 확인되지 않음 | Learning Guide는 "adapts explanations to your needs"인 대화 스타일임. 경로 계산은 확인되지 않음 ([Google blog](https://blog.google/technology/google-labs/notebooklm-student-features/), [Chat](https://support.google.com/gemininotebook/answer/16179559)) |
| (7) | 부분 지원 | 플래시카드에 "Got it!/Missed it!"를 표시하면 "Gemini Notebook will remember your progress". 결과를 리뷰하고 다시 풀 수 있음. 노트북을 가로지르는 학습자 모델은 확인되지 않음 ([Flashcards/Quizzes](https://support.google.com/gemininotebook/answer/16958963)) |
| (8) | 지원 | "uses direct quotes, text, and images from your sources as citations". hover하면 인용 전문이 보이고, 클릭하면 원문 위치로 이동함. 플래시카드와 퀴즈의 "Explain"도 인용과 함께 설명함 ([Chat](https://support.google.com/gemininotebook/answer/16179559), [Google blog](https://blog.google/technology/google-labs/notebooklm-student-features/)) |
| (9) | 부분 지원 | 플래시카드, 퀴즈(Hint, Explain), Learning Guide, 인터랙티브 마인드맵이 있음. 시뮬레이션은 확인되지 않음 ([Flashcards/Quizzes](https://support.google.com/gemininotebook/answer/16958963)) |
| (10) | 부분 지원 | Enterprise API(v1alpha)가 있고, 플래시카드 CSV 다운로드와 마인드맵 다운로드가 가능함. 소비자용 공개 API와 오픈소스는 확인되지 않음 ([Cloud docs](https://docs.cloud.google.com/agentspace/notebooklm-enterprise/docs/api-notebooks)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 소스 근거 답변과 클릭 가능한 인용.
- 소스로부터 학습 자료(플래시카드, 퀴즈, 마인드맵, 오디오·비디오 개요) 자동 생성.
- Learning Guide 튜터링.
- 무료 플랜에서도 이 기능을 쓸 수 있음.

**AIXON 대비 공백**
- 노트북(소스 묶음) 단위로 닫혀 있고, 전역 개념·선수 그래프가 없음.
- 학습자 모델은 덱 단위 진도 수준임.
- 연구 진화와 인용 그래프가 없음.
- 클라우드 서비스임.

---

## 10. ChatGPT study mode (OpenAI)

**한 줄 설명**
ChatGPT의 학습 모드. 답을 바로 주는 대신 소크라테스식 질문, 단계적 설명, 이해도 점검(퀴즈)으로 학습을 이끎.

**운영 주체:** OpenAI.

**현재 상태**
- 2025-07-29 출시. 당시 "available to logged in users on Free, Plus, Pro, Team", Edu는 수주 내 제공 ([OpenAI](https://openai.com/index/chatgpt-study-mode/)).
- 현재 FAQ: "available across ChatGPT plans globally on web, iOS, and Android, and is available for all ChatGPT models". Temporary Chats, GPTs, Projects에서는 쓸 수 없음 ([FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq)).
- 구현 방식(출시 당시): "powered by custom system instructions … we plan on training this behavior directly into our main models" ([OpenAI](https://openai.com/index/chatgpt-study-mode/)).
- 2026-03-10: "dynamic visual explanations". 70개 이상의 수학·과학 개념에서 변수와 공식을 조작할 수 있고, 모든 플랜에 제공됨 ([OpenAI](https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt), 날짜 교차확인: [TechCrunch](https://techcrunch.com/2026/03/10/chatgpt-can-now-create-interactive-visuals-to-help-you-understand-math-and-science-concepts/)).

**오픈소스:** 비공개.

**무료/유료:** 모든 플랜에서 쓸 수 있음(무료 포함). 메시지·레이트 한도는 각 플랜 규칙을 그대로 따름 ([FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq)).

**10개 기준 판정** (study mode와 OpenAI가 학습 기능으로 묶어 발표한 기능 범위만 평가함)

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | study mode 문서에 문헌 발견 언급이 없음. ChatGPT 일반 검색 기능은 평가 범위 밖 |
| (2) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (3) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (4) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (5) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (6) | 부분 지원 | "Lessons are tailored to the right level for the user, based on questions that assess skill level and memory from previous chats". FAQ 예시 "Help me turn them into a study plan". 그래프 기반 계산은 확인되지 않음 ([OpenAI](https://openai.com/index/chatgpt-study-mode/), [FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq)) |
| (7) | 부분 지원 | Memory를 켜면 "may remember your learning goals, preferred explanation style, or topics you have studied before". 출시 때는 "Goal setting and progress tracking across conversations"를 탐색 중이라고 했으나, 현재 FAQ에서 출시 여부는 확인되지 않음 ([FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq), [OpenAI](https://openai.com/index/chatgpt-study-mode/)) |
| (8) | 확인되지 않음 | FAQ는 업로드 자료 참조만 언급하고, 인용·출처 표시 기능은 언급하지 않음 ([FAQ](https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq)) |
| (9) | 지원 | Socratic 질문, 힌트, knowledge checks("Quizzes and open-ended questions")가 있음. 2026-03에는 인터랙티브 비주얼 모듈이 추가됨("adjust variables, manipulate formulas") ([OpenAI](https://openai.com/index/chatgpt-study-mode/), [OpenAI](https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt)) |
| (10) | 확인되지 않음 | study mode 전용 API나 공개 지시문은 확인되지 않음 |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 무료로 제공되는 소크라테스식 AI 튜터.
- 업로드 자료 기반 퀴즈와 플래시카드식 복습.
- 공식·변수 조작형 인터랙티브 비주얼(70개 이상 개념).

**AIXON 대비 공백**
- 명시적 개념·선수 그래프가 없음.
- 학습자 상태가 자유 형식 Memory 수준임.
- 인터랙티브 비주얼과 평가가 연동되는지 확인되지 않음.
- 출처 추적이 확인되지 않음.
- 클라우드 서비스임.

---

## 11. Claude learning mode (Anthropic)

**한 줄 설명**
Claude가 정답 대신 소크라테스식 질문으로 사고를 유도하는 학습 모드. Claude Code에서는 사용자가 코드 일부를 직접 작성하는 Learning output style로 제공됨.

**운영 주체:** Anthropic.

**현재 상태**
- 2025-04-02 Claude for Education에서 "Learning mode"를 도입함. Projects 안에서 동작하며 "Using Socratic questioning: Prompting with 'What evidence supports your conclusion?'" ([Anthropic](https://www.anthropic.com/news/introducing-claude-for-education))
- 2025-08-14 보도: Claude.ai 모든 사용자의 style 드롭다운에 "Learning"이 추가되고, Claude Code에 "Explanatory"와 "Learning" output style이 추가됨. 이는 2차 출처이며 공식 발표문은 확인하지 못함 ([Engadget](https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html))
- Claude Code 1.0.81 changelog: "Released output styles, including new built-in educational output styles 'Explanatory' and 'Learning'" ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md))
- 현재 공식 교육 페이지: "Claude's learning mode works like a good tutor: it asks questions that help you find the answers yourself." ([claude.com/solutions/education](https://claude.com/solutions/education))
- Claude.ai 일반 사용자용 스타일 메뉴의 현재 UI 경로는 공식 도움말로 확인되지 않음.

**오픈소스:** 비공개. Claude Code output style은 사용자가 정의할 수 있음 ([docs](https://code.claude.com/docs/en/output-styles)).

**무료/유료:** 보도 기준 모든 사용자. 플랜별 세부 조건은 확인되지 않음.

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | learning mode 범위에서 해당 기능은 확인되지 않음 |
| (2) | 확인되지 않음 | 위와 같음 |
| (3) | 확인되지 않음 | 위와 같음 |
| (4) | 확인되지 않음 | 위와 같음 |
| (5) | 확인되지 않음 | 위와 같음 |
| (6) | 확인되지 않음 | 위와 같음 |
| (7) | 부분 지원 | Claude memory는 "saves memory as a set of individual topics"이고 Settings > Memory에서 열람·편집할 수 있음. 학습 전용 학습자 모델은 아님 ([Claude memory](https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context)) |
| (8) | 확인되지 않음 | learning mode 문서에 출처 표시 언급이 없음 |
| (9) | 부분 지원 | Socratic 질문을 함 ([Anthropic](https://www.anthropic.com/news/introducing-claude-for-education)). Claude Code Learning style은 `TODO(human)`을 표시한 뒤 사용자가 코드를 쓰면 Insight로 피드백함 ([docs](https://code.claude.com/docs/en/output-styles)) |
| (10) | 부분 지원 | Claude Code는 "write a custom style"을 문서화함. 학습 모드 내부 지시문의 공개는 확인되지 않음 ([docs](https://code.claude.com/docs/en/output-styles)) |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 소크라테스식 튜터링.
- 코딩 실습형 학습(Learning output style).

**AIXON 대비 공백**
- 그래프, 경로, 평가 기반 학습자 모델, 출처 추적이 확인되지 않음.

---

## 12. Anki + FSRS

**한 줄 설명**
- Anki: 오픈소스 간격 반복 플래시카드 앱.
- FSRS: 사용자의 리뷰 로그로 개인 기억 모델 파라미터를 학습하는 오픈소스 스케줄러. Anki 23.10부터 내장 옵션.

**운영 주체**
- Anki: "Anki is a registered trademark of Ankitects Pty Ltd". 커뮤니티 프로젝트 ([apps.ankiweb.net](https://apps.ankiweb.net/)).
- FSRS: open-spaced-repetition 커뮤니티. 핵심 기여자 Jarrett Ye, MaiMemo가 지원 ([ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/ABC-of-FSRS)).

**현재 상태**
- Anki 데스크톱 현재 버전 26.09.3 ([apps.ankiweb.net](https://apps.ankiweb.net/)).
- FSRS 최신 버전은 FSRS-6, 파라미터 21개 ([The Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm)).

**오픈소스**
- Anki: AGPL-3.0+ ([LICENSE](https://github.com/ankitects/anki/blob/main/LICENSE)).
- FSRS 구현: fsrs4anki MIT, py-fsrs MIT, ts-fsrs MIT, fsrs-rs BSD-3-Clause ([fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki), [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs), [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs), [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs)).

**무료/유료** ([apps.ankiweb.net](https://apps.ankiweb.net/))
- 데스크톱 무료, AnkiDroid 무료, AnkiWeb 동기화 무료.
- AnkiMobile(iOS)은 유료("all purchases help fund Anki's development"). 가격은 확인하지 않음.

**FSRS 핵심** ([Anki manual](https://docs.ankiweb.net/deck-options.html), [The Algorithm](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm))
- "an alternative to Anki's legacy SuperMemo 2 (SM-2) algorithm".
- desired retention 기본값 90%.
- "Optimize"가 리뷰 이력으로 파라미터를 학습함.
- 망각곡선: R(t,S) = (1 + factor·t/S)^(−w20). D ∈ [1,10].
- 기반 논문으로 MaiMemo의 KDD 논문과 TKDE 논문을 인용함 ([ABC of FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/ABC-of-FSRS)).

**10개 기준 판정**

| 기준 | 판정 | 근거 |
|---|---|---|
| (1) | 확인되지 않음 | 덱 공유는 있으나 문헌 발견 기능은 확인되지 않음 ([apps.ankiweb.net](https://apps.ankiweb.net/)) |
| (2) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (3) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (4) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (5) | 확인되지 않음 | 해당 기능은 확인되지 않음 |
| (6) | 부분 지원 | 카드별 복습 일정을 개인 기억 파라미터로 최적화함. 학습 경로나 선수 순서는 아님 ([Anki manual](https://docs.ankiweb.net/deck-options.html)) |
| (7) | 지원 | 리뷰 이력과 개인 FSRS 파라미터("parameters that best fit your review history")가 있음. 증거는 사용자의 회상 자기평가. 매뉴얼이 "pressing 'Hard' instead of 'Again' when you forget"를 오남용으로 경고함 ([Anki manual](https://docs.ankiweb.net/deck-options.html)) |
| (8) | 확인되지 않음 | 카드 내용의 출처 추적 기능은 확인되지 않음 |
| (9) | 부분 지원 | 능동 회상 복습. 시뮬레이션은 확인되지 않음 |
| (10) | 지원 | AGPL-3.0 앱이고, MIT·BSD 라이선스의 FSRS 라이브러리가 여러 언어로 있음 |

**잘 해결하는 것 (AIXON이 차별점으로 주장하면 안 됨)**
- 개인화 간격 반복과 기억 모델 파라미터 최적화.
- 로컬 앱과 무료 동기화.
- 재사용 가능한 오픈소스 스케줄러.

**AIXON 대비 공백**
- 카드가 서로 독립적이며 개념·선수 그래프를 인지하지 않음.
- Math Academy 공식 페이지도 이 점을 기존 알고리즘의 한계로 지적함: "limited to the context of independent flashcards" ([Math Academy](https://www.mathacademy.com/how-our-ai-works)).

---

## Gaps & implications for AIXON

### A. prerequisite 그래프 기반 학습 계획: 선행 사례가 매우 많음

AIXON의 「개인화 prerequisite 학습 경로」는 새로운 아이디어가 아니며, ML 도메인에 한정해도 마찬가지다.

1. **이론**
   - KST는 1990년 *Psychological Review* 논문과 1999·2011년 단행본으로 정립되어 있음 ([ALEKS KST](https://www.aleks.com/about_aleks/knowledge_space_theory)).
2. **상용 대규모 서비스**
   - ALEKS: "over 50 million students", 26년치 데이터 ([Overview](https://www.aleks.com/about_aleks/overview)).
   - Math Academy: 수천 개 토픽의 그래프, 진단, FIRe를 갖추고 **Mathematics for Machine Learning** 301개 토픽까지 제공함 ([How Our AI Works](https://www.mathacademy.com/how-our-ai-works), [ML 과정](https://www.mathacademy.com/courses/mathematics-for-machine-learning)).
3. **ML 도메인 오픈소스: Metacademy (2014년 전후)** — 사실상 AIXON 학습 축의 직계 선행 사례
   - 개념 prerequisite 그래프.
   - 목표 개념에서 learning plan 생성.
   - 학습 완료 개념 추적과 implicit learned 추론.
   - learning goal 단위 간선과 선수 이유 텍스트.
   - 시간 추정과 roadmap.
   - 출처: [about.html](https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html), [graph_data.json](https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json)
4. **무료 LLM 튜터**
   - ChatGPT study mode, Claude learning mode, NotebookLM Learning Guide가 소크라테스식 튜터링과 퀴즈·플래시카드 생성을 이미 기본 제공함.

**AIXON이 차별점으로 주장하면 안 되는 것**

| 주장하면 안 되는 것 | 이미 하는 제품 |
|---|---|
| prerequisite 그래프 자체 | Metacademy, Math Academy, ALEKS |
| 목표 개념에서 학습 계획 생성 | Metacademy |
| 아는 개념 체크·추적 | Metacademy, Learn Anything |
| 진단 기반 배치와 개인화 경로 | Math Academy, ALEKS |
| ML 수학 선수지식 커리큘럼 | Math Academy |
| 그래프 인지형 간격 반복 | Math Academy FIRe |
| 최신 간격 반복 알고리즘 | Anki + FSRS |
| 소스 근거 답변·인용과 학습 자료 자동 생성 | NotebookLM/Gemini Notebook |
| 소크라테스식 AI 튜터 | ChatGPT, Claude, NotebookLM |
| 브라우저 인터랙티브 NN·Transformer 시각화 | TF Playground, Transformer/CNN Explainer, ChatGPT 비주얼 |
| 동료심사 인터랙티브 설명 | Distill |

### B. 조사 범위 안에서 비어 있는 영역 (추론, 다른 트랙 결과와 교차검증 필요)

1. **연구 산출물과 학습 그래프의 결합.** 분야, 문제, 논문, 모델, 방법을 개념·선수 그래프에 연결하는 제품은 12개 중 없음. (1)–(3) 기준이 전부 「확인되지 않음」이거나 「부분 지원」임. Metacademy의 리소스 포인터와 NotebookLM의 노트북 단위 소스가 가장 가까움.
2. **간선 단위 근거.** Metacademy에는 이미 큐레이터가 쓴 간선별 `reason` 텍스트가 있음(1,006/1,208). 따라서 AIXON의 "evidence-backed edges"가 차별점이 되려면 그 이상이 필요함. 예: 인용 가능한 출처(논문·교재 위치), 근거의 강도, 검토 상태. NotebookLM의 인용은 답변 단위이고 그래프 간선 단위가 아님.
3. **인터랙티브 랩 수행을 학습자 모델 증거로 쓰는 루프.** 공식 문서로 확인된 사례가 없음(Q4). 다만 조사 범위 밖의 제품은 확인하지 않았으므로 「없다」고 단정할 수 없음.
4. **로컬 우선, 사용자 소유의 평가 기반 학습자 모델.** 평가 기반 모델을 가진 Math Academy와 ALEKS는 비공개 클라우드 서비스임. 로컬 앱인 Anki는 카드 단위만 다룸. local-first 여부와 데이터 내보내기는 이번 10개 기준 밖이라 제품별로 조사하지 않았음.
5. **AI 연구의 최신성.** Metacademy 공개 덤프는 2014–2015년 수정 기록뿐이고 transformer와 attention 계열 개념이 없음. Math Academy는 수학 기초까지만 다룸.
6. **연구 진화(시간축).** 12개 제품 모두 「확인되지 않음」.

### C. 설계 시사점 (추론)

**포지셔닝**
- 「prerequisite 학습 경로」를 앞세우지 말 것.
- 대신 위 B의 1–4를 결합한 것을 내세우는 편이 정직함: 연구 문헌에 근거해 출처를 추적할 수 있는 개념·선수 그래프, 평가와 랩 수행 증거로 갱신되는 로컬 학습자 모델, 연구 진화와의 연결.

**Metacademy 자산 재사용**
- 스키마(개념 설명, learning goals, 시간 추정, 리소스 위치, goal 수준 간선, 간선 이유)는 검증된 선례임.
- 공개 덤프는 출발점으로 쓸 수 있음.
- 라이선스: 코드 GPLv3, 콘텐츠 CC BY-SA 3.0. 재배포하려면 각 라이선스 조건을 지켜야 함(법률 판단은 이 문서의 범위 밖).

**학습자 모델 설계**
- 자기보고 체크(Metacademy, Learn Anything)는 구현이 쉽지만 증거가 약함.
- 평가 증거(Math Academy, ALEKS), 그래프 전파(Metacademy의 implicit learned, Math Academy의 양·음 증거 전파), 기억 모델(FSRS)을 조합하는 것이 선행 사례와 정합적임.

**간격 반복**
- FSRS 라이브러리(MIT/BSD)는 재사용할 수 있음.
- 개념 그래프 위에서 반복 크레딧을 전파하는 방식은 Math Academy FIRe가 이미 공개적으로 설명했음. 이를 신규성으로 주장하지 말 것.

**인터랙티브 랩**
- TF Playground(Apache-2.0), Transformer/CNN Explainer(MIT), Distill 기사(CC-BY 4.0)는 임베드·재사용 후보임.
- 이들은 평가와 학습자 모델 연동이 확인되지 않았으므로, 연동 계층을 붙이는 쪽이 차별 후보임.

**지속성 리스크**
- Metacademy: 2인 수작업 큐레이션("countless hours") 후 2023년 보관, 현재 접속 불가.
- Learn Anything: 반복된 피벗과 저장소 이전.
- Distill: 2021년부터 무기한 휴간.
- 소수 인원이 운영하는 지식 큐레이션 프로젝트는 유지가 어렵다는 강한 선례이며, 1인 프로젝트인 AIXON은 큐레이션 자동화와 범위 통제가 필수임.

### D. 추가 확인이 필요한 항목
- metacademy.org의 현재 상태(Internet Archive 복구 후 스냅샷 확인).
- Math Academy 학습자 앱의 그래프 탐색 UI와 데이터 내보내기 여부.
- ALEKS의 API·LTI 연동.
- ChatGPT의 "Quizzes" 단축 기능과 플래시카드가 진도를 저장하는지.
- Claude.ai Learning 스타일의 현재 공식 도움말.
- Learn Anything의 운영 지속 여부.
- 범위 밖 선행 사례(예: Brilliant, Khan Academy, Arbital). Arbital은 concept dependency tracking 사례로 언급됨([learning.subwiki](https://learning.subwiki.org/wiki/Concept_dependency_tracking), 2차 출처).

---

## 출처 목록 (모두 확인 2026-10-15)

**Learn Anything**
- https://learn-anything.xyz/ — 홈, meta description(확인 2026-10-15)
- https://learn-anything.xyz/_build/.vite/manifest.json — 라우트 목록(확인 2026-10-15)
- https://learn-anything.xyz/_build/assets/index-BIK8JTzQ.js — onboarding 문구, 학습 상태, study guide(확인 2026-10-15)
- https://learn-anything.xyz/_build/assets/index-BXRjHR5G.js — 랜딩 토픽 그래프(connectedTopics)(확인 2026-10-15)
- https://learn-anything.xyz/_build/assets/_pages-Dp1-g3JL.js — topicsWantToLearn/Learning/Learned(확인 2026-10-15)
- https://docs.learn-anything.xyz/ — placeholder 문서(확인 2026-10-15)
- https://github.com/learn-anything — 조직, 공개 저장소 없음(확인 2026-10-15)
- https://github.com/learn-anything/learn-anything → https://github.com/linsa-io/linsa — 301 리디렉션, README(확인 2026-10-15)
- https://api.github.com/repositories/65219131 — 생성일, 푸시일, 라이선스, 별 수(확인 2026-10-15)
- https://github.com/linsa-io/linsa/commits/main — 커밋 1개, 2026-01-17(확인 2026-10-15)
- https://linsa.io — Linsa 제품 소개(확인 2026-10-15)
- https://news.ycombinator.com/item?id=14483578 (확인 2026-10-15)
- https://news.ycombinator.com/item?id=14798336 (확인 2026-10-15)
- https://news.ycombinator.com/item?id=14832129 (확인 2026-10-15)
- https://news.ycombinator.com/item?id=18688902 (확인 2026-10-15)
- https://news.ycombinator.com/item?id=40088501 (확인 2026-10-15)
- https://hn.algolia.com/api/v1/search?query=learn-anything.xyz&restrictSearchableAttributes=url — 제출 이력 조회에 사용(확인 2026-10-15)
- https://alternativeto.net/software/learn-anything/about — 2차 출처, MIT·마인드맵(확인 2026-10-15)
- https://raw.githubusercontent.com/learn-anything/curated-lists/master/readme.md (확인 2026-10-15)
- https://tproger.ru/news/learn-anything-search-engine — 2차 출처, 제작자(확인 2026-10-15)
- https://wiki.skiddle.id/ideas/learn-anything — 2차 출처, 위키 사본(확인 2026-10-15)
- https://www.producthunt.com/products/learn-anything-3 — 동명의 무관 제품(확인 2026-10-15)

**Metacademy**
- https://metacademy.org — 접속 실패(확인 2026-10-15)
- https://github.com/metacademy (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application — archived 2023-07-06, GPLv3(확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/server/static/html/about.html (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/server/apps/user_management/models.py (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/aux-model.js (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/models/explore-graph-model.js (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/server/static/javascript/agfk/views/agfk-concept-list-view.js (확인 2026-10-15)
- https://github.com/metacademy/metacademy-application/blob/master/dev_utils/graph_data.json — 직접 집계(확인 2026-10-15)
- https://github.com/metacademy/metacademy-content — deprecated, CC BY-SA 3.0(확인 2026-10-15)
- https://hunch.net/?p=2714 — Roger Grosse, 2014-02-16(확인 2026-10-15)
- https://news.ycombinator.com/item?id=39007587 — 2024-01-15(확인 2026-10-15)
- https://learning.subwiki.org/wiki/Concept_dependency_tracking — 2차 출처(확인 2026-10-15)

**Math Academy**
- https://www.mathacademy.com/ — $49/mo, JOIN BETA(확인 2026-10-15)
- https://www.mathacademy.com/how-our-ai-works (확인 2026-10-15)
- https://www.mathacademy.com/how-it-works (확인 2026-10-15)
- https://www.mathacademy.com/pedagogy (확인 2026-10-15)
- https://www.mathacademy.com/courses (확인 2026-10-15)
- https://www.mathacademy.com/courses/mathematics-for-machine-learning (확인 2026-10-15)
- https://www.mathacademy.com/faq — 무료 체험 없음, 30일 환불(확인 2026-10-15)
- https://www.mathacademy.com/adult-students (확인 2026-10-15)
- https://www.mathacademy.com/about-us (확인 2026-10-15)
- https://justinmath.com/golden-nuggets-podcast-39/ — 준공식, 직원 사이트(확인 2026-10-15)

**ALEKS**
- https://www.aleks.com/about_aleks/overview (확인 2026-10-15)
- https://www.aleks.com/about_aleks/knowledge_space_theory (확인 2026-10-15)
- https://www.aleks.com/independent (확인 2026-10-15)
- https://www.aleks.com/buy_aleks_now — 가격(확인 2026-10-15)
- https://www.aleks.com/free_trial (확인 2026-10-15)

**TensorFlow Playground**
- https://playground.tensorflow.org/ (확인 2026-10-15)
- https://github.com/tensorflow/playground (확인 2026-10-15)
- https://github.com/tensorflow/playground/commits/master (확인 2026-10-15)
- https://github.com/tensorflow/playground/blob/master/LICENSE (확인 2026-10-15)

**Distill**
- https://distill.pub/ (확인 2026-10-15)
- https://distill.pub/2021/distill-hiatus/ (확인 2026-10-15)
- https://distill.pub/journal/ (확인 2026-10-15)
- https://distill.pub/2021/gnn-intro/ (확인 2026-10-15)

**Transformer Explainer**
- https://github.com/poloclub/transformer-explainer (확인 2026-10-15)
- https://github.com/poloclub/transformer-explainer/commits/main (확인 2026-10-15)
- https://poloclub.github.io/transformer-explainer/ (확인 2026-10-15)
- https://dl.acm.org/doi/10.1145/3772318.3791725 (확인 2026-10-15)
- https://arxiv.org/abs/2408.04619 (확인 2026-10-15)

**CNN Explainer**
- https://github.com/poloclub/cnn-explainer (확인 2026-10-15)
- https://github.com/poloclub/cnn-explainer/commits/master (확인 2026-10-15)
- https://poloclub.github.io/cnn-explainer/ (확인 2026-10-15)
- https://doi.org/10.1109/TVCG.2020.3030418 (확인 2026-10-15)
- https://arxiv.org/abs/2004.15004 (확인 2026-10-15)

**NotebookLM / Gemini Notebook**
- https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/ — 2026-07-16 개명(확인 2026-10-15)
- https://workspaceupdates.googleblog.com/2026/07/notebooklm-now-gemini-notebook.html (확인 2026-10-15)
- https://blog.google/technology/google-labs/notebooklm-student-features/ — 2025-09-08(확인 2026-10-15)
- https://workspaceupdates.googleblog.com/2025/09/flashcards-quizzes-reports-notebook-lm-google-education.html — 2025-09-11(확인 2026-10-15)
- https://support.google.com/gemininotebook/answer/16958963 — Flashcards/Quizzes(확인 2026-10-15)
- https://support.google.com/gemininotebook/answer/16179559 — Chat, 인용, Learning Guide(확인 2026-10-15)
- https://support.google.com/gemininotebook/answer/16212283 — Mind Maps(확인 2026-10-15)
- https://support.google.com/gemininotebook/answer/16215270 — Sources(확인 2026-10-15)
- https://support.google.com/notebooklm/answer/16213268 — Plans(확인 2026-10-15)
- https://support.google.com/gemininotebook/answer/17670842 — Usage limits(확인 2026-10-15)
- https://docs.cloud.google.com/agentspace/notebooklm-enterprise/docs/api-notebooks — Enterprise API(확인 2026-10-15)
- https://notebooklm.google.com/ → https://notebook.google.com/ — 리디렉션 관찰(확인 2026-10-15)

**ChatGPT study mode** (openai.com과 help.openai.com은 직접 요청 시 403이 나와 `r.jina.ai` 리더로 본문을 확인함)
- https://openai.com/index/chatgpt-study-mode/ — 2025-07-29(확인 2026-10-15)
- https://help.openai.com/en/articles/11780217-chatgpt-study-mode-faq (확인 2026-10-15)
- https://openai.com/index/new-ways-to-learn-math-and-science-in-chatgpt — 2026-03-10(확인 2026-10-15)
- https://techcrunch.com/2026/03/10/chatgpt-can-now-create-interactive-visuals-to-help-you-understand-math-and-science-concepts/ — 날짜 교차확인(확인 2026-10-15)
- https://campustechnology.com/Articles/2025/07/30/New-ChatGPT-Study-Mode-Guides-Students-Through-Questions.aspx — 날짜 교차확인(확인 2026-10-15)

**Claude learning mode**
- https://www.anthropic.com/news/introducing-claude-for-education — 2025-04-02(확인 2026-10-15)
- https://claude.com/solutions/education (확인 2026-10-15)
- https://code.claude.com/docs/en/output-styles (확인 2026-10-15)
- https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md — 1.0.81(확인 2026-10-15)
- https://engadget.com/ai/anthropic-brings-claudes-learning-mode-to-regular-users-and-devs-170018471.html — 2차 출처, 2025-08-14(확인 2026-10-15)
- https://support.claude.com/en/articles/11817273-using-claude-s-chat-search-and-memory-to-build-on-previous-context — memory(확인 2026-10-15)

**Anki + FSRS**
- https://docs.ankiweb.net/deck-options.html — FSRS 섹션(확인 2026-10-15)
- https://apps.ankiweb.net/ (확인 2026-10-15)
- https://github.com/ankitects/anki/blob/main/LICENSE (확인 2026-10-15)
- https://github.com/open-spaced-repetition/fsrs4anki (확인 2026-10-15)
- https://github.com/open-spaced-repetition/fsrs4anki/wiki/ABC-of-FSRS (확인 2026-10-15)
- https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm (확인 2026-10-15)
- https://github.com/open-spaced-repetition/py-fsrs (확인 2026-10-15)
- https://github.com/open-spaced-repetition/ts-fsrs (확인 2026-10-15)
- https://github.com/open-spaced-repetition/fsrs-rs (확인 2026-10-15)

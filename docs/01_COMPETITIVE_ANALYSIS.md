# 01. Competitive Analysis — 기존 해결책과 빈틈

> 조사일 2026-10-15. 공식 문서·도움말·요금 페이지·저장소를 근거로 했다. 확인하지 못한 기능은 "확인되지 않음"이며 "없음"이 아니다. 원자료(제품별 근거 URL 포함): [research/A_literature_tools.md](research/A_literature_tools.md)(문헌 탐색·인용 그래프), [research/B_ai_assistants_kg.md](research/B_ai_assistants_kg.md)(AI 연구 보조·구조화 지식), [research/C_learning_tools.md](research/C_learning_tools.md)(학습·인터랙티브).

## 1. 평가 기준

(1) 문헌 탐색 (2) 인용·관계 시각화 (3) 시간에 따른 연구 발전 (4) 개념 지식 그래프 (5) 명시적 선수 그래프 (6) 개인화 학습 경로 (7) 학습자 상태 영속 (8) 관계의 근거·출처 (9) 인터랙티브 학습 (10) API·오픈소스·재사용. 판정: **지원** / 부분 지원 / 확인되지 않음 / 미지원(공식 근거).

## 2. 요약 표 (대표 제품)

| 제품 | (1) | (2) | (3) | (4) | (5) | (6) | (7) | (8) | (9) | (10) | 상태(2026-10) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Semantic Scholar | 지원 | 부분 | 부분 | 부분 | 확인 안 됨 | 확인 안 됨 | 부분 | **지원**(인용 문맥·의도·영향 인용) | 부분 | **지원**(API, Datasets ODC-BY) | 운영 |
| Connected Papers | 지원 | **지원**(공동 인용 + 서지 결합 유사도) | 부분 | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 부분 | 부분 | 확인 안 됨 | 부분 | 운영 |
| ResearchRabbit | 지원 | **지원** | 부분 | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 부분 | 부분 | 확인 안 됨 | 부분 | 2025-05 Litmaps 인수 보도, 2025-10 개편 |
| Litmaps | 지원 | **지원** | **지원**(시간축 x) | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 부분 | 부분 | 확인 안 됨 | 부분 | 운영 |
| scite | 지원 | 부분 | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 부분 | **지원**(지지·반대·언급 분류) | 부분 | 유료 API | 운영 |
| Elicit · SciSpace · Consensus | **지원** | 확인 안 됨~부분 | 확인 안 됨~부분 | 확인 안 됨~부분 | 확인 안 됨 | 확인 안 됨 | 부분 | **지원**(답변에 출처·인용) | 부분 | 일부 | 운영(Elicit 2026-09 Research Agent로 통합) |
| ORKG | 부분 | 부분 | 부분 | **지원**(기여·비교·연구 문제) | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | 부분(생성자 기록, 값별 인용 없음) | 확인 안 됨 | **지원**(CC0, SPARQL) | 운영 |
| Papers with Code | — | — | — | — | — | — | — | — | — | 덤프 CC BY-SA(스팸 다수) | 2025-07 종료, HF로 리다이렉트 |
| Metacademy | 부분 | 확인 안 됨 | 확인 안 됨 | **지원** | **지원**(간선 1,208개 중 1,006개에 이유) | **지원**(목표 개념에서 역으로 학습 계획) | 부분(자기 표시) | 부분 | 확인 안 됨 | **지원**(오픈소스) | 2023-07 저장소 보관, 데이터 2015년까지 |
| Math Academy | 확인 안 됨 | 확인 안 됨 | 확인 안 됨 | **지원** | **지원** | **지원**(배치 시험 + 지식 그래프) | **지원**(평가 기반) | 확인 안 됨 | 부분 | 확인 안 됨 | 운영(수학, ML용 수학 과정 포함) |
| ALEKS | 확인 안 됨 | — | — | 부분 | 부분 | **지원** | **지원**(KST 적응 평가) | — | 부분 | — | 운영 |
| TensorFlow Playground · Transformer/CNN Explainer · Distill | — | — | — | — | — | — | — | Distill 지원 | **지원** | **지원**(오픈소스) | Distill 2021-07부터 무기한 휴간 |
| NotebookLM(→ Gemini Notebook) · ChatGPT study mode · Claude learning mode | 일부 | 일부 | — | 일부 | 확인 안 됨 | 부분 | 부분(대화 기억) | NotebookLM 지원 | 지원~부분 | 일부 | NotebookLM 2026-07 이름 변경 |
| Anki + FSRS | — | — | — | — | — | 부분 | **지원**(복습 기록) | — | 부분 | **지원** | 운영 |

## 3. 이미 해결된 것 (AIXON의 차별점으로 주장하지 않는다)

- **논문 단위 탐색과 인용·유사도 그래프**: Semantic Scholar, Connected Papers, ResearchRabbit, Litmaps, Inciteful. 시간축 지도(Litmaps)와 "선행/후속 연구" 목록(Connected Papers, ResearchRabbit)도 있다.
- **인용의 성격과 문맥**: Semantic Scholar(배경·방법·결과 의도, 영향 인용), scite(지지·반대·언급).
- **구조화된 연구 기여·연구 문제 엔티티**: ORKG.
- **선수 그래프 기반 학습 계획**: Metacademy(ML, 2014년 무렵, 간선마다 이유), Math Academy·ALEKS(평가 기반 학습자 상태). AIXON의 선수 그래프는 새로운 개념이 아니다. Metacademy의 "간선마다 쓴 이유"가 AIXON 근거 기준의 **최저선**이다.
- **인터랙티브 설명**: TensorFlow Playground, Transformer Explainer, CNN Explainer, Distill.
- **출처를 붙인 LLM 답변**: Elicit, Consensus, SciSpace, NotebookLM.

## 4. 빈틈 (조사한 제품에서 확인되지 않은 것)

1. **모델·방법 단위의 유형 있는 연구 계보**(EXTENDS·ADAPTS·IMPROVES_ON·MITIGATES)와 **관계마다 붙은 원문 인용(특정 버전)·조건·검증/검토 상태** — 조사한 어떤 제품에서도 확인되지 않았다. Semantic Scholar·scite의 근거는 논문 사이 인용 문장 단위다.
2. **연구 지도와 개념 교육 페이지가 같은 Canonical ID로 묶인 구조** — 탐색 도구는 교육이 없고, 교육 도구(Metacademy, Math Academy)는 최신 연구 계보·논문과 연결되지 않는다.
3. **인터랙티브 시뮬레이션 결과를 평가 증거로 쓰는 것** — 조사한 12개 학습 도구에서 확인되지 않았다(P2 학습자 모델과 연결 예정).
4. **AI 생성 콘텐츠와 사람 검토 콘텐츠의 명시적 분리와 공개 관문** — LLM 도구들은 출처를 붙이지만 검토 상태를 공개 단위로 관리하지 않는다(추론, 공식 문서에서 확인되지 않음).

## 5. 차별점과 핵심 가치 제안

**"AI 분야의 구조를 탐색하는 지도와, 개별 개념을 제대로 이해하는 학습 경험을, 근거가 확인된 하나의 그래프 위에서 잇는다."**

| 차별점 | 근거가 되는 설계 | 검증 |
|---|---|---|
| 근거 기반 유형 계보 | 02 §7–8 Claim·Evidence·술어별 근거 정책, rejected tombstone | 시드 인용 121/121 원문 대조 |
| Graph ↔ Wiki 단일 ID | WIKI_CONTENT_ARCHITECTURE §2 | V-LINK-1, E2E-1 |
| 계산으로 확인한 교육 콘텐츠 | `python verify`, Lab golden fixture | V-CODE-1, E2E-2 |
| 넓은 지도 + 깊이 가시화 | atlas.yaml + Coverage | R-14 |
| 공개 관문 | ADR-017 | E2E-9 |

**대상 사용자와 JTBD**: [00_PRODUCT_BRIEF.md §3](00_PRODUCT_BRIEF.md). **MVP 범위와 비목표**: [07_MVP_ROADMAP.md](07_MVP_ROADMAP.md), [00 §5](00_PRODUCT_BRIEF.md). **성공 지표**: [00 §6](00_PRODUCT_BRIEF.md).

## 6. 재사용 가능성

| 대상 | 재사용 방식 | 조건 |
|---|---|---|
| arXiv 메타데이터·HTML | 식별자 검증, 인용 원문 대조 | 메타데이터 CC0, 전문은 짧은 인용만 |
| OpenAlex | 분야 매핑 참고, 인용 후보 | CC0. 메타데이터 오염·work 분할 주의(03 §5.1) |
| Semantic Scholar | externalIds 교차 확인, 인용 후보 | API 재배포 금지 |
| Metacademy 데이터 | 선수 간선 후보(P1, 2015년 이전 개념) | 라이선스 확인 필요(확인되지 않음) |
| d2l.ai 등 교재 | 링크로 안내(학습 자료 엔티티) | 복사하지 않는다(CC BY-SA 전염성) |
| Papers with Code 덤프 | 사용하지 않음 | 스팸 비율이 높음 |

# ISSUE_LOG — 발견한 결함과 처리

> 심각도: Critical(데이터·학습 결과 신뢰성 훼손 또는 핵심 구현 불가) · Major(주요 기능·정확성에 중대한 영향) · Minor · Enhancement. 상태: Fixed / Open / Accepted(근거 있는 예외) / Backlog.
> 모든 Fixed 항목에는 재발 방지 테스트 또는 검사가 있다(“회귀 검사” 열).

| ID | 심각도 | 영역 | 내용 | 근본 원인 | 처리 | 회귀 검사 | 상태 |
|---|---|---|---|---|---|---|---|
| I-01 | Critical | 계획기 | 같은 단위의 단계를 "마지막 위치로 모아" 합쳐, 그 사이에 있는 노드가 자신의 선수보다 앞에 올 수 있었다(예: xray@E가 alpha@E보다 먼저) | Codex 2차 구현이 명세(연속 병합)와 P1 기대(C, B, A)의 **명세 내부 모순**을 다른 방식으로 해결함 | 연속 병합으로 되돌리고, pass 2에서 차원 함의를 마지막에 방문하도록 명세(04 §4.3)와 코드를 함께 수정 | P16, 시드 모든 목표의 위상 순서 불변식 | Fixed |
| I-02 | Major | 숙련도 규칙 | 진단(explain)에서 틀린 뒤에도 같은 단위의 recognize가 "자기보고만 있음"으로 남아, 문항 없는 recognize 진단 단계가 생겼다 | "응답 없음"을 (단위, 차원) 단위로만 판단 | 그 단위의 어떤 차원에든 응답이 있으면 자기보고 주장 무효(mastery-v1.1, 04 §3.2) | P15b(재계획 시퀀스) | Fixed |
| I-03 | Critical | 데이터(atlas) | arXiv ID가 따옴표 없이 저장되어 YAML이 실수로 읽음 → `1611.03530`이 `1611.0353`으로 손상 | 스키마가 식별자 타입을 강제하지 않음 | 원본 텍스트에서 ID 복구, 문자열로 정규화. 검증기에 G021(식별자는 문자열) 추가, 식별자 검증기에 `invalid_id_type` | G021 테스트, verify_identifiers | Fixed |
| I-04 | Critical | 데이터(atlas) | 대표 논문 66편 중 **12편이 arXiv에 없는 논문에 지어낸 ID**(TransE, RankNet, Hessian-free, CTC, RRT, GPT-2, Lazaridou 등) | LLM(Codex)이 네트워크 없이 기억으로 작성 | arXiv API 제목 대조로 발견, 12편 삭제. 남은 54편 + 시드 13편 모두 일치 확인(2026-10-15) | `tools/verify_identifiers.py`(CI에서는 네트워크 필요 → 수동 단계) | Fixed |
| I-05 | Major | 데이터(atlas) | KU 76개가 모두 `method:`로 분류됨(VC 차원·ELBO는 Concept, StyleGAN·GAT는 Model, NER 등은 과제) | 분류 절차(02 §4.16) 미적용 | Concept 13, Model 6, Field 3(과제), Method 54로 재분류, 참조 갱신 | (사람 검토 항목) | Fixed |
| I-06 | Major | 데이터(atlas) | 시드에 있는 BERT 논문을 다른 ID로 중복 등록 | 파일 간 중복 확인 없이 작성 | 삭제하고 시드 ID를 `related`로 참조 | G005(병합 검증) | Fixed |
| I-07 | Major | 검증기 | 필수 필드 누락을 잡지 못함(빈 `explains` 자료 5건이 통과) | 03 §2.2의 필수 표시가 검증기에 없었음 | G020(필수 필드) 추가, 빈 자료 5건 삭제 | G020 테스트 | Fixed |
| I-08 | Critical | 인용 대조 | HTML 인라인 태그마다 공백을 넣어 `[11]`이 `[ 11 ]`이 됨 → 인용 부호가 있는 arXiv 인용 대조가 실패 | 텍스트 추출 방식 | 공백 무시 비교 + 하이픈 줄바꿈 두 변형 | 인용 마커 테스트, 시드 121/121 통과, 음성 대조(바꾼 인용 → not_found) | Fixed |
| I-09 | Minor | 계획기 | 같은 OR 그룹 선택이 `choices`에 중복 기록 | 상위 차원에서 하위 차원 요구를 다시 적용 | `for_dimension == d` 정확 일치 | 중복 선택 테스트 | Fixed |
| I-10 | Minor | 콘텐츠 | 대표 Wiki 예제 숫자 오류(0.504 → 0.503) | 손계산 반올림 | `python verify` assert가 발견, 본문·assert 수정 | V-CODE-1 | Fixed |
| I-11 | Minor | 문서 | 02 §9.1 T6 시나리오 설명이 실제로는 순환이 아님 | 서술 오류(Codex가 지적) | 문장 수정 | T6 | Fixed |
| I-12 | Enhancement | 학습 엔진(P2) | 조사 E 권고: 숙달 기준 강화(연속 정답 + 하루 뒤 새 변형), 수준과 증거량 분리 표시, 가지치기한 선수의 "추정" 표시, 역량 차원 순서 가정 재검토 | — | P2 착수 시 04 §3·§4.2 반영 | — | Backlog |
| I-13 | Minor | 학습 앱 | 휴대폰 폭에서 가로 넘침(단계 칩 줄) | grid 트랙 `1fr`이 내용 폭으로 늘어남 | `minmax(0,1fr)`, `min-width:0` | Playwright 390px 확인 | Fixed |
| I-14 | Minor | 저장소 | `~/aixon/ss_copilot.html`(01:32, CloudFront 403 오류 페이지)이 프로젝트 루트에 있음. 조사 에이전트가 남긴 것으로 보임 | 에이전트가 cwd에 다운로드 | 삭제하지 않음 — 사용자 확인 필요 | — | Open |
| I-15 | Major | 개발 환경 | `hub codex` worktree에 `node_modules`·`.venv`가 없음(git 제외), Codex 샌드박스는 네트워크가 없어 설치 불가 | 의존성은 추적되지 않음 | 오케스트레이터가 worktree에 하드링크·심볼릭 링크 제공. 이후 명세에 `scripts/link-deps.sh` 실행 지시 | — | Fixed(절차) |
| I-16 | Minor | 데이터 | 시드 W104(참조되지 않는 엔티티) 경고: `cifar-10`, `benchmark:wmt14-en-de-newstest2014` 등 | 근거 Claim에서 쓰지 않음 | 정보성 경고로 둠 | — | Accepted |
| I-17 | Major | 식별자 검증기 | 줄 단위 파서가 들여쓰기 형식이 바뀌면 논문을 하나도 찾지 못함(0건 → 통과처럼 보일 위험) | 정규식 파서 | YAML 파서로 읽기, 0건이면 결과가 비어 있음을 보고서에 명시 | 수동 실행 결과 54/54 | Fixed |
| I-18 | Major | 재현성 | 프로젝트 `.venv`에 `pypdf`가 없어 인용 대조가 PDF 근거 5건을 `no_pdf_support`로 내고 exit 1(지금까지의 121/121은 anaconda 파이썬으로 실행한 결과) | `requirements-dev.txt`에 pypdf 누락 | `pypdf==6.20.0` 추가, `.venv`에 설치 | 프로젝트 `.venv`로 `quotes --offline` 121/121, exit 0 | Fixed |
| I-19 | Major | 사이트(수식) | Astro 7에서 `markdown.remarkPlugins`가 동작하지 않자 Codex가 remark-math·rehype-katex를 빼고 Wiki 수식을 손으로 쓴 MathML로 바꿈 → R-05(KaTeX 빌드 렌더) 미충족, 문서마다 MathML을 손으로 써야 함 | Astro 7은 remark 파이프라인(`@astrojs/markdown-remark`)을 선택적 peer 의존성으로 분리. 샌드박스에 네트워크가 없어 설치 불가 | `@astrojs/markdown-remark@7.3.1`(게시 2주 이상) 설치 후 플러그인 복원 — 별도 사본 빌드에서 MathML 출력·`katex-error` 0 확인. KaTeX CSS 연결 누락도 함께 수정 | `check_dist.py` V-MATH, E2E-8 | Open(병합 시 수정) |
| I-20 | Minor | 개발 환경 | 하드링크 복사(`cp -al`)한 node_modules에서 `npm install`을 돌리자 `node_modules/.package-lock.json`이 제자리에서 바뀌어 base·Codex worktree의 같은 파일도 바뀜 | 하드링크는 내용을 공유하고, npm이 이 파일을 rename 없이 씀 | 바뀐 파일이 그것 하나뿐임을 `find -newermt`로 확인, 공유된 숨은 잠금 파일 삭제(npm이 디스크에서 다시 만듦), `npm ls` 정상 | 절차: 새 패키지는 base에 먼저 설치하거나 `cp -a` 사본에서 시험 | Fixed |

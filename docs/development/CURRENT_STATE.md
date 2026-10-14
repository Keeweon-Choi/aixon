# CURRENT_STATE — 작업 재개용 상태 (오케스트레이터가 갱신)

> 컴팩션·세션 교체(hub renew) 뒤에는 **이 파일부터 읽는다.** 마지막 갱신: 2026-10-15 02:05

## 0. 반드시 지킬 운영 조건 (사용자 지시)

1. **사용량 85% 규칙** (2026-10-15 01:56, 사용자가 자러 가며 hub-ops 경유로 남긴 지시)
   - Claude 사용량이 5시간 창 또는 주간 창 중 하나라도 **85% 이상**이면: 새 작업·새 서브에이전트를 시작하지 않는다. 지금 하던 단계만 안전한 지점까지 마치고 멈춘다. 어디까지 했고 무엇이 남았는지 이 파일과 `PROGRESS.md`에 정리한다.
   - 확인 시점: **단계를 시작할 때, 서브에이전트를 새로 띄우기 전**.
   - 확인 명령: `node "$(ls -d ~/.claude/plugins/cache/claude-dashboard/claude-dashboard/*/ | sort -V | tail -1)dist/check-usage.js" --json | jq -c '.claude | {five_hour: .fiveHourPercent, seven_day: .sevenDayPercent}'`
   - `/goal`은 사용자만 끌 수 있다. 85%를 넘으면 hub가 `/goal clear`를 넣는다. 그 전에 85%를 보면 목표 확인이 계속하라고 해도 새 일을 벌이지 않는다.
   - 이 조건은 컴팩션·renew 뒤에도 유지한다.
2. **실행 지침**: `docs/AUTONOMOUS_MVP_LOOP.md` (사용자 /goal: 설계 검증 → Critical/Major 수정 → P0 MVP 구현 → 검증 하네스 → 실제 Playwright E2E·회귀 → `MVP_ACCEPTANCE_REPORT.md`). 테스트 실패나 미검증 항목을 PASS로 적지 않는다. 사용자 데이터 파괴, 외부 배포, 자동 push 금지.
3. **커밋 정책**: `~/aixon`은 git 저장소가 아니다. 지침에 "사용자 요청 없이 자동 Commit 금지"가 있으므로 프로젝트 안에서 `git init`이나 커밋을 하지 않는다. Codex 작업은 통합용 저장소 `~/wt/aixon-base`(오케스트레이터가 관리, Codex worktree의 부모)에서 하고, 검증된 결과만 `~/aixon`으로 동기화한다(`rsync`, `.git` 제외).
4. **사용자 결정(10-14, hub 규칙)**: 명세가 확실한 구현은 Codex에 맡긴다(`hub codex <repo> <spec>`). Codex 샌드박스는 네트워크가 막혀 있으므로 의존성은 오케스트레이터가 미리 설치한다.
5. **Local-first 전달 전략(사용자 확정, 01:5x)**: WSL2에서 실행하고 Windows 브라우저로 쓰는 개인용 웹앱. MVP에는 외부 배포·가입·클라우드가 없다. 모바일은 최소 반응형만 지원한다. PWA·Tauri는 MVP 뒤에 검토한다. Export/Import·백업·복원을 둔다. 테스트 하네스는 localhost와 향후 배포 환경 모두에서 재사용할 수 있게 만든다(base URL 설정).

## 1. 현재 단계

- Phase: **설계 마무리(Phase 0) → 곧 Phase A(독립 설계 감사)**
- 완료: 조사 10건(`scratchpad/research/*.md`, 아래 경로), 설계 문서 초안 02·03·04·05·06·DECISIONS, Lab 기준값(`tools/gen_lab_fixtures.py`, `data/seed/lab_fixtures/softmax_temperature.json`), seedtool 1·2차(Codex, 검증 대기)
- 진행 중:
  - 시드 그래프 YAML 작성(15편 논문 원문 인용 검증 완료, 조립 중)
  - Physical AI 로드맵 학습 앱(사용자 요청 01:5x): 명세 작성 중 → Codex → Artifact 게시
- 남은 설계 문서: 00, 01, 07, 08, README, data/seed/README.md, 03 §5.1·04 §7·05 §4.4 조사 반영, ADR 추가(전달 전략, dagre)

## 2. 산출물·자료 위치

| 무엇 | 위치 |
|---|---|
| 조사 결과(임시, 재부팅 시 사라질 수 있음) | `/tmp/claude-1000/-home-choi-aixon/c0c841fd-2c04-4ea2-836b-e10cd7e5fb84/scratchpad/research/` (A·B·C 경쟁, D 데이터 소스, E 학습과학, F1–F3 시드 논문, G 시각화·기술, H 학습 자료, src/ 원문) |
| seedtool Codex 작업 | `~/wt/aixon-tools-1015-013405-aixon` (2차, 검증 대기) |
| 학습 앱 작업 저장소 | `scratchpad/aixon-study/` (roadmap.md, assessments.json, reference_calc.py) |

## 3. 다음 할 일 (순서)

1. seedtool 2차 결과 검증(테스트 재실행, 음성 대조) → `tools/`에 반영
2. 학습 앱 Codex 명세 완성·실행
3. 시드 그래프 YAML + 인용 대조 + 검증기 + E2E fixture(정답 계획은 손으로 독립 작성)
4. 남은 설계 문서 작성 → Phase A 감사(리뷰어 서브에이전트 2개, 사용량 확인 후)
5. `~/wt/aixon-base` 준비(의존성 설치) → Slice 0부터 Codex

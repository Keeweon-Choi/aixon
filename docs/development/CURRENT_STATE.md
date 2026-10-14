# CURRENT_STATE — 작업 재개용 상태 (오케스트레이터가 갱신)

> 컴팩션·세션 교체(hub renew) 뒤에는 **이 파일부터 읽는다.** 마지막 갱신: 2026-10-15 03:45

## 0. 반드시 지킬 운영 조건 (사용자 지시)

1. **사용량 85% 규칙** (2026-10-15 01:56, hub-ops 경유)
   - 5시간 창 또는 주간 창 중 하나라도 **85% 이상**이면 새 작업·새 서브에이전트를 시작하지 않는다. 하던 단계만 안전한 지점까지 마치고, 어디까지 했는지를 이 파일과 `PROGRESS.md`에 적는다.
   - 확인 시점: **단계를 시작할 때, 서브에이전트를 띄우기 전**.
   - 확인 명령: `node "$(ls -d ~/.claude/plugins/cache/claude-dashboard/claude-dashboard/*/ | sort -V | tail -1)dist/check-usage.js" --json | jq -c '.claude | {five_hour: .fiveHourPercent, seven_day: .sevenDayPercent}'`
   - `/goal`은 사용자만 끌 수 있다. 85%를 넘으면 hub가 `/goal clear`를 넣는다. 이 조건은 컴팩션·renew 뒤에도 유지한다.
2. **실행 지침**: `docs/AUTONOMOUS_MVP_LOOP.md` (사용자 /goal). 테스트 실패나 미검증 항목을 PASS로 적지 않는다. 사용자 데이터 파괴, 외부 배포, 자동 push 금지.
3. **범위(사용자 방향 수정, 02:1x, ADR-019)**: **v0.1 = Knowledge Atlas + Interactive AI Wiki.** GitHub Pages 정적 공개는 허용하지만 실제 배포(저장소 생성·push·Pages 활성화)는 사용자 승인 뒤에 한다(ADR-018). 서버·DB·LLM·계정은 P2. **AI 생성 콘텐츠 자동 게시 금지** → public 빌드는 사람이 승인한 콘텐츠만(ADR-017).
4. **커밋 정책**: `~/aixon`은 git 저장소가 아니다. 프로젝트 안에서 `git init`·커밋을 하지 않는다. Codex 작업은 통합용 저장소 `~/wt/aixon-base`(오케스트레이터가 관리, Codex worktree의 부모)에서 하고, 검증된 결과만 `~/aixon`으로 동기화한다:
   `rsync -a --exclude node_modules --exclude .venv --exclude .git --exclude data/cache --exclude __pycache__ --exclude .pytest_cache --exclude dist --exclude dist-public ~/wt/aixon-base/ /home/choi/aixon/`
5. **Codex**: 명세가 확실한 구현은 `hub codex ~/wt/aixon-base <spec>`. 샌드박스에 네트워크가 없고 worktree에는 의존성이 없다(I-15) → 새 worktree마다 `cp -al ~/wt/aixon-base/node_modules <wt>/node_modules; ln -s ~/wt/aixon-base/.venv <wt>/.venv`. 결과는 반드시 직접 다시 돌려 검증한다(음성 대조 포함).
6. 커밋 신원은 전역 git 설정을 그대로 쓴다.

## 1. 현재 단계 (AUTONOMOUS_MVP_LOOP 기준) — 03:45

| Phase | 상태 |
|---|---|
| 조사·설계·시드(Sprint 0) | 완료 |
| A 독립 설계 감사 | 진행 중 — sonnet 서브에이전트, 보고서 `scratchpad/design_audit.md` |
| B Critical/Major 수정 | 감사 결과 대기. 그사이 찾아 고친 것: I-18(pypdf), I-19(KaTeX 복원), Codex 대체 시드 병합 차단 |
| C–G 사이트·하네스·E2E | 첫 Codex 결과는 얇은 뼈대(310줄, 그래프·공개 관문·E2E 없음) → 병합 후 3갈래로 재분배 |
| H 회귀·CI·Clean env | 대기 |
| I 최종 독립 리뷰 | 대기 |

### 진행 중인 작업

| 작업 | 명세 | 위치 | 확인 방법 |
|---|---|---|---|
| A 그래프 화면(Codex) | `specs/codex_site_A_graph.md` | `~/wt/aixon-base-1015-034008-x` (브랜치 `codex/1015-034008-x`), pid 3128250 | `hub codex` (프로젝트 `[?]`라 완료 알림 없음 → 오케스트레이터 백그라운드 감시) |
| B 페이지·Lab·공개 관문(Codex) | `specs/codex_site_B_pages.md` | `~/wt/aixon-base-1015-034016-x` (브랜치 `codex/1015-034016-x`), pid 3128818 | 위와 같음 |
| C 하네스(Claude sonnet 서브에이전트) | `specs/site_C_harness.md` | `~/wt/aixon-harness` (브랜치 `harness/c`) | 완료 알림 |

공통 규칙·파일 소유·선택자 약속: `specs/site_common.md`. Codex 5시간 한도는 04:12에 풀린다(그 전에는 대기).

## 2. 산출물·자료 위치

| 무엇 | 위치 |
|---|---|
| 통합 저장소 | `~/wt/aixon-base` (기준 커밋 + 병합 커밋) |
| 조사 원본 10건 | `docs/research/` (원문 raw는 scratchpad `research/src/`) |
| 인용 원문 캐시 | `~/wt/aixon-base-1015-021626-aixon/data/cache/fulltext` |
| 사이트 Codex worktree | `~/wt/aixon-base-1015-022629-aixon` (진행표 `CODEX_PROGRESS.md`) |
| 대표 Wiki 초안 | `content-staging/scaled-dot-product-attention.mdx` (draft, ai_generated, verify 블록 2개 통과) → 사이트 병합 후 `src/content/wiki/`로 이동, Claim ID를 실제 시드 ID로 맞춤 |
| Physical AI 학습 앱(별도 요청, 완료) | `study/physical-ai/`, 게시 https://claude.ai/artifact/YEf5Rk65MR96u44242qddc (비공개) |
| 명세 | `specs/codex_site_mvp.md` 등 |

## 3. 다음 할 일 (순서)

1. 감사 보고서 수신 → Critical/Major 수정 → `08_ARCHITECTURE_REVIEW.md`
2. A·B·C 완료 → 각 브랜치에서 직접 재실행(음성 대조 포함) → `main`에 병합(A → B → C 순, 충돌은 소유표 기준)
3. `make verify`(fixture E2E + seed E2E 포함) → 실패 수정 → `artifacts/verification/runs/<run-id>/`
4. Clean env 검증(새 clone + `npm ci` + venv) → 최종 독립 리뷰 → `MVP_ACCEPTANCE_REPORT.md`(GitHub Pages 실배포 NOT RUN)
5. `~/aixon`으로 동기화(§0.4 명령)
6. 사용자 확인 대기 항목: `BLOCKERS.md`

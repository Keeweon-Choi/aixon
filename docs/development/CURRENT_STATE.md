# CURRENT_STATE — 작업 재개용 상태 (오케스트레이터가 갱신)

> 컴팩션·세션 교체(hub renew) 뒤에는 **이 파일부터 읽는다.** 마지막 갱신: 2026-10-15 14:3x

## 0. 반드시 지킬 운영 조건 (사용자 지시)

1. **실행 지침**: `docs/AUTONOMOUS_MVP_LOOP.md` (사용자 /goal). 테스트 실패나 미검증 항목을 PASS로 적지 않는다. 사용자 데이터 파괴, 외부 배포, 자동 push 금지.
2. **범위(사용자 방향 수정, 02:1x, ADR-019)**: **v0.1 = Knowledge Atlas + Interactive AI Wiki.** GitHub Pages 정적 공개는 허용하지만 실제 배포(저장소 생성·push·Pages 활성화)는 사용자 승인 뒤에 한다(ADR-018). 서버·DB·LLM·계정은 P2. 공개는 사람 승인(ADR-021) 또는 AI 교차 검증 패널 통과(사용자 결정 10-15, ADR-026, 기준 `docs/verification/CROSS_REVIEW.md`)뿐이다.
3. **저장소(사용자 결정 10-15)**: `~/aixon`이 정본 git 저장소다(개발 이력 포함). 통합용 `~/wt/aixon-base`는 이제 쓰지 않는다(읽기 전용 보관). 배포 승인됨: GitHub 공개 저장소 + Pages. Claude 표시는 상관없음. 라이선스: 텍스트 CC BY 4.0, 코드 MIT.
4. **Codex**: 명세가 확실한 구현은 `cd /home/choi/aixon && hub codex -m sol|terra|luna /home/choi/aixon <spec>`. 샌드박스에 네트워크가 없다. 결과는 반드시 직접 다시 돌려 검증한다(음성 대조 포함).
5. 커밋 신원은 전역 git 설정을 그대로 쓴다.

## 1. 현재 단계 — 2026-10-15 14:3x (v0.1 인수 완료, 배포 완료)

| Phase | 상태 |
|---|---|
| A 설계 감사 → B 수정 | 완료(31건, `docs/08_ARCHITECTURE_REVIEW.md`) |
| C–H 사이트·하네스·E2E·회귀 | 완료. 최신 깨끗한 환경 `make verify` 13단계 PASS (`artifacts/verification/runs/20261015T051054Z`, 커밋 67854ae, 2코어). 이전 `20261015T040334Z`(b6ca3d7)도 PASS. 67854ae 뒤 c6851db까지는 문서·.gitignore·verify-online 워크플로·quotes 종료 코드만 바뀌었고 GitHub CI가 c6851db에서 전체 `make verify`를 통과했다 |
| I 최종 독립 리뷰 | ACCEPT WITH FIXES → 지적 전부 수정·검증 후 병합(Major 2, 부분 충족 2, I-40 간헐 실패) |
| 인수 | 완료: `docs/verification/MVP_ACCEPTANCE_REPORT.md` 판정 PASS. 공개 준비 4개: 실배포 PASS(https://keeweon-choi.github.io/aixon/, 스모크 테스트 PASS), GitHub Actions PASS(CI 38686155036, Pages 38686154994, Verify Online 38686154873), 콘텐츠 승인 0건·게시 0건(사용자가 AI 교차 검증 경로를 택함, ADR-026), 사람이 직접 써 본 확인 NOT RUN. 검색엔진 색인·스크린 리더 확인도 NOT RUN |
| 남은 것 | BLOCKERS는 B-02(콘텐츠 게시 경로, ADR-026 도구 구현 중)만 열려 있다. 나머지는 해결(B-06은 GitHub verify-online). 아래 진행 중 목록 참고 |

진행 중(Codex worktree 검증 대기):

1. AI 교차 검증 도구: 브랜치 `codex/1015-140312-aixon`, 검증 중.
2. 로컬 검수 화면: 브랜치 `codex/1015-140314-aixon`, 검증 중.
3. 그 뒤: 패널 실행 → 자동 게시 → 배포된 사이트 재확인.

게시된 콘텐츠는 아직 0건이다.

모델 배정·하네스·PC 규칙은 `~/.local/share/hub/rules.md`(사용자 결정 10-15). 공개할 수 있는 저장소이므로 커밋에 Claude 표시를 넣지 않는다(B-08).

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
4. Clean env 검증(새 clone + `npm ci` + venv) → 최종 독립 리뷰 → `MVP_ACCEPTANCE_REPORT.md`(GitHub Pages 실배포는 이후 완료, 2026-10-15 14:3x)
5. `~/aixon`으로 동기화(§0.4 명령)
6. 사용자 확인 대기 항목: `BLOCKERS.md`

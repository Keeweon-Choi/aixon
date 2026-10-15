# PROGRESS — 작업 기록 (시간순, 2026-10-15)

| 시각 | 한 일 | 검증 결과 |
|---|---|---|
| 00:3x–01:3x | 조사 10건(경쟁 A·B·C, 데이터 D, 학습과학 E, 시드 논문 F1–F3, 시각화 G, 학습 자료 H) | 출처 URL 기록 |
| 01:1x–01:5x | seedtool 1·2차(Codex) → 오케스트레이터 검증·수정(I-01, I-02, I-09) | `pytest tools` 60 passed(seedtool 58 + 식별자 2), ruff 통과 |
| 01:5x–02:1x | Physical AI 학습 앱(사용자 별도 요청) Codex → 검증 → Artifact 게시 | selftest 10/10, 음성 대조 실패 확인, 390·1280px 넘침 0 |
| 02:0x–02:3x | 시드 그래프 조립, 인용 원문 대조 | 121/121, 변조 인용 음성 대조 not_found |
| 02:1x | 사용자 방향 수정 → v0.1 = Atlas + Wiki (ADR-019) | — |
| 02:2x–02:5x | atlas 분류 Codex → 오케스트레이터 재분류, ID 복구, 지어낸 arXiv 12건 삭제(I-03~I-06) | arXiv 54/54, 병합 G 0 |
| 02:3x–03:0x | Wiki 설계 4종, 대표 SDPA 문서 초안, 07·REQUIREMENT_TRACEABILITY·ISSUE_LOG | `python verify` 2/2 (I-10 발견·수정) |
| 02:26– | 사이트 MVP Codex(1015-022629 → 이어 하기 1015-023556, 한도 대기) | 검증 대기 |
| 03:0x | 01_COMPETITIVE_ANALYSIS, development 문서, E2E-10(ViT 여정) 추가 | — |
| 03:0x– | 독립 설계 감사(서브에이전트) | 대기 |
| 03:1x | pypdf 누락 발견(I-18) → 프로젝트 venv로 인용 121/121 재확인 | exit 0 |
| 03:1x–03:2x | Codex 사이트 결과 검토: 그래프 화면 없음, 공개 관문 미구현, 수식 손작성 MathML(I-19), 시드 파일을 지어낸 fixture로 덮어씀 → 작업 중지·보존 커밋, 뼈대만 병합(시드는 base 유지) | 병합 후 G 0, approve 0건 |
| 03:2x | KaTeX 복원(`@astrojs/markdown-remark` 7.3.1, katex 0.16.47 정렬), 대표 SDPA Wiki 투입, `<Lab id>` 래퍼, prettier | 실제 데이터 638쪽 빌드, katex-error 0, lint·typecheck 0 오류 |
| 03:40 | 남은 사이트 작업을 A(그래프, Codex)·B(페이지·Lab·공개 관문, Codex)·C(하네스, sonnet 서브에이전트)로 재분배, 공통 규칙·선택자 약속 | 진행 중 |
| 03:5x | 시드 요약 70개 교체·문제 이름 한국어화(I-21), golden 테스트 해시 무시(I-22) | G 0, 인용 121/121, `pytest tools` 60, 음성 대조 실패 확인 |
| 04:27–10:37 | Windows Update가 WSL을 종료(작업 중단, `/tmp` scratchpad 소실 — 감사 보고서 원본 포함) | hub가 Codex 작업 재개 |
| 10:5x–11:2x | 감사 반영 마무리(대표 Wiki 검증 블록), A·B·C 병합, 공개 관문을 Makefile·check_dist에 연결(오염 검사 음성 대조 확인) | 단위 20, 빌드 632쪽 |
| 11:2x–11:5x | 모델 배정 규칙(사용자 10-15) 적용: H1·F13(Codex Terra), E2E 통합·문서(Sonnet), 검증(Opus 5.5 High) | F13 MERGE, H1·E2E FIX FIRST → 수정 후 병합 |
| 11:57–12:02 | 깨끗한 환경 검증(새 clone + `npm ci` + 새 venv + `make verify`) 2회: 1회차 12단계 PASS 뒤 증거 복사에서 중단(I-36) → 수정 → 2회차 PASS | `artifacts/verification/runs/20261015T030106Z` |

## 마지막 테스트 결과 (12:02, 커밋 85c3c39, 깨끗한 환경)

- `make verify` 12단계 PASS: lint, typecheck, test(vitest 21 · pytest 200), validate, validate-fixtures, build(632쪽), check-dist, build-public(7쪽, 승인 0건), check-dist-public, e2e(fixture 108/108), e2e-seed(42 통과 + 4 fixme: P2), secrets
- 증거: `artifacts/verification/runs/20261015T030106Z/summary.json` (git dirty=false)

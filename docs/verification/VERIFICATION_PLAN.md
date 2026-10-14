# VERIFICATION_PLAN — v0.1 검증 계획

> 규칙(V-*)과 E2E 시나리오(E2E-1~10)의 정의는 [CONTENT_VALIDATION_PLAN.md](../CONTENT_VALIDATION_PLAN.md)에 있다. 이 문서는 **무엇을 어떤 순서로, 어디서, 어떤 기준으로 판정하는지**만 정한다. 요구사항 연결은 [REQUIREMENT_TRACEABILITY.md](REQUIREMENT_TRACEABILITY.md), 실행 결과는 [TEST_MATRIX.md](TEST_MATRIX.md).

## 1. 계층과 실행 순서 (`make verify`)

| 순서 | 계층 | 명령 | 막는 것 |
|---|---|---|---|
| 1 | 정적 분석 | `make lint` (prettier, eslint, astro check, ruff) | 문법·형식 오류 |
| 2 | 타입 | `make typecheck` (astro check, tsc) | 타입 불일치 |
| 3 | 단위 | `make test` (vitest: 로더·공개 필터·Lab L1–L7·검색, pytest: `tools` 60개(seedtool 58 + 식별자 2)·검증기) | 계산·규칙 회귀 |
| 4 | 데이터·콘텐츠 | `make validate` (seedtool G·W, validate_content V-*) | 그래프 불변식, Wiki 계약, 계산 블록 |
| 5 | 빌드 | `make build`, `make build-public` | MDX·KaTeX·컴포넌트 참조 오류(빌드 실패) |
| 6 | 산출물 | `make check-dist`, `make check-dist-public` | 깨진 링크, SEO 기본, 공개 관문 |
| 7 | 브라우저 | `make e2e` (fixture), `make e2e-seed` (실제 데이터) | 사용자 여정, 반응형, base 경로 |
| 8 | 보안 | `make secrets` | 키·비밀 유출 |
| 수동 | 외부 대조 | `seedtool quotes`, `verify_identifiers.py` | 인용 원문, arXiv ID (네트워크 필요) |

모든 단계를 실패해도 끝까지 돌리고(요약에 전부 남기기 위해), 하나라도 실패하면 exit 1이다. 증거는 `artifacts/verification/runs/<UTC 시각>/`(`summary.json`, 단계별 로그, `graph-validation.json`, Playwright 결과·실패 스크린샷·trace).

## 2. 환경

| 환경 | 용도 | 상태 |
|---|---|---|
| 로컬 WSL2 (Node 22, Python 3.12 venv, Chromium 1248) | 개발·전체 검증 | 사용 중 |
| Clean env (새 clone, `npm ci`, 새 venv) | 재현성 | 인수 전에 1회 |
| GitHub Actions `ci.yml` | push·PR마다 `make verify` | 설정만(저장소 없음, NOT RUN) |
| GitHub Pages | 실제 공개 URL | 사용자 승인 뒤(NOT RUN). 대신 `/aixon/` base 경로를 재현한 로컬 preview로 E2E-6 |

## 3. 판정 기준

- 상태는 PASS / FAIL / BLOCKED / NOT RUN / NOT APPLICABLE 다섯 가지만 쓴다. 돌리지 않은 것은 NOT RUN이다.
- **음성 대조**: 새 검사기는 일부러 틀린 입력에서 실패하는지 확인한 뒤에만 PASS로 인정한다(예: 인용 변조 → not_found, `wiki_bad/*` → 규칙 코드별 exit 1, 수치 fixture 변조 → E2E-2 실패).
- Codex·서브에이전트가 보고한 결과는 오케스트레이터가 다시 실행해 확인한 것만 기록한다.
- P2 범위(숙련도 저장·재계산 등)는 NOT APPLICABLE로 적고 근거(ADR-019)를 단다.

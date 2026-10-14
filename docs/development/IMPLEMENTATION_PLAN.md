# IMPLEMENTATION_PLAN — v0.1 구현 순서

> 범위: [07_MVP_ROADMAP.md](../07_MVP_ROADMAP.md) R-01~R-16. 구현 명세: [specs/codex_site_mvp.md](../../specs/codex_site_mvp.md). 검증: [CONTENT_VALIDATION_PLAN.md](../CONTENT_VALIDATION_PLAN.md). 마지막 갱신: 2026-10-15 03:10

## 원칙

- 하네스 먼저(지침 Phase C): 검증기·fixture·E2E 골격이 기능보다 앞선다.
- 서버·DB·LLM 없음(ADR-015). 빌드 산출물은 정적 파일뿐이다.
- 데이터가 진실 공급원이다: 화면은 `data/**/*.yaml`과 `src/content/wiki/*.mdx`에서만 만든다. 화면에서 사실을 지어내지 않는다.
- 미승인 콘텐츠는 public 빌드에 없다(ADR-017).

## Slice

| Slice | 내용 | 요구사항 | 완료 조건 | 담당 | 상태 |
|---|---|---|---|---|---|
| S0 | 시드·지도 데이터, seedtool, 식별자 검증, Lab fixture | R-01, R-09 | seedtool 60 통과, G 0, 인용 121/121, arXiv 54/54 | 오케스트레이터 + Codex | 완료 |
| S1 | Astro 기반, 그래프 로더, URL helper, vitest | R-01, R-06 | `make lint typecheck test` | Codex | 진행 중 |
| S2 | Wiki collection 스키마, 컴포넌트, 대표 문서 | R-03, R-04, R-05 | V-SCHEMA·V-CODE·V-MATH | Codex + 오케스트레이터(문서) | 진행 중 |
| S3 | Entity·Field·Claim·Coverage·About·404 | R-01, R-08, R-14 | V-LINK, V-CITE, V-STATUS | Codex | 진행 중 |
| S4 | Atlas·Trace·Lab island, 노드 검색, Pagefind | R-02, R-07, R-12, R-13 | vitest L1–L7, V-SEARCH | Codex | 진행 중 |
| S5 | 검증기(validate_content, check_dist, scan_secrets), fixture, Playwright E2E-1~9 | R-11, R-16 | `make verify` 녹색 | Codex → 오케스트레이터 재실행 | 진행 중 |
| S6 | public 빌드, `pages.yml`, 실제 시드 E2E(E2E-1·2·6·7·10) | R-10, R-15 | E2E-9, `make e2e-seed` | 오케스트레이터 | 대기 |
| S7 | Clean env, 최종 리뷰, 인수 보고서 | 전체 | `MVP_ACCEPTANCE_REPORT.md` | 오케스트레이터 + 리뷰 서브에이전트 | 대기 |

## 재현

```bash
cd ~/wt/aixon-base          # 또는 동기화된 ~/aixon
npm ci && python -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
npx playwright install chromium   # 이미 설치되어 있으면 생략
make verify                 # lint → typecheck → test → validate → build → check-dist → e2e
```

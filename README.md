# AIXON

AIXON v0.1은 AI 연구 지식을 근거와 함께 탐색하는 **Knowledge Atlas**와, 같은 그래프에 연결된 **Interactive AI Wiki**입니다.
서버·DB·LLM 없이 Astro 7로 만드는 정적 사이트이고, GitHub Pages에 올릴 수 있습니다.

- **Atlas**: 연구 분야와 개념을 계층으로 탐색하고, 논문·모델 사이의 관계(`INTRODUCES`, `ADAPTS`, `PREREQUISITE_OF` …)를 Claim과 근거(인용문·위치·원문 링크)로 확인합니다.
- **Wiki**: 수식(KaTeX), 실행 검증된 코드, 직접 만든 그림, 계산 가능한 Lab(softmax temperature, scaled dot-product)이 들어 있는 개념 설명입니다.
- **원칙**: 화면의 사실은 모두 `data/**/*.yaml`(그래프)과 `src/content/wiki/*.mdx`(Wiki)에서만 나옵니다. AI가 쓴 내용은 사람이 승인하기 전에는 공개되지 않습니다.

## 빠른 시작

필요한 것: Node 22, [uv](https://docs.astral.sh/uv/)(Python 3.12를 uv가 받는다), GNU make.

```bash
uv venv --python 3.12 .venv && uv pip install -r requirements-dev.txt   # Python 의존성(requirements-dev.in을 uv pip compile로 고정)
make install                 # npm ci + Python 의존성 확인
make build                   # 미리보기 빌드(dist/) + Pagefind 색인
npx astro preview            # http://localhost:4321/
make verify                  # 전체 검증 (아래 "검증" 참고)
```

Astro 명령은 쓰기 가능한 설정 폴더가 필요합니다: `XDG_CONFIG_HOME=/tmp/aixon-astro-config ASTRO_TELEMETRY_DISABLED=1`을 앞에 붙이세요(`make`는 알아서 붙입니다).

## 환경 변수

| 변수              | 기본값                                                    | 뜻                                                  |
| ----------------- | --------------------------------------------------------- | --------------------------------------------------- |
| `AIXON_BASE`      | `/`                                                       | 배포 경로(GitHub Pages는 `/<저장소 이름>/`)         |
| `AIXON_SITE`      | `http://localhost:4321`                                   | 사이트 주소(canonical, sitemap, robots.txt)         |
| `AIXON_BUILD`     | `preview`                                                 | `preview` 또는 `public` (아래 "빌드 모드")          |
| `AIXON_GRAPH`     | `data/seed/seed_graph.yaml,data/graph/atlas.yaml`         | 쉼표로 구분한 그래프 YAML. 없는 파일은 경고 후 건너뜀 |
| `AIXON_WIKI_DIR`  | `src/content/wiki`                                        | Wiki MDX 폴더                                       |
| `AIXON_E2E_TARGET` | `fixture`                                                | Playwright 대상: `fixture`(테스트용 가짜 데이터) 또는 `seed`(실제 시드) |

## 빌드 모드와 공개 규칙

|                  | `preview` (기본)                                   | `public`                                                              |
| ---------------- | -------------------------------------------------- | --------------------------------------------------------------------- |
| 용도             | 개발·검토. 모든 초안과 상태 배지를 보여 줌         | GitHub Pages 공개본                                                   |
| Claim            | 기각·폐기를 뺀 모두(상태 배지 포함), 기각은 자기 페이지에만 | `review.decision: approve`이고 `review.by`가 `human:`인 Claim만 |
| Wiki             | 모든 상태                                          | `status: published` + 사람 `review`가 있는 문서만                     |
| AI 요약          | 그대로 표시                                        | 사람이 `summary_review`로 승인하지 않으면 "준비 중"                   |
| `robots.txt`     | `Disallow: /`                                      | 색인 허용 + `sitemap-index.xml`                                       |

**AI가 쓴 내용은 자동으로 공개되지 않습니다.** agent의 "승인"은 승인이 아닙니다. `make check-dist-public`과 Playwright E2E-9가 이 규칙을 빌드 결과에서 다시 확인합니다.

## 콘텐츠 작업 흐름

1. **draft**: 문서를 쓰고(`status: draft`, AI가 썼다면 `ai_generated: true`) `make validate`로 검사합니다. 수식·역사·원리 섹션에는 `<Cite>`가, 실행 가능한 코드에는 ` ```python verify ` 블록과 `assert`가 필요합니다.
2. **사람 검토·일괄 승인**: `review/<name>.yaml`에 그래프 ID와 `wiki:<slug>`의 `recommendation`·`decision`을 적습니다. 사람이 근거와 숫자를 확인한 뒤 `tools/review.py approve-batch review/<name>.yaml --by human:<id>`를 실행합니다. 도구는 승인할 항목과 건너뛸 항목을 먼저 보여 주고 `승인할까요? [y/N]`를 묻습니다(`--yes`는 그 확인을 생략). 각 승인은 현재 콘텐츠 해시에 묶여 이후 수정하면 다시 승인해야 합니다.
3. **published**: Wiki 항목에 `publish: true`를 넣으면 일괄 승인 직후 `status: published`와 `published_at`이 기록됩니다. 이미 신선하게 승인된 문서 하나는 `tools/review.py publish wiki:<slug> --by human:<id>`로 게시할 수 있습니다. 이 단계부터 `public` 빌드에 나타납니다.

문서 형식은 [docs/CONTENT_SCHEMA.md](docs/CONTENT_SCHEMA.md), 검사 규칙(V-\*)은 [docs/CONTENT_VALIDATION_PLAN.md](docs/CONTENT_VALIDATION_PLAN.md)에 있습니다.

## 검수 화면

지속적인 사람 검수에는 `make review`를 실행합니다. 시작할 때 출력되는 `http://127.0.0.1:4400/?token=...` 주소만 브라우저에서 여세요. 서버는 localhost에만 바인딩하고 매번 새 토큰을 만듭니다. 화면에서 대기열·근거·사전 검수·AI 교차 검증 보고서를 읽고 결정을 모은 뒤 **결정 기록**을 누르면 `review/decisions/`에 기록하고 승인만 현재 콘텐츠 해시에 묶습니다. Wiki는 **승인 후 게시**를 함께 선택할 수 있습니다.

검토자 ID는 `human:<id>` 형식이어야 하며 `AIXON_REVIEWER=human:<id> make review`로 기본값을 바꿀 수 있습니다. 에이전트 세션에서 실행한 서버는 실수 방지를 위해 승인 기록과 커밋·배포를 거부합니다. 검토는 사람의 브라우저 세션에서 다시 시작하세요. 이 도구와 `tools/review_app/`은 공개 Astro 사이트나 GitHub Pages에 포함되지 않습니다.

## 검증

`make verify`는 아래 단계를 순서대로 모두 실행하고(하나가 실패해도 계속), 하나라도 실패하면 0이 아닌 코드로 끝납니다.

| 단계                | 하는 일                                                                                       |
| ------------------- | --------------------------------------------------------------------------------------------- |
| `lint`              | prettier, eslint, `astro check`, ruff                                                         |
| `typecheck`         | `astro check`, `tsc --noEmit`                                                                 |
| `test`              | vitest, pytest(`tools/`, `tests/python/`)                                                     |
| `validate`          | 그래프 불변식(`seedtool validate`), Wiki 규칙(`tools/validate_content.py`)                    |
| `build`             | 미리보기 빌드 + Pagefind                                                                      |
| `check-dist`        | `tools/check_dist.py dist`: 링크(base 포함), SEO, KaTeX/MathML, CDN 없음, sitemap, robots.txt |
| `build-public`      | 공개 빌드(`dist-public/`)                                                                     |
| `check-dist-public` | 위 검사 + 미승인 Claim·Wiki·AI 요약이 없는지                                                  |
| `e2e`               | Playwright, 테스트용 fixture 데이터(`dist-e2e/`, `dist-public-e2e/`), desktop + mobile        |
| `e2e-seed`          | Playwright, 실제 시드(`dist-seed/`), `@seed` 태그 시나리오(E2E-1·2·6·7·10)                    |
| `check-dist-seed`   | `tools/check_dist.py dist-seed --base /aixon/`: 시드 빌드의 링크·SEO 검사                   |
| `secrets`           | `tools/scan_secrets.py`: 추적 파일과 빌드 산출물의 키·비밀 검색                               |

개별 실행: `make lint test validate validate-fixtures build check-dist e2e e2e-seed secrets`, 정리: `make clean`(빌드 산출물만 지움), 서식: `make format`.

### 검증 실행 결과 읽기

`make verify`는 `artifacts/verification/runs/<UTC 시각>/`를 만듭니다(git에는 올리지 않음).

```text
summary.json            실행 id, 시작·끝, git commit과 dirty 여부, node/python/playwright 버전, OS,
                        단계별 {name, command, exit_code, status PASS|FAIL, duration_s, log}
logs/NN-<단계>.log      단계별 전체 출력 — 실패 원인은 여기서 시작
graph-validation.json   seedtool validate --json 결과(시드+atlas, fixture)
test-results/           Playwright JSON 보고서와 실패한 테스트의 출력
screenshots/            실패한 테스트의 스크린샷
playwright-traces/      실패한 테스트의 trace: npx playwright show-trace <파일>
```

환경 변수와 토큰은 기록하지 않습니다. 사람이 보기 좋은 보고서는 `npx playwright show-report playwright-report/fixture`(또는 `seed`)입니다.

### 테스트 데이터

- `tests/fixtures/`는 **가짜 데이터**입니다(`# TEST FIXTURE — not real research data`). 실제 빌드에서는 쓰이지 않고, 환경 변수로만 E2E 빌드에 연결됩니다.
- `tests/fixtures/wiki_bad/`에는 규칙마다 하나씩 일부러 틀린 문서가 있고, `tests/python/`이 "그 규칙만 걸리는지"를 확인합니다.
- E2E는 화면과 데이터를 대조합니다. 기대값은 앱 코드를 가져오지 않고 YAML·JSON을 직접 읽어 계산합니다(Lab 숫자는 `data/seed/lab_fixtures/softmax_temperature.json`).
- 로컬 `astro preview`는 `/aixon/` 아래에서 서비스해 GitHub Pages의 base 경로를 그대로 재현합니다.

## 문서와 명세

| 위치                      | 내용                                                         |
| ------------------------- | ------------------------------------------------------------ |
| `docs/`                   | 제품·데이터·UX 설계, ADR(`DECISIONS.md`), 검증 계획          |
| `docs/verification/`      | 요구사항 추적표, 이슈 로그                                   |
| `docs/development/`       | 현재 상태, 진행 기록, 구현 순서                              |
| `specs/`                  | 구현 명세와 공통 규칙(셀렉터 계약 포함)                      |
| `data/seed/`, `data/graph/` | 검증된 시드 그래프와 분야 지도                             |
| `tools/`                  | `seedtool.py`(그래프 검증·계획기), 검증기·실행기             |

## 배포

`.github/workflows/ci.yml`은 모든 push와 pull request에서 `make verify`를 돌리고 검증 결과와 Playwright 보고서를 올립니다.
`.github/workflows/pages.yml`은 공개 빌드를 만들어 `make check-dist-public`을 통과한 뒤에만 GitHub Pages에 배포하며, 수동 실행 또는 `main` push로만 시작합니다.
실제 배포(저장소 생성·push·Pages 활성화)는 사용자 승인 뒤에 합니다.

## 공개 배포 전 체크

GitHub 저장소의 **Settings → Environments → github-pages**에서 required reviewers를 지정합니다. 공개 대상의 사람 승인은 `tools/review.py`로 기록하고, 승인 뒤 내용을 고치면 다시 승인한 뒤 `make check-dist-public`을 실행합니다.

## 라이선스

글·데이터 설명 문장·직접 만든 그림은 CC BY 4.0, 코드는 MIT다. 자세한 범위는 [LICENSE-CONTENT.md](LICENSE-CONTENT.md)와 [LICENSE](LICENSE).

## AI 교차 검증

사람 승인 외에도 독립된 AI 검증자 두 명이 원문 우선·서술 우선으로 각각 검토하고,
인용 구절의 웹 원문 대조와 제3 검증자의 표본 감사를 통과한 콘텐츠를 공개할 수 있습니다.
검증 묶음은 `.venv/bin/python tools/cross_review.py packet <release>`로 만들고, 보고서를 받은 뒤
`confirm`, `check`, `sample`, `approve` 순서로 실행합니다. `approve`는 통과한 레코드에
내용 해시가 묶인 패널 승인을 기록합니다. 공개 관문은 빌드마다 보고서와 감사를 다시 검사합니다.
전체 판정 기준과 보고서 형식은 [AI 교차 검증 기준](docs/verification/CROSS_REVIEW.md)에 있습니다.

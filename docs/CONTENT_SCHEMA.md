# CONTENT_SCHEMA — Wiki 문서와 Graph 확장 스키마 (v0.1)

> Wiki MDX frontmatter, 문서 안 컴포넌트, Graph YAML 확장 필드의 계약. 빌드(Astro Content Collections의 zod 스키마)와 `tools/validate_content.py`가 이 문서를 그대로 구현한다. 아키텍처는 [WIKI_CONTENT_ARCHITECTURE.md](WIKI_CONTENT_ARCHITECTURE.md), Graph 기본 스키마는 [03_DATA_MODEL.md §2](03_DATA_MODEL.md).

## 1. Wiki 문서 위치와 ID

- 파일: `src/content/wiki/<slug>.mdx`. `<slug>`는 연결된 entity의 slug와 같다(`method:scaled-dot-product-attention` → `scaled-dot-product-attention.mdx`).
- 문서 ID: `wiki:<slug>`(frontmatter `id`). URL: `<base>/wiki/<slug>/`.

## 2. Frontmatter

```yaml
id: wiki:scaled-dot-product-attention           # 필수, ^wiki:[a-z0-9]+(-[a-z0-9]+)*$ , 파일명과 일치
entity: method:scaled-dot-product-attention     # 필수, Graph에 있는 KU·Field·Problem·Paper ID
title: "Scaled Dot-Product Attention"           # 필수, 표시 제목
subtitle: "query·key·value로 정보를 섞는 Transformer의 핵심 연산"   # 필수, 1문장(검색 결과·meta description)
status: draft                                   # 필수: outline | draft | reviewed | published
levels: [intuition, fundamentals, deep]         # 필수, 문서에 있는 단계(부분집합, 순서 고정)
sections: [overview, why, mechanism, math, example, code, visual, limitations, history, related, references]
                                                # 필수, 문서에 있는 섹션 id(아래 표의 부분집합)
authors:                                        # 필수, 1명 이상
  - {id: "agent:claude-opus-5-5", role: draft}  # id: agent:<model> 또는 human:<handle>; role: draft | edit | review
ai_generated: true                              # 필수. agent 저자가 한 명이라도 있으면 true
review: null                                    # reviewed·published에서 필수: {by: "human:<handle>", at: YYYY-MM-DD, decision: approve, note}
published_at: null                              # published에서 필수(YYYY-MM-DD)
sources: [src:arxiv:1706.03762v7, src:arxiv:2010.11929v2]   # 문서가 인용하는 Source ID(Graph에 있어야 함)
claims: [clm:intro-sdpa, clm:prereq-variance-of-sum-scaled-dot-product-attention-derive]
                                                # 문서가 근거로 쓰는 Claim ID(Graph에 있어야 함)
labs: [lab:softmax-temperature]                 # 문서에 들어 있는 Lab ID(Graph에 있어야 함)
figures:                                        # 문서 안 그림
  - {id: fig-sdpa-flow, origin: self-made, alt: "Q·Kᵀ → ÷√d_k → softmax → ×V 흐름도"}
updated_at: 2026-10-15                          # 필수
```

### 2.1 섹션 id (요구사항의 설명 구조)

| id | 제목 | 기본 단계 | 비고 |
|---|---|---|---|
| `overview` | 개요와 직관 (Overview & Intuition) | intuition | 거의 모든 문서 |
| `why` | 왜 중요한가 (Why It Matters) | intuition | |
| `mechanism` | 핵심 작동 원리 (Core Mechanism) | fundamentals | |
| `math` | 수학적 기초 (Mathematical Foundations) | fundamentals / deep | |
| `example` | 단계별 예제 (Step-by-step Examples) | fundamentals | 숫자는 `python verify`로 확인 |
| `code` | 구현 (Implementation / Code) | fundamentals | 실행 가능 코드는 `python verify` |
| `visual` | 시각적 설명 (Visual Explanations) | intuition | 직접 만든 SVG, Lab |
| `limitations` | 한계와 트레이드오프 (Limitations & Trade-offs) | deep | |
| `history` | 역사적 발전 (Historical Development) | deep | 연구 Claim 인용 |
| `related` | 관련 개념·논문 (Related Concepts / Papers) | — | **빌드가 Graph에서 생성**(문서에 적지 않아도 됨) |
| `references` | 참고문헌과 근거 (References & Evidence) | — | **빌드가 `sources`·`claims`·`<Cite>`에서 생성** |

문서는 개념의 성격에 맞는 섹션만 고른다(예: 역사적 인물·데이터셋 문서에 `code`가 없어도 된다). 섹션은 MDX 본문에서 `<Section id="math" level="fundamentals" title="수학적 기초">…</Section>`로 감싼다. frontmatter `sections`와 본문의 `<Section>` 집합은 같아야 한다(V-SCHEMA-3).

### 2.2 상태 전이 규칙 (검증기가 강제)

| 상태 | 조건 |
|---|---|
| `outline` | `<Section>` 제목과 요점 목록만 있어도 된다. `sources`가 비어도 된다 |
| `draft` | 본문이 있다. 수식·수치·역사 주장이 있는 섹션에는 `<Cite>`가 하나 이상 있다(V-CITE-2). 모든 `python verify` 블록이 통과한다 |
| `reviewed` | draft 조건 + `review.by`가 `human:`으로 시작 + `review.decision: approve` |
| `published` | reviewed 조건 + `published_at` |
| 공통 | `ai_generated: true`이면 `reviewed`·`published`에 사람 `review`가 반드시 있다. 문서가 인용한 Claim 가운데 `rejected`·`deprecated`가 있으면 오류, `proposed`·`disputed`면 경고 |

## 3. MDX 컴포넌트 (`src/components/wiki/`)

| 컴포넌트 | 쓰임 | props | 빌드 검증 |
|---|---|---|---|
| `<Section>` | 섹션 경계 | `id`(2.1 표), `level`(intuition·fundamentals·deep), `title` | id·level 유효 |
| `<Level>` | 섹션 안에서 단계별로 다른 설명 | `of`(intuition·fundamentals·deep) | 값 유효 |
| `<ConceptLink>` | 다른 개념으로 가는 링크 | `id`(entity ID), children(표시 텍스트) | `id`가 Graph에 있어야 함(V-LINK-1). Wiki가 있으면 Wiki로, 없으면 Entity 페이지로 |
| `<Cite>` | 출처 인용(위첨자 번호) | `src`(Source ID) 또는 `claim`(Claim ID), `loc`(예: "§3.2.1, 각주 4") | 대상 존재(V-CITE-1), frontmatter `sources`/`claims`에 포함(V-CITE-3) |
| `<Callout>` | 주의·정리 상자 | `kind`(note·warning·key) | — |
| `<Figure>` | 직접 만든 그림 | `id`(frontmatter `figures`에 있어야 함), children(인라인 SVG) | `origin: self-made`, `alt` 필수 |
| `<SoftmaxTemperatureLab>` | Lab island | `client:visible` | `labs`에 `lab:softmax-temperature` |

수식: `$…$`, `$$…$$`(remark-math → rehype-katex, 빌드 시 렌더링). 코드: 마크다운 코드 블록(Shiki). **검증 코드 블록**: 언어 뒤에 `verify`를 붙인다(```` ```python verify ````). 블록은 독립 실행할 수 있어야 하고(`numpy`만 허용), 문서의 숫자를 `assert`로 확인해야 한다. `tools/validate_content.py`가 추출해 실행한다(V-CODE-1).

## 4. Graph YAML 확장 (schema_version 1 유지, 선택 필드 추가)

| 필드 | 위치 | 의미 |
|---|---|---|
| `summary_review` | 모든 엔티티(선택) | `{by: human:*, at, decision: approve}`. AI 요약(`summary_by: agent:*`)이 public 빌드에 나오려면 필요 |
| `review` | Claim(기존) | public 빌드에 나오려면 `decision: approve` |
| `metadata_checked.arxiv` | Paper(기존) | `tools/verify_identifiers.py --write-checked`가 arXiv 제목 대조 성공 시 기록. 비어 있으면 "식별자 미검증" 배지 |

## 5. 빌드 산출 JSON

`dist/graph.json` (Atlas·Trace island 입력, 빌드 모드에 따라 걸러짐):
```json
{"graph_version": "…", "build": "preview|public",
 "nodes": [{"id": "model:vit", "type": "Model", "name": "ViT", "fields": ["field:vision-transformers"],
            "year": 2020, "wiki": {"status": "missing|outline|draft|reviewed|published", "url": "…"},
            "summary": "…", "summary_ai": true, "url": "…/e/model/vit/"}],
 "edges": [{"id": "clm:vit-adapts-transformer", "kind": "claim", "predicate": "ADAPTS", "source": "model:vit",
            "target": "model:transformer", "status": "verified", "reviewed": false, "url": "…/claims/vit-adapts-transformer/"},
           {"id": "parent:field:computer-vision>field:artificial-intelligence", "kind": "taxonomy",
            "source": "field:computer-vision", "target": "field:artificial-intelligence"},
           {"id": "member:model:vit>field:vision-transformers", "kind": "membership", "source": "model:vit", "target": "field:vision-transformers"}]}
```
`dist/node-index.json` (빠른 검색): `[{"id", "type", "name", "aliases", "url"}]`.

## 6. URL 규칙

| 대상 | URL | 예 |
|---|---|---|
| 분야 | `/fields/<slug>/` | `/fields/computer-vision/` |
| 엔티티 | `/e/<type-prefix>/<slug>/` | `/e/model/vit/`, `/e/concept/softmax/`, `/e/paper/dosovitskiy2020-vit/` |
| Wiki | `/wiki/<slug>/` | `/wiki/scaled-dot-product-attention/` |
| Claim | `/claims/<slug>/` (`clm:` 뺀 나머지) | `/claims/vit-adapts-transformer/` |
| 기타 | `/atlas/`, `/trace/`, `/coverage/`, `/search/`, `/about/` | |

모든 URL은 슬래시로 끝나고 디렉터리 `index.html`로 생성된다(GitHub Pages에서 직접 링크·새로고침 가능). 앞에 `AIXON_BASE`가 붙는다.

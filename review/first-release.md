# 첫 공개(first-release) 검토 시트

Scaled Dot-Product Attention 문서와, 그 문서가 기대는 claim·엔티티·분야·Lab 문항 44건을 미리 검토했다. 승인은 하지 않았다. 판단 근거는 각 항목의 `notes`에 적었다.

확인한 것:

- 인용 16건은 `seedtool quotes --offline`에서 모두 found로 나왔다. 그다음 원문(arXiv HTML 캐시)을 열어 술어별 판별 질문(02 §8), 방향, 조건을 직접 봤다.
- 논문 3편은 arXiv API와 OpenAlex에서 온라인으로 대조했다(2026-10-15). dblp는 봇 차단 때문에 확인하지 못했다.
- 문서의 `python verify` 블록 3개를 돌렸고 모두 통과했다. 손계산 예제, Lab fixture, 문항 정답은 다시 계산했다.
- `seedtool validate`에서 G 오류는 0건이다.

## 쓰는 법

1. `review/first-release.yaml`을 읽는다. 동의하지 않는 항목은 `decision`을 고친다(`approve` / `fix` / `exclude`). `approve`인 항목만 승인된다.
2. `fix` 항목은 아래 변경을 **먼저** 파일에 반영한다. 반영한 뒤 그 항목의 `decision`을 `approve`로 바꾼다. 승인은 내용 해시에 묶이므로, 승인한 뒤에 고치면 승인이 무효(stale)가 된다.
3. Claude Code 안이 아니라 일반 터미널에서 실행한다.

   ```bash
   cd ~/aixon && .venv/bin/python tools/review.py approve-batch review/first-release.yaml --by human:keeweon
   ```

**주의 1.** 지금 `tools/review.py`에는 `approve-batch`가 아직 없다. 명세(`specs/codex_review_batch.md`)만 있다. 이 명령이 구현된 뒤에 실행한다.

**주의 2.** 공개 관문(ADR-021)상, 문서는 인용한 claim 12건이 모두 공개될 때만 나간다. claim은 양 끝 엔티티가 공개돼야 나간다. 그래서 `method:shifted-window-attention`을 고치지 않고 실행하면 `clm:intro-shifted-window`가 빠지고, 그 결과 문서도 공개되지 않는다. 한 번에 내보내려면 fix 3건을 반영한 뒤 실행한다.

## 요약

| 권고 | 건수 | 내역 |
|---|---|---|
| approve | 41 | claim 12, 엔티티 14, 분야 10, Lab 1, 문항 4 |
| fix | 3 | wiki 1, 엔티티 1(`method:shifted-window-attention`), 분야 1(`field:language-modeling`) |
| exclude | 0 | |

(요청서에는 45건으로 적혀 있지만, 목록을 세면 Lab까지 포함해 44건이다.)

## fix 항목과 바꿀 내용

### 1. `wiki:scaled-dot-product-attention` (`src/content/wiki/scaled-dot-product-attention.mdx`)

필수 3곳:

- **L104**: 기초 단계 요약에서 독립 가정이 빠졌다. 또 논문이 "추정한다(We suspect)"고 쓴 내용을 사실처럼 단정한다.
  - 현재: `query와 key의 성분이 평균 0, 분산 1이라고 가정하면 dot product의 분산은 $d_k$입니다. $d_k$가 크면 점수가 커지고, softmax가 한 key에 쏠려 기울기가 아주 작아집니다.`
  - 변경: `query와 key의 성분이 서로 독립이고 평균 0, 분산 1이라고 가정하면 dot product의 분산은 $d_k$입니다. 논문은 $d_k$가 크면 점수의 크기가 커져 softmax가 한 key에 쏠리고 기울기가 아주 작은 영역으로 밀려난다고 추정합니다(We suspect).`
- **L118, L219**: 실제 값은 0.9548이다(fixture, Lab 표시값 모두). 소수 둘째 자리로 반올림하면 0.95인데 문서에는 0.96으로 적혀 있다.
  - L118: `약 0.96으로 거의 원-핫` → `약 0.95로 거의 원-핫`
  - L219: `약 0.53에서 0.96으로` → `약 0.53에서 0.95로`
- **L267**: Swin은 창을 층마다 계속 옮기지 않는다. 연속한 두 블록에서 일반 창과 옮긴 창을 번갈아 쓴다(§3.2). 계산량이 선형이 되는 이유는 창 분할이다(§1).
  - 변경: `Swin Transformer는 이미지를 겹치지 않는 창으로 나눠 창 안에서만 attention을 계산해, 창 크기가 고정이면 계산량이 이미지 크기에 선형이 되게 했습니다<Cite claim="clm:swin-mitigates-quadratic" loc="Swin §1" />. 창 사이는 연속한 두 블록에서 창 분할을 번갈아 바꿔(일반 창, 창 크기의 절반만큼 옮긴 창) 잇습니다<Cite claim="clm:intro-shifted-window" loc="Swin §3.2" />.`

권장 4곳(틀린 말은 아니지만 오해 여지가 있다):

- **L108**: `query와 key의 성분 $q_i, k_i$가 서로 독립이고` → `query와 key의 모든 성분 $q_1,\dots,q_{d_k}, k_1,\dots,k_{d_k}$가 서로 독립이고` (유도 셋째 줄 '분산의 합'이 성립하려면 성분 전체가 서로 독립이어야 한다)
- **L44**: `Multi-head attention</ConceptLink>은 이 연산을 여러 개 나란히 돌린 것이고` → `Multi-head attention</ConceptLink>은 query·key·value를 head마다 다른 학습된 행렬로 투영한 뒤 이 연산을 여러 개 나란히 돌리고 결과를 이어 붙인 것이고`
- **L276**: `실제로 더 빠르고 메모리를 덜 쓴다고` → `additive attention보다 실제로 더 빠르고 메모리를 덜 쓴다고`
- **L52**: `토큰이 n개, query·key 차원이` → `query가 n개, key·value가 m개, query·key 차원이`

선택: L37 `벡터의 길이(성분 개수)`와 L214 `벡터 길이 d_k`에서 '길이'를 '차원'으로 바꾼다. '길이'는 노름으로 읽힐 수 있다.

### 2. `method:shifted-window-attention` (`data/seed/seed_graph.yaml`)

summary를 다음으로 바꾼다.

> `이미지를 겹치지 않는 창으로 나눠 창 안에서만 self-attention을 계산하고, 연속한 두 블록에서 일반 창과 창 크기의 절반만큼 옮긴 창을 번갈아 써서 창 사이를 연결하는 방법이다.`

### 3. `field:language-modeling` (`data/graph/atlas.yaml`)

지금 요약은 자기회귀(다음 토큰 예측)만 정의한다. 그런데 이 분야에 있는 BERT는 마스크 언어 모델이다. summary를 다음으로 바꾼다.

> `언어 모델링은 텍스트의 확률 구조를 학습하는 분야로, 앞 문맥으로 다음 토큰을 예측하는 자기회귀 방식과 가려진 토큰을 양쪽 문맥으로 예측하는 마스크 언어 모델 방식을 포함한다.`

요약을 바꾸고 싶지 않다면 대안이 있다. `model:bert`의 `fields`를 `field:natural-language-processing`으로 옮기는 것이다. 다만 그러면 `model:bert`도 고친 것이 되어 재검토가 필요하다.

반영한 뒤 돌릴 것: `seedtool validate`(G 0), 문서 verify 블록. 이번 수정은 숫자가 들어간 문장만 바꾸고 assert는 건드리지 않는다.

## 직접 확인할 것 (학습자를 가장 크게 오도할 수 있는 순서)

1. **√d_k의 이유(L104, L108–L120).** 문서의 핵심 설명이다. 논문은 이를 추정으로 말하고, 독립·분산 1이라는 가정 아래에서만 성립한다. 기초 단계만 읽는 사람에게도 이 두 가지가 보이는지 확인한다. 각주 번호 '각주 4'는 PDF 기준이다. arXiv HTML에서는 번호가 다르게 보인다.
2. **Lab과 본문의 숫자.** Lab은 seed 42, 표본 1,000개로 0.5251→0.9548, Jacobian 0.3414→0.0628을 보여 준다. 본문 L118, L219, L224와 문항 `ai:lab-sdpa-01` 해설이 이 값과 같은 반올림으로 맞는지 본다. `ai:lab-sdpa-02` 해설의 Var 64.65는 표본 10,000개 기준이라, Lab 화면의 61.74와 다르다(둘 다 맞는 값이다).
3. **Swin 창 이동(L267, `method:shifted-window-attention`).** '층마다 옮긴다'는 표현은 이동이 누적된다고 읽힌다. 원문 §3.2 그림 2와 함께 본다.
4. **화면 문구 템플릿(데이터 밖, `src/lib/predicates.ts`).** INTRODUCES 설명이 '처음 제시한다'로 되어 있어 최초 발명처럼 읽힌다. 02 §8은 "최초 발명 여부는 판단하지 않음"이라고 한다. ADDRESSES 라벨 '문제 해결'은 성공처럼 읽히는데, 이 술어는 의도만 뜻한다. 이번 레코드의 문장 자체는 참이지만, 공개 전에 문구를 '제시', '다루는 문제'로 바꿀지 결정이 필요하다. 이 시트의 승인 대상은 아니다.
5. **BERT와 언어 모델링 정의(`field:language-modeling`).** Atlas에서 BERT를 '다음 토큰을 예측하는 분야'에 두면 GPT 계열과 혼동된다. 위 fix 3 가운데 어느 쪽으로 할지 정한다.

## 참고 (공개 결과에 영향, 오류 아님)

- 문서의 ConceptLink 중 `concept:dot-product`, `concept:softmax`, `concept:variance-of-sum`, `concept:softmax-temperature`, `method:positional-encoding`은 이번 범위 밖이다. 공개 빌드에서는 링크 없이 글자로만 보인다.
- Lab 안의 근거 인용(`clm:prereq-variance-of-sum-scaled-dot-product-attention-derive`)은 승인 전이라 공개 빌드에 나오지 않는다.
- BERT·ViT claim의 출처 논문(`paper:devlin2018-bert`, `paper:dosovitskiy2020-vit`)도 범위 밖이다. claim은 공개되지만 논문 페이지는 아직 비공개다.
- `clm:intro-additive-attention`에는 근거를 하나 더 붙이면 좋다(선택). 1409.0473v7 §3.1 4문단 `We parametrize the alignment model a as a feedforward neural network which is jointly trained with all the other components of the proposed system.`(대조 도구에서 found 확인)

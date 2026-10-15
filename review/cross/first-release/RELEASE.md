# first-release 게시 기록

- 게시일: 2026-10-15
- 방법: AI 교차 검증 패널(ADR-026). 기준은 `docs/verification/CROSS_REVIEW.md`.
- 승인 커밋: `a420066`. 되돌리려면 `git revert a420066` 후 push한다.
- 결과: 44건 승인(엔티티 27, Claim 12, 문항 4, Wiki 1). 공개 관문 기준 엔티티 31(문항 포함), Claim 12, Wiki 1, 출처 6, 제외 0.

## 검증자

모델은 모두 claude-opus-5-5(High)다. 레코드마다 원문 우선 1명과 서술 우선 1명이 따로 봤다.

| 범위 | 원문 우선 | 서술 우선 |
|---|---|---|
| 엔티티 27건 | `agent:opus55-src-ent-1015` | `agent:opus55-clm-ent-1015` |
| Claim 12건, 문항 4건 | `agent:opus55-src-clm-1015` | `agent:opus55-clm-clm-1015` |
| Wiki 1건(54문단) | `agent:opus55-src-wiki-1015` | `agent:opus55-clm-wiki-1015` |

표본 감사는 `agent:opus55-aud-1015`가 다른 보고서를 보지 않고 했다(5건, 모두 승인).

## 진행

1. 1차 검증
   - Claim 12건과 문항 4건은 두 검증자 모두 승인했다.
   - Wiki는 두 검증자 모두 수정 필요였다. 공통 지적은 두 가지다. multi-head attention에서 출력 투영(W^O)이 빠졌고, 논문의 추정(We suspect)에 없는 "한 key에 쏠림"을 논문 주장처럼 썼다. 한 명은 query를 "다른 토큰들의 key"와만 비교한다는 서술도 지적했다.
   - 엔티티는 원문 우선이 10건, 서술 우선이 13건을 수정 필요로 판정했다. 이유는 틀린 별칭, 출처 없는 한국어 별칭과 분야 이름, 다시 확인할 수 없는 dblp 키, 실험실 설정값, Transformer 요약이었다.
2. 수정(검증자가 아닌 편집 담당): `6e8bcf3`, `3740a47`.
3. 2차 검증: 바뀐 15건을 각 검증자가 다시 봤다. 모두 승인했고, 출처 등급 규칙에 못 미친 확인 3개는 출처를 보강했다.
4. 구절 대조: 보고서의 출처 구절 400개를 도구가 URL에서 다시 받아 모두 찾았다(`confirm.json`).
5. 표본 감사: 5건 모두 승인했고, 두 검증자가 놓친 오류는 없었다.

## 독립성 기록

- 검증자들이 같은 임시 폴더를 썼다. 한 검증자는 다른 검증자의 파일 이름을 봤고, 내려받기 폴더를 잠깐 옮겼다가 되돌렸다고 보고했다. 내용을 열었다는 보고는 없다. 다음 릴리스부터는 검증자마다 폴더를 따로 지정한다.
- 한 검증자의 grep 출력에 `specs/` 줄이 섞였다. 판정에는 쓰지 않았다고 보고했고, `specs/`에는 사전 검수 의견이 없다.

## 남은 메모 (게시를 막지 않음)

- `clm:intro-additive-attention`: 근거 인용문만으로는 additive 형태가 드러나지 않는다. 논문 §3.1의 문장을 두 번째 근거로 넣으면 더 단단해진다.
- 실험실의 온도 모드는 logit 입력이 5칸이라, 문항 `ai:lab-softmax-temp-01`의 [2, 1, 0]을 정확히 넣을 수 없다.
- 인용문 두 개가 원문의 수식 앞에서 끊긴다.
- 외부 데이터 문제: OpenAlex `W2626778328`의 DOI와 연도 필드가 잘못 합쳐져 있다.

## 공개된 레코드

| ID | 종류 | 이름 |
|---|---|---|
| `wiki:scaled-dot-product-attention` | Wiki | Scaled Dot-Product Attention |
| `clm:intro-sdpa` | Claim | Attention Is All You Need —INTRODUCES→ Scaled Dot-Product Attention |
| `clm:sdpa-is-a-attention` | Claim | Scaled Dot-Product Attention —IS_A→ Attention 메커니즘 |
| `clm:scaled-dot-product-attention-part-of-multi-head-attention` | Claim | Scaled Dot-Product Attention —PART_OF→ Multi-Head Attention |
| `clm:multi-head-attention-part-of-transformer-encoder-layer` | Claim | Multi-Head Attention —PART_OF→ Transformer 인코더 층 |
| `clm:transformer-encoder-layer-part-of-bert` | Claim | Transformer 인코더 층 —PART_OF→ BERT |
| `clm:transformer-encoder-layer-part-of-vit` | Claim | Transformer 인코더 층 —PART_OF→ Vision Transformer |
| `clm:transformer-addresses-sequential` | Claim | Transformer —ADDRESSES→ RNN의 순차 계산 |
| `clm:transformer-mitigates-sequential` | Claim | Transformer —MITIGATES→ RNN의 순차 계산 |
| `clm:intro-additive-attention` | Claim | Neural Machine Translation by Jointly Learning to Align and Translate —INTRODUCES→ Additive Attention |
| `clm:vit-adapts-transformer` | Claim | Vision Transformer —ADAPTS→ Transformer |
| `clm:swin-mitigates-quadratic` | Claim | Swin Transformer —MITIGATES→ 고해상도에서 attention의 이차 비용 |
| `clm:intro-shifted-window` | Claim | Swin Transformer: Hierarchical Vision Transformer using Shifted Windows —INTRODUCES→ Shifted Window Attention |
| `concept:attention-mechanism` | 엔티티 | Attention 메커니즘 |
| `method:additive-attention` | 엔티티 | Additive Attention |
| `method:multi-head-attention` | 엔티티 | Multi-Head Attention |
| `method:scaled-dot-product-attention` | 엔티티 | Scaled Dot-Product Attention |
| `method:shifted-window-attention` | 엔티티 | Shifted Window Attention |
| `method:transformer-encoder-layer` | 엔티티 | Transformer 인코더 층 |
| `model:bert` | 엔티티 | BERT |
| `model:swin` | 엔티티 | Swin Transformer |
| `model:transformer` | 엔티티 | Transformer |
| `model:vit` | 엔티티 | Vision Transformer |
| `paper:bahdanau2014-attention` | 엔티티 | Neural Machine Translation by Jointly Learning to Align and Translate |
| `paper:liu2021-swin` | 엔티티 | Swin Transformer: Hierarchical Vision Transformer using Shifted Windows |
| `paper:vaswani2017-transformer` | 엔티티 | Attention Is All You Need |
| `problem:quadratic-attention-cost-high-resolution` | 엔티티 | 고해상도에서 attention의 이차 비용 |
| `problem:sequential-computation-in-rnns` | 엔티티 | RNN의 순차 계산 |
| `field:artificial-intelligence` | 엔티티 | 인공지능 |
| `field:computer-vision` | 엔티티 | 컴퓨터 비전 |
| `field:deep-learning` | 엔티티 | 딥러닝 |
| `field:efficient-transformers` | 엔티티 | Efficient Transformers |
| `field:image-classification` | 엔티티 | 이미지 분류 |
| `field:language-modeling` | 엔티티 | 언어 모델링 |
| `field:machine-learning` | 엔티티 | 기계학습 |
| `field:machine-translation` | 엔티티 | 기계 번역 |
| `field:ml-systems-efficient-inference` | 엔티티 | ML Systems and Efficient Inference |
| `field:natural-language-processing` | 엔티티 | 자연어 처리 |
| `field:vision-transformers` | 엔티티 | 비전 트랜스포머 |
| `lab:softmax-temperature` | 엔티티 | Softmax Temperature & Scaled Dot-Product Lab |
| `ai:lab-softmax-temp-01` | 문항 | z = [2, 1, 0]에서 T를 1에서 0.1로 낮추면 가장 큰 확률은? |
| `ai:lab-softmax-temp-02` | 문항 | z = [2, 0], T = 2일 때 첫 번째 확률은? |
| `ai:lab-sdpa-01` | 문항 | scaling 없이 d_k를 4에서 512로 키우면 평균 최대 attention 가중치는? |
| `ai:lab-sdpa-02` | 문항 | q, k의 성분이 서로 독립이고 평균 0, 분산 1이다. d_k = 64일 때 q·k의 표준편차는? |

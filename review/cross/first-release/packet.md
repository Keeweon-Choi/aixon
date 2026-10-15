# Cross-review packet: first-release

## wiki:scaled-dot-product-attention (wiki)

Hash: `f7d4d6f07706`

Fields: para:1, para:2, para:3, para:4, para:5, para:6, para:7, para:8, para:9, para:10, para:11, para:12, para:13, para:14, para:15, para:16, para:17, para:18, para:19, para:20, para:21, para:22, para:23, para:24, para:25, para:26, para:27, para:28, para:29, para:30, para:31, para:32, para:33, para:34, para:35, para:36, para:37, para:38, para:39, para:40, para:41, para:42, para:43, para:44, para:45, para:46, para:47, para:48, para:49, para:50, para:51, para:52, para:53, para:54

```yaml
frontmatter:
  id: wiki:scaled-dot-product-attention
  entity: method:scaled-dot-product-attention
  title: Scaled Dot-Product Attention
  subtitle: query와 key의 내적으로 value를 섞는 Transformer의 핵심 연산과, √d_k로 나누는 이유
  levels:
  - intuition
  - fundamentals
  - deep
  sections:
  - overview
  - why
  - mechanism
  - math
  - example
  - code
  - visual
  - limitations
  - history
  authors:
  - id: agent:claude-opus-5-5
    role: draft
  ai_generated: true
  sources:
  - src:arxiv:1706.03762v7
  - src:arxiv:1409.0473v7
  - src:arxiv:2010.11929v2
  - src:arxiv:2103.14030v2
  - src:url:b301323053b2
  claims:
  - clm:intro-sdpa
  - clm:sdpa-is-a-attention
  - clm:scaled-dot-product-attention-part-of-multi-head-attention
  - clm:multi-head-attention-part-of-transformer-encoder-layer
  - clm:transformer-encoder-layer-part-of-bert
  - clm:transformer-encoder-layer-part-of-vit
  - clm:transformer-addresses-sequential
  - clm:transformer-mitigates-sequential
  - clm:intro-additive-attention
  - clm:vit-adapts-transformer
  - clm:swin-mitigates-quadratic
  - clm:intro-shifted-window
  labs:
  - lab:softmax-temperature
  figures:
  - id: fig-sdpa-flow
    origin: self-made
    alt: Q와 K의 전치를 곱해 점수 행렬을 만들고, √d_k로 나눈 뒤 행마다 softmax를 취해 가중치를 얻고, 그 가중치로 V의 행들을
      섞어 출력을 만드는 흐름
  updated_at: '2026-10-15'
paragraphs:
  para:1: <Section id="overview" level="intuition" title="개요와 직관">
  para:2: 'Google Research 블로그 글 "Transformer: A Novel Neural Network Architecture
    for Language Understanding"(Jakob Uszkoreit, 2017)은 "I arrived at the bank after
    crossing the river"(나는 강을 건넌 뒤 bank에 도착했다)라는 문장을 예로 듭니다. 여기서 "bank"가 은행이 아니라 강둑이라는
    것을 정하려면 "river"라는 단어를 함께 봐야 합니다. 이 글은 Transformer가 "bank"의 다음 표현을 계산할 때 문장의 다른
    모든 단어와 비교해 단어마다 attention 점수를 매기고, 이 점수가 다른 단어들이 "bank"의 새 표현에 **얼마나 기여할지** 정한다고
    설명합니다<Cite src="src:url:b301323053b2" loc="The Transformer 절" />. Scaled Dot-Product
    Attention은 Transformer에서 이 점수와 비율을 계산하는 연산입니다.'
  para:3: 각 단어(토큰)는 세 가지 역할의 벡터를 가집니다.
  para:4: '- **query(질의)**: 모든 key와 비교되는 벡터(self-attention에서는 자기 자신의 key도 포함)

    - **key(열쇠)**: query와 비교되어 점수를 정하는 벡터

    - **value(값)**: 그 점수로 얻은 가중치에 따라 섞여 출력이 되는 벡터'
  para:5: query와 각 key가 얼마나 잘 맞는지 점수를 매기고, 점수를 확률처럼 바꾼 뒤, 그 비율대로 value들을 섞습니다. 결과는
    value들의 가중합입니다. Transformer 논문은 attention 함수를 query와 key–value 쌍들을 출력으로 대응시키는
    함수라고 설명합니다(번역)<Cite claim="clm:sdpa-is-a-attention" loc="§3.2" />.
  para:6: 이 예에는 단서가 붙어 있습니다. 블로그는 Transformer가 "river"에 바로 주목하도록 학습할 수 **있다**(can
    learn)고 쓰고, 자신들의 영어–프랑스어 번역 모델에서 바로 이런 동작을 관찰했다고 덧붙입니다. 또 "river"가 높은 점수를 받을 수
    **있다**(could receive)고 씁니다<Cite src="src:url:b301323053b2" loc="The Transformer
    절" />. 점수는 학습된 query와 key로 계산되므로, 학습 결과 그런 관련도가 높은 점수로 나타나게 될 수 있을 뿐 늘 그렇게 된다는
    보장은 없습니다.
  para:7: '<Callout kind="key">

    한 줄 요약: **점수 = query·key, 가중치 = softmax(점수 ÷ √d_k), 출력 = 가중치로 섞은 value.** 여기서
    d_k는 query·key 벡터의 차원(성분 개수)입니다.

    </Callout>'
  para:8: </Section>
  para:9: <Section id="why" level="intuition" title="왜 중요한가">
  para:10: '- <ConceptLink id="method:multi-head-attention">Multi-head attention</ConceptLink>은
    query·key·value를 head마다 다른 학습된 행렬로 투영한 뒤 이 연산을 여러 개 나란히 돌리고, 결과를 이어 붙여 학습된 행렬
    $W^O$로 한 번 더 투영한 것이고<Cite claim="clm:scaled-dot-product-attention-part-of-multi-head-attention"
    loc="§3.2.2" />, <ConceptLink id="method:transformer-encoder-layer">Transformer
    encoder layer</ConceptLink>는 multi-head attention으로 시작합니다<Cite claim="clm:multi-head-attention-part-of-transformer-encoder-layer"
    loc="§3.1" />. BERT와 ViT는 이 encoder layer를 쌓아 만듭니다<Cite claim="clm:transformer-encoder-layer-part-of-bert"
    loc="BERT §3" /><Cite claim="clm:transformer-encoder-layer-part-of-vit" loc="ViT
    §3.1" />.

    - 순환 신경망(RNN)은 단어를 하나씩 순서대로 처리해서 학습 예제 안에서 병렬화가 어렵습니다. Transformer는 순환을 쓰지 않고
    attention만으로 이 순차 계산 문제를 풀려고 했고<Cite claim="clm:transformer-addresses-sequential"
    loc="§1" />, self-attention 층은 모든 위치를 **일정한 횟수의 순차 연산**으로 연결합니다(RNN은 시퀀스 길이 n에
    비례)<Cite claim="clm:transformer-mitigates-sequential" loc="§4, Table 1" />.

    - 이미지도 패치로 자르면 토큰처럼 다룰 수 있어서, 같은 연산이 비전으로 옮겨 갔습니다<Cite claim="clm:vit-adapts-transformer"
    loc="ViT §1" />.'
  para:11: </Section>
  para:12: <Section id="mechanism" level="fundamentals" title="핵심 작동 원리">
  para:13: query가 n개, key·value가 m개, query·key 차원이 $d_k$, value 차원이 $d_v$라고 합시다. 모든
    query를 행으로 쌓은 행렬을 $Q \in \mathbb{R}^{n \times d_k}$, key를 $K \in \mathbb{R}^{m
    \times d_k}$, value를 $V \in \mathbb{R}^{m \times d_v}$라고 하면(self-attention에서는
    m = n), 연산은 네 단계입니다.
  para:14: '1. **점수**: $S = QK^\top \in \mathbb{R}^{n \times m}$. $S_{ij}$는 i번째 query와
    j번째 key의 <ConceptLink id="concept:dot-product">dot product</ConceptLink>입니다.

    2. **스케일**: $S / \sqrt{d_k}$.

    3. **가중치**: 행마다 <ConceptLink id="concept:softmax">softmax</ConceptLink>를 취해 $A
    = \mathrm{softmax}(S/\sqrt{d_k})$. 각 행의 합은 1입니다.

    4. **출력**: $O = AV \in \mathbb{R}^{n \times d_v}$. i번째 출력은 value 행들을 $A$의 i번째
    행 비율로 섞은 것입니다.'
  para:15: 논문은 이 연산에 "Scaled Dot-Product Attention"이라는 이름을 붙였고<Cite claim="clm:intro-sdpa"
    loc="§3.2.1" />, query와 모든 key의 dot product를 $\sqrt{d_k}$로 나눈 뒤 softmax로 value의
    가중치를 얻는다고 설명합니다<Cite src="src:arxiv:1706.03762v7" loc="§3.2.1" />.
  para:16: "<Figure id=\"fig-sdpa-flow\">\n<svg viewBox=\"0 0 640 150\" role=\"img\"\
    \ aria-labelledby=\"fig-sdpa-flow-title\" xmlns=\"http://www.w3.org/2000/svg\"\
    >\n  <title id=\"fig-sdpa-flow-title\">Scaled Dot-Product Attention 계산 흐름</title>\n\
    \  <defs>\n    <marker id=\"fig-sdpa-arrow\" viewBox=\"0 0 10 10\" refX=\"9\"\
    \ refY=\"5\" markerWidth=\"7\" markerHeight=\"7\" orient=\"auto-start-reverse\"\
    >\n      <path d=\"M0 0 L10 5 L0 10 z\" fill=\"currentColor\"/>\n    </marker>\n\
    \  </defs>\n  <g font-family=\"IBM Plex Mono, monospace\" font-size=\"13\" fill=\"\
    currentColor\">\n    <rect x=\"10\" y=\"20\" width=\"70\" height=\"40\" rx=\"\
    4\" fill=\"none\" stroke=\"currentColor\"/><text x=\"45\" y=\"45\" text-anchor=\"\
    middle\">Q</text>\n    <rect x=\"10\" y=\"90\" width=\"70\" height=\"40\" rx=\"\
    4\" fill=\"none\" stroke=\"currentColor\"/><text x=\"45\" y=\"115\" text-anchor=\"\
    middle\">K</text>\n    <rect x=\"120\" y=\"55\" width=\"90\" height=\"40\" rx=\"\
    4\" fill=\"none\" stroke=\"currentColor\"/><text x=\"165\" y=\"80\" text-anchor=\"\
    middle\">QKᵀ</text>\n    <rect x=\"250\" y=\"55\" width=\"90\" height=\"40\" rx=\"\
    4\" fill=\"none\" stroke=\"currentColor\"/><text x=\"295\" y=\"80\" text-anchor=\"\
    middle\">÷ √d_k</text>\n    <rect x=\"380\" y=\"55\" width=\"100\" height=\"40\"\
    \ rx=\"4\" fill=\"none\" stroke=\"currentColor\"/><text x=\"430\" y=\"80\" text-anchor=\"\
    middle\">softmax(행)</text>\n    <rect x=\"520\" y=\"55\" width=\"110\" height=\"\
    40\" rx=\"4\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"/><text\
    \ x=\"575\" y=\"80\" text-anchor=\"middle\">A · V = O</text>\n    <rect x=\"380\"\
    \ y=\"110\" width=\"100\" height=\"32\" rx=\"4\" fill=\"none\" stroke=\"currentColor\"\
    \ stroke-dasharray=\"4 3\"/><text x=\"430\" y=\"131\" text-anchor=\"middle\">V</text>\n\
    \  </g>\n  <g stroke=\"currentColor\" fill=\"none\" marker-end=\"url(#fig-sdpa-arrow)\"\
    >\n    <line x1=\"80\" y1=\"40\" x2=\"118\" y2=\"68\"/>\n    <line x1=\"80\" y1=\"\
    110\" x2=\"118\" y2=\"82\"/>\n    <line x1=\"210\" y1=\"75\" x2=\"248\" y2=\"\
    75\"/>\n    <line x1=\"340\" y1=\"75\" x2=\"378\" y2=\"75\"/>\n    <line x1=\"\
    480\" y1=\"75\" x2=\"518\" y2=\"75\"/>\n    <line x1=\"480\" y1=\"126\" x2=\"\
    538\" y2=\"97\"/>\n  </g>\n</svg>\n</Figure>"
  para:17: 행렬 모양만 맞추면 구현이 거의 끝납니다. 점수 행렬은 n × m이라서 **토큰 수의 제곱**만큼 메모리를 씁니다(한계 절 참고).
  para:18: </Section>
  para:19: <Section id="math" level="fundamentals" title="수학적 기초">
  para:20: '$$

    \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V

    $$'
  para:21: $Q, K, V$는 query·key·value를 행으로 쌓은 행렬, $d_k$는 query와 key 벡터의 차원이고, softmax는
    점수 행렬의 **행마다** 따로 적용합니다. softmax는 벡터 $\mathbf{z}$를 $\mathrm{softmax}(\mathbf{z})_i
    = e^{z_i} / \sum_j e^{z_j}$로 바꿉니다. 두 가지 성질이 중요합니다.
  para:22: '- 결과는 모두 양수이고 합이 1입니다(가중치로 쓸 수 있다).

    - 모든 성분에 같은 상수를 더해도 결과가 같습니다: $\mathrm{softmax}(\mathbf{z} + c) = \mathrm{softmax}(\mathbf{z})$.
    구현에서 최댓값을 빼는 이유입니다.'
  para:23: '**왜 $\sqrt{d_k}$로 나누는가 (요약).** query와 key의 성분이 서로 독립이고 평균 0, 분산 1이라고 가정하면
    dot product의 분산은 $d_k$입니다. 논문은 $d_k$가 크면 dot product의 크기가 커져 softmax를 기울기가 아주
    작은 영역으로 밀어낸다고 추정합니다(We suspect). $\sqrt{d_k}$로 나누면 분산이 다시 1이 됩니다<Cite src="src:arxiv:1706.03762v7"
    loc="§3.2.1, 각주 4" />. 이 문서의 설명을 덧붙이면, 점수가 커지면 softmax가 한 key에 쏠립니다(아래 심화 단계의
    수치와 시각적 설명의 Lab). 유도는 심화 단계에서 볼 수 있습니다.'
  para:24: <Level of="deep">
  para:25: '**유도.** 논문은 "$d_k$가 크면 dot product의 크기가 커져 softmax를 기울기가 매우 작은 영역으로 밀어낸다고
    추정한다"고 씁니다(번역; 원문: "We suspect that for large values of d_k, the dot products
    grow large in magnitude, pushing the softmax function into regions where it has
    extremely small gradients"). 각주 4는 그 크기를 이렇게 설명합니다<Cite src="src:arxiv:1706.03762v7"
    loc="각주 4" />. query와 key의 모든 성분 $q_1,\dots,q_{d_k}, k_1,\dots,k_{d_k}$가 서로 독립이고
    평균 0, 분산 1이라고 가정하면:'
  para:26: '$$

    \begin{aligned}

    \mathbb{E}[q_i k_i] &= \mathbb{E}[q_i]\,\mathbb{E}[k_i] = 0 && \text{(독립)}\\

    \mathrm{Var}(q_i k_i) &= \mathbb{E}[q_i^2]\,\mathbb{E}[k_i^2] - 0 = 1 && \text{(독립,
    분산 1)}\\

    \mathrm{Var}(\mathbf{q}\cdot\mathbf{k}) &= \textstyle\sum_{i=1}^{d_k} \mathrm{Var}(q_i
    k_i) = d_k && \text{(독립이므로 분산의 합)}

    \end{aligned}

    $$'
  para:27: 세 번째 줄은 <ConceptLink id="concept:variance-of-sum">독립 확률변수 합의 분산</ConceptLink>
    성질입니다. 그래서 점수의 표준편차는 $\sqrt{d_k}$로 커집니다. 예를 들어 Lab과 같은 조건(key 8개, 표본 1,000개, seed
    42)에서 나누지 않으면, 평균 최대 가중치의 추정값이 $d_k = 64$(표준편차 8)에서 약 0.87로 한 key에 크게 쏠리고, $d_k
    = 512$에서는 약 0.95로 거의 원-핫이 됩니다(정확한 기댓값이 아니라 표본에서 얻은 추정값입니다). $\sqrt{d_k}$로 나누면
    분산이 다시 1이 됩니다. 이것을 softmax의 <ConceptLink id="concept:softmax-temperature">temperature</ConceptLink>를
    $\sqrt{d_k}$로 둔 것으로 볼 수도 있습니다(논문에는 없는 해석입니다).
  para:28: 이 설명은 **가정 아래의 근사 논증**입니다. 학습된 Q, K의 성분이 독립·분산 1이라는 보장은 없습니다. 논문도 "추정한다(We
    suspect)"고 썼습니다.
  para:29: </Level>
  para:30: </Section>
  para:31: <Section id="example" level="fundamentals" title="단계별 예제">
  para:32: 토큰 3개, $d_k = 2$인 작은 예를 손으로 계산해 봅니다. 설명을 위해 Q = K = V = X로 둡니다(실제 모델에서는
    학습된 투영 행렬을 곱해 만듭니다).
  para:33: '$$

    X = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}

    $$'
  para:34: '1. 점수 $S = XX^\top$: 첫 행은 $(1\cdot1+0\cdot0,\ 1\cdot0+0\cdot1,\ 1\cdot1+0\cdot1)
    = (1, 0, 1)$. 전체는 $\begin{pmatrix}1&0&1\\0&1&1\\1&1&2\end{pmatrix}$.

    2. 스케일: $\sqrt{2} \approx 1.4142$로 나누면 첫 행은 $(0.7071, 0, 0.7071)$.

    3. softmax: $e^{0.7071} \approx 2.0281$, $e^0 = 1$이므로 첫 행 가중치는 $(2.0281, 1, 2.0281)
    / 5.0562 \approx (0.401, 0.198, 0.401)$. 셋째 행은 $(0.248, 0.248, 0.503)$(반올림 때문에
    합이 0.999로 보입니다).

    4. 출력 첫 행: $0.401\cdot(1,0) + 0.198\cdot(0,1) + 0.401\cdot(1,1) \approx (0.802,
    0.599)$.'
  para:35: 스케일 없이 계산하면 첫 행 가중치는 $(0.422, 0.155, 0.422)$로 더 뾰족합니다. 이 예에서는 차이가 작지만,
    $d_k$가 커질수록 차이가 커집니다(시각적 설명의 Lab).
  para:36: </Section>
  para:37: <Section id="code" level="fundamentals" title="구현">
  para:38: numpy로 쓰면 몇 줄입니다. softmax에서 최댓값을 먼저 빼는 것은 결과를 바꾸지 않으면서(shift invariance)
    `exp`가 넘치는 것을 막기 위해서입니다. 아래는 **head 하나, 마스크 없는** 버전입니다. 디코더처럼 뒤쪽 토큰을 보면 안 되는 경우에는
    softmax 전에 해당 점수를 $-\infty$로 가립니다(논문 §3.2.3의 mask)<Cite src="src:arxiv:1706.03762v7"
    loc="§3.2.3" />.
  para:39: </Section>
  para:40: <Section id="visual" level="intuition" title="시각적 설명">
  para:41: 아래 Lab에서 직접 확인해 보세요. **숫자를 보기 전에 먼저 예측해 보세요.**
  para:42: '1. 온도 T를 낮추면 가장 큰 확률은 커질까요, 작아질까요?

    2. √d_k로 나누지 않고 벡터 차원 d_k만 키우면, 가중치는 한 key에 몰릴까요, 고르게 퍼질까요?'
  para:43: <Lab id="lab:softmax-temperature" />
  para:44: '<Callout kind="note">

    확인: (1) logit [2, 1, 0]에서 T를 1에서 0.1로 낮추면 가장 큰 확률이 0.665에서 0.99995로 커집니다. (2)
    나누지 않고 d_k를 4에서 512로 키우면 평균 최대 가중치가 약 0.53에서 0.95로 한 key에 몰립니다. √d_k로 나누면 0.34–0.37
    근처에서 거의 그대로입니다. (2)의 값은 Lab의 표본 추정값입니다(key 8개, 표본 1,000개, seed 42). 정확한 기댓값과는
    조금 다를 수 있습니다.

    </Callout>'
  para:45: <Level of="deep">
  para:46: 몰릴수록 softmax의 기울기도 작아집니다. softmax Jacobian의 Frobenius 노름(기울기 크기)은 나누지 않을
    때 d_k = 4에서 약 0.34, d_k = 512에서 약 0.06으로 줄고, √d_k로 나누면 0.36 근처로 유지됩니다. Lab은 seed
    42, 표본 1,000개로 계산한 고정값(0.525→0.955, 0.341→0.063)을 보여 주고, 아래 코드는 다른 난수로 같은 경향을
    다시 확인합니다.
  para:47: </Level>
  para:48: </Section>
  para:49: <Section id="limitations" level="fundamentals" title="한계와 트레이드오프">
  para:50: '- **계산·메모리가 토큰 수의 제곱**: self-attention 층의 계산량은 $O(n^2 \cdot d)$입니다<Cite
    src="src:arxiv:1706.03762v7" loc="Table 1" />. 고해상도 이미지처럼 토큰이 많으면 부담이 커집니다. Swin
    Transformer는 이미지를 겹치지 않는 창으로 나눠 창 안에서만 attention을 계산해, 창 크기가 고정이면 계산량이 이미지 크기에
    선형이 되게 했습니다<Cite claim="clm:swin-mitigates-quadratic" loc="Swin §1" />. 창 사이는
    연속한 두 블록에서 창 분할을 번갈아 바꿔(일반 창, 창 크기의 절반만큼 옮긴 창) 잇습니다<Cite claim="clm:intro-shifted-window"
    loc="Swin §3.2" />.

    - **순서를 모른다**: 점수 계산에 위치 정보가 없어서, self-attention에서 토큰 순서를 바꾸면 출력도 같은 순서로 바뀔 뿐
    각 토큰의 출력 값은 그대로입니다(순열 등변성, 구현 절의 확인 코드). 그래서 Transformer는 입력 embedding에 <ConceptLink
    id="method:positional-encoding">positional encoding</ConceptLink>을 더합니다<Cite src="src:arxiv:1706.03762v7"
    loc="§3.5" />.

    - **포화**: 스케일이 맞지 않으면 softmax가 원-핫에 가까워져 기울기가 작아집니다(수학 절). $\sqrt{d_k}$ 스케일은 성분
    분포에 대한 가정에 기댄 처방입니다.'
  para:51: </Section>
  para:52: <Section id="history" level="deep" title="역사적 발전">
  para:53: '- **2014 — 정렬을 함께 배우는 번역(Bahdanau et al.)**: 인코더–디코더 번역에서 문장 전체를 고정 길이
    벡터 하나로 압축하는 것이 병목이라고 보고, 디코더가 원문의 관련 위치를 부드럽게 찾게 했습니다<Cite claim="clm:intro-additive-attention"
    loc="§1" />. 이 점수 함수는 작은 신경망(덧셈 꼴)이라 additive attention이라고 불립니다<Cite src="src:arxiv:1706.03762v7"
    loc="§3.2.1" />.

    - **2017 — Transformer(Vaswani et al.)**: 당시 dot-product(곱셈형) attention은 additive
    attention과 함께 가장 널리 쓰이던 두 방식 중 하나였고, Transformer는 여기에 $1/\sqrt{d_k}$ 스케일을 더했습니다.
    논문은 dot-product attention이 스케일 인자를 빼면 자기들의 알고리즘과 같다고 쓰고(번역; 원문: "Dot-product attention
    is identical to our algorithm, except for the scaling factor of 1/√d_k"), 고도로
    최적화된 행렬 곱셈 코드로 구현할 수 있어 additive attention보다 실제로 더 빠르고 메모리를 덜 쓴다고 설명합니다<Cite src="src:arxiv:1706.03762v7"
    loc="§3.2.1" />.

    - **2020 — ViT(Dosovitskiy et al.)**: 이미지를 고정 크기 패치(예: 16×16)로 잘라 토큰처럼 다루고, 표준
    Transformer를 최소한만 바꿔 그대로 적용했습니다<Cite claim="clm:vit-adapts-transformer" loc="ViT
    §1, §3" />.

    - **2021 — Swin Transformer**: 창 단위 attention과 창 이동으로 전역 attention의 제곱 비용을 이미지
    크기에 선형인 비용으로 줄였습니다<Cite claim="clm:swin-mitigates-quadratic" loc="Swin §1" />.'
  para:54: </Section>
```

## clm:intro-sdpa (claim)

Hash: `1484d068a3a5`

Fields: relation, evidence[0]

```yaml
id: clm:intro-sdpa
predicate: INTRODUCES
subject: paper:vaswani2017-transformer
object: method:scaled-dot-product-attention
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    section: 3.2.1 Scaled Dot-Product Attention
    paragraph: 1
    html_id: S3.SS2.SSS1.p1
  quote: We call our particular attention "Scaled Dot-Product Attention" (Figure 2).
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: null
object_name: Scaled Dot-Product Attention
predicate_meaning: 논문이 방법·모델·데이터셋을 제시한다.
```

## clm:sdpa-is-a-attention (claim)

Hash: `f44280ccc951`

Fields: relation, evidence[0], evidence[1]

```yaml
id: clm:sdpa-is-a-attention
predicate: IS_A
subject: method:scaled-dot-product-attention
object: concept:attention-mechanism
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    section: 3.2 Attention
    paragraph: 1
    html_id: S3.SS2.p1
  quote: An attention function can be described as mapping a query and a set of key-value
    pairs to an output, where the query, keys, values, and output are all vectors.
  type: author_statement
  stance: supports
  source_detail: &id001
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
- source: src:arxiv:1706.03762v7
  locator:
    section: 3.2.1 Scaled Dot-Product Attention
    paragraph: 1
    html_id: S3.SS2.SSS1.p1
  quote: We call our particular attention "Scaled Dot-Product Attention" (Figure 2).
  type: author_statement
  stance: supports
  source_detail: *id001
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Scaled Dot-Product Attention
object_name: Attention 메커니즘
predicate_meaning: 더 일반적인 개념의 한 종류다.
```

## clm:scaled-dot-product-attention-part-of-multi-head-attention (claim)

Hash: `a2b3d602402a`

Fields: relation, evidence[0], evidence[1]

```yaml
id: clm:scaled-dot-product-attention-part-of-multi-head-attention
predicate: PART_OF
subject: method:scaled-dot-product-attention
object: method:multi-head-attention
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    figure: 2
    part: caption
    html_id: S3.F2
  quote: (left) Scaled Dot-Product Attention. (right) Multi-Head Attention consists
    of several attention layers running in parallel.
  type: author_statement
  stance: supports
  source_detail: &id001
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
- source: src:arxiv:1706.03762v7
  locator:
    section: 3.2.2 Multi-Head Attention
    paragraph: 1
  quote: On each of these projected versions of queries, keys and values we then perform
    the attention function in parallel, yielding
  type: author_statement
  stance: supports
  source_detail: *id001
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Scaled Dot-Product Attention
object_name: Multi-Head Attention
predicate_meaning: 전체를 이루는 구성 요소다.
```

## clm:multi-head-attention-part-of-transformer-encoder-layer (claim)

Hash: `58182b57a329`

Fields: relation, evidence[0]

```yaml
id: clm:multi-head-attention-part-of-transformer-encoder-layer
predicate: PART_OF
subject: method:multi-head-attention
object: method:transformer-encoder-layer
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    section: '3.1 Encoder and Decoder Stacks — Encoder:'
    paragraph: 1
    html_id: S3.SS1.SSS0.Px1.p1
  quote: Each layer has two sub-layers. The first is a multi-head self-attention mechanism,
    and the second is a simple, position-wise fully connected feed-forward network.
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Multi-Head Attention
object_name: Transformer 인코더 층
predicate_meaning: 전체를 이루는 구성 요소다.
```

## clm:transformer-encoder-layer-part-of-bert (claim)

Hash: `89580a18c6ce`

Fields: relation, evidence[0]

```yaml
id: clm:transformer-encoder-layer-part-of-bert
predicate: PART_OF
subject: method:transformer-encoder-layer
object: model:bert
status: verified
confidence: high
evidence:
- source: src:arxiv:1810.04805v2
  locator:
    section: 3 BERT — Model Architecture
    paragraph: 1
    html_id: S3.SS0.SSS0.Px1.p1
  quote: BERT’s model architecture is a multi-layer bidirectional Transformer encoder
    based on the original implementation described in Vaswani et al. (2017) and released
    in the tensor2tensor library.
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:1810.04805v2
    name: arXiv 1810.04805v2
    kind: paper_version
    paper: paper:devlin2018-bert
    url: https://arxiv.org/abs/1810.04805v2
    fulltext_url: https://arxiv.org/html/1810.04805v2
    version: 1810.04805v2
    retrieved_at: '2026-10-15'
    content_sha256: 132175f3436252c09af7d093258764a3c4dbd16be2be2e3c4369d9b01ba2bfa5
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Transformer 인코더 층
object_name: BERT
predicate_meaning: 전체를 이루는 구성 요소다.
```

## clm:transformer-encoder-layer-part-of-vit (claim)

Hash: `5693bdeb1131`

Fields: relation, evidence[0]

```yaml
id: clm:transformer-encoder-layer-part-of-vit
predicate: PART_OF
subject: method:transformer-encoder-layer
object: model:vit
status: verified
confidence: high
evidence:
- source: src:arxiv:2010.11929v2
  locator:
    section: 3.1 Vision Transformer (ViT)
    paragraph: 4
  quote: The Transformer encoder (Vaswani et al., 2017) consists of alternating layers
    of multiheaded self-attention (MSA, see Appendix A) and MLP blocks (Eq. 2, 3).
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:2010.11929v2
    name: arXiv 2010.11929v2
    kind: paper_version
    paper: paper:dosovitskiy2020-vit
    url: https://arxiv.org/abs/2010.11929v2
    fulltext_url: https://arxiv.org/html/2010.11929v2
    version: 2010.11929v2
    retrieved_at: '2026-10-15'
    content_sha256: 709184b1f6f5be852b85adad72d14c9999d55bee635d77db88e5497cbd888a8e
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Transformer 인코더 층
object_name: Vision Transformer
predicate_meaning: 전체를 이루는 구성 요소다.
```

## clm:transformer-addresses-sequential (claim)

Hash: `a23252b197b5`

Fields: relation, evidence[0], evidence[1]

```yaml
id: clm:transformer-addresses-sequential
predicate: ADDRESSES
subject: model:transformer
object: problem:sequential-computation-in-rnns
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    section: 1 Introduction
    paragraph: 4
    html_id: S1.p4.1
  quote: In this work we propose the Transformer, a model architecture eschewing recurrence
    and instead relying entirely on an attention mechanism to draw global dependencies
    between input and output.
  type: author_statement
  stance: supports
  source_detail: &id001
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
- source: src:arxiv:1706.03762v7
  locator:
    section: 1 Introduction
    paragraph: 2
    html_id: S1.p2
  quote: This inherently sequential nature precludes parallelization within training
    examples, which becomes critical at longer sequence lengths, as memory constraints
    limit batching across examples.
  type: author_statement
  stance: supports
  source_detail: *id001
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
note: '감사 F-02/F-03(2026-10-15): 술어를 직접 뒷받침하는 인용으로 교체·보강.'
subject_name: Transformer
object_name: RNN의 순차 계산
predicate_meaning: 연구 문제를 해결 대상으로 삼는다.
```

## clm:transformer-mitigates-sequential (claim)

Hash: `318fcd9afb24`

Fields: relation, evidence[0]

```yaml
id: clm:transformer-mitigates-sequential
predicate: MITIGATES
subject: model:transformer
object: problem:sequential-computation-in-rnns
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:1706.03762v7
  locator:
    section: 4 Why Self-Attention
    paragraph: 4
    html_id: S4.p4
  quote: As noted in Table 1, a self-attention layer connects all positions with a
    constant number of sequentially executed operations, whereas a recurrent layer
    requires
  type: analytical_result
  stance: supports
  source_detail:
    id: src:arxiv:1706.03762v7
    name: arXiv 1706.03762v7
    kind: paper_version
    paper: paper:vaswani2017-transformer
    url: https://arxiv.org/abs/1706.03762v7
    fulltext_url: https://arxiv.org/html/1706.03762v7
    version: 1706.03762v7
    retrieved_at: '2026-10-15'
    content_sha256: fe1288e9c6f8322156429ab44bf5ced203155f8ecc7ea9fe6cfd125872c72a3b
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Transformer
object_name: RNN의 순차 계산
predicate_meaning: 문제의 영향을 완화한다.
```

## clm:intro-additive-attention (claim)

Hash: `6d46a79928cb`

Fields: relation, evidence[0]

```yaml
id: clm:intro-additive-attention
predicate: INTRODUCES
subject: paper:bahdanau2014-attention
object: method:additive-attention
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:1409.0473v7
  locator:
    section: 1 Introduction
    paragraph: 4
    html_id: S1.p4
  quote: In order to address this issue, we introduce an extension to the encoder–decoder
    model which learns to align and translate jointly.
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:1409.0473v7
    name: arXiv 1409.0473v7
    kind: paper_version
    paper: paper:bahdanau2014-attention
    url: https://arxiv.org/abs/1409.0473v7
    fulltext_url: https://arxiv.org/html/1409.0473v7
    version: 1409.0473v7
    retrieved_at: '2026-10-15'
    content_sha256: 495bf11cf1d6053a2a1314f208010597b56efb2557e9e7408845b28eb646b741
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: null
object_name: Additive Attention
predicate_meaning: 논문이 방법·모델·데이터셋을 제시한다.
```

## clm:vit-adapts-transformer (claim)

Hash: `af3acc8c5d8c`

Fields: relation, evidence[0], evidence[1]

```yaml
id: clm:vit-adapts-transformer
predicate: ADAPTS
subject: model:vit
object: model:transformer
qualifiers:
  from_field: field:natural-language-processing
  to_field: field:computer-vision
status: verified
confidence: medium
evidence:
- source: src:arxiv:2010.11929v2
  locator:
    section: 1 Introduction
    paragraph: 3
    html_id: S1.p3.1
  quote: Inspired by the Transformer scaling successes in NLP, we experiment with
    applying a standard Transformer directly to images, with the fewest possible modifications.
  type: author_statement
  stance: supports
  source_detail: &id001
    id: src:arxiv:2010.11929v2
    name: arXiv 2010.11929v2
    kind: paper_version
    paper: paper:dosovitskiy2020-vit
    url: https://arxiv.org/abs/2010.11929v2
    fulltext_url: https://arxiv.org/html/2010.11929v2
    version: 2010.11929v2
    retrieved_at: '2026-10-15'
    content_sha256: 709184b1f6f5be852b85adad72d14c9999d55bee635d77db88e5497cbd888a8e
- source: src:arxiv:2010.11929v2
  locator:
    section: 3 Method
    paragraph: 1
  quote: In model design we follow the original Transformer (Vaswani et al., 2017)
    as closely as possible.
  type: author_statement
  stance: supports
  source_detail: *id001
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
note: '감사 F-02/F-03(2026-10-15): 술어를 직접 뒷받침하는 인용으로 교체·보강.'
subject_name: Vision Transformer
object_name: Transformer
predicate_meaning: 한 분야의 설계를 다른 분야에 적용한다.
```

## clm:swin-mitigates-quadratic (claim)

Hash: `815792d707fc`

Fields: relation, evidence[0]

```yaml
id: clm:swin-mitigates-quadratic
predicate: MITIGATES
subject: model:swin
object: problem:quadratic-attention-cost-high-resolution
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:2103.14030v2
  locator:
    section: 1 Introduction
    paragraph: 3
  quote: The linear computational complexity is achieved by computing self-attention
    locally within non-overlapping windows that partition an image (outlined in red).
    The number of patches in each window is fixed, and thus the complexity becomes
    linear to image size.
  type: analytical_result
  stance: supports
  source_detail:
    id: src:arxiv:2103.14030v2
    name: arXiv 2103.14030v2
    kind: paper_version
    paper: paper:liu2021-swin
    url: https://arxiv.org/abs/2103.14030v2
    fulltext_url: https://arxiv.org/html/2103.14030v2
    version: 2103.14030v2
    retrieved_at: '2026-10-15'
    content_sha256: 0af9b806a1e6ab1872c0843f70b071967f92b2a9c21f6c59a2446bfb530c0262
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: Swin Transformer
object_name: 고해상도에서 attention의 이차 비용
predicate_meaning: 문제의 영향을 완화한다.
```

## clm:intro-shifted-window (claim)

Hash: `f10e4ecf4504`

Fields: relation, evidence[0]

```yaml
id: clm:intro-shifted-window
predicate: INTRODUCES
subject: paper:liu2021-swin
object: method:shifted-window-attention
qualifiers: {}
status: verified
confidence: high
evidence:
- source: src:arxiv:2103.14030v2
  locator:
    section: 3.2 Shifted Window based Self-Attention
    paragraph: 3
  quote: To introduce cross-window connections while maintaining the efficient computation
    of non-overlapping windows, we propose a shifted window partitioning approach
    which alternates between two partitioning configurations in consecutive Swin Transformer
    blocks.
  type: author_statement
  stance: supports
  source_detail:
    id: src:arxiv:2103.14030v2
    name: arXiv 2103.14030v2
    kind: paper_version
    paper: paper:liu2021-swin
    url: https://arxiv.org/abs/2103.14030v2
    fulltext_url: https://arxiv.org/html/2103.14030v2
    version: 2103.14030v2
    retrieved_at: '2026-10-15'
    content_sha256: 0af9b806a1e6ab1872c0843f70b071967f92b2a9c21f6c59a2446bfb530c0262
verification:
  method: quote_match
  by: agent:claude-opus-5-5
  at: '2026-10-15'
subject_name: null
object_name: Shifted Window Attention
predicate_meaning: 논문이 방법·모델·데이터셋을 제시한다.
```

## concept:attention-mechanism (entity)

Hash: `0527334fba60`

Fields: name, summary, aliases, classification

```yaml
id: concept:attention-mechanism
name: Attention 메커니즘
summary: 출력의 각 위치가 입력의 여러 위치를 서로 다른 비중으로 참고하도록, 관련도 점수로 가중합을 만드는 신경망 구성 방식이다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
aliases:
- attention mechanism
- attention
- 어텐션
- 어텐션 메커니즘
fields:
- field:deep-learning
```

## method:additive-attention (entity)

Hash: `84e3940a7fb5`

Fields: name, summary, aliases, classification

```yaml
id: method:additive-attention
name: Additive Attention
summary: query와 key를 작은 피드포워드 신경망에 함께 넣어 점수를 계산하는 attention으로, Bahdanau 등의 신경망 기계
  번역 논문에서 제안되었다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- derive
aliases:
- Bahdanau attention
- additive attention
fields:
- field:machine-translation
- field:deep-learning
```

## method:multi-head-attention (entity)

Hash: `7ff50f3c04b9`

Fields: name, summary, aliases, classification

```yaml
id: method:multi-head-attention
name: Multi-Head Attention
summary: attention을 서로 다른 선형 투영 공간에서 여러 개 나란히 계산한 뒤 이어 붙이고 학습된 행렬로 한 번 더 투영해, 여러 종류의
  관계를 동시에 보도록 한 방법이다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- implement
estimated_minutes:
  explain: 25
aliases:
- multi-head attention
- MHA
- 멀티헤드 어텐션
fields:
- field:deep-learning
key_terms:
- multi-head self-attention
```

## method:scaled-dot-product-attention (entity)

Hash: `baeb486b2395`

Fields: name, summary, aliases, formula, classification

```yaml
id: method:scaled-dot-product-attention
name: Scaled Dot-Product Attention
summary: query와 key의 내적을 √d_k로 나눈 뒤 softmax로 가중치를 구해 value를 섞는 attention 연산으로, Transformer의
  기본 부품이다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- derive
- implement
formula: \mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V
estimated_minutes:
  explain: 25
  derive: 30
aliases:
- scaled dot-product attention
- SDPA
fields:
- field:deep-learning
```

## method:shifted-window-attention (entity)

Hash: `eee77ca83220`

Fields: name, summary, aliases, classification

```yaml
id: method:shifted-window-attention
name: Shifted Window Attention
summary: 이미지를 겹치지 않는 창으로 나눠 창 안에서만 self-attention을 계산하고, 연속한 두 블록에서 일반 창과 창 크기의 절반만큼
  옮긴 창을 번갈아 써서 창 사이를 연결하는 방법이다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
aliases:
- shifted window attention
- shifted windows
fields:
- field:vision-transformers
- field:efficient-transformers
```

## method:transformer-encoder-layer (entity)

Hash: `038413779a67`

Fields: name, summary, aliases, classification

```yaml
id: method:transformer-encoder-layer
name: Transformer 인코더 층
summary: multi-head self-attention과 위치별 피드포워드 네트워크를 잔차 연결과 층 정규화로 감싼 블록으로, Transformer
  인코더·BERT·ViT가 이 블록을 쌓아 만든다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- implement
aliases:
- Transformer encoder layer
- Transformer block
fields:
- field:deep-learning
key_terms:
- Transformer encoder
```

## model:bert (entity)

Hash: `7da10bbb02f6`

Fields: name, summary, variants, classification

```yaml
id: model:bert
name: BERT
summary: 양방향 Transformer 인코더를 마스크 언어 모델과 다음 문장 예측으로 사전학습한 뒤 여러 언어 과제에 미세조정하는 모델이다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
variants:
- BERT-Base
- BERT-Large
fields:
- field:language-modeling
```

## model:swin (entity)

Hash: `48112c5b449a`

Fields: name, summary, aliases, variants, classification

```yaml
id: model:swin
name: Swin Transformer
summary: 창 단위 attention과 창 이동, 계층적 특징 맵으로 이미지 크기에 선형인 계산량을 가지는 비전 Transformer다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
variants:
- Swin-T
- Swin-S
- Swin-B
- Swin-L
aliases:
- Swin
fields:
- field:vision-transformers
```

## model:transformer (entity)

Hash: `1b924c0e3294`

Fields: name, summary, aliases, variants, classification

```yaml
id: model:transformer
name: Transformer
summary: 순환과 합성곱 없이 attention만으로 만든 인코더–디코더 시퀀스 변환(sequence transduction) 모델로, WMT
  2014 영어–독일어·영어–프랑스어 번역과 English constituency parsing에서 평가되었다.
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
variants:
- base
- big
aliases:
- 트랜스포머
fields:
- field:machine-translation
- field:deep-learning
```

## model:vit (entity)

Hash: `307cb2176af7`

Fields: name, summary, aliases, variants, classification

```yaml
id: model:vit
name: Vision Transformer
summary: '이미지를 고정 크기 패치(예: 16×16)의 시퀀스로 바꿔 표준 Transformer 인코더로 처리하는 이미지 분류 모델이다.'
summary_by: agent:claude-opus-5-5
dimensions:
- recognize
- explain
- analyze
variants:
- ViT-B/16
- ViT-L/16
- ViT-H/14
aliases:
- ViT
- 비전 트랜스포머 모델
fields:
- field:vision-transformers
- field:image-classification
```

## paper:bahdanau2014-attention (entity)

Hash: `a83e0fa1c109`

Fields: classification, metadata

```yaml
id: paper:bahdanau2014-attention
title: Neural Machine Translation by Jointly Learning to Align and Translate
authors:
- Dzmitry Bahdanau
- Kyunghyun Cho
- Yoshua Bengio
earliest_public_date: '2014-09-01'
venue: ICLR 2015 (oral presentation)
identifiers:
  arxiv: '1409.0473'
  arxiv_doi: 10.48550/arXiv.1409.0473
  openalex:
  - W2133564696
metadata_checked:
  arxiv: '2026-10-15'
  openalex: '2026-10-15'
fields:
- field:machine-translation
```

## paper:liu2021-swin (entity)

Hash: `754ed3d85f94`

Fields: classification, metadata

```yaml
id: paper:liu2021-swin
title: 'Swin Transformer: Hierarchical Vision Transformer using Shifted Windows'
authors:
- Ze Liu
- Yutong Lin
- Yue Cao
- Han Hu
- Yixuan Wei
- Zheng Zhang
- Stephen Lin
- Baining Guo
earliest_public_date: '2021-03-25'
venue: ICCV 2021
identifiers:
  doi: 10.1109/ICCV48922.2021.00986
  arxiv: '2103.14030'
  arxiv_doi: 10.48550/arXiv.2103.14030
  openalex:
  - W3138516171
metadata_checked:
  arxiv: '2026-10-15'
  openalex: '2026-10-15'
fields:
- field:vision-transformers
```

## paper:vaswani2017-transformer (entity)

Hash: `1aaa1bc96f41`

Fields: classification, metadata

```yaml
id: paper:vaswani2017-transformer
title: Attention Is All You Need
authors:
- Ashish Vaswani
- Noam Shazeer
- Niki Parmar
- Jakob Uszkoreit
- Llion Jones
- Aidan N. Gomez
- Łukasz Kaiser
- Illia Polosukhin
earliest_public_date: '2017-06-12'
venue: 'NIPS 2017 (now NeurIPS): Advances in Neural Information Processing Systems
  30, pp. 5998–6008'
identifiers:
  arxiv: '1706.03762'
  arxiv_doi: 10.48550/arXiv.1706.03762
  openalex:
  - W2626778328
metadata_checked:
  arxiv: '2026-10-15'
  openalex: '2026-10-15'
fields:
- field:machine-translation
- field:deep-learning
```

## problem:quadratic-attention-cost-high-resolution (entity)

Hash: `072f6b869f7f`

Fields: name, summary, aliases, question, classification

```yaml
id: problem:quadratic-attention-cost-high-resolution
name: 고해상도에서 attention의 이차 비용
summary: 전역 self-attention의 계산량이 토큰 수의 제곱에 비례해, 고해상도 이미지나 밀집 예측 과제에서 비용이 너무 커지는 문제다.
summary_by: agent:claude-opus-5-5
question: 고해상도 이미지에서 attention 계산량을 이미지 크기에 선형으로 줄일 수 있는가?
aliases:
- quadratic attention cost
fields:
- field:vision-transformers
- field:efficient-transformers
```

## problem:sequential-computation-in-rnns (entity)

Hash: `f74bfe01289a`

Fields: name, summary, aliases, question, classification

```yaml
id: problem:sequential-computation-in-rnns
name: RNN의 순차 계산
summary: 순환 신경망은 시간 단계마다 이전 상태가 필요해 한 학습 예제 안에서 병렬 계산이 어렵다는 문제다.
summary_by: agent:claude-opus-5-5
question: 순서대로 계산하지 않고도 시퀀스를 모델링할 수 있는가?
aliases:
- sequential computation
fields:
- field:natural-language-processing
```

## field:artificial-intelligence (entity)

Hash: `d2afe7d82b28`

Fields: name, summary

```yaml
id: field:artificial-intelligence
name: 인공지능
summary: 지각·추론·학습·언어 같은 지적 능력을 계산으로 구현하는 방법을 연구하는 분야다.
summary_by: agent:claude-opus-5-5
parents: []
external_ids:
  openalex: https://openalex.org/subfields/1702
```

## field:computer-vision (entity)

Hash: `d7a831313663`

Fields: name, summary, classification

```yaml
id: field:computer-vision
name: 컴퓨터 비전
summary: 이미지와 영상에서 물체·장면·움직임 같은 정보를 인식하고 이해하는 방법을 연구하는 분야다.
summary_by: agent:claude-opus-5-5
parents:
- field:artificial-intelligence
external_ids:
  openalex: https://openalex.org/subfields/1707
```

## field:deep-learning (entity)

Hash: `552bc8c70ab5`

Fields: name, summary, classification

```yaml
id: field:deep-learning
name: 딥러닝
summary: 여러 층으로 쌓은 신경망으로 데이터의 표현을 단계적으로 학습하는 기계학습 방법을 다룬다.
summary_by: agent:claude-opus-5-5
parents:
- field:machine-learning
```

## field:efficient-transformers (entity)

Hash: `c9cdbf805250`

Fields: name, summary, classification

```yaml
summary_by: agent:codex
id: field:efficient-transformers
name: Efficient Transformers
summary: Efficient Transformers는 긴 입력에서 어텐션 계산 비용을 낮추는 구조를 연구하는 분야이다.
parents:
- field:ml-systems-efficient-inference
- field:deep-learning
```

## field:image-classification (entity)

Hash: `1918a2e74bbd`

Fields: name, summary, classification

```yaml
id: field:image-classification
name: 이미지 분류
summary: 이미지 한 장 전체에 미리 정한 범주 중 하나를 붙이는 과제다.
summary_by: agent:claude-opus-5-5
parents:
- field:computer-vision
```

## field:language-modeling (entity)

Hash: `1cb173641a0b`

Fields: name, summary, aliases, classification

```yaml
summary_by: agent:codex
id: field:language-modeling
name: 언어 모델링
aliases:
- Language Modeling
- LM
summary: 언어 모델링은 텍스트의 확률 구조를 학습하는 분야로, 앞 문맥으로 다음 토큰을 예측하는 자기회귀 방식과 가려진 토큰을 양쪽 문맥으로
  예측하는 마스크 언어 모델 방식을 포함한다.
parents:
- field:natural-language-processing
```

## field:machine-learning (entity)

Hash: `503cbed2a309`

Fields: name, summary, classification

```yaml
id: field:machine-learning
name: 기계학습
summary: 명시적인 규칙 대신 데이터에서 패턴을 학습해 예측이나 결정을 하는 알고리즘을 연구하는 인공지능의 한 분야다.
summary_by: agent:claude-opus-5-5
parents:
- field:artificial-intelligence
```

## field:machine-translation (entity)

Hash: `64fd86af742e`

Fields: name, summary, classification

```yaml
id: field:machine-translation
name: 기계 번역
summary: 한 언어의 문장을 다른 언어의 같은 뜻 문장으로 자동 번역하는 과제다.
summary_by: agent:claude-opus-5-5
parents:
- field:natural-language-processing
```

## field:ml-systems-efficient-inference (entity)

Hash: `8f7a7505f510`

Fields: name, summary, aliases, classification

```yaml
summary_by: agent:codex
id: field:ml-systems-efficient-inference
name: ML Systems and Efficient Inference
aliases:
- ML Systems
- Efficient Inference
summary: ML Systems and Efficient Inference는 모델 학습과 배포의 계산 및 메모리 효율을 연구하는 분야이다.
parents:
- field:machine-learning
```

## field:natural-language-processing (entity)

Hash: `109a86d9ffc5`

Fields: name, summary, classification

```yaml
id: field:natural-language-processing
name: 자연어 처리
summary: 사람의 언어로 된 텍스트와 음성을 컴퓨터가 이해하고 생성하도록 하는 방법을 연구하는 분야다.
summary_by: agent:claude-opus-5-5
parents:
- field:artificial-intelligence
external_ids:
  openalex: https://openalex.org/T10181
```

## field:vision-transformers (entity)

Hash: `2bf61d894410`

Fields: name, summary, classification

```yaml
id: field:vision-transformers
name: 비전 트랜스포머
summary: 이미지를 패치 시퀀스로 바꿔 Transformer의 self-attention으로 처리하는 비전 모델 계열을 다룬다.
summary_by: agent:claude-opus-5-5
parents:
- field:computer-vision
- field:deep-learning
```

## lab:softmax-temperature (entity)

Hash: `27d7d3b26c2b`

Fields: name, parameters, demonstrates

```yaml
id: lab:softmax-temperature
name: Softmax Temperature & Scaled Dot-Product Lab
component: softmax-temperature
version: 1
parameters:
- name: T
  min: 0.05
  max: 5
  step: 0.001
  default: 1
  scale: log
- name: d_k
  min: 1
  max: 1024
  default: 64
  choices:
  - 1
  - 4
  - 16
  - 64
  - 256
  - 512
  - 1024
- name: n_keys
  min: 8
  max: 8
  step: 1
  default: 8
- name: seed
  min: 0
  max: 4294967295
  step: 1
  default: 42
demonstrates:
- unit: concept:softmax
  dimensions:
  - explain
- unit: concept:softmax-temperature
  dimensions:
  - explain
- unit: concept:variance-of-sum
  dimensions:
  - explain
- unit: method:scaled-dot-product-attention
  dimensions:
  - derive
items:
- ai:lab-softmax-temp-01
- ai:lab-softmax-temp-02
- ai:lab-sdpa-01
- ai:lab-sdpa-02
reference_impl: tools/gen_lab_fixtures.py
```

## ai:lab-softmax-temp-01 (item)

Hash: `2a8329962e66`

Fields: prompt, answer, choices, rationale

```yaml
id: ai:lab-softmax-temp-01
assesses:
  unit: concept:softmax-temperature
  dimension: explain
kind: lab_prediction
prompt: z = [2, 1, 0]에서 T를 1에서 0.1로 낮추면 가장 큰 확률은?
choices:
- 커진다
- 작아진다
- 그대로다
answer: 0
rationale: '0.665 → 0.99995: 온도를 낮추면 분포가 argmax로 몰린다'
lab: lab:softmax-temperature
scenario:
  logits:
  - 2
  - 1
  - 0
  T_from: 1
  T_to: 0.1
```

## ai:lab-softmax-temp-02 (item)

Hash: `08febb51ac94`

Fields: prompt, answer, tolerance, rationale

```yaml
id: ai:lab-softmax-temp-02
assesses:
  unit: concept:softmax-temperature
  dimension: explain
kind: lab_prediction
prompt: z = [2, 0], T = 2일 때 첫 번째 확률은?
answer: 0.731
tolerance: 0.005
rationale: e¹/(e¹+1) ≈ 0.731
lab: lab:softmax-temperature
scenario:
  logits:
  - 2
  - 0
  T: 2
verified_by: computation
```

## ai:lab-sdpa-01 (item)

Hash: `d4dcfe67c198`

Fields: prompt, answer, choices, rationale

```yaml
id: ai:lab-sdpa-01
assesses:
  unit: method:scaled-dot-product-attention
  dimension: derive
kind: lab_prediction
prompt: scaling 없이 d_k를 4에서 512로 키우면 평균 최대 attention 가중치는?
choices:
- 1에 가까워진다(포화)
- 0에 가까워진다
- 변하지 않는다
answer: 0
rationale: 0.525 → 0.955 (seed 42, 표본 1,000)
lab: lab:softmax-temperature
scenario:
  scaled: false
  d_k_from: 4
  d_k_to: 512
  n_keys: 8
```

## ai:lab-sdpa-02 (item)

Hash: `adb35e295077`

Fields: prompt, answer, tolerance, rationale

```yaml
id: ai:lab-sdpa-02
assesses:
  unit: concept:variance-of-sum
  dimension: explain
kind: lab_prediction
prompt: q, k의 성분이 서로 독립이고 평균 0, 분산 1이다. d_k = 64일 때 q·k의 표준편차는?
answer: 8
tolerance: 0.5
rationale: √64 = 8 (seed 42, 표본 10,000에서 Var 64.65)
lab: lab:softmax-temperature
scenario:
  d_k: 64
verified_by: computation
```

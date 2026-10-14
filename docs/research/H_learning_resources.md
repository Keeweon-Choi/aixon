# H. 학습 리소스 조사: AIXON 선수지식 경로 (설계 단계)

- 확인일: **2026-10-15**. 표와 노트에 적은 URL은 모두 이날 직접 열어 확인했다(각 항목에 "확인 2026-10-15" 표기).
- 범위: 27개 단위, 단위마다 1–3개의 무료 리소스(표 78행, 서로 다른 리소스 약 50개).
- 역량 차원(AIXON `LearningResource` ↔ concept 링크용):
  - **recognize**: 식별하고 정의할 수 있다.
  - **explain**: 원리와 이유를 개념적으로 설명할 수 있다.
  - **derive**: 수식을 직접 전개할 수 있다.
  - **implement**: 코드로 구현하거나 계산할 수 있다.
  - **analyze**: 적용·비교·비판할 수 있다.

---

## 0. 조사·검증 방법

1. 웹 페이지는 `curl`로 HTML 원문을 받아 `<title>`, h1–h4 제목, 앵커 `id`, 본문 문장을 직접 대조했다. 표에 적은 딥링크 앵커(`#...`)는 모두 해당 HTML에 `id`로 실제 존재하는 것만 썼다.
2. 논문은 arXiv abs 페이지에서 제목, 저자, 라이선스 링크, 최신 버전을 확인했다. 이어서 arXiv PDF 텍스트를 추출(pypdf, 파일로 저장하지 않고 파이프로 처리)하거나 ar5iv HTML(`https://ar5iv.labs.arxiv.org/html/<id>`)로 절 번호, 식, 각주를 대조했다.
   - ar5iv는 arXiv Labs의 HTML 렌더링이다. 각주 번호가 PDF와 다를 수 있다. 예: Vaswani 등의 "각주 4"는 PDF v7 기준 번호다.
3. 길이 표기 기준은 세 가지다.
   - "(명시)": 페이지에 직접 적혀 있는 값.
   - "(YouTube 메타데이터)": 3Blue1Brown 영상의 YouTube 페이지 `lengthSeconds` 값.
   - "(추정)": 본문 단어 수(코드 블록 제외)나 PDF 쪽수로 계산한 값.
4. d2l.ai의 절 번호는 현재 배포본 **"Dive into Deep Learning 1.0.3"**(페이지 `<title>`)을 기준으로 했다.
   - ko.d2l.ai는 구판(MXNet/Gluon 기반) 번역이라 절 번호가 다르다. 기록용 링크는 영문판을 쓴다.
5. deeplearningbook.org는 절 단위 앵커가 없다. 그래서 "장 URL + 절 번호(인쇄본 쪽, TOC 기준)"로 적었다.

## 1. 출처별 공통 정보 (저자·발행처·라이선스)

| 출처 | 저자/발행 | 라이선스 (확인 근거) | 비고 |
|---|---|---|---|
| d2l.ai: *Dive into Deep Learning* 1.0.3 | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola. 인쇄본은 Cambridge University Press | 본문 **CC BY-SA 4.0**, 샘플 코드 **수정 MIT**(LICENSE-SAMPLECODE). 근거: GitHub README "License Summary" (https://github.com/d2l-ai/d2l-en, 확인 2026-10-15) | 절마다 PyTorch / MXNet / JAX / TensorFlow 탭이 있다. 14.2 등 일부 절은 PyTorch·MXNet만 있다 |
| CS231n course notes (cs231n.github.io) | Stanford CS231n. 노트 문의처로 Andrej Karpathy 명시 | 노트 페이지에는 라이선스 표기가 없다. 저장소 LICENSE는 **MIT**("Copyright (c) 2015 Andrej Karpathy", https://github.com/cs231n/cs231n.github.io, 확인 2026-10-15) | — |
| deeplearningbook.org: *Deep Learning* | Ian Goodfellow, Yoshua Bengio, Aaron Courville. MIT Press, 2016 | **오픈 라이선스 아님.** 온라인 HTML은 무료다. FAQ: "our contract with MIT Press forbids distribution of too easily copied electronic formats", HTML은 "a sort of weak DRM" (확인 2026-10-15) | 절 앵커 없음 |
| Distill (distill.pub) | 글별 저자 | 글 하단 표기: augmented-rnns(2016)는 **CC BY 2.0**, computing-receptive-fields(2019)는 **CC BY 4.0** | 재사용된 외부 그림은 제외 |
| arXiv 논문 9편 | 논문별 | 9편 모두 abs 페이지 라이선스 링크가 `arxiv.org/licenses/nonexclusive-distrib/1.0/`이다. 즉 **arXiv 비독점 배포 라이선스**이며 오픈 라이선스가 아니다 | 1706.03762 PDF 1쪽에 Google의 표·그림 재사용 허가 문구가 있다(학술·언론 목적, 출처 표기 조건) |
| 3Blue1Brown | Grant Sanderson. 텍스트 각색자는 레슨별로 표기 | **오픈 라이선스 아님.** FAQ: 60초 미만 클립·정지화상은 출처 표기 등을 조건으로 사용 가능, 그 외 용도는 라이선스 문의 (https://www.3blue1brown.com/faq, 확인 2026-10-15) | 영상과 텍스트 각색본을 함께 제공 |
| jalammar.github.io | Jay Alammar | 각 글 하단에 **CC BY-NC-SA 4.0** | Illustrated Transformer 한국어 번역: https://nlpinkorean.github.io/illustrated-transformer/ (원저자 허락을 받은 번역으로 표기되어 있음. 라이선스 표기 없음. 확인 2026-10-15) |
| The Annotated Transformer | Harvard NLP. v2022: Austin Huang, Suraj Subramanian, Jonathan Sum, Khalid Almubarak, Stella Biderman. 원작: Sasha Rush | 페이지 표기 없음. 저장소 LICENSE는 **MIT**("Copyright (c) 2018 Alexander Rush", https://github.com/harvardnlp/annotated-transformer, 확인 2026-10-15) | — |
| PyTorch Tutorials | 튜토리얼별 저자 | 저장소 LICENSE는 **BSD 3-Clause** (https://github.com/pytorch/tutorials, 확인 2026-10-15). 페이지 하단에는 "© PyTorch. Copyright © The Linux Foundation" | `pytorch.org/tutorials/...` 주소는 `docs.pytorch.org/tutorials/...`로 리다이렉트된다 |
| Lil'Log | Lilian Weng | 표기 없음("© 2026 Lil'Log"). 번역은 사전 이메일 요청(FAQ) | — |
| Grinstead & Snell, *Introduction to Probability* | Charles M. Grinstead, J. Laurie Snell (AMS 2판). Peter G. Doyle의 CHANCE Project 판(2006-07-04) | **GNU Free Documentation License** (PDF 1쪽) | 책 전체가 PDF 한 개(518쪽) |
| JMLR / PMLR / NeurIPS Proceedings | 논문별 | JMLR 페이지: "© JMLR 2014". PMLR·NeurIPS 페이지에는 라이선스 표기가 없다(무료 공개) | 절 앵커 없음(PDF) |

---

## 2. 요약 표

> 형식 표기: text = 본문, code = 실행 가능한 코드 포함, video = 영상, paper section = 논문의 특정 절.

| unit | title | URL | section | format | dimensions | license |
|---|---|---|---|---|---|---|
| U01 내적 (dot product)·a | Dot products and duality (Essence of Linear Algebra, Chapter 9) | https://www.3blue1brown.com/lessons/dot-products | Numerical Method / Geometric Interpretation / Duality | video 14:11 + text | recognize, explain | 오픈 라이선스 아님 (3b1b FAQ) |
| U01 내적·b | Dive into Deep Learning — 2.3. Linear Algebra | https://d2l.ai/chapter_preliminaries/linear-algebra.html#dot-products | 2.3.8. Dot Products | text + code | recognize, explain, implement | CC BY-SA 4.0 / 코드 수정 MIT |
| U01 내적·c | Transformers, the tech behind LLMs \| Deep Learning Chapter 5 | https://www.3blue1brown.com/lessons/gpt#dot-product | "Dot Product" 소절 | video + text | explain | 오픈 라이선스 아님 |
| U02 행렬 곱셈·a | Matrix multiplication as composition (Essence of Linear Algebra, Chapter 4) | https://www.3blue1brown.com/lessons/matrix-multiplication | Composition is Multiplication / Noncommutativity / Associativity | video 10:03 + text | explain | 오픈 라이선스 아님 |
| U02 행렬 곱셈·b | Dive into Deep Learning — 2.3. Linear Algebra | https://d2l.ai/chapter_preliminaries/linear-algebra.html#matrixmatrix-multiplication | 2.3.9. Matrix–Vector Products, 2.3.10. Matrix–Matrix Multiplication | text + code | recognize, implement | CC BY-SA 4.0 / 코드 수정 MIT |
| U02 행렬 곱셈·c | Deep Learning — Chapter 2 Linear Algebra | https://www.deeplearningbook.org/contents/linear_algebra.html | 2.2 Multiplying Matrices and Vectors (pp.32–34) | text | recognize, derive | 오픈 라이선스 아님 (무료 HTML) |
| U03 softmax 함수·a | Dive into Deep Learning — 4.1. Softmax Regression | https://d2l.ai/chapter_linear-classification/softmax-regression.html#the-softmax | 4.1.1.2. The Softmax, 4.1.2.2. Softmax and Cross-Entropy Loss | text + code | recognize, explain, derive | CC BY-SA 4.0 / 코드 수정 MIT |
| U03 softmax 함수·b | CS231n — Linear classification: Support Vector Machine, Softmax | https://cs231n.github.io/linear-classify/#softmax | Softmax classifier, Practical issues: Numeric stability (#softmax-stability), SVM vs. Softmax | text | explain, implement, analyze | 페이지 표기 없음, 저장소 MIT |
| U03 softmax 함수·c | Deep Learning — Chapter 6 Deep Feedforward Networks | https://www.deeplearningbook.org/contents/mlp.html | 6.2.2.3 Softmax Units for Multinoulli Output Distributions (+ 4.1 Overflow and Underflow, numerical.html) | text | derive, analyze | 오픈 라이선스 아님 |
| U04 softmax 온도·a | Distilling the Knowledge in a Neural Network | https://arxiv.org/abs/1503.02531 <br> https://ar5iv.labs.arxiv.org/html/1503.02531#S2 | §2 Distillation (식 1), §2.1, §3 | paper section | recognize, derive, analyze | arXiv 비독점 배포 라이선스 |
| U04 softmax 온도·b | Transformers, the tech behind LLMs \| Deep Learning Chapter 5 | https://www.3blue1brown.com/lessons/gpt#softmax | "Softmax" 절 | video 27:14 + text | explain | 오픈 라이선스 아님 |
| U04 softmax 온도·c | Dive into Deep Learning — 4.1. Softmax Regression | https://d2l.ai/chapter_linear-classification/softmax-regression.html#the-softmax | 4.1.1.2 (Boltzmann exp(−E/kT)), 4.1.5. Exercises (온도 문항) | text | recognize, analyze | CC BY-SA 4.0 |
| U05 독립 확률변수 합의 분산 (Bienaymé)·a | Grinstead and Snell's Introduction to Probability (CHANCE Project 판) | https://math.dartmouth.edu/~prob/prob/prob.pdf | §6.2 Variance of Discrete Random Variables, Theorem 6.8·6.9 (PDF 267–268쪽) | text (PDF 교과서) | recognize, derive | GNU FDL |
| U05 Bienaymé·b | Dive into Deep Learning — 22.6. Random Variables | https://d2l.ai/chapter_appendix-mathematics-for-deep-learning/random-variables.html#variances | 22.6.1.5. Variances, 22.6.1.10. Covariance (식 22.6.43–22.6.44) | text + code | recognize, explain | CC BY-SA 4.0 |
| U05 Bienaymé·c | CS231n — Neural Networks Part 2: Setting up the Data and the Loss | https://cs231n.github.io/neural-networks-2/#init | Weight Initialization: "Calibrating the variances with 1/sqrt(n)" | text | derive, analyze | 저장소 MIT |
| U06 토큰/단어 임베딩·a | Transformers, the tech behind LLMs \| Deep Learning Chapter 5 | https://www.3blue1brown.com/lessons/gpt#embedding | Tokens, Embedding (Embedding Matrix / Direction / Dot Product / Beyond words) | video 27:14 + text | recognize, explain | 오픈 라이선스 아님 |
| U06 임베딩·b | The Illustrated Word2vec | https://jalammar.github.io/illustrated-word2vec/ | 전체 (Word Embeddings, Analogies, Skipgram, Negative Sampling, Window Size and Number of Negative Samples) | text + 일러스트 | explain, analyze | CC BY-NC-SA 4.0 |
| U06 임베딩·c | Dive into Deep Learning — 10.7. Sequence-to-Sequence Learning for Machine Translation | https://d2l.ai/chapter_recurrent-modern/seq2seq.html#encoder | 10.7.2. Encoder (embedding layer) | text + code | explain, implement | CC BY-SA 4.0 |
| U07 어텐션 일반·a | Dive into Deep Learning — 11.1. Queries, Keys, and Values | https://d2l.ai/chapter_attention-mechanisms-and-transformers/queries-keys-values.html | 11.1 본문 (식 11.1.1–11.1.3), 11.1.1. Visualization | text + code | recognize, explain | CC BY-SA 4.0 |
| U07 어텐션 일반·b | Attention and Augmented Recurrent Neural Networks | https://distill.pub/2016/augmented-rnns/ | Attentional Interfaces | text + 도식 | explain | CC BY 2.0 |
| U07 어텐션 일반·c | Visualizing A Neural Machine Translation Model (Mechanics of Seq2seq Models With Attention) | https://jalammar.github.io/visualizing-neural-machine-translation-mechanics-of-seq2seq-models-with-attention/#lets-pay-attention-now | "Let's Pay Attention Now" | text + 애니메이션 | explain | CC BY-NC-SA 4.0 |
| U08 가산(Bahdanau) 어텐션·a | Neural Machine Translation by Jointly Learning to Align and Translate | https://arxiv.org/abs/1409.0473 <br> https://ar5iv.labs.arxiv.org/html/1409.0473#S3.SS1 | §3.1 Decoder: General Description (식 4–6), App. A.1.2 Alignment Model | paper section | recognize, derive | arXiv 비독점 배포 라이선스 |
| U08 가산 어텐션·b | Dive into Deep Learning — 11.3. Attention Scoring Functions | https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html#additive-attention | 11.3.4. Additive Attention (+ 11.4. The Bahdanau Attention Mechanism) | text + code | explain, implement | CC BY-SA 4.0 |
| U08 가산 어텐션·c | Attention? Attention! | https://lilianweng.github.io/posts/2018-06-24-attention/#summary | A Family of Attention Mechanisms → Summary (점수 함수 비교표) | text | analyze | 명시 없음 |
| U09 스케일드 내적 어텐션·a | Attention Is All You Need | https://arxiv.org/abs/1706.03762 <br> https://ar5iv.labs.arxiv.org/html/1706.03762#S3.SS2.SSS1 | §3.2.1 Scaled Dot-Product Attention + 각주 4 (PDF v7 p.4) | paper section | recognize, derive, analyze | arXiv 비독점 배포 라이선스 (+ Google 표·그림 허가 문구) |
| U09 스케일드 내적·b | Dive into Deep Learning — 11.3. Attention Scoring Functions | https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html#dot-product-attention | 11.3.1, 11.3.2 (Masked Softmax, Batch Matrix Multiplication), 11.3.3 | text + code | explain, derive, implement | CC BY-SA 4.0 |
| U09 스케일드 내적·c | Attention in transformers, step-by-step \| Deep Learning Chapter 6 | https://www.3blue1brown.com/lessons/attention#the-attention-pattern | The Attention Pattern / Queries / Keys | video 26:09 + text | explain | 오픈 라이선스 아님 |
| U10 멀티헤드 어텐션·a | Attention Is All You Need | https://ar5iv.labs.arxiv.org/html/1706.03762#S3.SS2.SSS2 <br> (abs: https://arxiv.org/abs/1706.03762) | §3.2.2 Multi-Head Attention (+ §3.2.3) | paper section | recognize, derive | arXiv 비독점 배포 라이선스 |
| U10 멀티헤드·b | Dive into Deep Learning — 11.5. Multi-Head Attention | https://d2l.ai/chapter_attention-mechanisms-and-transformers/multihead-attention.html | 11.5.1. Model, 11.5.2. Implementation | text + code | explain, implement | CC BY-SA 4.0 |
| U10 멀티헤드·c | The Illustrated Transformer | https://jalammar.github.io/illustrated-transformer/#the-beast-with-many-heads | "The Beast With Many Heads" | text + 일러스트 | explain | CC BY-NC-SA 4.0 |
| U11 위치 인코딩·a | Attention Is All You Need | https://ar5iv.labs.arxiv.org/html/1706.03762#S3.SS5 | §3.5 Positional Encoding (+ Table 3 row (E)) | paper section | recognize, explain, analyze | arXiv 비독점 배포 라이선스 |
| U11 위치 인코딩·b | Dive into Deep Learning — 11.6. Self-Attention and Positional Encoding | https://d2l.ai/chapter_attention-mechanisms-and-transformers/self-attention-and-positional-encoding.html#positional-encoding | 11.6.3 (11.6.3.1 Absolute / 11.6.3.2 Relative Positional Information) | text + code | explain, derive, implement | CC BY-SA 4.0 |
| U11 위치 인코딩·c | The Illustrated Transformer | https://jalammar.github.io/illustrated-transformer/#representing-the-order-of-the-sequence-using-positional-encoding | "Representing The Order of The Sequence Using Positional Encoding" | text + 일러스트 | explain | CC BY-NC-SA 4.0 |
| U12 Transformer 인코더 층·a | Attention Is All You Need | https://ar5iv.labs.arxiv.org/html/1706.03762#S3.SS1 | §3.1 Encoder and Decoder Stacks ("Encoder:"), §3.3 Position-wise Feed-Forward Networks | paper section | recognize, explain | arXiv 비독점 배포 라이선스 |
| U12 인코더 층·b | Dive into Deep Learning — 11.7. The Transformer Architecture | https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html#encoder | 11.7.1–11.7.4 | text + code | explain, implement | CC BY-SA 4.0 |
| U12 인코더 층·c | The Annotated Transformer | https://nlp.seas.harvard.edu/annotated-transformer/#encoder | Part 1 → Encoder and Decoder Stacks → Encoder | text + code | implement, analyze | 페이지 표기 없음, 저장소 MIT |
| U13 패치 임베딩·ViT·a | An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale | https://arxiv.org/abs/2010.11929 <br> https://ar5iv.labs.arxiv.org/html/2010.11929#S3.SS1 | §3.1 Vision Transformer (ViT), 식 (1)–(4) | paper section | recognize, explain, derive | arXiv 비독점 배포 라이선스 |
| U13 패치 임베딩·ViT·b | Dive into Deep Learning — 11.8. Transformers for Vision | https://d2l.ai/chapter_attention-mechanisms-and-transformers/vision-transformer.html#patch-embedding | 11.8.1–11.8.6 (핵심: 11.8.2. Patch Embedding) | text + code | explain, implement | CC BY-SA 4.0 |
| U14 클래스 토큰 [CLS]·a | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | https://arxiv.org/abs/1810.04805 <br> https://ar5iv.labs.arxiv.org/html/1810.04805#S3 | §3 BERT → "Input/Output Representations" 단락 | paper section | recognize, explain | arXiv 비독점 배포 라이선스 |
| U14 [CLS]·b | An Image is Worth 16x16 Words | https://ar5iv.labs.arxiv.org/html/2010.11929#A4.SS3 <br> (abs: https://arxiv.org/abs/2010.11929) | §3.1의 [class] 토큰 서술 + App. D.3 Head Type and Class Token (Figure 9) | paper section | explain, analyze | arXiv 비독점 배포 라이선스 |
| U14 [CLS]·c | Dive into Deep Learning — 11.8. Transformers for Vision | https://d2l.ai/chapter_attention-mechanisms-and-transformers/vision-transformer.html#putting-it-all-together | 11.8.1. Model, 11.8.4. Putting It All Together | text + code | implement | CC BY-SA 4.0 |
| U15 층 정규화·a | Layer Normalization | https://arxiv.org/abs/1607.06450 <br> https://ar5iv.labs.arxiv.org/html/1607.06450#S3 | §3 Layer normalization (식 3), §5.1 Invariance under weights and data transformations (Table 1) | paper section | recognize, derive, analyze | arXiv 비독점 배포 라이선스 |
| U15 층 정규화·b | Dive into Deep Learning — 8.5. Batch Normalization | https://d2l.ai/chapter_convolutional-modern/batch-norm.html#layer-normalization | 8.5.2.3. Layer Normalization (식 8.5.4–8.5.5) | text | recognize, explain | CC BY-SA 4.0 |
| U15 층 정규화·c | Dive into Deep Learning — 11.7. The Transformer Architecture | https://d2l.ai/chapter_attention-mechanisms-and-transformers/transformer.html#residual-connection-and-layer-normalization | 11.7.3. Residual Connection and Layer Normalization | text + code | implement, analyze | CC BY-SA 4.0 |
| U16 배치 정규화·a | Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift | https://arxiv.org/abs/1502.03167 <br> https://ar5iv.labs.arxiv.org/html/1502.03167#S3 | §3 (Algorithm 1, 역전파 식), §3.1, §3.2 | paper section | recognize, derive, analyze | arXiv 비독점 배포 라이선스 |
| U16 배치 정규화·b | Dive into Deep Learning — 8.5. Batch Normalization | https://d2l.ai/chapter_convolutional-modern/batch-norm.html#batch-normalization-layers | 8.5.1–8.5.6 (특히 8.5.3. Implementation from Scratch, 8.5.6. Discussion) | text + code | explain, implement, analyze | CC BY-SA 4.0 |
| U16 배치 정규화·c | Deep Learning — Chapter 8 Optimization for Training Deep Models | https://www.deeplearningbook.org/contents/optimization.html | 8.7.1 Batch Normalization | text | explain, analyze | 오픈 라이선스 아님 |
| U17 잔차 연결·ResNet·a | Deep Residual Learning for Image Recognition | https://arxiv.org/abs/1512.03385 <br> https://ar5iv.labs.arxiv.org/html/1512.03385#S3.SS1 | §3.1 Residual Learning, §3.2 Identity Mapping by Shortcuts (식 1–2), §3.3, §4.1 | paper section | recognize, explain, analyze | arXiv 비독점 배포 라이선스 |
| U17 잔차 연결·ResNet·b | Dive into Deep Learning — 8.6. Residual Networks (ResNet) and ResNeXt | https://d2l.ai/chapter_convolutional-modern/resnet.html#residual-blocks | 8.6.1. Function Classes, 8.6.2. Residual Blocks, 8.6.3. ResNet Model | text + code | explain, implement | CC BY-SA 4.0 |
| U18 합성곱 층·a | CS231n — Convolutional Neural Networks (CNNs / ConvNets) | https://cs231n.github.io/convolutional-networks/#conv | Convolutional Layer (Convolution Demo, Implementation as Matrix Multiplication 포함) | text + 애니메이션 데모 | explain, derive, analyze | 저장소 MIT |
| U18 합성곱 층·b | Dive into Deep Learning — 7.2. Convolutions for Images | https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html | 7.2.1–7.2.5 | text + code | explain, implement | CC BY-SA 4.0 |
| U18 합성곱 층·c | Deep Learning — Chapter 9 Convolutional Networks | https://www.deeplearningbook.org/contents/convnets.html | 9.1 The Convolution Operation, 9.2 Motivation (pp.327–335) | text | recognize, explain, derive | 오픈 라이선스 아님 |
| U19 수용 영역·a | Computing Receptive Fields of Convolutional Neural Networks | https://distill.pub/2019/computing-receptive-fields/ | Single-path networks, Arbitrary computation graphs, Discussion: receptive fields of modern networks | text + 도식 | derive, analyze | CC BY 4.0 |
| U19 수용 영역·b | Dive into Deep Learning — 7.2. Convolutions for Images | https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html#feature-map-and-receptive-field | 7.2.6. Feature Map and Receptive Field | text | recognize, explain | CC BY-SA 4.0 |
| U19 수용 영역·c | CS231n — Convolutional Neural Networks (ConvNet Architectures) | https://cs231n.github.io/convolutional-networks/#layerpat | Layer Patterns: "Prefer a stack of small filter CONV to one large receptive field CONV layer" | text | analyze | 저장소 MIT |
| U20 귀납적 편향 (CNN vs Transformer)·a | Dive into Deep Learning — 7.1. From Fully Connected Layers to Convolutions | https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html#constraining-the-mlp | 7.1.1. Invariance, 7.1.2 (Translation Invariance, Locality) | text | explain, derive | CC BY-SA 4.0 |
| U20 귀납적 편향·b | Deep Learning — Chapter 9 Convolutional Networks | https://www.deeplearningbook.org/contents/convnets.html | 9.2 Motivation (equivariance), 9.4 Convolution and Pooling as an Infinitely Strong Prior (pp.339–342) | text | recognize, explain, analyze | 오픈 라이선스 아님 |
| U20 귀납적 편향·c | An Image is Worth 16x16 Words | https://ar5iv.labs.arxiv.org/html/2010.11929#S3.SS1.SSS0.Px1 <br> (abs: https://arxiv.org/abs/2010.11929) | §3.1 "Inductive bias." 단락 | paper section | analyze | arXiv 비독점 배포 라이선스 |
| U21 드롭아웃·a | Dive into Deep Learning — 5.6. Dropout | https://d2l.ai/chapter_multilayer-perceptrons/dropout.html | 5.6 도입부 (식 5.6.1), 5.6.1–5.6.3 | text + code | explain, derive, implement | CC BY-SA 4.0 |
| U21 드롭아웃·b | CS231n — Neural Networks Part 2 | https://cs231n.github.io/neural-networks-2/#reg | Regularization → Dropout, Inverted Dropout | text + code | explain, implement | 저장소 MIT |
| U21 드롭아웃·c | Dropout: A Simple Way to Prevent Neural Networks from Overfitting | https://jmlr.org/papers/v15/srivastava14a.html | §4 Model Description, §7 Salient Features, §9 Marginalizing Dropout | paper section | recognize, derive, analyze | © JMLR 2014 (오픈 라이선스 표기 없음) |
| U22 ReLU·a | Dive into Deep Learning — 5.1. Multilayer Perceptrons | https://d2l.ai/chapter_multilayer-perceptrons/mlp.html#relu-function | 5.1.2.1. ReLU Function (식 5.1.4–5.1.5) | text + code | recognize, explain, implement | CC BY-SA 4.0 |
| U22 ReLU·b | CS231n — Neural Networks Part 1: Setting up the Architecture | https://cs231n.github.io/neural-networks-1/#actfun | Commonly used activation functions | text | explain, analyze | 저장소 MIT |
| U22 ReLU·c | ImageNet Classification with Deep Convolutional Neural Networks | https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html | §3.1 ReLU Nonlinearity (Figure 1) | paper section | analyze | 명시 없음 (무료 공개) |
| U23 AlexNet·a | ImageNet Classification with Deep Convolutional Neural Networks | https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html | §3 The Architecture (3.1–3.5), §4 Reducing Overfitting (4.1–4.2), §6 Results | paper section | recognize, explain, analyze | 명시 없음 (무료 공개) |
| U23 AlexNet·b | Dive into Deep Learning — 8.1. Deep Convolutional Neural Networks (AlexNet) | https://d2l.ai/chapter_convolutional-modern/alexnet.html#alexnet | 8.1.1–8.1.3 | text + code | explain, implement | CC BY-SA 4.0 |
| U23 AlexNet·c | CS231n — Convolutional Neural Networks (Case studies) | https://cs231n.github.io/convolutional-networks/#case | Case studies (LeNet / AlexNet / ZF Net / GoogLeNet / VGGNet / ResNet) | text | recognize | 저장소 MIT |
| U24 VGG·a | Very Deep Convolutional Networks for Large-Scale Image Recognition | https://arxiv.org/abs/1409.1556 <br> https://ar5iv.labs.arxiv.org/html/1409.1556#S2 | §2.1 Architecture, §2.2 Configurations (Table 1–2), §2.3 Discussion | paper section | recognize, analyze | arXiv 비독점 배포 라이선스 |
| U24 VGG·b | Dive into Deep Learning — 8.2. Networks Using Blocks (VGG) | https://d2l.ai/chapter_convolutional-modern/vgg.html | 8.2.1–8.2.3 | text + code | explain, implement | CC BY-SA 4.0 |
| U24 VGG·c | CS231n — Convolutional Neural Networks (Case studies) | https://cs231n.github.io/convolutional-networks/#case | "VGGNet in detail" | text | analyze | 저장소 MIT |
| U25 지식 증류 (KD)·a | Distilling the Knowledge in a Neural Network | https://arxiv.org/abs/1503.02531 <br> https://ar5iv.labs.arxiv.org/html/1503.02531#S2 | §2 Distillation, §2.1 Matching logits is a special case of distillation, §3 Preliminary experiments on MNIST | paper section | recognize, explain, derive, analyze | arXiv 비독점 배포 라이선스 |
| U25 지식 증류·b | Knowledge Distillation Tutorial | https://docs.pytorch.org/tutorials/beginner/knowledge_distillation_tutorial.html | Knowledge distillation run / Cosine loss minimization run / Intermediate regressor run | text + code (notebook) | implement, analyze | 저장소 BSD 3-Clause |
| U26 전이학습 (사전학습 + 미세조정)·a | CS231n — Transfer Learning and Fine-tuning Convolutional Neural Networks | https://cs231n.github.io/transfer-learning/ | Transfer Learning (3가지 시나리오, When and how to fine-tune?, Practical advice) | text | explain, analyze | 저장소 MIT |
| U26 전이학습·b | Dive into Deep Learning — 14.2. Fine-Tuning | https://d2l.ai/chapter_computer-vision/fine-tuning.html#steps | 14.2.1. Steps, 14.2.2. Hot Dog Recognition | text + code | explain, implement, analyze | CC BY-SA 4.0 |
| U26 전이학습·c | BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding | https://ar5iv.labs.arxiv.org/html/1810.04805#S3 <br> (abs: https://arxiv.org/abs/1810.04805) | §3 BERT (pre-training / fine-tuning 2단계), §3.1, §3.2 | paper section | recognize, explain | arXiv 비독점 배포 라이선스 |
| U27 기울기 소실·a | Dive into Deep Learning — 5.4. Numerical Stability and Initialization | https://d2l.ai/chapter_multilayer-perceptrons/numerical-stability-and-init.html#vanishing-and-exploding-gradients | 5.4.1 (5.4.1.1–5.4.1.2), 5.4.2.2. Xavier Initialization | text + code | explain, derive, implement | CC BY-SA 4.0 |
| U27 기울기 소실·b | Deep Learning — Chapter 8 Optimization for Training Deep Models | https://www.deeplearningbook.org/contents/optimization.html | 8.2.5 Long-Term Dependencies (+ 10.7 The Challenge of Long-Term Dependencies, rnn.html, pp.396–399) | text | derive | 오픈 라이선스 아님 |
| U27 기울기 소실·c | Understanding the difficulty of training deep feedforward neural networks | https://proceedings.mlr.press/v9/glorot10a.html | §3, §4.2.1 Theoretical Considerations and a New Normalized Initialization, §4.3 | paper section | derive, analyze | 명시 없음 (무료 공개) |

---

## 3. 단위별 노트

> 각 리소스: 저자/발행 · 형식 · 길이 · 라이선스 · 확인일, 이어서 차원별 근거(본문에서 직접 확인한 내용 기준).

### U01 내적 (dot product)

**a. Dot products and duality** (3Blue1Brown, Essence of Linear Algebra Chapter 9)
- 정보: Grant Sanderson. 2016-08-24. 텍스트 각색은 Kurt Bruns & James Schloss.
- 형식·길이: video 14:11 (YouTube 메타데이터) + 텍스트 각색본 약 2,800단어.
- 라이선스: 오픈 라이선스 아님.
- 확인 2026-10-15
- 차원 근거:
  - recognize: "Numerical Method" 절에서 좌표끼리 곱해 더하는 계산으로 내적을 정의한다.
  - explain: "Geometric Interpretation"에서 w를 v 방향 직선에 투영한 길이 × v의 길이로 설명하고, "Order Doesn't Matter"를 다룬다. "Duality"에서는 1×2 행렬(수직선으로 가는 선형변환)과 벡터의 대응을 시각화한다.

**b. D2L 2.3.8 Dot Products**
- 형식·길이: text + code. 해당 소절 약 3–5분 (추정).
- 라이선스: CC BY-SA 4.0 / 코드 수정 MIT.
- 확인 2026-10-15
- 차원 근거:
  - recognize: x^T y = Σ x_i y_i 정의와 ⟨x, y⟩ 표기.
  - explain: 가중합으로 해석하고, 가중치가 비음수이면서 합이 1이면 가중평균, 정규화한 벡터에서는 각도의 코사인이 된다고 설명한다.
  - implement: `torch.dot(x, y)`와 "원소곱 후 sum" 예제가 있다(MXNet/JAX/TF 탭 동일).

**c. 3b1b Deep Learning Chapter 5의 "Dot Product" 소절**
- 형식·길이: 소절 약 300단어, 2분 (추정). 전체 영상은 27:14.
- 확인 2026-10-15
- 차원 근거:
  - explain: 임베딩 공간에서 내적을 "두 벡터가 얼마나 잘 정렬되는가"의 척도로 쓰는 직관을 준다. 이후 attention의 query·key 유사도(U09)로 바로 이어진다.

### U02 행렬 곱셈 (matrix multiplication)

**a. Matrix multiplication as composition** (3b1b, Chapter 4)
- 정보: 2016-08-08. 텍스트 각색은 River Way.
- 형식·길이: video 10:03 (YouTube 메타데이터) + 텍스트 약 2,100단어.
- 확인 2026-10-15
- 차원 근거:
  - explain: 행렬은 기저벡터가 도착하는 위치(열)이고, 행렬곱은 선형변환의 합성이라는 관점을 준다. "Computing the New Matrix"와 "General Form"에서 곱 규칙을 이 관점으로 끌어내고, "Noncommutativity"(전단 변환 예)와 "Associativity"를 합성으로 설명한다.

**b. D2L 2.3.9–2.3.10**
- 형식·길이: text + code. 약 5–8분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: A ∈ R^{n×k}, B ∈ R^{k×m}의 곱 C를 행·열 내적으로 정의한다.
  - implement: `torch.mm(A, B)`와 `A @ B` 예제가 있다.
- 비고: attention 구현으로 이어지는 연결 고리로 **11.3.2.2 Batch Matrix Multiplication**(https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-scoring-functions.html#batch-matrix-multiplication, 확인 2026-10-15)을 함께 연결할 것을 권한다. Q ∈ R^{n×a×b}, K ∈ R^{n×b×c}에 대한 BMM과 `torch.bmm`을 다룬다.

**c. Deep Learning 2.2** (pp.32–34)
- 형식·길이: text. 약 2쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: C_{i,j} = Σ_k A_{i,k} B_{k,j} (식 2.5). 원소곱(Hadamard, A ⊙ B)과 구분하고, 내적 = x^T y이며 C_{i,j}는 A의 i행과 B의 j열의 내적이라고 정리한다.
  - derive: 분배법칙(2.6), 결합법칙(2.7), 비가환성, (AB)^T = B^T A^T (2.9)를 보이고, 이를 이용해 x^T y = y^T x (2.10)를 유도한다.

### U03 softmax 함수

**a. D2L 4.1**
- 형식·길이: text + code. 4.1 전체 약 4,000단어(25–30분), 핵심 소절은 약 10분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: 4.1.1.2에서 softmax 정의, 출력이 비음수이고 합이 1이라는 성질, argmax 불변(식 4.1.4)을 다룬다.
  - explain: 로짓을 확률로 바꾸는 이유와 Gibbs/Boltzmann 기원을 설명한다.
  - derive: 4.1.2.2에서 교차엔트로피와 결합한 손실(식 4.1.9)과, 로짓에 대한 기울기 ∂l/∂o_j = softmax(o)_j − y_j (식 4.1.10)를 유도한다.
- 비고: 구현은 **4.4 Softmax Regression Implementation from Scratch**(https://d2l.ai/chapter_linear-classification/softmax-regression-scratch.html, 확인 2026-10-15)에서 `softmax()`를 직접 작성한다. implement 차원 보강용으로 함께 연결할 것을 권한다.

**b. CS231n linear-classify**
- 형식·길이: text. #softmax, #softmax-stability, #svmvssoftmax 합계 약 1,700단어, 12분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 정규화된 클래스 확률로 해석하는 관점, 정보이론 관점("Information theory view": 교차엔트로피 H(p,q) 최소화), 확률적 해석을 제시한다.
  - implement: log C = −max_j f_j로 이동시키는 안정화 트릭과 numpy 코드(`f -= np.max(f)`)가 있다.
  - analyze: "SVM vs. Softmax"에서 hinge 손실과 교차엔트로피의 행동 차이를 비교한다.

**c. Deep Learning 6.2.2.3** (+ 4.1 Overflow and Underflow, pp.78–80, https://www.deeplearningbook.org/contents/numerical.html, 확인 2026-10-15)
- 형식·길이: text. 약 3–4쪽 (추정).
- 확인 2026-10-15
- 차원 근거:
  - derive: log softmax(z)_i = z_i − log Σ_j exp(z_j) (식 6.30)를 전개한다.
  - analyze:
    - 첫 항은 포화되지 않는다.
    - log Σ exp ≈ max_j z_j 근사로 "음의 로그우도는 가장 활발한 오답을 강하게 벌한다"고 분석한다.
    - 4.1에서는 softmax(z), z = x − max_i x_i로 overflow/underflow를 막는 이유를 설명한다.

### U04 softmax 온도 (temperature)

**a. Hinton, Vinyals & Dean (2015), arXiv 1503.02531 (v1)**
- 형식·길이: PDF 9쪽. §2–§3은 약 2.5쪽 (PDF pp.2–4).
- 확인 2026-10-15
- 차원 근거:
  - recognize: 식 (1) q_i = exp(z_i/T) / Σ_j exp(z_j/T). 원문: "T is a temperature that is normally set to 1. Using a higher value for T produces a softer probability distribution over classes."
  - derive: §2.1에서 ∂C/∂z_i = (1/T)(q_i − p_i) (식 2)로 시작해 고온 근사(식 3)를 거친다. 로짓을 평균 0으로 맞추면 ≈ (1/(NT²))(z_i − v_i) (식 4)가 되어, 고온 극한에서 logit matching과 같아진다.
  - analyze:
    - soft target 기울기는 1/T²로 줄어든다. 그래서 hard target과 함께 쓸 때 T²를 곱해야 한다.
    - §3(MNIST)에서는 은닉층이 층당 300유닛 이상이면 T > 8에서 결과가 비슷했다. 층당 30유닛으로 줄이면 T 2.5–4가 더 좋았다.

**b. 3b1b Chapter 5 "Softmax" 절**
- 정보: 2024-04-01. 텍스트 각색은 Justin Sun.
- 형식·길이: 절 약 460단어(3분, 추정). 전체 영상 27:14.
- 확인 2026-10-15
- 차원 근거:
  - explain: 샘플링할 때 지수에 상수 T를 넣는다. 원문: "when T is larger, more weight is given to lower values, making the distribution more uniform. When T is smaller, the larger values will dominate … when T is equal to 0, all the weight goes to the maximum value". 로짓이라는 용어도 소개한다.

**c. D2L 4.1.1.2 + 4.1.5 Exercises**
- 형식: text.
- 확인 2026-10-15
- 차원 근거:
  - recognize: Boltzmann 분포 exp(−E/kT)와 "temperature"를 올리고 내린다는 개념을 소개한다.
  - analyze: 4.1.5의 연습문제 "Q(i) ∝ P(i)^α … Which choice of α corresponds to doubling the temperature? … temperature approach 0 / ∞"로 온도 효과를 직접 분석하게 한다.

### U05 독립 확률변수 합의 분산 (Bienaymé)

**a. Grinstead & Snell §6.2**
- 형식·길이: PDF 교과서 518쪽 중 267–268쪽(PDF 쪽 번호이며 인쇄본 쪽 번호는 미확인). 약 2쪽.
- 라이선스: GNU FDL.
- 확인 2026-10-15
- 차원 근거:
  - recognize: Theorem 6.8 "Let X and Y be two independent random variables. Then V(X + Y) = V(X) + V(Y)."
  - derive:
    - 증명은 V(X+Y) = E((X+Y)²) − (a+b)²에서 출발해, 독립이면 E(XY) = E(X)E(Y)임을 써서 V(X) + V(Y)를 얻는다.
    - Theorem 6.9는 독립시행의 합 S_n과 평균 A_n에 대해 V(S_n) = nσ², V(A_n) = σ²/n을 증명한다.

**b. D2L 22.6.1.5 Variances, 22.6.1.10 Covariance**
- 형식·길이: text + code. 해당 소절 약 5분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: 분산 성질을 나열한다. Var(aX + b) = a²Var(X), 독립이면 Var(X + Y) = Var(X) + Var(Y), 표준편차 형태는 σ_{X+Y} = √(σ_X² + σ_Y²)이다.
  - explain: 공분산을 포함한 일반식 Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y) (식 22.6.44)를 제시한다. 단 유도는 "some algebra can show"로 생략되어 있어 derive용으로는 a가 필요하다.

**c. CS231n #init "Calibrating the variances with 1/sqrt(n)"**
- 형식·길이: text. 약 1,000단어, 8분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - derive: s = Σ_i w_i x_i에 대해 Var(s) = Σ Var(w_i x_i) = Σ [E(w_i)]²Var(x_i) + [E(x_i)]²Var(w_i) + Var(x_i)Var(w_i) = (n Var(w)) Var(x)로 전개한다. 평균 0, 독립, 동일분포 가정을 명시한다.
  - analyze: 결론으로 `w = np.random.randn(n) / sqrt(n)`를 제시하고, ReLU는 평균이 양수라 가정이 깨진다는 점을 지적한다. ReLU용 권장값은 `w = np.random.randn(n) * sqrt(2.0/n)`이다.
- 비고:
  - 같은 논리가 Transformer의 1/√d_k 스케일링 근거가 된다. 관련 리소스는 Vaswani 각주 4(U09-a), d2l 11.3.1(U09-b), Xavier 초기화 유도(d2l 5.4.2.2, U27-a)다.
  - Wikipedia "Variance" §Sum of uncorrelated variables(https://en.wikipedia.org/wiki/Variance#Sum_of_uncorrelated_variables, CC BY-SA 4.0, 확인 2026-10-15)는 "Bienaymé formula"라는 명칭과 1853년 기원, 상관 변수의 일반식(공분산 합)을 정리한 보조 참고다.

### U06 토큰/단어 임베딩 (입력 = 벡터 시퀀스)

**a. 3b1b Chapter 5: Tokens, Embedding 절들**
- 형식·길이: video 27:14 + text. 관련 절 약 1,400단어 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: 입력 텍스트를 토큰으로 나눈 뒤, 각 토큰을 임베딩 행렬(Embedding Matrix)에서 조회해 고차원 벡터로 바꾼다. 결과는 벡터의 시퀀스가 된다.
  - explain:
    - "Direction": 공간의 방향이 의미를 담는다(예: 'Italian-ness' 방향).
    - "Dot Product": 정렬도를 측정한다.
    - "Beyond words": 네트워크를 통과하며 벡터가 문맥을 흡수한다.

**b. The Illustrated Word2vec** (Jay Alammar)
- 정보: "Written on March 27, 2019".
- 형식·길이: text + 일러스트. 약 4,700단어, 25–30분 (추정).
- 라이선스: CC BY-NC-SA 4.0.
- 확인 2026-10-15
- 차원 근거:
  - explain: "Personality Embeddings"로 벡터 표현과 코사인 유사도의 직관을 잡고, "Word Embeddings", "Analogies"로 이어간다.
  - analyze: Skipgram과 Negative Sampling 학습 과정을 다루고, "Window Size and Number of Negative Samples"에서 하이퍼파라미터 선택을 논의한다.

**c. D2L 10.7.2 Encoder**
- 형식·길이: text + code. 해당 단락 약 3–5분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 원문 "we use an embedding layer to obtain the feature vector for each token". 임베딩 층의 가중치는 (vocab_size × embed_size) 행렬이고, 토큰 인덱스 i에 대해 i번째 행을 꺼낸다.
  - implement: `self.embedding = nn.Embedding(vocab_size, embed_size)` 코드.
- 비고:
  - derive 보강용으로 **D2L 15.1 Word Embedding (word2vec)**(https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html, 확인 2026-10-15)을 쓸 수 있다. one-hot은 코사인 유사도로 단어 유사성을 표현하지 못한다는 점, skip-gram의 log P(w_o | w_c)와 중심어 벡터에 대한 기울기 유도(15.1.3.1)를 다룬다.
  - Transformer 맥락은 Vaswani §3.4 Embeddings and Softmax(https://ar5iv.labs.arxiv.org/html/1706.03762#S3.SS4)에 있다. 두 임베딩 층과 pre-softmax 선형층이 가중치를 공유하고, 임베딩에 √d_model을 곱한다.

### U07 어텐션 메커니즘 (일반 개념: query–key 호환도로 value 가중합)

**a. D2L 11.1**
- 형식·길이: text + code. 약 1,500단어, 10분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: Attention(q, D) = Σ_i α(q, k_i) v_i (식 11.1.1). 이 연산을 "attention pooling"이라 부른다.
  - explain: (키, 값) 데이터베이스와 query 비유를 쓴다. 가중치가 비음수이면 출력은 값들이 만드는 convex cone 안에 있고, 합이 1이면 convex combination이 된다. softmax 정규화(식 11.1.3)와 `show_heatmaps` 시각화도 다룬다.
- 비고: **11.2 Attention Pooling by Similarity**(https://d2l.ai/chapter_attention-mechanisms-and-transformers/attention-pooling.html, 확인 2026-10-15)는 Nadaraya–Watson 커널 회귀를 어텐션으로 해석한다. gaussian, boxcar, epanechikov 커널 코드가 있어 derive/implement 보강용으로 좋다.

**b. Attention and Augmented Recurrent Neural Networks** (Chris Olah & Shan Carter, Google Brain, Distill)
- 정보: 2016-09-08.
- 형식·길이: text + 도식. 약 4,700단어, 25–30분 (추정).
- 라이선스: CC BY 2.0.
- 확인 2026-10-15
- 차원 근거:
  - explain: "Attentional Interfaces"에서 다음 흐름을 설명한다.
    1. attending RNN이 query를 생성한다.
    2. 각 항목을 query와 내적해 점수를 낸다.
    3. 점수를 softmax에 넣어 attention 분포를 만든다.
    4. 이 분포로 가중합한다.
  - 미분 가능성은 "we focus everywhere, just to different extents"로 설명한다.

**c. Visualizing A Neural Machine Translation Model** (Jay Alammar)
- 정보: "Written on May 9, 2018".
- 형식·길이: text + 동영상 애니메이션. 약 1,750단어, 10–15분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain:
    - 고정 크기 context vector가 병목이 되는 문제에서 출발한다.
    - 해결책으로 encoder가 모든 hidden state를 디코더에 넘긴다.
    - 디코더는 각 hidden state에 점수를 매기고, softmax한 점수로 곱해 더한다. 이 단계를 애니메이션으로 보여 준다.
    - Bahdanau et al. 2014와 Luong et al. 2015를 출처로 소개한다.
- 비고: Deep Learning 12.4.5.1 "Using an Attention Mechanism and Aligning Pieces of Data"(https://www.deeplearningbook.org/contents/applications.html, 확인 2026-10-15)는 Transformer 이전 시점의 짧은 교과서 서술이라 선택 참고로 둔다.

### U08 가산(Bahdanau) 어텐션

**a. Bahdanau, Cho & Bengio, arXiv 1409.0473 (PDF v7 대조)**
- 형식·길이: PDF 15쪽. §3.1은 p.3, A.1.2는 p.12. 해당 부분 약 1.5쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize:
    - 식 (5) c_i = Σ_j α_ij h_j
    - 식 (6) α_ij = exp(e_ij) / Σ_k exp(e_ik)
    - e_ij = a(s_{i−1}, h_j)는 "alignment model"이다.
  - derive: App. A.1.2에서 a(s_{i−1}, h_j) = v_a^T tanh(W_a s_{i−1} + U_a h_j)를 제시한다(W_a ∈ R^{n×n}, U_a ∈ R^{n×2n}, v_a ∈ R^n). U_a h_j는 i와 무관하므로 미리 계산해 비용을 줄일 수 있다고 논의한다.

**b. D2L 11.3.4 Additive Attention + 11.4**
- 11.4 URL: https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html (확인 2026-10-15)
- 형식·길이: text + code. 약 20분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain:
    - query와 key의 차원이 다를 때 쓸 수 있는 대안으로 a(q, k) = w_v^T tanh(W_q q + W_k k) (식 11.3.7)를 소개하고, "query와 key를 concat해 단일 은닉층 MLP에 넣는 것"으로 해석한다.
    - 11.4.1에서는 c_{t'} = Σ_t α(s_{t'−1}, h_t) h_t (식 11.4.1)로, 디코더 상태를 query로, encoder 상태를 key·value로 쓴다.
  - implement: `AdditiveAttention` 클래스(masked softmax, dropout, `torch.bmm`)와 `Seq2SeqAttentionDecoder`.

**c. Attention? Attention!** (Lilian Weng)
- 정보: 2018-06-24.
- 형식·길이: text. "Estimated Reading Time: 21 min" (명시).
- 라이선스: 명시 없음.
- 확인 2026-10-15
- 차원 근거:
  - analyze: "Summary" 표에서 점수 함수를 한 번에 비교한다. Content-base(Graves2014), Additive(Bahdanau2015), Location-Base, General, Dot-Product(Luong2015), Scaled Dot-Product(Vaswani2017)가 들어 있다.

### U09 스케일드 내적 어텐션 (scaled dot-product)

**a. Vaswani et al. §3.2.1 + 각주 4 (PDF v7 p.4)**
- 형식·길이: PDF 15쪽 중 약 0.5쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: Attention(Q, K, V) = softmax(QK^T / √d_k) V.
  - derive: 각주 4 원문 "assume that the components of q and k are independent random variables with mean 0 and variance 1. Then their dot product … has mean 0 and variance d_k." 그래서 1/√d_k로 스케일한다. Bienaymé(U05)의 직접 응용이다.
  - analyze: 원문 "additive attention outperforms dot product attention without scaling for larger values of d_k". 큰 내적이 softmax를 "extremely small gradients" 영역으로 밀어낸다는 가설을 제시한다.
- 비고: ar5iv에서는 이 각주 번호가 다르게 렌더링되므로, 인용할 때는 "PDF v7 각주 4"로 적는다.

**b. D2L 11.3.1–11.3.3**
- 형식·길이: text + code. 약 1,700단어, 12분 + 코드 (추정).
- 확인 2026-10-15
- 차원 근거:
  - derive:
    - 가우시안 커널의 지수 −½‖q − k_i‖²를 전개하면 q^T k_i 항만 남긴다. ‖q‖² 항은 정규화로 사라지고, ‖k_i‖은 batch/layer norm으로 거의 일정하다.
    - 독립·평균 0·분산 1 가정에서 분산이 d가 되므로 1/√d로 스케일한다.
  - implement:
    - 11.3.2.1 `masked_softmax`, 11.3.2.2 `torch.bmm`
    - 11.3.3 `DotProductAttention`: `scores = torch.bmm(queries, keys.transpose(1, 2)) / math.sqrt(d)`

**c. Attention in transformers, step-by-step** (3b1b Chapter 6)
- 정보: 2024-04-07.
- 형식·길이: video 26:09 (YouTube 메타데이터) + text 약 5,700단어.
- 확인 2026-10-15
- 차원 근거:
  - explain:
    - query와 key의 내적 격자에 열 단위 softmax를 적용한 것이 "attention pattern"이다.
    - "for numerical stability … divide all of these values by the square root of the dimension of that key-query space".
    - masking: 마스킹할 칸을 −∞로 둔 뒤 softmax를 적용한다.
    - 마지막으로 value 벡터를 가중합한다.

### U10 멀티헤드 어텐션

**a. Vaswani §3.2.2 (+§3.2.3)**
- 확인 2026-10-15
- 차원 근거:
  - recognize: MultiHead(Q, K, V) = Concat(head_1, …, head_h) W^O, head_i = Attention(QW_i^Q, KW_i^K, VW_i^V). 사영 행렬의 차원도 명시한다.
  - derive: h = 8, d_k = d_v = d_model/h = 64. 원문 "Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality". §3.2.3은 encoder-decoder attention, encoder self-attention, decoder self-attention이라는 세 가지 용도를 정리한다.

**b. D2L 11.5**
- 형식·길이: text + code. 약 600단어 + 코드, 10분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: h개 헤드가 각자 다른 선형 사영 공간에서 attention을 계산하고, 결과를 concat한 뒤 출력 사영을 거친다.
  - implement: `MultiHeadAttention` 클래스, 그리고 헤드를 배치 차원으로 접어 병렬 계산하는 `transpose_qkv` / `transpose_output`.

**c. The Illustrated Transformer** (Jay Alammar)
- 정보: "Written on June 27, 2018".
- 형식·길이: 전체 약 4,250단어, 25분. 해당 절은 약 5분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 멀티헤드가 주는 두 이점(서로 다른 위치에 집중, 여러 "representation subspaces")을 설명한다. Transformer는 8개 헤드를 쓰므로 Q/K/V 가중치 세트가 8개, Z가 8개 나오고, 이를 concat해 W^O를 곱하는 과정을 그림으로 보여 준다.
- 비고: 3b1b Chapter 6 "Counting Parameters"(https://www.3blue1brown.com/lessons/attention#counting-parameters, 확인 2026-10-15)는 GPT-3이 블록당 96개 헤드를 쓰고 멀티헤드 블록당 약 6억 파라미터라는 계산을 보여 준다. analyze 보강용이다.

### U11 위치 인코딩 (positional encoding)

**a. Vaswani §3.5**
- 확인 2026-10-15
- 차원 근거:
  - recognize: PE(pos, 2i) = sin(pos / 10000^{2i/d_model}), PE(pos, 2i+1) = cos(…).
  - explain: 순환도 합성곱도 없으므로 순서 정보를 따로 넣어야 하며, 위치 벡터를 임베딩과 같은 차원으로 만들어 더한다. 고정 offset k에 대해 PE_{pos+k}를 PE_pos의 선형함수로 표현할 수 있어 상대 위치 학습이 쉬울 것이라는 가설을 제시한다.
  - analyze: 학습형 위치 임베딩과 "nearly identical results"(Table 3 row (E))였다. 그런데도 sinusoidal을 고른 이유는 학습 때보다 긴 시퀀스로 외삽할 수 있을 가능성이다.

**b. D2L 11.6.3**
- 형식·길이: text + code. 약 10분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - implement: `PositionalEncoding` 클래스와 열별 곡선 시각화.
  - explain: 11.6.3.1에서 0–7의 이진 표현을 예로, "a higher bit has a lower frequency"라는 비유를 쓴다.
  - derive: 11.6.3.2에서 ω_j = 1/10000^{2j/d}일 때 (p_{i,2j}, p_{i,2j+1})가 (p_{i+δ,2j}, p_{i+δ,2j+1})로 가는 사상이 2×2 회전 행렬임을 유도한다(식 11.6.3).

**c. The Illustrated Transformer, Positional Encoding 절**
- 확인 2026-10-15
- 차원 근거:
  - explain: 각 입력 임베딩에 특정 패턴의 위치 벡터를 더하는 과정을 그림으로 보여 준다. Q/K/V로 사영된 뒤 내적 어텐션에서 의미 있는 거리를 제공한다는 직관도 준다.
- 비고: ViT App. D.4 Positional Embedding(https://ar5iv.labs.arxiv.org/html/2010.11929#A4.SS4, 확인 2026-10-15)의 Table 8은 위치 임베딩 ablation이다. 위치 임베딩이 없으면 0.61382, 1-D는 0.64206 등이다. 이미지 맥락의 analyze 보강용이다.

### U12 Transformer 인코더 층

**a. Vaswani §3.1, §3.3**
- 확인 2026-10-15
- 차원 근거:
  - recognize: N = 6개의 동일한 층으로 이루어지고, 각 층은 multi-head self-attention과 position-wise FFN 두 서브층을 가진다. 각 서브층 출력은 LayerNorm(x + Sublayer(x))이고 d_model = 512다.
  - explain: FFN(x) = max(0, xW_1 + b_1)W_2 + b_2 (식 2). "two convolutions with kernel size 1"로 볼 수 있고 d_ff = 2048이다.

**b. D2L 11.7**
- 형식·길이: text + code. 약 1,900단어, 15분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 11.7.1 전체 구조, 11.7.3 "add & norm".
  - implement: `PositionWiseFFN`, `AddNorm`, `TransformerEncoderBlock`, `TransformerEncoder` 클래스.

**c. The Annotated Transformer**
- 정보: v2022(Austin Huang 외), 원작 Sasha Rush.
- 형식·길이: text + code. 전체 약 6,800단어(코드 포함). 실습 포함 1시간 이상 (추정).
- 확인 2026-10-15
- 차원 근거:
  - implement: `LayerNorm`, `SublayerConnection`, `EncoderLayer` 등 PyTorch 코드를 논문 문장과 나란히 제시한다. 같은 페이지 "#attention"에 `attention()` 함수(scaled dot-product)도 있다.
  - analyze: `SublayerConnection` docstring "Note for code simplicity the norm is first as opposed to last." 즉 논문의 post-norm과 달리 pre-norm으로 구현했다.
- 비고(정규화 위치 비교 포인트):

  | 구현 | 정규화 위치 |
  |---|---|
  | Vaswani 논문 | LayerNorm(x + Sublayer(x)) → post-norm |
  | d2l `AddNorm` | 잔차 연결 직후 LN → post-norm |
  | Annotated Transformer | pre-norm |
  | ViT 식 (2)–(3), d2l `ViTBlock` | pre-norm |

### U13 패치 임베딩 & Vision Transformer

**a. Dosovitskiy et al., arXiv 2010.11929 (PDF v2 대조, ICLR 2021)**
- 형식·길이: PDF 22쪽. §3.1은 pp.3–4, 약 1.5쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize/explain:
    - 원문 "The standard Transformer receives as input a 1D sequence of token embeddings".
    - 이미지 x ∈ R^{H×W×C}를 평탄화한 패치 시퀀스 x_p ∈ R^{N×(P²·C)}로 바꾼다(N = HW/P²).
    - 학습 가능한 선형 사영 E로 D차원 "patch embeddings"를 만든다.
  - derive:
    - 식 (1) z_0 = [x_class; x_p^1 E; …; x_p^N E] + E_pos
    - 식 (2)–(3) LN을 각 블록 앞에 두는 MSA/MLP와 잔차 연결("Layernorm (LN) is applied before every block"). MLP는 GELU를 쓰는 2층이다.
    - 식 (4) y = LN(z_L^0)
  - "Hybrid Architecture" 단락도 함께 볼 만하다.

**b. D2L 11.8**
- 형식·길이: text + code. 약 1,200단어(10분) + 학습 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: Fig. 11.8.1(9개 패치 + "<cls>")에서 패치 수 m = hw/p², 각 패치 길이 cp²를 보여 준다. 11.8.6에서는 작은 데이터(Fashion-MNIST)에서 ResNet보다 못한 이유를 다룬다.
  - implement:
    - `PatchEmbedding`: `nn.LazyConv2d(num_hiddens, kernel_size=patch_size, stride=patch_size)` 후 flatten. 패치별 선형 사영을 합성곱으로 등가 구현한 것이다.
    - `ViTMLP`, `ViTBlock`(pre-norm), `ViT`.
    - 11.8.5 학습.

### U14 클래스 토큰 ([CLS])

**a. BERT §3 "Input/Output Representations"** (arXiv 1810.04805, PDF v2 p.4 대조)
- 확인 2026-10-15
- 차원 근거:
  - recognize: 원문 "The first token of every sequence is always a special classification token ([CLS]). The final hidden state corresponding to this token is used as the aggregate sequence representation for classification tasks."
  - explain: 같은 단락에서 문장 쌍을 하나의 시퀀스로 묶는 입력 표현을 설명한다.

**b. ViT §3.1 + App. D.3 (PDF v2 pp.16–17)**
- 확인 2026-10-15
- 차원 근거:
  - explain: 원문 "Similar to BERT's [class] token, we prepend a learnable embedding … (z_0^0 = x_class), whose state at the output of the Transformer encoder (z_L^0) serves as the image representation y".
  - analyze: D.3과 Figure 9는 GAP(패치 출력 평균) 분류기와 class token을 비교한다. 원문 "Both work similarly well, but require different learning-rates". 초기 GAP 실험의 저조한 성능은 추가 토큰이나 GAP 때문이 아니라 학습률 차이로 "fully explained"된다고 결론짓는다.

**c. D2L 11.8.1, 11.8.4**
- 확인 2026-10-15
- 차원 근거:
  - implement:
    - `self.cls_token = nn.Parameter(torch.zeros(1, 1, num_hiddens))`
    - `torch.cat`으로 패치 임베딩 앞에 붙인다(`num_steps = num_patches + 1`).
    - 학습형 `pos_embedding`을 쓴다.
    - head에는 `X[:, 0]`만 넣는다.

### U15 층 정규화 (layer normalization)

**a. Ba, Kiros & Hinton (2016), arXiv 1607.06450 (v1)**
- 형식·길이: PDF 14쪽. §3은 p.2, §5.1은 p.3. 해당 부분 약 2쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize/derive: 식 (3) μ^l = (1/H) Σ_i a_i^l, σ^l = √((1/H) Σ_i (a_i^l − μ^l)²). 같은 층의 모든 은닉 유닛이 정규화 항을 공유하고, 학습 사례마다 항이 달라진다(배치와 무관). §3.1은 RNN에 적용한다.
  - analyze: §5.1 Table 1은 batch norm, weight norm, layer norm의 불변성을 비교한다. 비교 항목은 가중치 행렬 re-scaling/re-centering, 가중치 벡터 re-scaling, 데이터셋 re-scaling/re-centering, 단일 사례 re-scaling이다.

**b. D2L 8.5.2.3**
- 형식·길이: text. 약 3분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: LN(x) = (x − μ̂)/σ̂ (식 8.5.4–8.5.5).
  - explain: 원문 "It works just like a batch norm, only that it is applied to one observation at a time". 스케일 불변이고 배치 크기와 무관하다.

**c. D2L 11.7.3**
- 확인 2026-10-15
- 차원 근거:
  - implement: `nn.LayerNorm(2)`와 `nn.BatchNorm1d(2)`의 정규화 축을 비교하는 코드, 그리고 `AddNorm`(dropout 후 잔차 연결 + LN).
  - analyze: 원문 "batch normalization is usually empirically less effective than layer normalization in natural language processing tasks, where the inputs are often variable-length sequences".

### U16 배치 정규화 (batch normalization)

**a. Ioffe & Szegedy (2015), arXiv 1502.03167 (v3)**
- 형식·길이: PDF 11쪽. §3은 p.3, §3.1–3.2는 p.4. 해당 부분 약 3쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: Algorithm 1 "Batch Normalizing Transform". 미니배치 평균·분산으로 정규화한 뒤 γ, β로 스케일·시프트한다. ε는 수치 안정성용이다.
  - derive: 역전파 chain rule 식(∂ℓ/∂x̂_i, ∂ℓ/∂σ_B², ∂ℓ/∂μ_B, ∂ℓ/∂x_i 등).
  - analyze:
    - §3.1: 추론 시에는 미니배치에 의존하지 않고 출력이 결정적이어야 한다.
    - §3.2: 합성곱에서는 "different elements of the same feature map, at different locations, are normalized in the same way". 즉 위치 전체에 걸쳐 함께 정규화한다.
    - §3.3–3.4: 높은 학습률과 정규화 효과를 주장한다.

**b. D2L 8.5**
- 형식·길이: text + code. 약 3,600단어, 25분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 8.5.2.1–8.5.2.2 FC 층과 합성곱 층에서의 적용, 8.5.2.4 예측 시 처리.
  - implement: 8.5.3 `batch_norm` 함수와 `BatchNorm` 클래스(from scratch), 8.5.4 `BNLeNetScratch`, 8.5.5 `BNLeNet`.
  - analyze: 8.5.6에서 원 논문의 "internal covariate shift" 설명을 비판적으로 검토하며, 직관과 실제 설명을 구분하라고 강조한다.

**c. Deep Learning 8.7.1**
- 형식·길이: text. 약 4쪽 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 원문 "not an optimization algorithm at all … a method of adaptive reparametrization". H' = (H − μ)/σ, 그리고 γH' + β로 표현력을 회복한다.
  - analyze: 깊은 선형 네트워크(ŷ = x w_1 w_2 … w_l) 예로 한 번의 갱신이 2차·3차 이상의 고차 효과를 만든다는 문제를 들어, BN이 학습을 쉽게 만드는 이유를 분석한다.

### U17 잔차 연결 / ResNet

**a. He, Zhang, Ren & Sun (2015), arXiv 1512.03385 (v1)**
- 형식·길이: PDF 12쪽. §3은 p.3. 약 3쪽 + §4.1.
- 확인 2026-10-15
- 차원 근거:
  - recognize: §3.2 y = F(x, {W_i}) + x (식 1). 차원이 맞지 않으면 y = F(x, {W_i}) + W_s x (식 2). 원문 "introduce neither extra parameter nor computation complexity".
  - explain: §3.1에서 H(x) 대신 잔차 F(x) := H(x) − x를 학습시킨다. 항등 사상이 최적에 가까우면 잔차를 0으로 밀어붙이는 편이 쉽기 때문이다.
  - analyze: §4.1 "Plain Networks"에서 34층 plain 망이 18층보다 학습 오차까지 높다는 degradation을 보이고(과적합이 아님), residual 망과 비교한다.

**b. D2L 8.6**
- 형식·길이: text + code. 약 3,000단어, 20분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 8.6.1 Function Classes는 중첩 함수 클래스여야 깊게 쌓을수록 확실히 나아진다고 논증한다. 8.6.2는 잔차 매핑 g(x) = f(x) − x를 다룬다.
  - implement: `Residual(num_channels, use_1x1conv=False, strides=1)` 클래스, `ResNet`, `ResNeXtBlock`.

### U18 합성곱 층 (convolutional layer)

**a. CS231n #conv**
- 형식·길이: text + JS 애니메이션 데모. 약 3,900단어, 25–30분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: local connectivity("receptive field … (equivalently this is the filter size)"), depth / stride / zero-padding, parameter sharing.
  - derive: 출력 크기 (W − F + 2P)/S + 1과 정수 조건. 예를 들어 (10 − 3 + 0)/2 + 1 = 4.5라 불가능하다.
  - analyze:
    - 파라미터 수 예: 5×5×3 = 75 weights + 1 bias.
    - "Convolution Demo": 5×5×3 입력에 대한 애니메이션.
    - "Implementation as Matrix Multiplication": im2col로 합성곱을 큰 행렬곱 하나로 바꾼다(U02와 연결).

**b. D2L 7.2**
- 형식·길이: text + code. 약 2,300단어, 15분 + 실습 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 7.2.1 cross-correlation 연산, 7.2.5 cross-correlation과 convolution의 관계.
  - implement: `corr2d(X, K)`, `Conv2D(nn.Module)`, 7.2.3 엣지 검출, 7.2.4 입력·출력 쌍으로 커널 학습.
- 비고: 7.3 Padding and Stride, 7.4 Multiple Input and Multiple Output Channels로 이어진다(TOC에서 확인).

**c. Deep Learning 9.1–9.2 (pp.327–335)**
- 형식: text.
- 확인 2026-10-15
- 차원 근거:
  - recognize: 합성곱 정의, 그리고 "many neural network libraries implement a related function called the cross-correlation"(식 9.6).
  - derive: 1D 이산 합성곱은 Toeplitz 행렬, 2D는 doubly block circulant 행렬과의 곱(희소 행렬)으로 볼 수 있다.
  - explain: 9.2의 세 아이디어 sparse interactions, parameter sharing, equivariant representations.

### U19 수용 영역 (receptive field)

**a. Computing Receptive Fields of Convolutional Neural Networks** (André Araujo, Wade Norris, Jack Sim, Distill)
- 정보: Published Nov. 4, 2019. DOI 10.23915/distill.00021.
- 형식·길이: text + 도식. 약 5,700단어, 35–45분 (추정).
- 라이선스: CC BY 4.0.
- 확인 2026-10-15
- 차원 근거:
  - derive: r_L = 1, r_{L−1} = k_L에서 출발해 k_l = 1인 경우 r_{l−1} = s_l·r_l − (s_l − 1) 등 재귀식을 세운다. 이를 닫힌 형식 r_0 = Σ_{l=1}^{L} ((k_l − 1) Π_{i=1}^{l−1} s_i) + 1로 푼다. 영역 좌표 u_0, v_0 (r_0 = v_0 − u_0 + 1)와 effective stride/padding도 유도한다.
  - analyze: 임의 계산 그래프(다중 경로)를 다루고, "Discussion: receptive fields of modern networks"에서 현대 네트워크를 분석한다. 저자들은 TensorFlow 코드베이스에 통합한 오픈소스 계산 라이브러리도 소개한다.

**b. D2L 7.2.6**
- 형식·길이: text. 약 3분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: 원문 "its receptive field refers to all the elements (from all the previous layers) that may affect the calculation of x during the forward propagation".
  - explain: 수용 영역은 입력의 실제 크기보다 클 수 있다. 2×2 커널을 2층 쌓으면 수용 영역이 넓어지는 예를 든다.

**c. CS231n #layerpat**
- 형식·길이: text. 약 700단어 (추정).
- 확인 2026-10-15
- 차원 근거:
  - analyze: 3×3 CONV 3층은 입력을 7×7로 본다. 비선형이 3번 들어가고, 파라미터는 27C²로 7×7 단일층의 49C²보다 적다. 단점은 중간 활성값을 저장할 메모리다(VGG U24와 연결).

### U20 귀납적 편향 (CNN의 국소성·이동 등변성 vs Transformer)

**a. D2L 7.1**
- 형식·길이: text. 약 2,800단어, 20분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 7.1.1에서 translation invariance와 locality라는 원칙을 세운다.
  - derive:
    - 완전연결 층의 4차 가중치 텐서에 translation invariance([V]_{i,j,a,b} = [V]_{a,b})를 부과하면 식 7.1.2가 된다.
    - 여기에 locality(|a|, |b| > Δ이면 0)를 더하면 식 7.1.3, 즉 합성곱 층이 된다. 파라미터는 4×10^6에서 4Δ²로 줄어든다.
    - 7.1.2.2 원문: "All learning depends on imposing inductive bias. When that bias agrees with reality, we get sample-efficient models…"
- 용어 주의: d2l의 "translation invariance"는 "입력이 이동하면 은닉 표현도 이동한다"는 뜻이다. 엄밀히는 등변성(b, c 참고)이다.

**b. Deep Learning 9.2 & 9.4**
- 형식·길이: text. 약 9쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: 등변성 정의 "f(g(x)) = g(f(x))". 합성곱은 이동 함수 g에 대해 등변이다.
  - explain: 9.4는 합성곱·풀링을 완전연결망에 대한 "infinitely strong prior"로 해석한다.
  - analyze: 원문 "convolution and pooling can cause underfitting". prior의 가정이 맞을 때만 유용하다.

**c. ViT §3.1 "Inductive bias."**
- 확인 2026-10-15
- 차원 근거:
  - analyze: 원문 "In CNNs, locality, two-dimensional neighborhood structure, and translation equivariance are baked into each layer … In ViT, only MLP layers are local and translationally equivariant, while the self-attention layers are global." 2D 구조는 패치 분할과, 해상도를 바꿔 fine-tuning할 때 위치 임베딩을 조정하는 데만 쓰인다.
- 비고: d2l 11.8.6(U13-b 페이지)은 "Transformers lack those useful principles in convolution, such as translation invariance and locality"라고 정리한다. 작은 데이터에서는 ResNet이, 약 3억 장 규모에서는 ViT가 우세하다는 데이터 규모 의존성을 함께 서술한다.

### U21 드롭아웃 (dropout)

**a. D2L 5.6**
- 형식·길이: text + code. 약 1,500단어(10분) + 실습 20–30분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - derive: 도입부 식 (5.6.1)에서 확률 p로 h' = 0, 그 외에는 h' = h/(1−p)로 두면 "the expectation remains unchanged, i.e., E[h'] = h"이다.
  - explain: 5.6.1에서 은닉층에 적용하는 방식을 설명한다.
  - implement: 5.6.2에서 U[0, 1] 샘플로 Bernoulli 마스크를 만들어 직접 구현하고, 5.6.3에서 간결한 구현을 보인다.

**b. CS231n #reg (Dropout)**
- 형식·길이: text + code. 해당 부분 약 600단어 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 학습 중 dropout은 "sampling a Neural Network within the full Neural Network"로 해석할 수 있다.
  - implement: vanilla dropout과 "Inverted Dropout" numpy 코드. 학습 시 스케일링해서 테스트 코드는 그대로 둔다.

**c. Srivastava, Hinton, Krizhevsky, Sutskever, Salakhutdinov (JMLR 15(56):1929−1958, 2014)**
- PDF: https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf (확인 2026-10-15)
- 형식·길이: 30쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: §4에서 r_j^{(l)} ~ Bernoulli(p), ỹ^{(l)} = r^{(l)} * y^{(l)}.
  - analyze: §6에서 이미지, TIMIT, 텍스트 등 벤치마크와 Bayesian NN, 표준 정규화와 비교한다. §7 Salient Features는 7.5 Monte-Carlo Model Averaging vs. Weight Scaling 등을 다룬다.
  - derive: §9 Marginalizing Dropout(9.1 Linear Regression, 9.2 Logistic Regression and Deep Networks).
- **표기 주의**: d2l의 p는 "드롭" 확률이고, CS231n과 Srivastava 논문의 p는 "유지" 확률이다.

### U22 ReLU

**a. D2L 5.1.2.1**
- 형식·길이: text + code. 약 5분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: ReLU(x) = max(x, 0) (식 5.1.4).
  - explain: 음수 입력에서 도함수는 0, 양수에서 1이다. 0에서는 미분할 수 없어 왼쪽 도함수(0)를 쓴다("set of measure zero"). 원문 "it mitigated the well-documented problem of vanishing gradients". pReLU 변형(식 5.1.5)도 소개한다.
  - implement: `torch.relu` 플롯과 autograd로 그린 도함수 플롯.

**b. CS231n #actfun**
- 형식·길이: text. 약 1,170단어, 8분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain/analyze:
    - 장점: Krizhevsky et al.에서 SGD 수렴이 "a factor of 6" 빨랐다(선형이고 포화하지 않는 형태). 연산도 단순하다.
    - 단점: "dying ReLU". 학습률이 너무 크면 최대 40%의 유닛이 죽을 수 있다.
    - Leaky ReLU와 Maxout을 비교한다.
    - TLDR 권고: "Use the ReLU non-linearity, be careful with your learning rates…"

**c. AlexNet §3.1 ReLU Nonlinearity**
- 형식·길이: 약 0.5쪽.
- 확인 2026-10-15
- 차원 근거:
  - analyze: Figure 1은 4층 CNN이 CIFAR-10에서 25% 학습 오차에 도달하는 데 ReLU가 tanh보다 "six times faster"임을 보인다. 포화하는 비선형(tanh, sigmoid)과 포화하지 않는 max(0, x)의 학습 속도를 비교한다.

### U23 AlexNet

**a. Krizhevsky, Sutskever & Hinton, NIPS 2012** (Advances in Neural Information Processing Systems 25)
- PDF: https://papers.nips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf (확인 2026-10-15)
- 형식·길이: 9쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: §3.5 원문 "the net contains eight layers with weights; the first five are convolutional and the remaining three are fully-connected". §3.2는 2-GPU 분할이다.
  - explain: §3.1 ReLU, §3.3 Local Response Normalization, §3.4 Overlapping Pooling.
  - analyze: §4 과적합 대응(4.1 데이터 증강, 4.2 Dropout), §6 결과.

**b. D2L 8.1**
- 형식·길이: text + code. 약 3,600단어(25분) + 학습 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 8.1.1 표현 학습의 역사와 "Missing Ingredient: Data / Hardware". 8.1.2.2 원문 "AlexNet changed the sigmoid activation function to a simpler ReLU activation function". 8.1.2.3 용량 제어(dropout, 증강).
  - implement: `AlexNet(d2l.Classifier)`와 8.1.3 학습.

**c. CS231n #case**
- 형식·길이: text. 약 870단어 (추정).
- 확인 2026-10-15
- 차원 근거:
  - recognize: AlexNet은 ILSVRC 2012에서 top-5 오류 16%를 기록했다(2위 26%). LeNet보다 깊고 크며, CONV 층을 연속으로 쌓았다. LeNet, ZF Net, GoogLeNet, VGGNet, ResNet으로 이어지는 계보 속 위치를 알려 준다.

### U24 VGG

**a. Simonyan & Zisserman, arXiv 1409.1556 (PDF v6 대조)**
- 형식·길이: PDF 14쪽. §2는 pp.2–3, 약 2쪽.
- 확인 2026-10-15
- 차원 근거:
  - recognize: 원문 "we use very small 3 × 3 receptive fields throughout the whole net". §2.2 Table 1은 구성 A–E, Table 2는 파라미터 수(133–144M)다.
  - analyze: §2.3에서 3×3 두 층은 5×5, 세 층은 7×7의 "effective receptive field"를 가진다. 비선형이 3번 들어가고, 파라미터는 27C² 대 49C²다(원문 "i.e. 81% more"). 이를 7×7 필터를 3×3으로 분해하도록 강제하는 정규화로 해석한다.

**b. D2L 8.2**
- 형식·길이: text + code. 약 1,400단어(10분) + 학습 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 블록(3×3 conv 반복 + 2×2 max-pool) 단위로 설계한다는 개념.
  - implement: `vgg_block(num_convs, out_channels)`(`nn.LazyConv2d(…, kernel_size=3, padding=1)`, `nn.MaxPool2d(kernel_size=2, stride=2)`)와 `VGG(arch=…)`. VGG-11 구성은 arch=((1, 64), (1, 128), (2, 256), (2, 512), (2, 512))이다.

**c. CS231n "VGGNet in detail"**
- 형식·길이: text. 약 5분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - analyze: 3×3 conv(stride 1, pad 1)와 2×2 pool(stride 2) 구성에서 층별 메모리와 가중치를 계산한다. 합계는 "TOTAL memory: 24M * 4 bytes ~= 93MB / image (only forward! ~*2 for bwd)", "TOTAL params: 138M parameters"이고, 메모리는 앞쪽 CONV 층, 파라미터는 마지막 FC 층에 몰려 있다는 관찰로 이어진다.

### U25 지식 증류 (knowledge distillation, 온도 포함)

**a. Hinton, Vinyals & Dean (2015), arXiv 1503.02531, Section 2 (요청 지정 리소스)**
- 형식·길이: PDF 9쪽. §2–§3은 pp.2–4.
- 확인 2026-10-15
- 차원 근거:
  - recognize/explain:
    - 큰(cumbersome) 모델의 지식을 작은 모델로 옮긴다.
    - transfer set에서 큰 모델이 "high temperature"로 만든 soft target으로 학습한다. 같은 고온으로 학습하고, 학습 뒤에는 T = 1을 쓴다.
    - 정답 레이블과의 교차엔트로피를 가중 결합한다. soft 항의 기울기가 1/T²로 줄어 T²를 곱한다.
  - derive: §2.1(식 2–4). 고온 극한에서 logit matching이 증류의 특례가 된다.
  - analyze: §3(MNIST)
    - teacher 67 errors, 정규화 없는 800-800 student 146 errors.
    - soft target(T = 20)을 맞추는 과제만 추가하면 74 errors.
    - transfer set에서 숫자 3을 빼도 bias를 보정하면 109 errors(그중 3이 14개).

**b. Knowledge Distillation Tutorial** (PyTorch Tutorials, Author: Alexandros Chariton)
- 정보: Created On Aug 22, 2023 / Last Updated Jan 24, 2025 / Last Verified Nov 05, 2024.
- 형식·길이: text + code(Colab/Notebook). 실행 포함 40–60분 (추정, 하드웨어 요구사항 미확인).
- 확인 2026-10-15
- 차원 근거:
  - implement: CIFAR-10 teacher/student, cross-entropy 기준선, "Knowledge distillation run"이 있다. `soft_targets = softmax(teacher_logits / T)`, `log_softmax(student_logits / T)`로 soft-target 손실을 만들고 `* (T ** 2)` 스케일을 곱한 뒤 label loss와 가중합한다. 코드 주석: "Scaled by T**2 as suggested by the authors of the paper".
  - analyze: "Cosine loss minimization run", "Intermediate regressor run" 같은 변형과 결과를 비교한다.

### U26 전이학습 (사전학습 + 미세조정)

**a. CS231n transfer-learning**
- 형식·길이: text. 약 1,100단어, 8분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 세 가지 시나리오를 소개한다.
    - ConvNet as fixed feature extractor: AlexNet의 4096-D "CNN codes"를 특징으로 쓴다.
    - Fine-tuning the ConvNet.
    - Pretrained models.
  - analyze:
    - "When and how to fine-tune?": 새 데이터의 크기(작음/큼)와 원 데이터와의 유사도에 따라 전략을 고른다.
    - "Practical advice": 사전학습 모델이 주는 제약이 있고, fine-tune하는 가중치에는 작은 학습률을 쓴다.

**b. D2L 14.2**
- 형식·길이: text + code(PyTorch/MXNet). 약 1,500단어(10분) + 학습 (추정).
- 확인 2026-10-15
- 차원 근거:
  - explain: 14.2.1의 4단계.
    1. 소스 모델을 사전학습한다.
    2. 출력층을 제외하고 복사한다.
    3. 새 출력층을 무작위로 초기화한다.
    4. 타깃 데이터로 학습한다.
  - implement: ImageNet으로 사전학습한 ResNet-18을 hot dog 데이터로 `train_fine_tuning`한다. 출력층은 "a learning rate ten times greater"로 학습한다.
  - analyze: 같은 구조를 무작위 초기화로 처음부터 학습한 모델과 비교한다. 같은 epoch에서 fine-tuning 쪽이 더 좋다.

**c. BERT §3 (+§3.1, §3.2)**
- 확인 2026-10-15
- 차원 근거:
  - recognize: 원문 "There are two steps in our framework: pre-training and fine-tuning."
  - explain: §3.1에서 Masked LM과 NSP로 사전학습한다. §3.2에서는 같은 사전학습 파라미터로 초기화한 뒤 과제별로 전체를 fine-tuning하며, 입력과 출력만 바꾼다.
- 비고(선택 보강, 모두 확인 2026-10-15):
  - ViT §3.2 Fine-tuning and Higher Resolution (https://ar5iv.labs.arxiv.org/html/2010.11929#S3.SS2): 대규모로 사전학습한 뒤 예측 head를 제거하고 0으로 초기화한 D×K 층을 붙인다. 고해상도로 fine-tuning할 때는 위치 임베딩을 조정한다.
  - PyTorch "Transfer Learning for Computer Vision Tutorial" (Sasank Chilamkurthy, https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html, BSD 3-Clause): "Finetuning the ConvNet"과 "ConvNet as fixed feature extractor"를 구현하는 대안이다.
  - Jay Alammar "The Illustrated BERT, ELMo, and co. (How NLP Cracked Transfer Learning)" (https://jalammar.github.io/illustrated-bert/, CC BY-NC-SA 4.0): NLP 전이학습의 흐름을 시각적으로 설명한다.
  - Deep Learning 15.2 Transfer Learning and Domain Adaptation (pp.534–539, https://www.deeplearningbook.org/contents/representation.html): 이론적 정의.

### U27 기울기 소실 (vanishing gradients)

**a. D2L 5.4**
- 형식·길이: text + code. 약 1,900단어, 15분 (추정).
- 확인 2026-10-15
- 차원 근거:
  - derive: 식 5.4.2는 깊은 네트워크의 기울기를 L − l개 Jacobian 행렬(M^{(L)} … M^{(l+1)})과 기울기 벡터의 곱으로 쓴다. 이 곱은 지나치게 작아지거나 커질 수 있다. 5.4.2.2에서는 Var[o_i] = n_in σ² γ²를 유도한다(U05와 연결).
  - explain/implement:
    - 5.4.1.1: sigmoid와 그 기울기를 autograd로 그리는 코드.
    - 5.4.1.2: 가우시안 랜덤 행렬 100개를 곱해 기울기 폭주를 시연한다.

**b. Deep Learning 8.2.5 Long-Term Dependencies (+10.7, https://www.deeplearningbook.org/contents/rnn.html)**
- 형식·길이: text. 8.2.5 약 2쪽(추정) + 10.7은 pp.396–399.
- 확인 2026-10-15
- 차원 근거:
  - derive: 같은 W를 t번 곱하는 경로를 고유분해 W^t = V diag(λ)^t V^{-1}로 분석한다. 원문 "the vanishing and exploding gradient problem refers to the fact that gradients through such a graph are also scaled according to diag(λ)^t". 10.7에서는 RNN의 장기 의존성 문제로 확장한다.

**c. Glorot & Bengio (AISTATS 2010, PMLR 9:249–256)**
- PDF: https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf (확인 2026-10-15)
- 형식·길이: 8쪽.
- 확인 2026-10-15
- 차원 근거:
  - analyze: §3 "Effect of Activation Functions and Saturation During Training"에서 활성함수별 포화를 관찰하고, §4.3에서 학습 중 역전파되는 기울기를 분석한다.
  - derive: §4.2.1에서 선형 영역을 가정하고 층별 활성·기울기 분산의 전파를 분석한다(원문 "the variance of the back-propagated gradients decreases as we go backwards in the network"). 그 결과로 normalized initialization W ~ U[−√6/√(n_j + n_{j+1}), √6/√(n_j + n_{j+1})] (식 16)를 제안한다.

---

## 4. 제외하거나 검증하지 못한 항목 (기록하지 않음)

- **Penn State STAT 414 Lesson 24.3**(선형결합의 분산 증명 후보): curl과 WebFetch 모두 SSL 인증서 검증에 실패해 열 수 없었다. 따라서 제외했다.
- **3Blue1Brown "But what is the Central Limit Theorem?"** (https://www.3blue1brown.com/lessons/clt): 레슨 페이지에 텍스트 본문이 없다(약 740단어, 대부분 메뉴와 후원자 목록). 분산의 합 법칙을 다루는지 페이지에서 확인할 수 없어 제외했다.
- **Deep Learning 3.8 Expectation, Variance and Covariance**: 본문 검색에서 독립 변수 합의 분산 공식을 찾지 못해 U05에서 제외했다.
- **Wikipedia "Bienaymé's identity"**: 공식만 진술하고 증명이 없다. U05의 보조 참고로는 "Variance" 문서의 해당 절이 더 낫다.
- **ko.d2l.ai**: 구판 번역이라 절 번호가 1.0.3과 다르다. 기록용 링크로는 권장하지 않는다.
- **딥링크 한계**:
  - deeplearningbook.org, JMLR, NeurIPS, PMLR, Grinstead & Snell PDF는 절 단위 앵커가 없다(장·논문 URL + 절 번호로 기재).
  - arXiv 절 딥링크는 ar5iv(arXiv Labs) 앵커다. 위치는 ar5iv 렌더링과 PDF 텍스트로 교차 확인했다.

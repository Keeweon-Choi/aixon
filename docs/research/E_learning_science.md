# E. 학습과학·학습자 모델링 근거 조사 — AIXON 학습 엔진 설계용

- 작성일: 2026-10-15
- 범위: 요청된 13개 주제와 마지막의 "AIXON MVP 권고"
- 검증 방법: DOI는 Crossref API로 서지 정보를 대조했다. 초록은 OpenAlex·출판사·PubMed·ERIC에서 확인했다. 수치가 중요한 논문 일부는 PDF 본문 텍스트를 직접 추출해 확인했다(DKT, Khajah et al., Baker et al. 2008, Pelánek 2016/2018, RefD, Pan 2017, Gordon 2016, Doignon & Falmagne, Krathwohl 2002 등). 패키지 버전·라이선스는 PyPI·npm·crates.io·CRAN·GitHub API로 확인했다. 모든 확인일은 2026-10-15다.
- 표기
  - 〔추론〕: 출처가 직접 말하지 않은, 이 조사자의 판단이나 계산
  - (서지만 확인): 서지 정보만 확인했고 본문·초록은 열람하지 못함
  - (2차 확인): 2차 출처로만 확인함
  - "확인되지 않음": 찾지 못했거나 검증하지 못함

---

## 0. 핵심 결론

1. **단일 사용자 환경에서는 모집단 보정이 필요한 모델을 원리적으로 쓸 수 없다.** BKT 파라미터 적합, IRT 문항 보정, Elo 문항 난이도 추정, DKT가 모두 여기에 해당한다. 데이터가 조금 부족한 수준의 문제가 아니라 식별 구조 자체의 문제다. IRT 2PL은 피험자 약 500명, 3PL은 약 1,000명이 필요하고, Elo 문항 난이도는 학생 100명 이상이 필요하다. DKT 원 논문의 데이터는 학생 1.6만~4.7만 명 규모였다.
2. **숙달 판정에서는 모델 선택보다 증거 선택과 임계값이 더 중요하다.** Pelánek & Řihák(2017, 2018)은 시뮬레이션과 실데이터 양쪽에서 이를 보였다. 이들은 단순한 지수이동평균(EMA)이 숙달 기준으로 적합하다고 결론지었다.
3. **기본 파라미터를 쓰는 BKT는 사실상 "연속 정답 2–5회" 규칙이다.** 몇 회인지는 임의로 정한 파라미터에 따라 달라진다. 게다가 학습 전이 확률 P(T) 때문에 실제로는 학습하지 않은 사용자도 '숙달'로 판정될 수 있다. 정답률이 30%로 고정된 비학습자는 20문항 안에 약 33% 확률로 숙달 판정을 받는다〔추론: 직접 계산〕.
4. **FSRS-6(파라미터 21개)는 개인 이력 없이 기본 파라미터로 바로 동작한다.** py-fsrs 6.3.2의 옵티마이저는 Review 상태 리뷰가 512건 미만이면 기본값을 그대로 돌려준다. 다만 FSRS는 플래시카드 회상 데이터로 설계·평가된 모델이므로, 개념 이해 문항에 적용하는 것은 검증되지 않은 확장이다.
5. **슬라이더 조작은 ICAP 틀에서 'Active'(조작적 행동) 수준이다.** 학습의 증거로 볼 수 없다. 예측을 먼저 하게 하는 설계에서는 효과가 보고됐고(Crouch et al. 2004), 수동 관찰은 시연을 보지 않은 집단과 차이가 없었다.
6. **자기평가와 실제 수행의 상관은 평균 r≈.29 수준이다**(Zell & Krizan 2014). 설명적 지식에서 과대평가가 특히 크고, 메커니즘이 눈에 보이는 환경에서 더 강해진다(Rozenblit & Keil 2002). 시각적 실습 랩이 이 착각을 키울 수 있다는 점에 주의해야 한다〔추론〕.
7. **즉시 수행은 장기 파지를 보장하지 않는다.** 5분 뒤 시험에서는 재학습이 유리했지만 1주 뒤에는 시험 연습이 더 나았다(Roediger & Karpicke 2006). 분산 연습의 이득도 1주 뒤에는 없다가 4주 뒤에 크게 나타났다(Rohrer & Taylor 2006). 따라서 '숙달'에는 지연 증거가 필요하다.
8. **KST의 outer fringe(학습 준비 상태) 개념은 큐레이션된 선수 그래프 위에서 바로 쓸 수 있다.** 반면 "상위 문항 성공 → 선수 개념 숙달"이라는 하향 추론은 '추정' 상태로만 다뤄야 한다.
9. **선수관계 자동 추출 성능은 대략 정확도·F1 60–85% 수준이다.** 사람 평가자 간 일치도도 중간 정도(Pearson r≈.36)에 그친다. 따라서 자동 결과는 제안용으로만 쓰고, 그래프 반영 전에 사람 승인을 거쳐야 한다.
10. **AIXON 역량 차원 초안 {recognize, explain, derive, implement, analyze}은 개정 Bloom 분류학과 부분적으로만 대응한다.** 세 가지 문제가 있다. Krathwohl(2002)이 이미 완화한 엄격한 위계를 가정하고 있다. 'implement'라는 용어가 A&K의 Implementing과 뜻이 다르다. Evaluate·Create 범주와 지식 유형 차원이 빠져 있다.

### 주제별 권고 요약

| # | 주제 | 권고 | 핵심 근거 |
|---|---|---|---|
| 1 | BKT | 나중(조건부) | 파라미터별 적합 불가, 기본값 사용 시 N-연속정답 규칙과 같아짐, 식별성·퇴화 문제 |
| 2 | DKT | 해당 없음 | 대규모 다중 학습자 데이터가 전제이고, 해석 불가·불일치 예측 문제가 있음 |
| 3 | IRT | 해당 없음(외부 보정 문항은행이 있으면 나중) | 문항 보정에 수십~수천 명이 필요 |
| 4 | Elo | 나중(선택) | 문항 난이도 추정에 학생 100명 이상 필요, 선수구조가 있는 영역에는 부적합 |
| 5 | KST/ALEKS | **MVP(개념만 차용)** | outer fringe = 학습 준비 상태. 하향 추론은 '추정'으로만 |
| 6 | FSRS/SM-2/Leitner | **MVP: FSRS-6 기본값** / 개인 최적화는 나중 | 이력 없이 동작. 최적화는 512건 이상 |
| 7 | 인출·사전시험·생성 효과 | **MVP(설계 원칙)** | 데이터가 필요 없고 효과가 견고함. 복잡 자료에서의 경계 조건은 논쟁 중 |
| 8 | ICAP | **MVP(증거 규칙)** | 조작(Active)은 증거가 아님. 생성(Constructive) 산출물만 채점 |
| 9 | 자기평가 정확도 | **MVP(배제 규칙)** | r≈.29. 자기보고는 진단 트리거로만 사용 |
| 10 | 완전학습·숙달 기준 | **MVP(규칙 기반 기준)** | 3연속 정답 + 지연 검증. 임계값을 명시적으로 기록 |
| 11 | 인터랙티브 시뮬레이션 | **MVP(랩 설계 원칙)** | 가벼운 안내 + 예측·설명·전이. 비안내 발견학습은 효과가 낮음 |
| 12 | 선수관계 자동 학습 | 나중(사람 승인 전제) | 정확도 60–85%, 정답 기준 자체가 불확실 |
| 13 | 평가 타당도·분류학 | **MVP(문항 설계 기준)** | 새 상황·예측·오개념 기반 오답지. 차원 초안 수정 필요 |

---

## 1. Bayesian Knowledge Tracing (Corbett & Anderson)

**개요.** 기능(skill)마다 '안다/모른다'라는 이진 잠재 상태를 두는 은닉 마르코프 모형이다. 문제를 풀 때마다 정오 관측으로 숙달 확률 P(L)을 갱신한다. 표준형은 기능별로 파라미터 4개를 쓴다.
- P(L0): 초기 숙달
- P(T): 기회마다 학습 전이
- P(G): 모르는데 맞힘
- P(S): 아는데 틀림

표준형은 망각을 포함하지 않는다.

**핵심 1차 문헌**
- Corbett, A. T., & Anderson, J. R. (1994). Knowledge tracing: Modeling the acquisition of procedural knowledge. *User Modeling and User-Adapted Interaction*, 4(4), 253–278. https://doi.org/10.1007/BF01099821. Crossref 메타데이터에는 발행연도가 1995로 표기돼 있으나, 인용 관행은 1994다. 원문 PDF가 스캔본이라 텍스트를 확인하지 못했다. 확인 2026-10-15
- Beck, J. E., & Chang, K.-m. (2007). Identifiability: A fundamental problem of student modeling. *User Modeling 2007*, LNCS 4511, 137–146. https://doi.org/10.1007/978-3-540-73078-1_17 (서지만 확인. 내용은 Baker et al. 2008의 서술로 확인) 확인 2026-10-15
- Baker, R. S. J. d., Corbett, A. T., & Aleven, V. (2008). More accurate student modeling through contextual estimation of slip and guess probabilities in Bayesian knowledge tracing. *ITS 2008*, LNCS 5091, 406–415. https://doi.org/10.1007/978-3-540-69132-7_44. 정정본 PDF: https://learninganalytics.upenn.edu/ryanbaker/BCA2008W.pdf (본문 확인) 확인 2026-10-15
- van de Sande, B. (2013). Properties of the Bayesian knowledge tracing model. *Journal of Educational Data Mining*, 5(2), 1–10. https://doi.org/10.5281/zenodo.3554629 (초록 확인) 확인 2026-10-15
- Pelánek, R. (2017). Bayesian knowledge tracing, logistic models, and beyond: an overview of learner modeling techniques. *UMUAI*, 27(3–5), 313–350. https://doi.org/10.1007/s11257-017-9193-2. 프리프린트: http://www.fi.muni.cz/~xpelanek/publications/umuai-overview.pdf (본문 일부 확인) 확인 2026-10-15
- Pardos, Z. A., & Heffernan, N. T. (2010). Modeling individualization in a Bayesian networks implementation of knowledge tracing. *UMAP 2010*, LNCS, 255–266. https://doi.org/10.1007/978-3-642-13470-8_24 (서지만 확인) 확인 2026-10-15
- Yudelson, M. V., Koedinger, K. R., & Gordon, G. J. (2013). Individualized Bayesian knowledge tracing models. *AIED 2013*, LNCS, 171–180. https://doi.org/10.1007/978-3-642-39112-5_18 (서지만 확인) 확인 2026-10-15
- Badrinath, A., Wang, F., & Pardos, Z. (2021). pyBKT: An accessible Python library of Bayesian knowledge tracing models. *EDM 2021*. https://arxiv.org/abs/2105.00385 (초록 확인) 확인 2026-10-15

**데이터 요구와 가정**
- 각 문항(단계)이 기능 하나에 대응한다고 가정한다. 숙달은 이진 상태이고, 표준형에서는 한 번 배우면 잊지 않는다.
- 파라미터는 기능마다 다수 학생의 시퀀스로 EM이나 격자 탐색을 써서 적합한다.
- **식별성 문제.** Baker et al.(2008)은 이렇게 요약했다: "different combinations of the four parameters can fit the same data equivalently well, but yield very different estimates of the probability that the student knows the skill … different model parameters may require very different amounts of practice before inferring that the student has reached mastery." van de Sande(2013)는 학생 평균 수행 곡선이 실제로는 파라미터 3개에만 의존하는 지수 형태임을 해석적으로 보였다.
- **모형 퇴화.** G나 S가 0.5를 넘으면 모르는 학생이 더 잘 맞히는 역설이 생긴다. Middle School Tutor 데이터(학생 232명, 581,785 트랜잭션, 기능 253개)에서 "76% of skills in the Dirichlet priors model and 75% of skills in the baseline model were theoretically degenerate"였다(Baker et al. 2008).
- **실무 관행.** "the guess parameter is bounded to be between 0 and 0.3, and the slip parameter … between 0 and 0.1"(Baker et al. 2008). 숙달 임계값으로는 P(L)≥0.95가 표준처럼 쓰여 왔다(Pelánek & Řihák 2018의 서술).
- **개인화의 위험.** "Individualization increases the number of model parameters and carries the risk of overfitting. The individualized parameters are fitted using only few data points…"(Pelánek 2017).

**출력.** 기능별 P(L)과 다음 문항의 정답 확률.

**단일 사용자·소량 데이터 적용성**

기능별 시퀀스가 하나뿐이고 길이도 짧기 때문에 기능별 파라미터 4개를 적합할 수 없다. 남는 선택지는 기본값을 고정해 쓰는 것뿐이고, 그러면 다음 문제들이 생긴다〔추론: 직접 계산, 갱신 순서는 사후확률 계산 후 학습 전이, 임계값 0.95〕.

P(L)≥0.95에 도달하는 데 필요한 연속 정답 수:

| P(L0) | P(T) | P(G) | P(S) | 필요 연속 정답 |
|---|---|---|---|---|
| 0.1 | 0.1 | 0.2 | 0.1 | 4 |
| 0.3 | 0.1 | 0.2 | 0.1 | 3 |
| 0.5 | 0.1 | 0.2 | 0.1 | 2 |
| 0.3 | 0.1 | 0.3 | 0.1 | 4 |
| 0.1 | 0.05 | 0.3 | 0.1 | 5 |

- 이 범위에서 BKT는 **N-연속정답 규칙(N=2–5)과 사실상 같다.** 출력이 확률처럼 보이지만 그 정밀성은 허구이고, 임의로 고른 기본값이 곧 임계값을 정한다.
- **P(T)>0은 정오와 무관하게 매 시도마다 학습이 일어난다고 가정한다.** L0=0.3, T=0.1, G=0.2, S=0.1일 때, 실제 정답률이 고정된 비학습자가 숙달 판정을 받을 확률은 다음과 같다. 이는 "증거로만 갱신"이라는 AIXON 원칙과 충돌한다.

| 비학습자의 실제 정답률 | 10문항 내 숙달 판정 확률 | 20문항 내 숙달 판정 확률 |
|---|---|---|
| 0.2 | 5.5% | 11.7% |
| 0.3 | 16.7% | 32.9% |
| 0.5 | 55.2% | 82.6% |

- 오답 하나가 섞일 때의 궤적: C,C,W,C,C,C → P(L) = 0.69, 0.92, 0.63, 0.90, 0.98, 0.995.
- 표준형에는 망각이 없어서 복습 스케줄러와 따로 논다. BKT+F 같은 망각 확장이 필요하다. 역량 차원별 상태도 기본 모형에는 없다.

**구현 라이브러리.** pyBKT 1.4.3: PyPI 2026-08-05, MIT, GitHub CAHLR/pyBKT 마지막 push 2026-10-09로 유지 중이다. forgets, multigs(문항별 guess/slip), multilearn 변형을 지원하고 EM 적합을 쓴다. 확인 2026-10-15

**권고: 나중(조건부).** MVP에서는 쓰지 않는다. 기본값 BKT는 같은 동작을 하는 투명한 규칙(N-연속정답, EMA)보다 나을 것이 없고, 해석상 오해만 낳는다. 증거가 충분히 쌓인 뒤에도 기능별 파라미터는 금지하고, 문항 유형별로 공유하는 파라미터만 후보로 삼는다. 단순 규칙 대비 오프라인 성능 비교를 통과할 때만 도입한다(M5 참조).

---

## 2. Deep Knowledge Tracing (Piech et al. 2015)

**개요.** RNN/LSTM에 (문항 태그, 정오) 시퀀스를 넣어 다음 정오를 예측한다. 전문가의 기능 매핑이 필요 없는 대신, 개념별 잠재 상태를 해석할 수 없다.

**핵심 1차 문헌**
- Piech, C., Bassen, J., Huang, J., Ganguli, S., Sahami, M., Guibas, L., & Sohl-Dickstein, J. (2015). Deep knowledge tracing. *Advances in Neural Information Processing Systems 28*, 505–513. https://proceedings.neurips.cc/paper/2015/hash/bac9162b47c56fc8a4d2a519803d51b3-Abstract.html. arXiv:1506.05908의 저자 표기는 "Jonathan Spencer"다. (본문 Table 1 확인) 확인 2026-10-15
- Khajah, M., Lindsey, R. V., & Mozer, M. C. (2016). How deep is knowledge tracing? *EDM 2016*. https://arxiv.org/abs/1604.02416 (본문 확인) 확인 2026-10-15
- Wilson, K. H., Karklin, Y., Han, B., & Ekanadham, C. (2016). Back to the basics: Bayesian extensions of IRT outperform neural networks for proficiency estimation. *EDM 2016*. https://arxiv.org/abs/1604.02336 (초록 확인) 확인 2026-10-15
- Gervet, T., Koedinger, K., Schneider, J., & Mitchell, T. (2020). When is deep learning the best approach to knowledge tracing? *JEDM*, 12(3), 31–54. https://doi.org/10.5281/zenodo.4143613 (초록 확인) 확인 2026-10-15
- Liu, Z., Liu, Q., Chen, J., Huang, S., Tang, J., & Luo, W. (2022). pyKT: A Python library to benchmark deep learning based knowledge tracing models. *NeurIPS 2022 Datasets and Benchmarks*. https://arxiv.org/abs/2206.11460 (초록 확인) 확인 2026-10-15
- Yeung, C.-K., & Yeung, D.-Y. (2018). Addressing two problems in deep knowledge tracing via prediction-consistent regularization. *L@S 2018*, 1–10. https://doi.org/10.1145/3231644.3231647 (초록 확인) 확인 2026-10-15

**데이터 요구.** 원 논문 Table 1의 규모는 다음과 같다.

| 데이터셋 | 학생 수 | 태그 수 | 응답 수 | AUC (DKT vs BKT) |
|---|---|---|---|---|
| Khan Math | 47,495 | 69 | 1,435K | 0.85 vs 0.68 |
| ASSISTments 2009–10 | 15,931 | 124 | 526K | 0.86 vs 0.67 |

**비판**
- **Khajah et al.(2016).** 같은 ASSISTments 데이터에서 고전 BKT를 다시 돌리자 AUC가 0.67이 아니라 0.73이 나왔다. 평가 절차의 편향이 있었다는 뜻이다. 망각을 넣은 BKT+F는 0.83이었다. 확장된 BKT는 네 데이터셋 평균에서 "indistinguishable from that of DKT"였다. 또 반감기 약 5스텝의 지수가중 평균, 즉 파라미터 하나짜리 자기회귀 모형이 고전 BKT보다 ASSISTments에 더 잘 맞았다. 단순한 최근성(recency) 모델이 강력하다는 점은 MVP 설계에 직접적인 함의가 있다.
- **Wilson et al.(2016).** "IRT-based methods consistently matched or outperformed DKT across all data sets…"
- **Gervet et al.(2020).** "Logistic regression … leads on datasets of moderate size or containing a very large number of interactions per student, whereas Deep Knowledge Tracing leads on datasets of large size or where precise temporal information matters most. Markov process methods, like BKT, lag behind…"
- **pyKT(2022).** 잘못된 평가 설정이 레이블 누수로 성능을 부풀리고, 많은 후속 DKT 변형의 개선폭이 원 DKT 대비 "minimal"이었다.
- **Yeung & Yeung(2018).** 학생이 어떤 기능을 잘 수행해도 그 기능의 예측 숙달도가 오히려 떨어지는 경우가 있었고, 시점 간 예측도 일관되지 않았다. 숙달 판정에 쓰기에는 의미론적으로 불안정하다.
- Xiong et al.(2016, EDM, "Going deeper with deep knowledge tracing")의 데이터 중복 지적은 원문을 찾았으나 PDF 텍스트 추출에 실패해 수치를 **확인하지 못했다**.

**출력.** 다음 문항의 정답 확률(전 기능에 대한 벡터).

**단일 사용자 적용성.** 해당 없음. 학습자 1명의 시퀀스로는 학습이 불가능하다. 사전학습 모델을 들여오더라도 AIXON의 개념·문항 체계와 다르고, 증거 기반 설명 가능성 원칙과도 충돌한다.

**구현 라이브러리.** pykt-toolkit: GitHub MIT, 2026-10-11 push. PyPI 최신은 0.0.38(2022-10-16)이라 PyPI 배포가 갱신되지 않고 있다. 확인 2026-10-15

**권고: 해당 없음.** 다중 사용자 데이터 수집 계획이 생기기 전까지는 검토할 필요가 없다.

---

## 3. 문항반응이론 (IRT: 1PL/2PL/3PL)

**개요.** P(정답 | θ)를 로지스틱 함수로 모형화한다. 1PL(Rasch)은 난이도 b만, 2PL은 변별도 a를 더하고, 3PL은 추측 c까지 둔다. 학습자 능력 θ와 문항 모수를 같은 척도에 놓는다.

**핵심 문헌**
- Rasch, G. (1960). *Probabilistic models for some intelligence and attainment tests*. 1980년 University of Chicago Press 판이 있다. Open Library 레코드: https://openlibrary.org/search?q=Probabilistic+models+for+some+intelligence+and+attainment+tests (서지만 확인) 확인 2026-10-15
- Lord, F. M., & Novick, M. R. (1968). *Statistical theories of mental test scores*. Addison-Wesley. 2PL·3PL 로지스틱 모형을 다룬 Birnbaum의 장이 실린 것으로 널리 인용되지만, 목차는 직접 확인하지 않았다. (서지만 확인, Open Library) 확인 2026-10-15
- Lord, F. M. (1980). *Applications of item response theory to practical testing problems*. Erlbaum. ISBN 089859006X (서지만 확인) 확인 2026-10-15
- Hulin, C. L., Lissak, R. I., & Drasgow, F. (1982). Recovery of two- and three-parameter logistic item characteristic curves: A Monte Carlo study. *Applied Psychological Measurement*, 6(3), 249–260. https://doi.org/10.1177/014662168200600301 (초록 확인) 확인 2026-10-15
- Linacre, J. M. (1994). Sample size and item calibration stability. *Rasch Measurement Transactions*, 7(4), 328. https://www.rasch.org/rmt/rmt74m.htm 확인 2026-10-15
- Benedetto, L., et al. (2023). A survey on recent approaches to question difficulty estimation from text. *ACM Computing Surveys*, 55(9), 1–37. https://doi.org/10.1145/3556538 (서지 확인) 확인 2026-10-15

**보정에 필요한 데이터**
- Rasch(Linacre 1994):

| 보정 안정성 | 신뢰수준 | 최소 표본 범위 | 대부분 용도의 표본 |
|---|---|---|---|
| ±1 logit | 95% | 16–36 | 30 |
| ±½ logit | 95% | 64–144 | 100 |
| 고부담(high stakes) | 99% 이상 | 250 ~ 문항 수×20 | 250 |

- 2PL·3PL(Hulin et al. 1982): 2PL은 "tests of 30 items and samples of 500 appear adequate for some purposes". 3PL은 "samples of 1,000 examinees with tests of 60 items seem to be required for highly accurate estimation".
- 기본 가정: 단일차원성, 국소독립, 그리고 검사 중에는 능력이 변하지 않는다는 정적 능력 가정. 학습이 진행되는 상황과는 맞지 않는다.

**출력.** 표준오차가 붙은 θ, 문항 모수, 검사정보함수.

**단일 사용자 적용성.** 해당 없음. 문항 모수 추정에 필요한 '피험자'는 서로 다른 사람이어야 한다. 한 사람이 같은 문항을 반복해 풀면 학습과 기억이 섞여 독립 관측이 되지 않는다. 대안은 두 가지다.
- 작성자가 정한 난이도 등급을 사전값으로 쓰는 것. 보정되지 않은 값이다.
- 텍스트 기반 문항 난이도 추정(QDET, Benedetto et al. 2023). 이 도메인에서는 검증되지 않았다〔추론〕.

**구현 라이브러리**

| 라이브러리 | 버전 | 라이선스 | 비고 |
|---|---|---|---|
| R mirt | 1.48 (CRAN 2026-10-06) | GPL(≥3) | |
| R TAM | 4.3-25 (2025-08-28) | GPL(≥2) | |
| R eRm | 1.0-10 (2025-05-27) | GPL-3 | |
| Python py-irt | 0.7.1 (2026-03-24) | MIT | Python <3.12 제약 |
| Python girth | 0.8.0 (2021-11) | MIT | 2021년 이후 릴리스 없음 |

모두 확인 2026-10-15.

**권고: 해당 없음.** 외부에서 보정된 문항은행을 들여오는 경우에만 나중에 검토한다. 다만 "어려운 문항을 맞히면 더 강한 증거"라는 IRT의 발상은 문항 가중치에 비공식적으로 반영할 수 있다〔추론〕.

---

## 4. Elo 기반 학습자 모델링 (Pelánek 2016)

**개요.** 학습자가 문항에 답하는 것을 학습자와 문항의 '경기'로 본다. 매 응답마다 온라인으로 갱신한다.
- 예측: P = σ(θ − d)
- 학습자 갱신: θ ← θ + K(정오 − P)
- 문항 갱신: d ← d − K(정오 − P)

**핵심 문헌**
- Pelánek, R. (2016). Applications of the Elo rating system in adaptive educational systems. *Computers & Education*, 98, 169–179. https://doi.org/10.1016/j.compedu.2016.03.017. 프리프린트: https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf (본문 확인) 확인 2026-10-15
- Klinkenberg, S., Straatemeier, M., & van der Maas, H. L. J. (2011). Computer adaptive practice of Maths ability using a new item response model for on the fly ability and difficulty estimation. *Computers & Education*, 57(2), 1813–1824. https://doi.org/10.1016/j.compedu.2011.02.003 (서지만 확인) 확인 2026-10-15
- Pelánek, R., Papoušek, J., Řihák, J., Stanislav, V., & Nižnan, J. (2017). Elo-based learner modeling for the adaptive practice of facts. *UMUAI*, 27(1), 89–118. https://doi.org/10.1007/s11257-016-9185-7 (서지만 확인) 확인 2026-10-15

**데이터 요구와 가정(Pelánek 2016 본문)**
- 선행 연구는 고정 K=0.4를 썼다. 개선안은 불확실성 함수 U(n)=a/(1+bn)이다. n은 응답 수이고, a=1, b=0.05는 데이터에 적합된 값이다.
- 객관식 추측은 이동된 로지스틱 1/k + (1−1/k)σ(θ−d)로 반영한다.
- 정답과 오답에 서로 다른 상수를 쓰는 PFAE 변형이 있다.
- Elo는 단일 패스 SGD에 해당한다.
- 적용 범위: "suitable mainly for adaptive practice or low stakes testing … does not provide statistical guarantees on estimated skills"
- 데이터 요구: "the system needs at least 100 students to get good estimates of item difficulty"
- 적합한 영역: "domains with simple structure: learning of factual knowledge, foreign language vocabulary… More complex domains, involving for example prerequisite relations among skills, require more involved student modeling approaches"

**출력.** 학습자 기술 θ(전역 또는 개념별)와 문항 난이도 d.

**단일 사용자 적용성**
- 문항 난이도를 추정할 수 없다. 학생이 100명 이상 필요하고, 한 사람의 반복 응답에서는 문항 난이도와 학습 효과가 뒤섞인다.
- 난이도를 작성자 값으로 고정하면 Elo는 "난이도로 가중한 EMA"와 비슷해진다. 하지만 난이도가 보정되지 않았으니 단순 EMA보다 낫다는 근거가 없다〔추론〕.
- AIXON은 선수관계 구조가 핵심인 영역이므로, Pelánek이 직접 밝힌 적용 범위 밖이다.

**구현.** 라이브러리가 필요 없다. 위 수식 몇 줄이면 된다.

**권고: 나중(선택).** 문항은행이 커지고 문항 난이도 사전값이 어느 정도 신뢰할 만해지면 EMA의 대안으로 오프라인 비교 후보에 넣는다.

---

## 5. 지식공간이론 (KST; Doignon & Falmagne)과 ALEKS

**개요**
- 지식 상태는 학습자가 풀 수 있는 문항들의 부분집합이다. 실현 가능한 상태들의 집합을 지식 구조라고 한다.
- 선수관계, 곧 surmise relation 또는 surmise function은 "q를 숙달했다면 q의 선수 문항(들 중 한 clause)도 숙달했다"는 함의를 담는다. 이 함의가 상태 공간을 강하게 제약한다.
- 학습 공간(learning space)은 두 공리를 만족하는 지식 구조다.
  - [L1] Learning smoothness: "the learner can reach state L by mastering items one by one"
  - [L2] Learning consistency: "Knowing more does not prevent learning something new"

**핵심 문헌**
- Doignon, J.-P., & Falmagne, J.-C. (1985). Spaces for the assessment of knowledge. *International Journal of Man-Machine Studies*, 23(2), 175–196. https://doi.org/10.1016/S0020-7373(85)80031-6 (서지 확인) 확인 2026-10-15
- Doignon, J.-P., & Falmagne, J.-C. (1999). *Knowledge Spaces*. Springer. https://doi.org/10.1007/978-3-642-58625-5 (서지만 확인) 확인 2026-10-15
- Falmagne, J.-C., & Doignon, J.-P. (2011). *Learning Spaces*. Springer. https://doi.org/10.1007/978-3-642-01039-2 (서지만 확인) 확인 2026-10-15
- Doignon, J.-P., & Falmagne, J.-C. (2015). Knowledge spaces and learning spaces. arXiv:1511.06757. *New Handbook of Mathematical Psychology*의 장(章) 원고. https://arxiv.org/abs/1511.06757 (본문 확인) 확인 2026-10-15
- Falmagne, J.-C., Cosyn, E., Doignon, J.-P., & Thiéry, N. (2006). The assessment of knowledge, in theory and in practice. *ICFCA 2006*, LNCS 3874, 61–79. https://doi.org/10.1007/11671404_4 (서지만 확인) 확인 2026-10-15
- ALEKS 공식 페이지 "Research Behind ALEKS – Knowledge Space Theory". https://www.aleks.com/about_aleks/knowledge_space_theory 확인 2026-10-15

**핵심 내용과 실증(Doignon & Falmagne 2015 본문)**
- **outer fringe.** 상태 K의 outer fringe는 K∪{q}도 상태가 되는 q들의 집합으로, 지금 "ready to learn"인 문항이다. inner fringe는 최근에 숙달한 쪽의 경계다. 학습 공간에서는 두 fringe만으로 상태 전체가 결정된다.
- **확률 모형.** 문항마다 부주의 오류 β_q와 우연 정답 η_q를 둔다. 주관식 응답을 쓰는 ALEKS에서는 우연 정답 확률이 0이거나 매우 낮다고 본다.
- **ALEKS 규모.** Algebra 1은 약 350개 개념에 실현 가능한 상태가 수백만 개이고, 적응형 평가 약 25–30문항으로 상태를 추정한다(ALEKS 페이지). 초등수학 도메인은 416문항 중 평가 1회에 최대 35문항을 쓴다.
- **타당도 실증("extra problem" 방법).** 평가 125,786건, 324문항에서 측정했다. 사분상관 중앙값은 약 .68, 묶은 데이터로는 약 .80이었고, phi 계수 중앙값은 .43이었다.
- **outer fringe의 예측력.** outer fringe에서 고른 문항을 실제로 학습에 성공할 확률이 "about .93"이었다. 수십만 건의 ALEKS 평가에 기반한 수치다.
- **AND-only DAG와 KST.** 선수관계를 AND 조건만 있는 DAG로 표현하면, 그 구조는 합집합·교집합에 닫힌 준순서(quasi-ordinal) 공간과 일대일로 대응한다(Birkhoff 정리, 같은 장). 이 경우 "q 성공은 모든 조상 숙달을 함의한다"가 된다. 반면 surmise function은 대안 clause, 즉 OR 형태의 선수 경로를 허용한다.

**데이터 요구.** 결정론적 부분, 즉 구조는 전문가가 큐레이션할 수 있어서 모집단 데이터가 없어도 된다. 확률적 평가(β, η, 상태 분포)를 보정하고 구조를 정제하는 데는 대규모 응답 데이터가 쓰였다. ALEKS의 타당도 수치도 대규모 데이터에서 나온 것이다.

**출력.** 지식 상태(숙달 문항 집합), inner fringe와 outer fringe.

**단일 사용자 적용성(비판)**
- **유용한 부분.** outer fringe = "다음에 배울 수 있는 개념"이라는 정의는 AIXON의 경로 계획기에 그대로 옮길 수 있다. 데이터도 필요 없다.
- **위험한 부분.** "상위 개념 성공 → 선수 개념 숙달"이라는 하향 추론은 그래프가 인지 구조를 충실히 반영하고(원저자도 "assuming that the learning space is a faithful representation" 전제를 단다), 동시에 우연 정답이 거의 없을 때만 성립한다. AIXON 상황은 이 조건과 거리가 있다.
  - ML·수학에서는 부분 지식이나 우회 전략으로 상위 문제를 풀 수 있다. 예를 들어 softmax 온도 효과를 직관적으로 맞히면서도 지수함수의 성질은 모를 수 있다.
  - 객관식이나 LLM 채점에서는 우연 정답과 오채점이 있다.
  - AIXON의 단위는 문항이 아니라 '개념×역량 차원'이라 KST의 문항 단위와 1:1로 대응하지 않는다〔추론〕.
- 따라서 하향 추론 결과는 '추정(presumed)' 상태로만 표시하고, 짧은 확인 문항을 거친 뒤에만 건너뛰게 해야 한다(M2 참조).

**구현 라이브러리**

| 패키지 | 버전 | 라이선스 | 비고 |
|---|---|---|---|
| R kst | 0.5-6 (CRAN 2026-10-04) | GPL(≥2) | |
| R pks | 0.8-0 (2026-09-16) | GPL(≥2) | 확률적 지식구조, BLIM 추정 |
| R DAKS | 2.1-3 (2016-06-06) | GPL(≥2) | 오래 갱신되지 않음 |

Python 구현은 이 조사에서 확인하지 않았다. 확인 2026-10-15

**권고: MVP(개념만 차용).** 다음 세 가지를 쓴다.
1. outer fringe 기반의 학습 준비 판정
2. "추정" 상태와 검증 후 건너뛰기
3. 그래프에 대안 선수 경로(OR clause)를 표현할 여지를 남기는 것〔추론〕

확률적 적응형 배치 평가(BLIM)는 개념마다 검증된 문항이 여러 개 쌓인 뒤의 '나중' 과제다.

---

## 6. 간격 반복: FSRS, SM-2, Leitner, 그리고 간격 효과의 근거

### 6.1 FSRS (Free Spaced Repetition Scheduler)

**개요.** 카드마다 기억 상태를 난이도 D(1–10)와 안정성 S로 표현한다. S는 회상 확률 R이 90%가 되는 간격(일)이다. 망각곡선으로 R을 예측하고, 목표 보유율(desired retention)에 맞춰 다음 간격을 정한다. MaiMemo의 DHP/DSR 모형에서 출발했다.

**버전과 파라미터 수.** awesome-fsrs 위키 "The Algorithm"(구 fsrs4anki 위키에서 이전) 기준이다.

| 버전 | 파라미터 수 | 주요 변경 |
|---|---|---|
| FSRS v3 | 13 | |
| FSRS v4 | 17 | |
| FSRS-4.5 | 17 | 망각곡선 형태 변경 |
| FSRS-5 | 19 | 당일(same-day) 리뷰를 학습에 반영 |
| **FSRS-6** | **21** | 당일 리뷰 식 개선, 감쇠 w20을 학습 가능하게 함 |
| FSRS-7 | 34 | srs-benchmark에 결과가 있으나 정식 릴리스는 확인되지 않음 |

FSRS-6의 핵심 식은 다음과 같다.
- 당일 리뷰 후 안정성: S′ = S·e^{w17·(G−3+w18)}·S^{−w19}
- 망각곡선: R(t,S) = (1 + factor·t/S)^{−w20}, factor = 0.9^{−1/w20} − 1. 이렇게 하면 R(S,S)=90%가 된다.

FSRS-7은 srs-benchmark README에 "the newest version … fractional interval lengths … forgetting curve now has 8 optimizable parameters"로 소개돼 있다. fsrs-rs main 브랜치에는 v7 코드 경로(model_v7.rs 등)가 있다. 그러나 fsrs-rs 릴리스 노트, Anki, py-fsrs, ts-fsrs에 정식 탑재됐는지는 **확인되지 않았다**.

**FSRS-6 기본 파라미터.** py-fsrs README와 위키에서 일치한다.
`0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542`

이 기본값이 어떤 절차로 산출됐는지는 1차 문서에서 **확인되지 않았다**. srs-benchmark에 FSRS-6용 pooled pretraining 스크립트가 있다는 사실만 확인했다.

**py-fsrs 스케줄러 기본 설정**
- desired_retention 0.9
- learning_steps (1분, 10분), relearning_steps (10분)
- maximum_interval 36500일
- fuzzing 켜짐
- 시간은 UTC만 지원

**개인 이력 없이 동작하는가: 그렇다.** 기본 파라미터로 바로 스케줄링한다. py-fsrs README도 "If you're not familiar with optimizing FSRS, it is best not to modify these default values."라고 안내한다.

**옵티마이저 요구사항(코드로 직접 확인)**
- **py-fsrs.** `pip install "fsrs[optimizer]"`로 설치하며 PyTorch가 필요하다. `fsrs/optimizer.py`는 Review 상태 리뷰 수가 mini_batch_size=512 미만이면 `DEFAULT_PARAMETERS`를 그대로 반환한다. 최적 보유율 계산은 "at least 512 ReviewLog objects"가 있고 각 로그에 review_duration이 기록돼 있어야 한다.
- **fsrs-rs(Anki가 쓰는 Rust 구현, main 브랜치 `src/training.rs`).** 학습 항목이 8개 미만이면 기본값을 반환한다. 64개 미만이면 초기 안정성 w0–w3만 맞추고 나머지는 기본값을 쓴다.
- **Anki 매뉴얼.** FSRS가 잘 동작하지 않는 이유로 "Low number of reviews (less than a few hundred)"를 든다. desired retention에 대해서는 "The default is 90% … Above 90% the workload increases very quickly, and above 97% the workload can be overwhelming"라고 쓴다. 재최적화는 "once every month is sufficient"라고 한다.

**벤치마크(srs-benchmark README).** 데이터는 Anki 사용자 약 1만 명, 리뷰 약 7.27억 건이다. 당일 리뷰를 제외한 평가 기준(9,999개 컬렉션, 349,923,850 리뷰) 결과는 다음과 같다.

| 모델 | Log Loss | RMSE(bins) | AUC | 비고 |
|---|---|---|---|---|
| FSRS-7 | 0.3401 | | | |
| MOVING-AVG | 0.3369 | | 0.7001 | 시간 정보 없음, 파라미터 0개 |
| FSRS-6 | 0.3460 | 0.0653 | 0.7034 | 사용자별 최적화 |
| FSRS-7 default param. | 0.3620 | | 0.7029 | 사용자별 최적화 없음 |
| AVG | 0.3945 | | 0.4997 | 기준선 |

- 현재 결과표에는 FSRS-6 기본값 행과 SM-2 행이 없다.
- **비판적 해석〔추론〕.** 시간 정보를 전혀 쓰지 않는 MOVING-AVG가 Log Loss에서 FSRS-6보다 낮다. 이는 이 지표의 상당 부분이 사용자 평균 회상률의 추세로 설명된다는 뜻이다. MOVING-AVG로는 간격을 정할 수 없으므로, 예측 지표가 좋다고 곧바로 스케줄링이 좋다는 결론이 나오지는 않는다.
- 기본값 모델은 최적화 모델보다 나쁘지만 기준선 AVG보다는 분명히 낫다.

**FSRS의 가정(비판)**
- 입력은 Again/Hard/Good/Easy 자기평가 버튼이다. 카드는 서로 독립이다. 플래시카드 회상 데이터로 설계되고 평가됐다.
- 개념 간 선수관계는 없다. 선수 개념을 복습해도 하위 카드의 상태가 바뀌지 않는다.
- 개념 이해나 문제 풀이 문항, 특히 매번 다른 변형을 내는 문항에 FSRS의 S/D 모형이 맞는지는 검증되지 않았다〔추론〕.

**관련 1차 문헌**
- Ye, J., Su, J., & Cao, Y. (2022). A stochastic shortest path algorithm for optimizing spaced repetition scheduling. *KDD '22*, 4381–4390. https://doi.org/10.1145/3534678.3539081 (초록 확인: MaiMemo 2.2억 건 로그, 배포됨) 확인 2026-10-15
- Su, J., Ye, J., Nie, L., Cao, Y., & Chen, Y. (2023). Optimizing spaced repetition schedule by capturing the dynamics of memory. *IEEE TKDE*, 35(10), 10085–10097. https://doi.org/10.1109/TKDE.2023.3251721 (초록 확인) 확인 2026-10-15
- FSRS 알고리즘 위키: https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm 확인 2026-10-15
- srs-benchmark: https://github.com/open-spaced-repetition/srs-benchmark 확인 2026-10-15
- Anki 매뉴얼(Deck Options/FSRS): https://docs.ankiweb.net/deck-options.html 확인 2026-10-15
- Anki 23.10 릴리스 노트("Support for FSRS … is now integrated into Anki"): https://github.com/ankitects/anki/releases/tag/23.10. Anki 26.09(2026-09-14)는 fsrs-rs 6.6.2로 갱신했다. 확인 2026-10-15

**open-spaced-repetition 조직과 라이브러리(GitHub API·레지스트리 기준)**

| 저장소/패키지 | 라이선스 | 최신 버전·활동 |
|---|---|---|
| **py-fsrs** (PyPI `fsrs`) | MIT | **6.3.2** (2026-08-09). 6.3.1은 2026-03-10. Python ≥3.10. FSRS-6 구현 |
| **ts-fsrs** (npm) | MIT | **5.4.2** (2026-09-01). README 배지는 FSRS v6. 6.0.0-beta.14(2026-10-09)가 진행 중이며 v6 문서 PR은 Node.js 24+를 요구. 5.x README는 Node.js 20 미만을 지원하지 않음 |
| @open-spaced-repetition/binding (ts용 옵티마이저) | MIT | 0.5.0 (2026-06-06) |
| fsrs-rs (crate `fsrs`) | BSD-3-Clause | 6.6.2 (2026-08-28) |
| fsrs-optimizer | GitHub 기준 BSD-3-Clause | PyPI 6.5.0 (2026-02-02) |
| fsrs4anki | MIT | |
| srs-benchmark | GitHub API에 라이선스 표기 없음 | 2026-10-14 push |
| awesome-fsrs 위키 | CC0-1.0 | |

모두 확인 2026-10-15. 마지막 push는 py-fsrs 2026-08-09, ts-fsrs 2026-10-11, fsrs-rs 2026-10-09로, 세 핵심 저장소 모두 활발히 유지되고 있다.

### 6.2 SM-2

Woźniak, P. A. (1990). *SuperMemo 2: Algorithm*. https://super-memory.com/english/ol/sm2.htm 확인 2026-10-15
- 문항마다 E-Factor 초기값 2.5. I(1)=1일, I(2)=6일, I(n)=I(n−1)·EF(올림)
- 0–5 등급. EF′ = EF + (0.1 − (5−q)·(0.08 + (5−q)·0.02)), EF 하한 1.3
- q<3이면 간격을 처음부터 다시 시작한다(EF는 유지). 그날 4 미만 문항은 4 이상이 나올 때까지 반복한다.
- 평가: 기억 모형이 없는 휴리스틱이다. 자기평가 0–5 등급에 의존하고, 실패 후 처음부터 다시 시작하는 규칙이 거칠다. 개인 데이터 없이 동작하고 설명하기 쉽다는 장점이 있다.

### 6.3 Leitner

Leitner, S. (1972). *So lernt man lernen*. Herder. 초판 연도와 내용은 2차 확인(https://en.wikipedia.org/wiki/Leitner_system)이다. Herder 판의 존재는 Open Library 레코드로 확인했다. 1차 서지 레코드는 DNB 접근 차단으로 확인하지 못했다. 확인 2026-10-15
- 카드를 칸에 넣고, 맞히면 다음 칸으로, 틀리면 첫 칸으로 보낸다. 칸이 뒤로 갈수록 복습 주기가 길다.
- 파라미터 학습이 없고, 가장 투명한 기준선이다.
- py-fsrs README가 같은 조직의 sm-2, leitner-box 파이썬 패키지를 소개하고 있다.

### 6.4 간격 효과·교차 연습의 근거

- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354–380. https://doi.org/10.1037/0033-2909.132.3.354. 184편 논문, 317개 실험, 839개 평가를 종합했다. 최대 파지를 주는 간격(ISI)은 보유 기간이 길수록 커진다. (초록 확인) 확인 2026-10-15
- Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). Spacing effects in learning: A temporal ridgeline of optimal retention. *Psychological Science*, 19(11), 1095–1102. https://doi.org/10.1111/j.1467-9280.2008.02209.x. 1,350명 이상이 사실 학습에 참여했다. 최적 간격은 1주 시험 지연의 약 20–40%에서 1년 지연의 약 5–10%로 줄어든다. (초록 확인) 확인 2026-10-15
- Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques. *Psychological Science in the Public Interest*, 14(1), 4–58. https://doi.org/10.1177/1529100612453266. 연습 시험과 분산 연습은 "high utility"로 평가됐다. 정교화 질문, 자기설명, 교차 연습은 moderate였다. 요약, 밑줄, 키워드 기억법, 심상, 재독은 low였다. (초록 확인) 확인 2026-10-15
- Rohrer, D., & Taylor, K. (2006). The effects of overlearning and distributed practise on the retention of mathematics knowledge. *Applied Cognitive Psychology*, 20(9), 1209–1224. https://doi.org/10.1002/acp.1266. 대학생 216명이 수학 문제를 학습했다. 분산의 이득은 1주 뒤에는 "nil", 4주 뒤에는 "extremely large"였다. 과잉학습(overlearning)은 효과가 없었다. (초록 확인) 확인 2026-10-15
- Rohrer, D., Dedrick, R. F., & Stershic, S. (2015). Interleaved practice improves mathematics learning. *Journal of Educational Psychology*, 107(3), 900–908. https://doi.org/10.1037/edu0000001. 7학년 126명 대상이다. 교차 연습은 1일 뒤 d=0.42, 30일 뒤 d=0.79의 이득을 보였다. (초록 확인) 확인 2026-10-15

**적용성 비판.** 간격 효과의 증거는 대부분 언어·사실 회상에서 나왔다. Cepeda 2006의 제목부터가 "verbal recall tasks"다. 수학 절차 학습에서의 증거(Rohrer & Taylor 2006)도 있다. 그러나 복잡한 개념 이해에 대한 직접 증거는 적다. 따라서 "개념 숙달을 FSRS 간격으로 관리한다"는 것은 합리적 외삽이지 검증된 설계가 아니다〔추론〕.

### 6.5 권고

- **MVP: FSRS-6 기본 파라미터를 쓴다.** 파이썬 스택이면 py-fsrs 6.3.2, 웹·TS 스택이면 ts-fsrs 5.4.2를 쓰고, ts-fsrs 6.x 베타는 피한다. 원자적 인출 카드(정의, 공식, 핵심 사실, 짧은 예측 문항)를 스케줄한다. 구체 설정은 M3에 있다.
- **나중:** Review 상태 리뷰가 512건 이상 쌓이면 개인 최적화를 시도한다(py-fsrs가 정한 하한). 시간 분할 홀드아웃에서 기본값보다 Log Loss가 개선될 때만 채택한다.
- **SM-2와 Leitner:** 쓰지 않는다. FSRS 라이브러리에 문제가 생길 때 쓸 설명 가능한 대체안으로만 남겨 둔다.

---

## 7. 인출 연습(시험 효과), 사전시험·예측 효과, 생성 효과

**개요.** 정보를 다시 읽는 것보다 기억에서 꺼내 보는 것(시험)이 장기 파지를 높인다. 학습 전에 틀릴 것이 뻔한 질문에 먼저 답해 보는 사전시험도, 정답을 확인할 기회가 이어지면 학습을 돕는다. 답을 스스로 생성하면 읽기만 할 때보다 기억이 좋아진다.

**핵심 1차 문헌과 주요 결과**
- Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning. *Psychological Science*, 17(3), 249–255. https://doi.org/10.1111/j.1467-9280.2006.01693.x. 5분 뒤 시험에서는 재학습이 더 나았다. 2일 뒤와 1주 뒤 시험에서는 "prior testing produced substantially greater retention than studying"이었다. 그런데 재학습 집단의 자신감이 더 높았다. (초록 확인) 확인 2026-10-15
- Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. *Psychological Bulletin*, 140(6), 1432–1463. https://doi.org/10.1037/a0037559. 초록 기준으로 회상형 시험이 재인형보다 이득이 컸다. 전체 효과 g≈0.50(효과크기 159개)은 2차 확인이다. 확인 2026-10-15
- Adesope, O. O., Trevisan, D. A., & Sundararajan, N. (2017). Rethinking the use of tests: A meta-analysis of practice testing. *Review of Educational Research*, 87(3), 659–701. https://doi.org/10.3102/0034654316689306. 초록 기준으로 연습 시험이 재학습을 포함한 모든 비교 조건보다 나았다. 전체 g≈0.61은 2차 확인이고, 재학습 대비 수치는 **확인되지 않음**. 확인 2026-10-15
- Karpicke, J. D., & Blunt, J. R. (2011). Retrieval practice produces more learning than elaborative studying with concept mapping. *Science*, 331(6018), 772–775. https://doi.org/10.1126/science.1199327. 추론 문항에서도, 최종 시험이 개념도 작성일 때도 인출 연습이 우세했다. (초록 확인) 확인 2026-10-15
- **경계 조건 논쟁**
  - van Gog, T., & Sweller, J. (2015). Not new, but nearly forgotten: the testing effect decreases or even disappears as the complexity of learning materials increases. *Educational Psychology Review*, 27(2), 247–264. https://doi.org/10.1007/s10648-015-9310-x (초록 확인) 확인 2026-10-15
  - Karpicke, J. D., & Aue, W. R. (2015). The testing effect is alive and well with complex materials. *Educational Psychology Review*, 27(2), 317–326. https://doi.org/10.1007/s10648-015-9309-3 (서지만 확인) 확인 2026-10-15
- Kornell, N., Hays, M. J., & Bjork, R. A. (2009). Unsuccessful retrieval attempts enhance subsequent learning. *JEP: LMC*, 35(4), 989–998. https://doi.org/10.1037/a0015729. 허구의 상식 문항과 약한 연상어로 실험했다. 실패한 인출 시도도 이후 학습을 높였다. (초록 확인) 확인 2026-10-15
- Richland, L. E., Kornell, N., & Kao, L. S. (2009). The pretesting effect: Do unsuccessful retrieval attempts enhance learning? *JEP: Applied*, 15(3), 243–257. https://doi.org/10.1037/a0016496. 사전시험에서 틀린 문항만 분석해도 사후시험 성적이 더 좋았다. 단순한 주의 유도 효과는 통제했다. (초록 확인) 확인 2026-10-15
- Pan, S. C., & Carpenter, S. K. (2023). Prequestioning and pretesting effects: a review…. *Educational Psychology Review*, 35(4), Article 97. https://doi.org/10.1007/s10648-023-09814-5. 정답을 학습할 기회가 뒤따를 때 효과가 나타나고, 절차와 평가 방식에 따라 크기가 달라진다. (초록 확인) 확인 2026-10-15
- Slamecka, N. J., & Graf, P. (1978). The generation effect: Delineation of a phenomenon. *JEP: Human Learning and Memory*, 4(6), 592–604. https://doi.org/10.1037/0278-7393.4.6.592 (서지 확인) 확인 2026-10-15
- Bertsch, S., Pesta, B. J., Wiscott, R., & McDaniel, M. A. (2007). The generation effect: A meta-analytic review. *Memory & Cognition*, 35(2), 201–210. https://doi.org/10.3758/BF03193441. 86개 연구, 효과크기 445개를 종합했고 전체 효과는 .40이었다(PubMed 초록 https://pubmed.ncbi.nlm.nih.gov/17645161/, 2차 경유 확인). 확인 2026-10-15
- **예측 효과**
  - Brod, G. (2021). Predicting as a learning strategy. *Psychonomic Bulletin & Review*, 28(6), 1839–1847. https://doi.org/10.3758/s13423-021-01904-1. 예측은 단순한 인출과 구별된다. 예상과 다른 답에 대한 놀람이 주의와 부호화를 강화한다고 본다. 추측(guessing)과도 구별된다. (초록 확인) 확인 2026-10-15
  - Brod, G., Hasselhorn, M., & Bunge, S. A. (2018). When generating a prediction boosts learning: The element of surprise. *Learning and Instruction*, 55, 22–31. https://doi.org/10.1016/j.learninstruc.2018.01.013 (서지만 확인) 확인 2026-10-15
  - Crouch, C. H., Fagen, A. P., Callan, J. P., & Mazur, E. (2004). Classroom demonstrations: Learning tools or entertainment? *American Journal of Physics*, 72(6), 835–838. https://doi.org/10.1119/1.1707018. "students who passively observe demonstrations understand the underlying concepts no better than students who do not see the demonstration at all … students who predict the demonstration outcome before seeing it … display significantly greater understanding." (초록 확인) 확인 2026-10-15

**데이터 요구.** 통계 모형이 아니라 설계 원칙이므로 사용자 데이터가 필요 없다.

**단일 사용자 적용성: 높다.** 비판적으로 짚어 둘 점이 세 가지 있다.
1. 회상형 문항이 재인형보다 효과가 크다(Rowland). 객관식 위주의 recognize 문항으로 복습을 채우면 이득이 줄어든다.
2. 복잡한 자료에서 효과가 줄어드는지는 아직 논쟁 중이다. 유도 같은 고상호작용 문항은 인출 연습만으로 충분하지 않을 수 있으므로, 풀이 예제와 피드백을 함께 줘야 한다〔추론〕.
3. 사전시험과 예측은 정답 피드백이 이어질 때만 이득이 있다. 사전시험의 오답을 숙달 감점이나 진도 차단에 쓰면 안 되고, 기저선 증거로만 써야 한다〔추론〕.

**권고: MVP(설계 원칙).**
- 모든 복습은 다시 읽기가 아니라 인출 형태로 만든다.
- 레슨 앞에 2–3문항짜리 사전질문을 두고 피드백을 준다.
- 랩에서는 조작하기 전에 예측하게 한다.
- derive와 explain 차원은 생성형 과제(빈칸 유도, 자기설명)로 연습시킨다.

---

## 8. ICAP 틀 (Chi & Wylie 2014)

**개요.** 학습자의 겉으로 드러난 행동으로 인지적 관여를 네 모드로 나눈다.
- Passive: 주의를 기울여 받아들임
- Active: 조작적(manipulative) 행동
- Constructive: 주어진 정보를 넘어서는 산출물을 생성함
- Interactive: 상대와 함께 생성(co-generative)함

ICAP 가설은 학습 성과가 I > C > A > P 순이라고 예측한다.

**핵심 문헌**
- Chi, M. T. H., & Wylie, R. (2014). The ICAP framework: Linking cognitive engagement to active learning outcomes. *Educational Psychologist*, 49(4), 219–243. https://doi.org/10.1080/00461520.2014.965823. 필기, 개념도, 자기설명 연구로 검증했다. 산출물 평가와 적절한 통제 조건 선택에 ICAP을 쓰자고 제안한다. (초록 확인) 확인 2026-10-15
- Chi, M. T. H. (2009). Active-constructive-interactive: A conceptual framework for differentiating learning activities. *Topics in Cognitive Science*, 1(1), 73–105. https://doi.org/10.1111/j.1756-8765.2008.01005.x (초록 확인) 확인 2026-10-15
- Chi, M. T. H., et al. (2018). Translating the ICAP theory of cognitive engagement into practice. *Cognitive Science*, 42(6), 1777–1832. https://doi.org/10.1111/cogs.12626. Active와 Passive를 "manipulative and attentive behaviors"로 규정한다. 교사들은 "had minimal success in designing Constructive and Interactive activities"였지만, 학생들은 Constructive 맥락에서 Active보다 유의하게 더 많이 학습했다. (초록 확인) 확인 2026-10-15

**"슬라이더 조작은 학습의 증거가 아니다"와의 관계**
- 슬라이더를 움직이는 것은 정의상 Active, 곧 조작적 행동이다. ICAP은 관여 모드와 학습 성과 사이의 관계를 다루는 이론이고, 관여 자체를 성과 측정으로 보지 않는다. 따라서 조작 로그는 학습 증거가 될 수 없다. 이 결론은 ICAP의 정의에서 바로 나온다.
- 조작 전 예측, 조작 후 설명, 새 조건에서의 예측처럼 학습자가 무언가를 생성하는 단계를 넣어야 Constructive가 된다. 이 산출물들은 채점할 수 있으므로 증거가 된다.
- Crouch et al.(2004)의 결과는 이 구분을 실증적으로 뒷받침한다. 수동 관찰은 시연을 보지 않은 것과 차이가 없었고, 먼저 예측한 집단은 더 많이 이해했다.
- LLM 튜터와의 대화가 ICAP의 Interactive, 즉 동료와 함께 생성하는 모드에 해당하는지는 **확인되지 않았다**. 원 틀은 사람 대 사람을 기준으로 정의돼 있다.

**권고: MVP(증거 규칙).**
- 랩 텔레메트리(조작 횟수, 체류 시간)는 관여 지표로만 저장하고 숙달 갱신에는 절대 쓰지 않는다.
- 증거는 채점 가능한 Constructive 산출물에서만 만든다.

---

## 9. 자기평가 정확도

**핵심 문헌과 결과**
- Zell, E., & Krizan, Z. (2014). Do people have insight into their abilities? A metasynthesis. *Perspectives on Psychological Science*, 9(2), 111–125. https://doi.org/10.1177/1745691613518075. 메타분석 22편을 종합했다. 자기평가와 수행의 상관은 평균 M=.29(SD=.11), 범위 .09–.63이었다. 영역이 구체적일 때, 과제가 객관적이거나 익숙하거나 덜 복잡할 때 상관이 더 강했다. (초록 확인) 확인 2026-10-15
- Kruger, J., & Dunning, D. (1999). Unskilled and unaware of it. *JPSP*, 77(6), 1121–1134. https://doi.org/10.1037/0022-3514.77.6.1121 (서지 확인) 확인 2026-10-15
- **통계적 인공물이라는 비판**
  - Nuhfer, E., et al. (2016). Random number simulations reveal how random noise affects the measurements and graphical portrayals of self-assessed competency. *Numeracy*, 9(1). https://doi.org/10.5038/1936-4660.9.1.4 (서지 확인) 확인 2026-10-15
  - Gignac, G. E., & Zajenkowski, M. (2020). The Dunning-Kruger effect is (mostly) a statistical artefact…. *Intelligence*, 80, 101449. https://doi.org/10.1016/j.intell.2020.101449. 사분위 그래프 방법은 평균 이상 효과와 평균으로의 회귀로 교란된다. N=929 표본에서 DK 가설이 예측하는 이분산성을 찾지 못했다. (초록 확인) 확인 2026-10-15
- Rozenblit, L., & Keil, F. (2002). The misunderstood limits of folk science: an illusion of explanatory depth. *Cognitive Science*, 26(5), 521–562. https://doi.org/10.1207/s15516709cog2605_1. 착각은 사실, 절차, 서사보다 설명적 지식에서 훨씬 강했고, "most robust where the environment supports real-time explanations with visible mechanisms"였다(초록 확인). 실험 절차는 이해도를 평정하게 한 뒤 설명을 쓰게 하고 다시 평정하게 하는 방식이었고, 재평정에서 점수가 떨어졌다(2차 확인). 확인 2026-10-15
- Koriat, A., & Bjork, R. A. (2005). Illusions of competence in monitoring one's knowledge during study. *JEP: LMC*, 31(2), 187–194. https://doi.org/10.1037/0278-7393.31.2.187. 학습판단(JOL)은 시험 때는 없을 정보가 눈앞에 있는 상태에서 이뤄지기 때문에 유능감 착각이 생긴다. (초록 확인) 확인 2026-10-15
- Reder, L. M., & Ritter, F. E. (1992). What determines initial feeling of knowing? Familiarity with question terms, not with the answer. *JEP: LMC*, 18(3), 435–451. https://doi.org/10.1037/0278-7393.18.3.435. 제목이 결론이다: 안다는 느낌은 답이 아니라 질문 용어의 친숙도에서 온다. (초록 일부 확인) 확인 2026-10-15
- Dunlosky, J., & Rawson, K. A. (2012). Overconfidence produces underachievement: Inaccurate self evaluations undermine students' learning and retention. *Learning and Instruction*, 22(4), 271–280. https://doi.org/10.1016/j.learninstruc.2011.08.003. 초록은 출판사가 비공개로 처리해 **직접 확인하지 못했다**. 과신이 조기 학습 종료와 낮은 파지로 이어진다는 내용은 제목과 2차 서술로만 확인했다. 확인 2026-10-15
- Deslauriers, L., McCarty, L. S., Miller, K., Callaghan, K., & Kestin, G. (2019). Measuring actual learning versus feeling of learning in response to being actively engaged in the classroom. *PNAS*, 116(39), 19251–19257. https://doi.org/10.1073/pnas.1821936116. 능동 수업 집단이 실제로 더 많이 배웠지만, 배웠다는 느낌은 더 낮았다. (초록 확인) 확인 2026-10-15
- Butterfield, B., & Metcalfe, J. (2001). Errors committed with high confidence are hypercorrected. *JEP: LMC*, 27(6), 1491–1494. https://doi.org/10.1037/0278-7393.27.6.1491 (서지 확인) 확인 2026-10-15

**비판적 정리**
- Dunning-Kruger 효과는 그 형태와 크기가 통계적 인공물 논쟁 속에 있다. 그러나 AIXON 설계에 필요한 결론은 DK 효과에 의존하지 않는다. "자기평가는 실제 수행과 중간 정도로만 상관한다(r≈.29)"는 결론은 메타종합으로 견고하다.
- **AIXON에서 특히 위험한 조합〔추론〕.** 메커니즘이 눈에 보이는 인터랙티브 랩(Rozenblit & Keil)과, 정답 정보가 화면에 있을 때 하는 자기평정(Koriat & Bjork)이 겹치면 과대평가가 가장 커질 것으로 예상된다.

**권고: MVP(배제 규칙)**
- 자기보고("익숙함", "이해함")는 숙달을 갱신하지 않는다.
- 쓸 수 있는 용도는 두 가지다.
  - **진단 트리거.** 사용자가 "안다"고 하면 1–3문항 확인 퀴즈를 내고, 통과하면 건너뛴다.
  - **답안별 확신도.** 확신도를 함께 받아 높은 확신의 오답을 오개념 신호로 표시하고 교정 피드백을 우선한다(hypercorrection). 확신도와 정답률을 나란히 보여주는 보정(calibration) 피드백도 줄 수 있다〔추론: 설계 응용〕.

---

## 10. 완전학습과 실제 시스템의 숙달 기준

**원전과 효과 근거**
- Bloom, B. S. (1968). Learning for mastery. *Evaluation Comment*, 1(2). UCLA CSEIP. ERIC ED053419: https://eric.ed.gov/?id=ED053419. ERIC 초록 확인. 다른 서명 표기로 "Mastery Learning"도 쓰인다. "Most students, perhaps over 90 percent, can master what teachers have to teach them". 적성(필요 학습시간), 수업의 질, 수업 이해력, 인내, 허용 시간이라는 5변수를 제시했다. 확인 2026-10-15
- Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective as one-to-one tutoring. *Educational Researcher*, 13(6), 4–16. https://doi.org/10.3102/0013189X013006004. Anania와 Burke의 학위논문을 근거로 전통 수업, 완전학습, 개인교습 세 조건을 비교했다. (초록 확인) 확인 2026-10-15
- Kulik, C.-L. C., Kulik, J. A., & Bangert-Drowns, R. L. (1990). Effectiveness of mastery learning programs: A meta-analysis. *Review of Educational Research*, 60(2), 265–299. https://doi.org/10.3102/00346543060002265. 통제 평가 108건을 종합했다. 시험 성적에 긍정 효과가 있었고, 하위권 학생에게 더 강했다. 학습 시간이 늘 수 있고, "self-paced mastery programs often reduce the completion rates in college classes"였다. 흔히 인용되는 평균 효과 0.52가 이 1990 논문의 수치인지는 **확인되지 않음**이다. 1986 논문의 수치일 가능성이 있다. (초록 확인) 확인 2026-10-15
- Slavin, R. E. (1987). Mastery learning reconsidered. *Review of Educational Research*, 57(2), 175–213. https://doi.org/10.3102/00346543057002175. 4주 이상 진행된 집단 기반 완전학습은 표준화 성취도 측정에서 "essentially no evidence"를 보였다. 연구자가 만든 측정에서는 중간 정도의 긍정 효과가 있었고, 유지 증거는 약했다. (초록 확인) 확인 2026-10-15
- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. *Educational Psychologist*, 46(4), 197–221. https://doi.org/10.1080/00461520.2011.611369. 인간 개인교습은 d=0.79로, 흔히 믿는 2.0이 아니었다. ITS는 0.76이었다. (초록 확인) 확인 2026-10-15
- von Hippel, P. T. (2024). Two-sigma tutoring: Separating science fiction from science fact. *Education Next*, 24(2), 22–31. https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science/. 동료심사 학술지가 아닌 정책 매체지만 저자는 연구자다. 요지는 다음과 같다. 2σ는 3주 실험과 방금 배운 내용의 좁은 시험에서 나왔다. 추가 시험과 피드백, 튜터 훈련, 수업 대체, 추가 시간이 섞여 있었다. "have never been replicated". 확인 2026-10-15

**실제 시스템의 숙달 기준(공식 문서)**
- **ASSISTments Skill Builders.** https://www.assistments.org/individual-resource/skillbuilders 확인 2026-10-15
  - "determine if students have mastered … by seeing if they can answer three questions in a row correctly"
  - "If a student answers incorrectly or uses a hint, the stars explode and reset to zero."
  - "If a student does not get three stars in a row within 10 questions, a limit message appears."
- **Kelly, K., Wang, Y., Thompson, T., & Heffernan, N. (2015).** Defining mastery: Knowledge tracing versus N-consecutive correct responses. *EDM 2015*, 630–631. https://www.educationaldatamining.org/EDM2015/proceedings/poster630-631.pdf. 다음 문항 정답 예측에서는 N-CCR이 KT보다 정확했다. "a threshold of 3 consecutive correct responses provides adequate practice"였고, 전이 문항 예측은 N이 클수록 정확했다. (본문 확인) 확인 2026-10-15
- **Khan Academy.** "How do Khan Academy's Mastery levels work?" https://support.khanacademy.org/hc/en-us/articles/5548760867853 (2026-10-09 갱신본, Zendesk API로 본문 확인) 확인 2026-10-15
  - Attempted: 연습에서 70% 미만 정답
  - Familiar: 70–99% 정답
  - Proficient: 100% 정답
  - **Mastered: Proficient 상태에서 혼합 기능 평가(mixed-skill assessment), 곧 단원 시험이나 코스 챌린지를 맞혀야 한다.** 틀리면 단계가 내려간다.
  - "How is my mastery percentage calculated?" https://support.khanacademy.org/hc/en-us/articles/48411237993357. Proficient와 Mastered만 숙달 비율에 포함된다. 확인 2026-10-15
- **Cognitive Tutor 계열 BKT.** "this model is also often used in practice with a standard mastery threshold 0.95"(Pelánek & Řihák 2018의 서술).

**Pelánek의 숙달 기준 연구**
- Pelánek, R., & Řihák, J. (2017). Experimental analysis of mastery learning criteria. *UMAP '17*, 156–163. https://doi.org/10.1145/3079628.3079667. "the choice of data sources used for mastery decision and setting of thresholds are more important than the choice of a learner modeling technique … a simple exponential moving average method is a suitable technique for mastery criterion." (초록 확인) 확인 2026-10-15
- Pelánek, R., & Řihák, J. (2018). Analysis and design of mastery learning criteria. *New Review of Hypermedia and Multimedia*, 24(3), 133–159. https://doi.org/10.1080/13614568.2018.1476596. 프리프린트: http://www.fi.muni.cz/~xpelanek/publications/nrhm-mastery.pdf (본문 확인) 확인 2026-10-15
  - EMA 정의: θ0=0, θk = α·θk−1 + (1−α)·ck, θk ≥ T이면 숙달
  - NCC의 단점: 오타 하나에도 0부터 다시 시작해 의욕을 떨어뜨릴 수 있다.
  - "Even small changes in thresholds can have large impact on learners practice"
  - 연습 맥락에서는 거짓 음성(불필요한 과잉연습)을 피해야 하고, 고부담 맥락에서는 거짓 양성을 피해야 한다.
  - 임계값은 effort-score 그래프로 정한다. 실제 운영 시스템에서는 α=0.9를 썼다.
- Pelánek, R. (2018). Conceptual issues in mastery criteria: Differentiating uncertainty and degrees of knowledge. *AIED 2018*, LNCS, 450–461. https://doi.org/10.1007/978-3-319-93843-1_33. 초록은 Masaryk 대학 기록(https://www.muni.cz/en/research/publications/1448696)으로 확인했다. 흔히 쓰는 기준은 "the degree of achieved knowledge and the uncertainty of the estimate"를 하나의 임계값 비교로 섞어 버린다. 확인 2026-10-15

**EMA의 동작〔추론: 계산〕.** θ0=0에서 시작할 때 임계값에 도달하는 데 필요한 연속 정답 수는 다음과 같다.

| α \ T | 0.6 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|
| 0.6 | 2 | 3 | 4 | 5 |
| 0.7 | 3 | 4 | 5 | 7 |
| 0.8 | 5 | 6 | 8 | 11 |
| 0.9 | 9 | 12 | 16 | 22 |

α=0.9는 처음부터 시작하면 문항이 많이 필요하다. 성인 단일 사용자에게는 α=0.6–0.7이 현실적이다.

**단일 사용자 적용성.** 규칙 기반 기준은 데이터 없이 동작하고 설명하기 쉬워서 가장 적합하다. 다만 임계값을 데이터로 맞출 수 없으니, 처음에는 보수적인 기본값을 두고 그 근거를 기록해 두는 것이 중요하다. 자기주도형 완전학습이 완료율을 낮춘다는 결과(Kulik 1990)는 사용자가 1명인 자발적 시스템에서 과잉연습 비용이 곧 이탈로 이어진다는 경고로 읽어야 한다.

**권고: MVP.** "연속 정답 3회(서로 다른 문항, 힌트 없음, 첫 시도) + 지연 검증 1회"를 쓰고, 수준과 불확실성을 분리해 표시한다. 구체 규칙은 M2에 있다.

---

## 11. 개념 학습용 인터랙티브 시뮬레이션 (PhET 등)

**핵심 문헌과 결과**
- Wieman, C. E., Adams, W. K., & Perkins, K. K. (2008). PhET: Simulations that enhance learning. *Science*, 322(5902), 682–683. https://doi.org/10.1126/science.1161948. PhET 연구 프로그램 개관이다. (서지 확인) 확인 2026-10-15
- Adams, W. K., Reid, S., LeMaster, R., McKagan, S. B., Perkins, K. K., Dubson, M., & Wieman, C. E. (2008). A study of educational simulations Part I – Engagement and learning. *Journal of Interactive Learning Research*, 19(3), 397–419. 서지 기록: https://jila.colorado.edu/bibcite/reference/2239. 아카이브본: https://phet.colorado.edu/publications/archive/PhET%20interview%20Paper%20Part%20I.htm (아카이브본 확인) 확인 2026-10-15
  - 수백 건의 개별 학생 인터뷰에 기반한 정성 연구다.
  - "Students engage in exploration and sense-making only after they begin to interact with the simulation."
  - 안내는 고정 대본이 아니라 질문, 특히 예측 질문 형태일 때 탐구에 초점을 준다.
  - "Features can be so much fun to play with that students are distracted from learning."
  - 기대와 다른 결과가 나오자 학생들이 시뮬레이션을 그대로 믿었다(오해를 부른 기본 설정의 사례). "Every feature adds to a student's cognitive load and so needs to have educational purpose."
- Podolefsky, N. S., Perkins, K. K., & Adams, W. K. (2010). Factors promoting engaged exploration with computer simulations. *PRST-PER*, 6(2), 020117. https://doi.org/10.1103/PhysRevSTPER.6.020117. 명시적 안내가 적어도 탐구가 일어났다. 이를 지지한 것은 시뮬레이션의 실세계 연결, 보이지 않는 것의 표상, 비유, 실시간 피드백이었다. (초록 확인) 확인 2026-10-15
- Finkelstein, N. D., et al. (2005). When learning about the real world is better done virtually…. *PRST-PER*, 1(1), 010103. https://doi.org/10.1103/PhysRevSTPER.1.010103. 시뮬레이션 집단이 개념 조사에서도, 실제 회로를 조립하고 설명하는 과제에서도 실물 장비 집단을 앞섰다. (초록 확인) 확인 2026-10-15
- Chamberlain, J. M., Lancaster, K., Parson, R., & Perkins, K. K. (2014). How guidance affects student engagement with an interactive simulation. *Chemistry Education Research and Practice*, 15(4), 628–638. https://doi.org/10.1039/C4RP00009A. n=210. 탐색형 기능의 사용 비율은 가벼운 안내 85%, 중간 68%, 무거운 안내 9%였다(p<0.0005). 안내가 가벼운 집단이 더 많이 탐색했고, 1주 뒤 다시 그리기 과제로 보아 상호작용에 주의를 기울였다. 주 측정은 클릭 데이터와 수업 관찰에 기반한 관여였다. 표준화된 학습 성과 검사는 초록에 언급되지 않았다. (초록 확인) 확인 2026-10-15
- **안내와 발견학습 메타분석**
  - Alfieri, L., Brooks, P. J., Aldrich, N. J., & Tenenbaum, H. R. (2011). Does discovery-based instruction enhance learning? *Journal of Educational Psychology*, 103(1), 1–18. https://doi.org/10.1037/a0021017. 비보조 발견학습은 명시적 교수보다 불리했다(d=−0.38, 580개 비교). 보강된 발견학습(피드백, 풀이 예제, 스캐폴딩, 설명 유도)은 유리했다(d=0.30, 360개 비교). 초록 수치는 저자 PDF(https://www.fisme.science.uu.nl/publicaties/literatuur/2011_alfieri_discovery_learning.pdf)의 검색 결과로 확인했다. 확인 2026-10-15
  - Lazonder, A. W., & Harmsen, R. (2016). Meta-analysis of inquiry-based learning: Effects of guidance. *Review of Educational Research*, 86(3), 681–718. https://doi.org/10.3102/0034654315627366. 연구 72편을 종합했다. 안내는 학습 활동 d=0.66, 수행 성공 d=0.71, 학습 성과 d=0.50의 효과를 보였다. (초록 확인) 확인 2026-10-15
  - de Jong, T., & van Joolingen, W. R. (1998). Scientific discovery learning with computer simulations of conceptual domains. *Review of Educational Research*, 68(2), 179–201. https://doi.org/10.3102/00346543068002179. 발견학습에서 학습자가 겪는 문제와 그것을 보완하는 교수 지원을 다룬다. (초록 확인) 확인 2026-10-15
  - Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does not work…. *Educational Psychologist*, 41(2), 75–86. https://doi.org/10.1207/s15326985ep4102_1 (서지 확인) 확인 2026-10-15
  - Mayer, R. E. (2004). Should there be a three-strikes rule against pure discovery learning? *American Psychologist*, 59(1), 14–19. https://doi.org/10.1037/0003-066X.59.1.14 (서지 확인) 확인 2026-10-15
  - Chernikova, O., et al. (2020). Simulation-based learning in higher education: A meta-analysis. *Review of Educational Research*, 90(4), 499–541. https://doi.org/10.3102/0034654320933544. 연구 145편, g=0.85였다. 스캐폴딩 효과가 있었고, 사전지식이 높으면 성찰 단계, 낮으면 예제가 도움이 됐다. 의료·교사교육 같은 복잡 기술 중심이라 개념 시뮬레이션에 바로 일반화하기는 어렵다. (초록 확인) 확인 2026-10-15

**효과가 나는 조건 정리**
1. 학습자가 직접 상호작용해야 한다.
2. 탐구를 이끄는 질문과 예측이 있어야 하되, 단계별 지시처럼 무거운 안내는 탐색을 줄인다.
3. 순수한 비안내 발견은 피한다.
4. 개념과 무관한 재미 요소를 넣지 않는다.
5. 기본값이 오개념을 유도하지 않도록 점검한다.

**AIXON softmax 온도·attention 랩에의 함의〔추론〕**

랩을 예측 → 조작 → 설명 → 전이 4단계로 짠다.
- **예측(조작 전):** "T→0이면 분포가 어떻게 되나?" 같은 질문에 먼저 답한다. 이 답은 현재 상태를 보여주는 증거다.
- **조작:** 슬라이더를 움직인다. 텔레메트리만 남긴다.
- **설명:** 짧은 서술형으로 이유를 쓴다. 채점 대상이다.
- **전이(랩 종료 후, 새 수치):** 예를 들어 d_k를 4배로 키우면 √d_k 스케일링이 없을 때 softmax가 어떻게 포화되는지 예측한다. 이것이 학습 증거다.

"메커니즘이 보이는 환경"은 설명 깊이의 착각을 키울 수 있으므로(9절), 랩이 끝난 뒤의 자기평가는 받지 않는다.

**권고: MVP(랩 설계 원칙).** 데이터가 필요 없다. 위 4단계 구조와 "조작 로그 ≠ 증거" 규칙을 적용한다.

---

## 12. 데이터와 텍스트에서 선수관계 학습하기

**핵심 문헌과 보고된 정확도**
- Talukdar, P. P., & Cohen, W. W. (2012). Crowdsourced comprehension: Predicting prerequisite structure in Wikipedia. *BEA Workshop* (NAACL 2012). https://aclanthology.org/W12-2037/. CrowdComp 데이터셋을 만들었다. (서지 확인) 확인 2026-10-15
- Liang, C., Wu, Z., Huang, W., & Giles, C. L. (2015). Measuring prerequisite relations among concepts (RefD). *EMNLP 2015*, 1668–1674. https://doi.org/10.18653/v1/D15-1193 (본문 확인) 확인 2026-10-15
  - CrowdComp, 다섯 도메인 교차 평가(out-of-domain): 평균 정확도는 RefD-TFIDF 61.2%, MaxEnt(재구현) 60.4%였다.
  - 대학 강좌 데이터(in-domain): CS는 정확도 77.1%, F1 75.1%(TFIDF). MATH는 정확도 73.9%, F1 71.9%(EQUAL).
  - 평가 세트는 소수 클래스를 오버샘플링해 균형을 맞췄다. 실제 그래프는 대부분의 쌍이 비선수 관계라서, 실사용 정밀도는 이보다 낮을 수 있다〔추론〕.
- Gordon, J., Zhu, L., Galstyan, A., Natarajan, P., & Burns, G. (2016). Modeling concept dependencies in a scientific corpus. *ACL 2016*, 866–875. https://doi.org/10.18653/v1/P16-1082 (본문 확인) 확인 2026-10-15
  - ACL Anthology 코퍼스에서 토픽 300개 사이의 의존 관계를 추정했다.
  - 상위 20개 간선의 정밀도는 교차엔트로피 방법 0.851, 단어 유사도 0.808이었다. 그런데 **무작위 기준선이 0.659**였다.
  - 의존 관계에 대한 평가자 간 일치도는 Pearson r=0.357(전체), 0.395(NLP 연구자)였다. 사람이 판단한 '정답' 자체가 상당히 불확실하다.
- Pan, L., Li, C., Li, J., & Tang, J. (2017). Prerequisite relation learning for concepts in MOOCs. *ACL 2017*, 1447–1456. https://doi.org/10.18653/v1/P17-1133. Coursera 기반 6개 데이터셋에서 F1 70.2–72.6%였고, 기존 방법 대비 F1이 5.9–48.0% 개선됐다. (본문 Table 3 확인) 확인 2026-10-15
- Li, I., Fabbri, A. R., Tung, R. R., & Radev, D. R. (2019). What should I learn first: Introducing LectureBank for NLP education and prerequisite chain learning. *AAAI 2019*, 33(01), 6674–6681. https://doi.org/10.1609/aaai.v33i01.33016674 (서지 확인) 확인 2026-10-15
- **서베이.** Bai, Y., Liu, Z., Guo, T., Hou, M., & Xiao, K. (2025, online 2025-04-30). Prerequisite relation learning: A survey and outlook. *ACM Computing Surveys*, Article 3733593. https://doi.org/10.1145/3733593. 권·호는 Crossref에 아직 없다. 분류는 지식 개념(KC)과 학습 객체(LO) 두 단위, 그리고 네 가지 방법 유형이다. 평가 방법론과 응용(학습 경로 생성, 교육과정 설계)도 다룬다. (초록 확인) 확인 2026-10-15
- **LLM 기반**
  - Yang, R., et al. (2024). Leveraging large language models for concept graph recovery and question answering in NLP education. arXiv:2402.14293. 학술지·학회 게재 여부는 **확인되지 않음**. LLM 제로샷 개념 그래프 복원이 지도학습 방법과 경쟁력이 있었다("an average 3% F1 score improvement"). https://arxiv.org/abs/2402.14293 (초록 확인) 확인 2026-10-15
  - Li, X., Min, F., Li, M., Zhang, C., & Wang, Z. (2025/2026). AutoPRE: Discovering concept prerequisites with LLM agents. *NLPCC 2025*, LNCS, 199–211. https://doi.org/10.1007/978-981-95-3343-5_16. 성능 수치는 **확인되지 않음**. (서지만 확인) 확인 2026-10-15
  - Aytekin, M. C., & Saygın, Y. (2024, online). Discovering prerequisite relations using large language models. *Interactive Learning Environments*. https://doi.org/10.1080/10494820.2024.2375338. 성능 수치는 **확인되지 않음**. (서지만 확인) 확인 2026-10-15

**데이터 요구.** 텍스트 기반 방법(RefD, 임베딩, LLM)은 학습자 데이터가 필요 없다. 반대로 학습자 수행 데이터에서 선수관계를 발견하는 방법(DKT의 영향 그래프, 연관규칙 등)은 다수 학습자를 전제로 한다.

**단일 사용자 적용성(비판)**
- 텍스트·LLM 기반 후보 제안은 쓸 수 있다.
- 하지만 보고된 성능이 정확도·F1 60–85% 수준이고, 정답 기준(사람 판정)의 일치도도 낮다. 자동 간선을 그대로 넣으면 선수관계가 틀릴 확률이 상당하다.
- 틀린 선수 간선의 비용은 비대칭이다. 거짓 간선은 불필요한 선행학습을 강요하고, 누락 간선은 준비되지 않은 개념을 열어준다〔추론〕.
- 단일 사용자의 수행 데이터로 선수관계를 학습하는 것은 사실상 불가능하다. 개념당 관측이 너무 적고, 학습 순서가 계획기에 의해 정해지기 때문에 교란된다〔추론〕.

**권고: 나중(사람 승인 전제).**
- LLM이나 텍스트로 후보 간선을 제안하고, 출처·근거 문장·신뢰도를 함께 저장한다.
- 사용자가 승인한 간선만 그래프에 반영한다.
- 사용자가 직접 큐레이션한 간선을 정답 집합으로 삼아 precision@k를 주기적으로 측정한다.
- 자동 삽입은 금지한다.

---

## 13. 평가 타당도 기초, 개정 Bloom 분류학, AIXON 역량 차원 대응

**핵심 문헌**
- Hestenes, D., Wells, M., & Swackhamer, G. (1992). Force Concept Inventory. *The Physics Teacher*, 30(3), 141–158. https://doi.org/10.1119/1.2343497 (서지 확인) 확인 2026-10-15
  - PhysPort 기준: 원판 29문항, v95는 30문항이다. 객관식이고, "everyday language and common-sense distractors"를 쓴다. 뉴턴 역학의 가장 기본 개념을 측정하며, 연구 검증 등급은 최고("Gold Star")다. https://www.physport.org/assessments/assessment.cfm?A=FCI 확인 2026-10-15
- Hake, R. R. (1998). Interactive-engagement versus traditional methods…. *American Journal of Physics*, 66(1), 64–74. https://doi.org/10.1119/1.18809. N=6,542, 강좌 62개다. 평균 정규화 이득은 전통 강좌 ⟨g⟩=0.23±0.04, 상호작용 참여 강좌 ⟨g⟩=0.48±0.14였다. (초록 확인) 확인 2026-10-15
- Huffman, D., & Heller, P. (1995). What does the force concept inventory actually measure? *The Physics Teacher*, 33(3), 138–143. https://doi.org/10.1119/1.2344171. Hestenes & Halloun(1995)의 반론은 *The Physics Teacher*, 33(8), 502. https://doi.org/10.1119/1.2344278. 요지는 2차 확인이다. 요인분석에서 문항 간 상관이 느슨해, FCI가 단일 구성개념을 측정하는지 의문을 제기했고, 원저자는 방법론을 반박했다. 확인 2026-10-15
- Adams, W. K., & Wieman, C. E. (2011). Development and validation of instruments to measure learning of expert-like thinking. *International Journal of Science Education*, 33(9), 1289–1312. https://doi.org/10.1080/09500693.2010.512369. 개념검사를 만들고 검증할 때 학생 인터뷰가 핵심이며, 표준 심리측정 절차와 정렬해야 한다. (초록 확인) 확인 2026-10-15
- Messick, S. (1995). Validity of psychological assessment…. *American Psychologist*, 50(9), 741–749. https://doi.org/10.1037/0003-066X.50.9.741. 통합 구성개념 타당도와 여섯 측면(내용, 실질, 구조, 일반화, 외적, 결과)을 제시했다. (초록 확인) 확인 2026-10-15
- National Research Council (2001). *Knowing What Students Know: The Science and Design of Educational Assessment*. National Academies Press. https://doi.org/10.17226/10019. 평가 삼각형(인지·관찰·해석)은 NAP 장 페이지와 2차 인용으로 확인했다. 확인 2026-10-15
- Mislevy, R. J., Steinberg, L. S., & Almond, R. G. (2003). On the structure of educational assessments. *Measurement*, 1(1), 3–62. https://doi.org/10.1207/S15366359MEA0101_02 (초록 확인). 증거중심설계(ECD)의 세 모델(Student / Evidence / Task)은 같은 저자들의 Leverage Points 보고서 본문에서 확인했다: https://www.oerl.sri.com/downloads/mislevy2.pdf. 확인 2026-10-15
- Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman. ISBN 0321084055. Open Library 레코드 (서지만 확인) 확인 2026-10-15
- Krathwohl, D. R. (2002). A revision of Bloom's taxonomy: An overview. *Theory Into Practice*, 41(4), 212–218. https://doi.org/10.1207/s15430421tip4104_2 (본문 확인) 확인 2026-10-15
  - 원 분류학은 "a cumulative hierarchy; that is, mastery of each simpler category was prerequisite to mastery of the next"를 가정했다.
  - 개정판에서는 "the requirement of a strict hierarchy has been relaxed to allow the categories to overlap one another … some cognitive processes associated with Understand (e.g., Explaining) are more cognitively complex than at least one of the cognitive processes associated with Apply (e.g., Executing)."
  - 인지과정 19개: 1.1 Recognizing, 1.2 Recalling / 2.1 Interpreting … 2.7 Explaining / 3.1 Executing, 3.2 Implementing / 4.1 Differentiating, 4.2 Organizing, 4.3 Attributing / 5.1 Checking, 5.2 Critiquing / 6.1 Generating, 6.2 Planning, 6.3 Producing
  - 지식 차원: Factual, Conceptual, Procedural, Metacognitive
- Rittle-Johnson, B., Siegler, R. S., & Alibali, M. W. (2001). Developing conceptual understanding and procedural skill in mathematics: An iterative process. *Journal of Educational Psychology*, 93(2), 346–362. https://doi.org/10.1037/0022-0663.93.2.346. 개념적 지식과 절차적 지식은 순서대로가 아니라 반복적으로, 양방향으로 발달한다. (초록 확인) 확인 2026-10-15
- Seddon, G. M. (1978). The properties of Bloom's taxonomy of educational objectives for the cognitive domain. *Review of Educational Research*, 48(2), 303–323. https://doi.org/10.3102/00346543048002303. 분류학의 위계 속성을 검토한 리뷰다. 결론은 이 조사에서 **직접 확인하지 못했다**. (서지만 확인) 확인 2026-10-15

**기억이 아니라 이해를 측정하는 문항의 조건**

FCI, Adams & Wieman, ECD를 종합했다. 각 항목의 AIXON 적용은 〔추론〕이다.
1. **새 상황.** 학습 중에 본 문항과 수치를 재사용하면 그 문항의 답을 기억하는지를 재게 된다. 매번 변형을 만들고, 지연된 시점에 묻는다.
2. **정량 계산 없이 질적 예측이나 설명을 요구한다.** FCI는 계산이 거의 없다.
3. **알려진 오개념을 오답지로 쓴다.** 예를 들어 "온도를 올리면 최댓값 항목의 확률이 올라간다", "√d_k로 나누는 것은 계산 편의 때문이다".
4. **표상을 바꾼다.** 수식, 그래프, 코드 사이를 오가게 한다.
5. **증거 규칙을 명시한다.** 문항마다 어떤 관찰이 어떤 주장(개념×차원)을 얼마나 지지하는지 적어 둔다(ECD의 Evidence model).
6. **문항 검증.** 생성한 문항이 회상만으로 풀리는지 자체 점검하고, 가능하면 think-aloud로 확인한다. 최소한 "정답 문구를 외워도 풀 수 있는가"를 체크리스트로 둔다.

**AIXON 역량 차원 초안과 개정 Bloom의 대응**

| AIXON 차원 | A&K 인지과정 (Krathwohl 2002 Table 3) | 대응 | 문제점 |
|---|---|---|---|
| recognize | 1.1 Recognizing (Remember) | 정확히 일치 | 객관식이라 추측이 가능해 증거가 약하다. 재노출 문항은 기억을 잰다 |
| explain | 2.7 Explaining (Understand) | 일치 | Explaining은 일부 Apply보다 복잡하다고 명시돼 있어 순서 가정과 충돌한다. 작문 능력이 섞이고 LLM 채점 오류가 있을 수 있다 |
| derive | 단일 대응 없음. 아래 세 경우로 갈림 | 불명확 | 같은 'derive' 문항이 설계에 따라 다른 구성개념을 잰다. 외운 유도를 재현하는 것은 이해의 증거가 아니다 |
| implement | A&K의 3.2 Implementing은 "익숙하지 않은 과제에 절차를 적용"한다는 뜻 | **용어 충돌** | 코드 구현과 의미가 다르다. 프로그래밍 숙련도가 섞이는 것은 Messick이 말한 구성개념 무관 분산이다 |
| analyze | 4.0 Analyze (Differentiating / Organizing / Attributing) | 부분 일치 | ML 맥락의 '분석'(예: 온도에 따른 엔트로피 변화 추론)은 Understand의 Inferring/Explaining이나 Evaluate에 해당할 수 있다 |
| (없음) | 5.0 Evaluate (Checking, Critiquing), 6.0 Create (Generating, Planning, Producing) | **누락** | 연구 학습에 핵심인 능력(논문 주장 검증, 구현 정합성 확인, 실험 설계)이 빠져 있다 |
| (없음) | 지식 차원: Factual / Conceptual / Procedural / Metacognitive | **누락** | 인지과정만 있고 지식 유형 축이 없다 |

'derive'는 문항 설계에 따라 다음 중 하나가 된다.
- 알려진 유도를 재현하는 경우: Remember(Recalling) 또는 Apply(Executing)
- 새로운 유도나 변형을 하는 경우: Apply(Implementing) 또는 Create(Generating, Planning, Producing)
- 유도가 맞는지 검토하는 경우: Evaluate(Checking)

**초안의 구조적 문제**
1. **순서 가정.** recognize < explain < derive < implement < analyze라는 선형 위계는 근거가 약하다.
   - Krathwohl(2002)이 엄격한 위계를 명시적으로 완화했다.
   - 개념적 지식과 절차적 지식은 반복적·양방향으로 발달한다(Rittle-Johnson et al. 2001).
   - 예: softmax를 수치적으로 안정되게 구현(implement)할 수 있으면서 그 야코비안은 유도(derive)하지 못하는 일이 흔하다〔추론〕.
2. **중첩.** 유도는 일종의 설명이고, explain과 analyze의 경계도 모호하다. 차원끼리 상관된 증거를 독립된 숙달로 세면 같은 증거를 여러 번 세게 된다〔추론〕.
3. **단일 라벨 태깅의 비현실성.** 실제 문항은 여러 차원의 증거가 된다. 문항과 (개념, 차원)은 다대다로 매핑하되, 주 차원과 부 차원을 구분해야 한다〔추론〕.
4. **희소성.** 개념 수 × 5차원 셀을 단일 사용자의 증거로 채우기는 어렵다. 개념마다 '목표 차원 프로필'을 두어 2–3개 차원만 활성화하는 편이 현실적이다〔추론〕.

**권고: MVP(문항 설계 기준과 차원 수정)**
- 차원은 순서 없는 증거 채널로 다룬다. 차원 간 선수관계를 가정하지 않는다.
- 'implement'는 'implement-in-code'(코드 구현)로 이름을 바꾸고, 정의와 예시 문항을 명시한다.
- 'evaluate/critique' 차원은 나중에 추가하는 것을 검토한다.
- 개념마다 목표 차원 프로필과 차원별 채점 루브릭을 둔다.

---

## AIXON MVP 권고 (Recommendations for AIXON MVP)

### M1. 아키텍처 원칙

1. **증거 원장(append-only evidence ledger)을 유일한 진실 원천으로 둔다.** 숙달 상태는 원장에서 언제든 다시 계산할 수 있는 파생 뷰로만 존재해야 한다. 그래야 나중에 모델을 바꿔도 전체 이력에 재적용할 수 있고, 시간 분할 오프라인 평가도 할 수 있다〔추론〕.
2. **증거 레코드의 최소 필드〔추론〕.**
   - 타임스탬프(UTC; py-fsrs는 UTC만 지원)
   - item_id, item_variant_id
   - (concept_id, dimension, 가중치) 목록
   - 문항 유형: MCQ, 수치, 서술, 코드, 유도, 예측
   - 맥락: pretest, in-lesson, lab-predict, lab-transfer, review, mixed-assessment
   - 첫 시도 여부, 힌트 사용 여부
   - 결과: 0/1 또는 루브릭 부분점수
   - 채점 주체(auto / LLM / self)와 채점 신뢰도
   - 응답 시간, 확신도(선택)
   - 해당 개념의 마지막 노출 이후 경과 시간
3. **증거가 아닌 것은 숙달 갱신에서 원천 배제한다.**
   - 읽기, 체류 시간, 슬라이더 조작(ICAP의 Active)
   - 자기보고(r≈.29)
   - 힌트를 쓴 시도
   - 같은 세션 안에서 같은 문항을 재시도한 경우

### M2. MVP 학습자 상태 모델: 규칙 기반이고 설명 가능하게

근거는 Pelánek & Řihák 2017/2018, ASSISTments, Kelly et al. 2015, Khan Academy, Roediger & Karpicke 2006, Rohrer & Taylor 2006이다. 구체적인 수치는 〔추론〕이며, 데이터가 쌓이면 재조정한다.

**적격 증거.** 다음 조건을 모두 만족해야 한다.
- 첫 시도이고 힌트가 없다.
- 처음 보는 문항 변형이거나, 마지막으로 본 지 7일 이상 지났다.
- 자동 채점이거나, 검증된 루브릭으로 채점했다.
- LLM이 서술형을 채점한 경우 '약한 증거'로 표시한다. 약한 증거만으로는 숙달에 도달할 수 없고, 적어도 하나는 자동 채점 증거여야 한다.

**(개념, 차원) 상태 전이**

| 상태 | 조건 |
|---|---|
| `none` | 적격 증거 없음 |
| `attempted` | 적격 증거 1건 이상 |
| `provisional` | 적격 증거로 **연속 정답 3회**, 그중 서로 다른 문항 2개 이상 |
| `mastered` | `provisional` 이후 **1일 이상 지나서(가능하면 3일 이상)** 새 변형을 맞힘. 가능하면 여러 개념이 섞인 맥락에서(Khan의 Mastered가 혼합 평가를 요구하는 것과 같은 취지) |
| `needs_review` | `mastered`에서 적격 오답이 나옴. `provisional`로 강등하고 재확인을 스케줄 |

**표시.** 수준과 불확실성을 분리한다(Pelánek 2018).
- 수준: 진행 막대로 EMA(α=0.7)를 보여준다. 처음부터 5연속 정답이면 0.8에 도달한다.
- 불확실성: 적격 증거 수와 마지막 적격 증거 이후 경과일을 별도로 보여준다.
- 연속 정답이 끊겨도 EMA는 완만하게 떨어진다. 이 덕분에 NCC의 "0부터 다시" 문제로 인한 사기 저하가 줄어든다.

**선수관계 처리(KST 차용, 보수적으로)**
- 개념 c를 숙달해도 선수 개념을 `mastered`로 올리지 않는다. 대신 `presumed`로 표시한다.
- `presumed` 상태 개념의 교수(teaching)는 건너뛸 수 있다. 다만 1–2문항짜리 **검증 후 건너뛰기(verify-before-skip)** 확인을 계획기가 반드시 넣는다.
- c에서 실패하면 선수 개념 중 `presumed`/`provisional`인 것부터 상향 진단 문항을 낸다.
- '학습 준비' = 모든 선수 개념이 `mastered`이거나 검증을 통과한 개념. KST의 outer fringe와 같은 개념이다.

**자기보고.** "이미 안다"는 진단 트리거로만 쓴다. 확인 퀴즈를 통과하면 `provisional`로 시작하고, 지연 검증을 거쳐 `mastered`가 된다.

규칙 요약(의사코드):
```
eligible = first_attempt and not hint and (new_variant or days_since_seen >= 7) and grader_ok
streak = consecutive eligible correct (>=2 distinct items within it)
provisional := streak >= 3
mastered    := provisional and later eligible correct on new variant, >= 1 day after provisional
lapse       := mastered and eligible incorrect  -> provisional + schedule recheck
level = EMA(alpha=0.7) over eligible outcomes; uncertainty = (n_eligible, days_since_last)
```

### M3. MVP 복습 스케줄러

- **라이브러리.** FSRS-6 기본 파라미터를 쓴다. 파이썬이면 `fsrs` 6.3.2(MIT), TS면 `ts-fsrs` 5.4.2(MIT)다. 이력 없이 동작하는 것은 공식적으로 지원되는 기본 사용법이다.
- **스케줄 단위.** 원자적 인출 카드를 스케줄한다. 카드는 (개념, 차원)에 연결된 회상형·예측형 짧은 문항이다. 개념의 숙달 상태 자체는 FSRS로 계산하지 않는다. FSRS의 R은 카드 회상 확률이지 개념 숙달이 아니다.
- **평가 매핑〔추론〕.**
  - 적격 오답이나 힌트 사용은 `Again`, 적격 정답은 `Good`으로 바꾼다.
  - Anki의 FSRS 데이터는 버튼 자기평가에 기반한다. AIXON에서는 Hard/Easy를 자기평가로 받지 않는 편이 증거 원칙과 맞는다.
  - 응답 시간 같은 객관적 신호로 Hard/Easy를 만들 수도 있지만, 그 경우 오프라인 비교 후에만 쓴다.
- **설정〔추론〕.**
  - desired_retention은 기본값 0.9로 둔다. Anki 문서는 0.9를 넘기면 작업량이 급증한다고 경고한다. 부담이 크면 0.85로 낮춘다.
  - 기초 개념을 주기적으로 재검증할 수 있도록 maximum_interval을 180–365일로 제한한다.
  - 기본 학습 단계(1분, 10분)는 플래시카드용이다. 개념 문항에서 같은 세션 반복은 즉시 수행만 부풀리므로, learning_steps는 비우거나 짧게 1단계만 둔다.
- **세션 구성.** 기한이 된 카드를 개념을 섞어 낸다(교차 연습: 30일 뒤 d=0.79, Rohrer et al. 2015). 복습할 때마다 문항 변형을 바꿔 답을 외우는 것을 막는다.
- **감사 표본〔추론〕.** 복습의 약 5–10%를 `mastered` 개념 중 무작위 표본으로 채운다. 스케줄러가 약하다고 본 곳만 보는 피드백 루프를 깨기 위해서다.

### M4. 실습 랩 증거 규칙

| 랩 단계 | 산출물 | 증거로 쓰는가 |
|---|---|---|
| 조작 전 예측 | 예측 답 | 사전시험 맥락의 증거. 현재 상태를 나타내며 오답이어도 학습을 돕는다 |
| 슬라이더 조작 | 텔레메트리 | **아님**(Active) |
| 조작 후 설명 | 짧은 서술 | 약한 증거(LLM 채점 시) |
| 새 설정에서의 전이 예측 | 예측 답 | **증거**(in-lesson 맥락) |
| 지연 재검사(다음 날 이후) | 답 | `mastered` 판정에 쓰이는 증거 |

### M5. 복잡한 모델로 넘어가기 위한 최소 데이터와 검증 조건

| 후보 | 1차 문헌의 최소 요구 | AIXON 전환 조건〔추론〕 |
|---|---|---|
| FSRS 개인 최적화 | py-fsrs: Review 상태 리뷰 512건 미만이면 기본값 반환. fsrs-rs: 8개 미만이면 기본값, 64개 미만이면 S0만 적합. Anki: "few hundred" 미만이면 성능 저하 | Review 상태 리뷰 **1,000건 이상**, 사용 기간 3개월 이상. 최근 20% 리뷰로 시간 분할 홀드아웃을 만들어 Log Loss가 기본값보다 개선될 때만 채택. 재최적화는 월 1회 |
| 공유 파라미터 BKT / PFA류 로지스틱 / 고정 난이도 Elo | 다수 학습자를 전제로 함(기능별 적합) | 적격 첫 시도 **약 1,000건 이상**, 개념 50개 이상, 지연 재검사 200건 이상. 문항 유형별 공유 파라미터만 허용. 시간 분할 홀드아웃에서 EMA 규칙보다 Log Loss/AUC가 부트스트랩 신뢰구간 밖으로 개선될 때만 채택 |
| KST 확률적 배치 평가(BLIM) | ALEKS는 대규모 데이터로 보정 | 개념마다 검증된 문항이 3–5개 이상일 때. β, η는 보수적 사전값으로 시작 |
| IRT, Elo 문항 난이도 | Rasch는 문항당 30–100명, 2PL 약 500명, 3PL 약 1,000명, Elo는 100명 이상 | **단일 사용자에게는 해당 없음.** 외부 보정 문항은행을 쓸 때만 |
| DKT | 학습자 1.6만–4.7만 명, 응답 0.5M–1.4M(원 논문 데이터) | **해당 없음** |
| LLM 선수관계 제안 | 정확도·F1 약 60–85%, 사람 간 일치도 낮음 | 언제든 가능하나 제안 전용. 승인 간선 기준 precision@k를 추적 |

원칙: 복잡한 모델은 "논문에서 더 좋았다"가 아니라 **AIXON 자신의 시간 분할 데이터에서 단순 규칙을 이길 때만** 도입한다. 이 근거는 Khajah et al.(2016), Gervet et al.(2020), pyKT(2022)가 보여준 단순 모델의 강세와 평가 함정이다.

### M6. 개인화의 주요 위험과 완화책

1. **선수 개념을 잘못 건너뛰는 거짓 양성 숙달.** 가장 비용이 큰 위험이다.
   - 원인: 객관식 우연 정답, 부분 지식이나 우회 전략에 의한 상위 문제 성공, 반복 문항의 답 암기, LLM 오채점, 자기보고, 랩 관여를 학습으로 착각하는 것
   - 완화:
     - `presumed`와 `mastered`를 분리하고 검증 후에만 건너뛴다.
     - 하류 개념에서 실패하면 상향 진단을 자동으로 건다.
     - 기초 개념(자식 노드가 많은 허브)에는 더 엄격한 임계값을 쓴다〔추론〕.
2. **과잉연습과 이탈(거짓 음성).** 자기주도형 완전학습이 완료율을 낮춘다는 결과가 있다(Kulik 1990).
   - 완화: 기준을 짧게(3+1) 유지하고, 짧은 진단으로 바로 통과할 수 있는 test-out 경로를 둔다.
3. **임계값의 자의성.** 작은 변화도 큰 영향을 준다(Pelánek & Řihák 2018).
   - 완화: 규칙에 버전을 붙여 원장과 함께 기록한다. 데이터가 쌓이면 자기 데이터로 effort-score 분석을 해 재조정한다.
4. **즉시 수행과 파지를 혼동하는 것.**
   - 완화: `mastered`에 지연 증거를 의무화한다(Roediger & Karpicke 2006; Rohrer & Taylor 2006).
5. **차원 측정의 교란.** implement에는 코딩 능력, explain에는 작문 능력과 LLM 채점이 섞인다.
   - 완화: 차원별 루브릭을 두고, 약한 증거만으로 숙달에 도달하지 못하게 한다.
6. **스케줄러 피드백 루프.** 긴 간격 때문에 오래 확인하지 않은 `mastered` 개념이 생긴다.
   - 완화: 최대 간격 제한과 무작위 감사 표본을 둔다.
7. **Goodhart 효과.** 초록 체크 표시를 모으는 것이 목표가 될 수 있다. 사용자가 1명이면 재시도를 반복해 '게임'하기도 쉽다.
   - 완화: 첫 시도만 증거로 인정하고, 불확실성을 함께 표시한다.
8. **불투명성과 모델 드리프트.**
   - 완화: 결정론적 규칙을 쓰고, 원장에서 다시 계산할 수 있게 하며, "왜 이 상태인가"를 증거 목록으로 보여준다.
9. **데이터 손실(로컬 우선 환경).**
   - 완화: 원장을 백업하고 무결성을 검사한다. 시간대는 UTC로 통일한다.

### M7. 열린 질문〔추론〕

- 수학적 개념 문항에서 FSRS의 S/D 모형이 얼마나 맞는지는 AIXON 자체 데이터로 검증해야 한다. 1,000건 이상 쌓인 뒤 보정 곡선을 확인한다.
- LLM 채점의 신뢰도를 어떻게 측정할지 정해야 한다. 예를 들어 일부 서술 답안을 사용자가 재채점해 일치도를 추적할 수 있다.
- 'evaluate/critique' 차원을 언제 도입할지 정해야 한다. 논문 읽기 기능과 함께 도입하는 것이 자연스럽다.

---

## 부록: 확인되지 않음과 한계

- Xiong et al.(2016, EDM, paper_133)의 ASSISTments 중복 레코드 지적과 수치: PDF 텍스트 추출에 실패해 **확인되지 않음**.
- Adesope et al.(2017)의 재학습 대비 효과크기: **확인되지 않음**. 전체 g≈0.61은 2차 확인.
- Kulik et al.(1990)의 평균 효과 0.52: 1990 논문의 수치인지 **확인되지 않음**.
- Dunlosky & Rawson(2012)의 초록과 세부 절차: 출판사가 비공개로 처리해 **확인되지 않음**.
- FSRS-6 기본 파라미터의 산출 절차, FSRS-7의 정식 릴리스와 Anki 탑재 여부: **확인되지 않음**(2026-10-15 기준).
- Seddon(1978)의 결론: **확인되지 않음**.
- Leitner(1972)의 1차 서지 레코드: DNB 접근 차단으로 Open Library와 Wikipedia(2차)로만 확인.
- Corbett & Anderson(1994) 원문: 스캔 PDF라 0.95 임계값을 원문에서 직접 확인하지 못했고, Pelánek & Řihák(2018)의 서술로만 확인했다.
- LLM 기반 선수관계 연구(AutoPRE, Aytekin & Saygın)의 성능 수치: **확인되지 않음**.
- 이 문서의 BKT·EMA 수치표는 문헌 값이 아니라 이 조사자가 직접 계산한 것이다〔추론〕. 계산 가정은 각 표 위에 적었다.

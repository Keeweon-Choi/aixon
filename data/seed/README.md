# data/seed — 검증된 시드 그래프

AIXON의 정확성 기준이 되는 데이터다. 스키마는 [docs/03_DATA_MODEL.md](../../docs/03_DATA_MODEL.md), 의미 규칙과 불변식(G·W)은 [docs/02_DOMAIN_ONTOLOGY.md](../../docs/02_DOMAIN_ONTOLOGY.md)를 따른다.

## 파일

| 파일 | 내용 |
|---|---|
| `seed_graph.yaml` | CNN → Transformer → ViT 계보. 논문 15편, 지식 단위 36개, 학습 자료 73개, 문항 19개, Lab 1개, 학습 목표 2개, **Claim 105개** |
| `learner_e2e.yaml` | E2E용 학습자 상태(P2 학습 엔진 기준 구현 검증용) |
| `expected_plan_e2e.json` | 위 학습자로 `lo:vit-attention-math`를 계획한 정답. 계획기 출력과 별개로 손으로 유도해 맞춤 |
| `lab_fixtures/softmax_temperature.json` | Softmax Temperature Lab 기준값. `tools/gen_lab_fixtures.py`(numpy)가 생성 |

넓은 분야 지도는 [`../graph/atlas.yaml`](../graph/atlas.yaml)(분야 92, 논문 54편)이다. 지도는 시드와 함께 읽어 하나의 그래프로 검증한다.

## Claim 상태 (2026-10-15)

| 상태 | 수 | 의미 |
|---|---|---|
| verified | 95 | 인용 원문이 지정한 버전의 논문에 실제로 있음(근거 132건 대조, 원문 `content_sha256` 고정) |
| disputed | 1 | `clm:bn-mitigates-ics` — 원 논문 주장과 반대 근거(Santurkar et al. 2018)를 함께 둔다 |
| proposed | 8 | 근거가 아직 부족한 후보(설계 감사로 선수 관계 5건을 내림). 공개 그래프·선수 계산에 쓰지 않는다 |
| rejected | 1 | `vgg-extends-alexnet` — 검토에서 기각. 다시 제안되지 않도록 남긴다 |

**verified는 "사람이 공개 승인했다"는 뜻이 아니다.** 인용이 원문과 일치함을 기계로 확인했다는 뜻이다. 공개 승인은 사람이 `tools/review.py`로 기록하는 `review`(내용 해시 포함)로 따로 관리한다(ADR-021, ADR-022).

## 검증

```bash
.venv/bin/python tools/seedtool.py validate data/seed/seed_graph.yaml data/graph/atlas.yaml   # G 오류 0이어야 함
.venv/bin/python tools/seedtool.py quotes --offline --cache data/cache/fulltext data/seed/seed_graph.yaml  # 캐시가 있을 때
.venv/bin/python tools/verify_identifiers.py data/seed/seed_graph.yaml data/graph/atlas.yaml  # 네트워크 필요
.venv/bin/python -m pytest tools/test_seedtool.py
```

## 수정 규칙

- ID는 바꾸지 않는다(그래프·Wiki·URL이 ID로 묶인다). 지울 때는 `rejected`로 남긴다.
- 식별자(arXiv ID 등)는 반드시 따옴표로 감싼 문자열로 쓴다(I-03, G021).
- 인용(`quote`)은 원문에서 그대로 복사한다. 요약하거나 고치지 않는다. 바꾼 뒤에는 `quotes`를 다시 돌린다.
- LLM이 쓴 내용은 `*_by: agent:*`로 표시하고, 검증 전에는 verified로 올리지 않는다.

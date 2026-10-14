# 04. Personalized Learning Engine

> 학습자 모델, 증거 기반 숙련도 갱신, 결정적(deterministic) 학습 경로 계획을 정의한다. 계획기가 쓰는 그래프 의미는 [02 §6.1](02_DOMAIN_ONTOLOGY.md#61-prerequisite-graph의-형식-의미), 저장은 [03 §4](03_DATA_MODEL.md#4-개인-데이터-sqlite-스키마).
> 작성 2026-10-15 · 상태: MVP 설계안 v1 · `algorithm_version: planner-v1`, `rule_version: mastery-v1`

---

## 1. 요구사항과 원칙

| 원칙 | 구체화 |
|---|---|
| **증거 기반** | 숙련도를 바꾸는 것은 **평가 문항 응답**뿐이다. 자료를 열거나 읽음 표시를 하거나 Lab 슬라이더를 움직인 것은 기록만 하고 숙련도는 바꾸지 않는다 |
| **자기보고는 신호일 뿐** | "안다"는 자기보고는 `claimed` 표시만 하고, 계획기는 이것을 **짧은 진단 문항**으로 바꾼다. 자기보고만으로 선수 단계를 생략하지 않는다 |
| **결정적** | 같은 그래프 버전, 같은 학습자 상태, 같은 옵션이면 바이트 단위로 같은 계획이 나온다. LLM을 쓰지 않는다 |
| **설명 가능** | 모든 단계와 생략에는 구조화된 이유가 붙는다(어떤 Claim 때문에 필요한지, 어떤 응답 때문에 생략했는지) |
| **사용자 자율** | 학습자는 언제든 단계를 직접 생략(override)할 수 있다. 시스템은 이것을 숙련으로 기록하지 않고 "본인 선택으로 생략"으로 표시한다 |
| **작은 데이터에 맞는 단순함** | 사용자가 한 명이고 데이터가 거의 없다. 통계 모델(BKT, IRT, DKT)은 적합할 데이터가 없으므로 설명 가능한 규칙을 쓴다(§7) |

---

## 2. Learner Model

| 구성요소 | 표현 | 저장(03 §4) | 단계 |
|---|---|---|---|
| Concept Mastery | `(unit, dimension)`마다 범주형 상태: `unknown · claimed · practicing · mastered · needs_review` | `mastery_state`(파생) | P0 |
| Competency Dimension | recognize · explain · derive · implement · analyze (02 §5) | 상태의 키 | P0 |
| Self-reported Familiarity | 단위별 0~4. 0 처음 봄 · 1 들어 봄 · 2 대략 앎 · 3 설명할 수 있음 · 4 유도·구현할 수 있음 | `learning_event(self_report)` → `mastery_state.self_report` | P0 |
| Assessment Evidence | 문항 응답(정오, 힌트 사용, 문맥, 시각) | `assessment_attempt`(추가만) | P0 |
| Mastery Confidence | 서열 `low · medium · high`. **확률 아님** | `mastery_state.confidence` | P0 |
| Learning History | 이벤트 + 응답 | `learning_event`, `assessment_attempt` | P0 |
| Active Learning Goals | 목표와 현재 계획 | `learning_goal`, `learning_plan` | P0 |
| Reading list | 논문별 읽기 상태 | `paper_status` | P0 |
| Retention / Review State | `needs_review` 상태(P0) + 복습 일정(FSRS, P1) | `mastery_state`, `review_card` | P0/P1 |
| Interest Profile | 명시적 관심 분야 + 방문 기록 | `interest`(P1) | P1 |
| Personal Notes | 메모와 엔티티·Claim 연결 | `note`, `note_link` | P1 |

### 2.1 단일 점수 표현의 한계 (채택하지 않은 이유)

1. **차원을 뭉갠다**: "attention 0.7"은 "설명은 되지만 √d_k 스케일링은 유도하지 못함"을 표현하지 못한다. 경로 계획은 차원별 상태가 있어야 맞게 동작한다(02 §6.1).
2. **증거의 질을 숨긴다**: 객관식 하나를 맞힌 0.7과 수치 문제 셋을 맞힌 0.7이 같아 보인다.
3. **"주장했지만 확인 안 됨"을 표현하지 못한다**: 자기보고와 평가 결과가 한 숫자에 섞인다.
4. **가짜 정밀도**: 보정 데이터 없이 0.73 같은 숫자를 보여 주면 측정한 것처럼 보이지만 실제로는 측정하지 않았다.

그래서 내부 표현은 **차원별 범주형 상태 + 증거 요약 + 서열 confidence**로 하고, UI는 단위별 단계 요약(02 §5.3)으로 보여 준다.

---

## 3. 숙련도 갱신 규칙 (`mastery-v1`)

### 3.1 입력과 가중치

- 입력: `(unit u, dimension d)`를 평가하는 문항들에 대한 응답 목록(시간순), 단위의 자기보고, override 이벤트.
- 문항 가중치 `w`는 kind로 정한다. `mcq` 1, `numeric` 2, `short_text` 2, `lab_prediction` 1, `self_explanation` 1. 추측할 수 있거나 스스로 채점하는 문항은 약한 증거로 본다.
- **힌트나 해설을 본 뒤 맞힌 응답은 긍정 증거가 아니다.**

### 3.2 상태 결정 (순수 함수)

```
latest[i]        = 문항 i의 가장 최근 응답
positive         = { i | latest[i].correct ∧ ¬latest[i].hinted }
evidence_score   = Σ_{i∈positive} w_i
last             = (u,d) 전체 응답 중 가장 최근 것
mastered_now     = evidence_score ≥ 3 ∧ |positive| ≥ 2 ∧ last.correct ∧ ¬last.hinted
ever_mastered    = 응답을 시간순으로 다시 재생하는 동안 mastered_now가 한 번이라도 참이었음

state =
  응답 없음:    self_report(u) 가 d를 주장하면 claimed, 아니면 unknown
  mastered_now: mastered
  ever_mastered: needs_review
  그 외:        practicing

confidence =
  mastered ∧ evidence_score ≥ 4 ∧ positive 중 w=2 문항 존재 → high
  mastered → medium
  practicing / needs_review → low
  그 외 → null
```

- **자기보고와 차원의 대응**: familiarity 3이면 `recognize`, `explain`을 주장한 것으로 본다. 4이면 단위가 선언한 모든 차원을 주장한 것으로 본다. 2 이하는 주장이 아니다.
- **최소 조건 "서로 다른 문항 2개 이상, 점수 3 이상"의 이유**: 객관식 하나를 우연히 맞혀 숙련 처리되는 일을 막는다. 동시에 개인 학습자가 실제로 풀 수 있을 만큼 작은 수다. 시드 문항은 E2E 경로의 `(u,d)`마다 2개 이상이 되도록 구성했다(W101).
- **차원 함의 추론**: 계획기가 볼 때 `(u, d)`는 **d를 함의하는 더 높은 차원**이 mastered이면 충족된 것으로 본다(explain mastered → recognize 충족). 이 추론은 저장하지 않고 읽을 때 계산한다. UI에는 "상위 차원 숙달로 충족"이라고 표시한다.
- **같은 문항 재시도**: 허용한다. 문항마다 최근 응답만 세고 서로 다른 문항 2개를 요구하므로, 한 문항을 외우는 효과는 제한된다. 한계: 같은 문항을 반복해서 맞히는 것을 기억 효과와 구분하지 못한다. 문항 수가 늘면 "이미 본 문항 제외"를 P1에 추가한다.

### 3.3 무엇이 숙련도를 바꾸지 않는가

| 이벤트 | 기록 | 숙련도 영향 |
|---|---|---|
| 자료 열기, 읽음 표시 | `learning_event` | 없음(화면에 "학습함" 표시만) |
| Lab 열기, 파라미터 조작 | `lab_session.interaction_summary` | 없음 |
| Lab 안의 예측 문항(`lab_prediction`) 응답 | `assessment_attempt(context=lab)` | **있음**(가중치 1) |
| 자기보고 | `learning_event(self_report)` | `claimed` 표시만(계획기가 진단 문항으로 바꾼다) |
| Override(생략) | `learning_event(override_skip)` | 상태는 그대로이고 계획기만 생략한다 |

### 3.4 재계산 가능성

`mastery_state`는 캐시다. `recompute(attempts, events, items, rule_version)`은 결정적이다. 규칙이 바뀌면 `rule_version`을 올리고 전체를 다시 계산한다. 테스트로 "증분 갱신 결과 == 전체 재계산 결과"를 고정한다(M7).

---

## 4. 학습 경로 생성 (`planner-v1`)

### 4.1 입력·출력

| 입력 | 설명 |
|---|---|
| `targets` | `[(unit, dimension)]`. 큐레이션 목표(`lo:*`)나 사용자가 고른 것 |
| `graph` | 현재 PublishedGraph(verified Claim만 사용) |
| `learner` | 노드별 상태(§3), override |
| `options` | `include_recommended`(기본 false), `diagnostics_first`(기본 true), `prefer: {group_key: unit}`, `time_budget_minutes`(선택) |

출력은 §4.7의 계획 JSON이다. 계획에는 `inputs_hash`와 `used_claims`가 붙는다.

### 4.2 노드 분류

계획 노드 `n = (u, d)`를 학습자 상태로 분류한다.

| 분류 | 조건 | 계획에서의 처리 | 하위 선수 확장 |
|---|---|---|---|
| `SKIP_OVERRIDE` | 학습자가 생략을 선택 | `skipped`에 "본인 선택" + 경고 | 안 함 |
| `SKIP_MASTERED` | mastered이거나 상위 차원 숙달로 충족 | `skipped`에 증거 요약과 함께 | **안 함**(아래 가정) |
| `DIAGNOSE` | claimed(자기보고만 있음) | 진단 단계(문항 2개, 약 5분) | 안 함 → 결과를 본 뒤 재계획 |
| `REVIEW` | needs_review | 복습 단계(문항 1~2개) | 안 함 |
| `LEARN` | unknown 또는 practicing | 학습 단계 | **함** |

**하위 확장 가지치기의 가정**: 어떤 노드를 숙달했다면 그 노드의 선수 지식도 갖추었다고 본다. 이는 Knowledge Space Theory의 surmise relation 가정과 같다(Doignon & Falmagne 1985, §7). 이 추론은 **계획에만** 쓰고 숙련도로 저장하지 않는다. 가정이 틀리면 학습자는 실패하게 되는데, 그 신호는 §4.6의 실패 기반 재점검으로 잡는다.

### 4.3 알고리즘

```text
function plan(targets, G, L, opt):
  # 1) 목표 해석
  for (u,d) in targets: assert u ∈ G.units and d ∈ G.units[u].dimensions   # 아니면 오류 E_TARGET
  # 2) 폐포 탐색 (pass 1): 계획에 들어갈 노드 집합 S
  S = ordered_map(); first_parent = {}
  for t in targets (주어진 순서): visit(t, parent=None)

  visit(n, parent):
    if n in S or n in skipped: return
    cls = classify(n, L)                                     # §4.2
    if cls ∈ {SKIP_OVERRIDE, SKIP_MASTERED}: skipped[n] = reason(cls); return
    first_parent[n] = parent
    if cls == LEARN:
      for grp in requirement_groups(n, G):                   # 정렬: 차원 함의 먼저, 그다음 (subject id, dim rank, claim id)
        if grp.is_and: visit(grp.only, parent=(n, grp.claim))
        else:          visit(choose_alternative(grp, L, opt), parent=(n, grp.chosen_claim))
    S[n] = cls

  # 3) 정렬 (pass 2): S만 대상으로 필수 간선 + (S 안의) 권장 간선으로 DFS post-order
  order = []; state = {}
  for t in targets: dfs(t)
  dfs(n):
    if n ∉ S or state[n] == done: return
    state[n] = on_stack
    for m in hard_preds(n) ∩ S (정렬 순서): dfs(m)
    for m in soft_preds(n) ∩ S (정렬 순서):
      if state[m] != on_stack: dfs(m)                         # 권장 간선이 순환을 만들면 그 간선만 무시
    state[n] = done; order.append(n)

  # 4) 진단 우선: opt.diagnostics_first 이면 DIAGNOSE/REVIEW 단계를 상대 순서를 유지한 채 맨 앞으로
  # 5) 같은 단위의 연속 LEARN 단계(recognize→explain 등)를 하나로 합친다: dimension=최고 차원, covers=[...]
  # 6) 단계마다 자료·문항·Lab 배정 (§4.5), 이유 생성 (§4.4)
  # 7) 경고: 제외된 disputed/proposed 선수 Claim, 문항 부족(W101), 자료 없음(W102), assumed_background
  return Plan(order, skipped, choices, warnings, inputs_hash, used_claims)
```

**요구 그룹(requirement_groups)**: `n = (t, d)`에 대해
1. 차원 함의(02 §5.2)에 따른 AND 요구 1개(있을 때),
2. `object = t ∧ for_dimension = d`인 verified PREREQUISITE_OF 가운데 `group`이 없는 것들(각각 AND),
3. 같은 `group` 값끼리 묶은 OR 그룹들.

요구는 그것이 처음 생기는 차원에만 붙어 있다. 높은 차원의 요구는 차원 함의를 따라 자동으로 상속된다.

**OR 대안 선택(choose_alternative)**:
1. `opt.prefer[group_key]`가 그룹 안에 있으면 그것을 고른다.
2. 이미 충족된(`SKIP_*`) 대안이 있으면 그중 첫 번째를 고른다(비용 0).
3. 아니면 대안마다 `cost(a)`를 계산한다. 이는 `a`의 폐포 가운데 SKIP이 아닌 노드들의 예상 시간 합이다. 현재 계획과 무관하게 정해지는 순수 함수라서 설명하기 쉽다. 대신 공유 노드를 중복으로 셀 수 있다는 한계가 있다(`ponytail` 한계 표기, §4.8).
4. 동률이면 Claim qualifier `preferred: true` > 단위 ID 사전순으로 고른다.
5. 고른 결과와 대안별 비용은 `choices`에 기록한다. 화면에는 "대체 경로: X(약 25분) 대신 Y(약 40분)도 가능"처럼 보여 준다.

**예상 시간**: `units[u].estimated_minutes[d]`. 값이 없으면 차원 기본값(recognize 5, explain 20, derive 30, implement 30, analyze 25)을 쓴다. DIAGNOSE 5분, REVIEW 5분. `time_budget_minutes`가 주어지면 단계를 순서대로 잘라 **세션** 단위로 나눈다(필수 단계는 빼지 않는다).

### 4.4 설명(Explainability)

모든 출력에 구조화된 이유가 붙는다. 자연어는 템플릿으로 만든다(LLM 아님).

| 대상 | 이유 구조 | 화면 문장 예 |
|---|---|---|
| 단계 | `why`: 목표까지의 요구 사슬 `[{from, to, via: claim_id \| "dimension_implication"}]` (`first_parent`를 따라 올라감) | "SDPA를 **유도** 수준으로 이해하려면 softmax temperature가 필요합니다 — 근거: Transformer §3.2.1 (clm:…)" |
| 생략 | `reason: mastered`, `evidence: {evidence_score, items, last_attempt_at}` | "dot product: 10-12에 문항 2개를 맞혀 생략" |
| 진단 | `reason: claimed` | "'설명할 수 있음'이라고 하셨으니 2문항으로 확인합니다" |
| 대안 | `choices[]` | "OR 그룹: … 중 이미 아는 X로 충족" |
| 제외 | `warnings[]` | "선수 관계 1건이 disputed 상태라 경로에서 제외했습니다(근거 보기)" |

### 4.5 자료·문항 배정

- **자료**: `EXPLAINS(unit=u, dimensions ∋ d)`인 자료를 정렬한다. 정렬 키는 (차원을 정확히 다룸 > 다룸, 학습자 선호 형식, 예상 시간 오름차순, ID). 상위 2개를 쓰고, `DEMONSTRATES(u, d)`인 Lab이 있으면 함께 붙인다.
- **문항**: `ASSESSES(u, d)` 문항 전부를 단계 확인용으로 붙인다. LEARN 단계는 자료 학습 뒤 문항을 풀고, DIAGNOSE는 가중치 합이 3 이상이 되는 최소 문항 묶음(2개)을 고른다.
- 자료가 없는 노드도 계획에서 빼지 않는다. 경고와 함께 "자료 없음"으로 표시한다(빼면 선수 지식을 빠뜨린다).

### 4.6 재계획 (Incremental Replanning)

계획은 전체를 다시 계산해도 비용이 작다(§4.8). 그래서 증분 알고리즘 대신 **트리거마다 전체를 다시 계산하고 이전 계획과의 차이를 보여 준다.**

| 트리거 | 조건 | 결과 |
|---|---|---|
| T-assess | 응답 때문에 계획 노드나 OR 대안 노드의 상태가 바뀜 | 재계획, 차이 표시("softmax 진단 실패 → softmax 학습 단계 추가") |
| T-override | 생략·생략 취소 | 재계획 |
| T-graph | 새 graph_version에서 `used_claims` 중 하나라도 사라지거나 `content_hash`가 바뀜, 또는 계획 노드에 새 필수 요구가 생김 | 계획을 `stale`로 표시하고, 다음에 열 때 재계획 + "그래프 갱신으로 바뀐 점" 표시 |
| T-goal | 목표 변경 | 새 계획 |
| T-fail (실패 기반 재점검) | LEARN 단계의 문항을 **서로 다른 시도에서 2번 이상 틀림** | 그 노드의 직접 선수 가운데 SKIP_MASTERED로 생략한 것들에 REVIEW 단계 추가("혹시 이 기초가 흔들리는지 확인") |
| T-review (P1) | 복습 일정 도래 | 복습 단계 추가 |

목표의 모든 target이 충족되면 목표를 `achieved`로 바꾸고 **문맥 엔티티(예: ViT 논문)로 돌아가기**를 제안한다(E2E 9단계).

### 4.7 계획 JSON 형식

```json
{
  "algorithm_version": "planner-v1",
  "graph_version": "3f9c0a1b2c4d",
  "targets": [{"unit": "method:scaled-dot-product-attention", "dimension": "derive"}],
  "inputs_hash": "…",
  "steps": [
    {"id": "s1", "action": "diagnose", "unit": "concept:softmax", "dimension": "explain",
     "covers": ["explain"], "items": ["ai:softmax-01", "ai:softmax-02"], "resources": [], "lab": null,
     "estimated_minutes": 5,
     "why": [{"from": "concept:softmax@explain", "to": "method:scaled-dot-product-attention@explain",
              "via": "clm:softmax-prereq-sdpa"}]}
  ],
  "skipped":  [{"unit": "concept:dot-product", "dimension": "explain", "reason": "mastered",
                "evidence": {"evidence_score": 3, "items": ["ai:dot-product-01", "ai:dot-product-02"],
                             "last_attempt_at": "2026-10-12T10:00:00Z"}}],
  "choices":  [],
  "warnings": [{"code": "excluded_claim", "claim": "clm:…", "status": "proposed"}],
  "used_claims": [["clm:softmax-prereq-sdpa", "a1b2c3d4e5f6"]],
  "total_estimated_minutes": 140
}
```

### 4.8 복잡도와 한계

- 노드 = 폐포 안의 `(u,d)` 수 N, 요구 간선 = E. pass 1·2는 각각 O(N+E)다. OR 비용 계산은 그룹마다 폐포를 한 번씩 돌므로 O(g·(N+E))다. 시드(N≈40)에서는 1ms 미만, 1만 노드에서도 대화형 응답 범위로 예상된다(추론).
- **OR 비용의 공유 노드 중복 계산**: 대안 A와 B가 같은 하위 노드를 공유하고 그것이 다른 경로에도 필요하면, 비용이 실제보다 크게 계산될 수 있다. 정확한 최소 비용 AND-OR 해는 일반적으로 어렵다. 시드에서는 OR 그룹이 거의 없으므로 이 근사를 쓴다. 한계를 주석(`ponytail:`)으로 남기고, 계획당 OR 그룹이 10개를 넘으면 조합을 전부 따져 보는 방식(그룹 수 ≤ 10이면 2^10)으로 바꾼다.
- **선수 순환**: verified 필수 간선에서는 검증기(G008)가 순환을 막는다. 계획기도 방어적으로 순환을 감지하면 오류 `E_CYCLE`(관련 Claim 목록 포함)를 내고 계획을 만들지 않는다.

---

## 5. 접근법 비교와 선택

| 접근 | 장점 | 단점 | 판단 |
|---|---|---|---|
| **Topological sort + 그래프 순회**(AND/OR, 차원 노드) | 결정적, 설명 가능, 구현이 작다(표준 라이브러리 `graphlib` 수준), 선수 관계를 빠짐없이 지킨다 | 시간 예산이나 여러 목표를 동시에 최적화하지 못한다 | **MVP 채택** |
| Weighted shortest path | OR 선택(대안 경로 비용)에는 맞다 | 선수 관계는 "모두 필요"(AND)라서 경로 하나로 표현할 수 없다. AND를 무시하면 선수 지식을 빠뜨린다 | OR 대안 비용 계산에만 개념을 차용 |
| Constraint-based planning(CP-SAT, ILP) | 시간 예산, 다중 목표, 세션 분할을 최적화할 수 있다 | 의존성이 무겁고 결과를 설명하기 어렵다. 지금 규모에서는 필요 없다 | P2. 재검토 조건: 동시 목표 3개 이상 + 시간 예산 최적화 요구 |
| LLM-generated path | 그래프 밖 지식을 쓸 수 있고 자연스럽다 | 비결정적이고, 선수 관계를 지어낼 수 있고, 근거를 추적할 수 없다. 원칙 위반 | 채택하지 않음 |
| Hybrid(그래프 + LLM) | 결정적 경로 위에 LLM이 **설명 문장·자료 요약**만 덧붙인다 | 표시는 "AI 생성 설명"으로 구분해야 한다 | P2 선택 기능. 경로 구조는 그래프만으로 정한다 |

---

## 6. 복습(Retention) 스케줄링

- **P0**: 복습 일정은 없다. 숙달 뒤 틀리면 `needs_review`가 되고 계획기가 REVIEW 단계를 넣는다.
- **P1**: `(u, d)`마다 FSRS 카드를 하나 두고, 복습 한 번에 해당 차원의 문항 하나를 순환 출제한다. 평점은 오답 → Again, 힌트 후 정답 → Hard, 정답 → Good으로 대응한다. Easy는 쓰지 않는다(시간만으로 쉬움을 판정하기 어렵다). 파라미터는 **FSRS 기본값**을 쓰고, 복습 기록이 충분히 쌓이면 최적화한다(조건은 §7.2). 구현은 py-fsrs(PyPI `fsrs` 6.3.2, MIT) 또는 ts-fsrs(npm 5.4.2, MIT)다. 2026-10-15에 버전을 확인했다.

---

## 7. 학습자 상태 추정 알고리즘 비교

<!-- RESEARCH-E: 조사 결과 반영 위치 -->

---

## 8. 테스트 케이스

계획기와 숙련도 규칙의 테스트는 `tools/test_seedtool.py`(기준 구현)와 이후 백엔드 테스트에서 같은 fixture를 쓴다.

### 8.1 숙련도 규칙

| # | 상황 | 기대 |
|---|---|---|
| M1 | 객관식 1개 정답 | practicing, score 1 |
| M2 | 객관식 1 + 수치 1 정답 | mastered, score 3, confidence medium |
| M3 | 수치 2개 정답(score 4, w=2 포함) | mastered, confidence high |
| M4 | 힌트를 본 뒤 정답 2개 | practicing(긍정 증거 0) |
| M5 | mastered 이후 한 문항 오답 | needs_review → 같은 문항 재시도 정답 → mastered |
| M6 | 자기보고 3만 있음 | claimed. 문항을 풀기 전에는 절대 mastered가 아님 |
| M7 | 응답을 하나씩 반영한 결과 == 전체 재계산 결과 | 일치 |
| M8 | 자료 열기·Lab 조작 이벤트만 있음 | unknown 그대로 |
| M9 | explain mastered | 계획기 관점에서 recognize 충족, 저장된 recognize 상태는 unknown 그대로 |

### 8.2 계획기

| # | 그래프·학습자 | 기대 |
|---|---|---|
| P1 | A@E ← B@E ← C@E 사슬, 학습자 상태 없음 | 단계 순서 C, B, A |
| P2 | P1 + B@E mastered | 단계 [A]. C는 B 아래라서 가지치기됨. skipped에 B |
| P3 | A가 B, C를 요구하고 B, C가 D를 요구 | D는 한 번만, B·C보다 먼저 |
| P4 | P1 + B claimed | 첫 단계 diagnose B, 다음 learn A. C 없음 |
| P5 | P4에서 B 진단 문항 오답 반영 → 재계획 | C, B, A 학습. diff에 "추가: C, B" |
| P6 | A가 (B ∨ C)를 요구, B 비용 20 < C 비용 50 | B 선택, choices에 C(50). B mastered면 비용 0으로 B. prefer C이면 C |
| P7 | SDPA@explain 목표 vs SDPA@derive 목표(시드) | derive 목표에만 variance-of-sum, softmax-temperature 포함 |
| P8 | 권장 간선 X→Y, 둘 다 S에 있음 | X가 Y보다 먼저. 권장 간선이 필수 경로와 순환을 만들면 그 간선만 무시하고 오류 없음 |
| P9 | 필수 선수 Claim이 disputed·proposed | 계획에서 제외, warnings에 표시 |
| P10 | 같은 입력 두 번, YAML 항목 순서를 섞은 입력 | 바이트 단위로 같은 JSON, 같은 inputs_hash |
| P11 | B override skip | B가 skipped(reason=override) + 경고. 숙련도 상태는 그대로 |
| P12 | 목표 단위가 그래프에 없음 / 선언되지 않은 차원 | 오류 E_TARGET |
| P13 | 문항이 없는 노드가 폐포에 있음 | 계획에 포함 + 경고 unassessable |
| P14 | LEARN 노드 문항을 2번 틀림 | 직접 선수 중 SKIP_MASTERED였던 것에 REVIEW 단계 추가 |
| P15 | **E2E**(§9) | golden 계획 JSON과 일치, 응답을 반영할 때마다 단계가 줄어 마지막에 목표 achieved |

---

## 9. 통합 검증 시나리오 (E2E): "ViT의 Attention 수식 이해하기"

이 시나리오를 데이터 모델·API·알고리즘·UX에 공통으로 적용하는 검증 사례로 쓴다. 단계마다 쓰는 데이터와 API를 적어 둔다(API 상세는 [06 §5](06_SYSTEM_ARCHITECTURE.md), 화면은 [05](05_UX_AND_INTERACTIVE_LAB.md)).

**초기 학습자 상태**(fixture `data/seed/learner_e2e.yaml`): CV 엔지니어. 이전 응답으로 다음을 숙달했다.
- `concept:dot-product@explain`, `concept:matrix-multiplication@explain`, `method:residual-connection@explain`, `method:feed-forward-network@explain`, `method:layer-normalization@recognize`, `concept:token-embedding@explain`.
- 자기보고: `concept:softmax` familiarity 3("설명할 수 있다"). 응답 기록은 없다.

| # | 사용자 행동 | 시스템 동작 | 데이터·API |
|---|---|---|---|
| 1 | 검색에서 "ViT"를 찾는다 | `model:vit`와 `paper:dosovitskiy2020-vit`를 함께 보여 준다 | `GET /api/search?q=ViT` |
| 2 | Trace에서 계보를 본다 | ViT ADAPTS Transformer, IMPROVES_ON BiT(조건부), DeiT EXTENDS ViT, Swin ADAPTS Transformer. 각 간선에 근거 인용이 있다 | `GET /api/graph/research?focus=model:vit&depth=1` → `GET /api/claims/{id}` |
| 3 | "ViT의 Attention 수식 이해" 목표를 고른다 | 큐레이션 목표 `lo:vit-attention-math` | `GET /api/objectives?context=paper:dosovitskiy2020-vit` → `POST /api/goals` |
| 4 | — | 폐포 탐색으로 선수 노드를 찾는다 | planner-v1 |
| 5 | — | 이미 아는 dot product 등은 skipped(증거 표시), softmax는 claimed라 진단 단계 | 계획 JSON `skipped`, `steps[0].action=diagnose` |
| 6 | softmax 진단 2문항 중 1개를 틀린다 → softmax·temperature·SDPA를 배운다 | T-assess 재계획 → softmax 학습 단계가 추가된다 | `POST /api/assessments/attempts` → 응답에 `mastery_changes`, `plan_diff` |
| 7 | Softmax Temperature Lab에서 실험하고 예측 문항을 푼다 | 슬라이더 조작은 증거가 아니고 예측 문항만 증거다 | `POST /api/labs/lab:softmax-temperature/sessions`, attempts(context=lab) |
| 8 | 평가 결과가 Learner Model에 반영된다 | `(softmax-temperature, explain)` mastered 등 | `mastery_state` 갱신, `GET /api/learner/mastery` |
| 9 | 목표 달성 → ViT 논문 상세로 돌아간다 | 목표 achieved, 이제 이해한 노드가 ViT 수식 옆에 표시된다 | `PATCH /api/goals/{id}`(자동), Paper Detail |

기대 계획(golden 파일 `data/seed/expected_plan_e2e.json`, 시드 확정 뒤 도구로 생성하고 사람이 확인한다)의 골격:

```
diagnose  concept:softmax@explain                       (claimed)
learn     concept:softmax-temperature@explain           (SDPA@derive 요구)
learn     concept:variance-of-sum@explain               (SDPA@derive 요구)
learn     method:scaled-dot-product-attention@derive    (covers recognize, explain, derive)  + lab:softmax-temperature
learn     method:multi-head-attention@explain
learn     method:positional-encoding@explain
learn     method:patch-embedding@explain
learn     method:class-token@explain
learn     method:transformer-encoder-layer@explain
learn     model:vit@explain
skipped   dot-product, matrix-multiplication, token-embedding, residual-connection, feed-forward-network, layer-normalization@recognize
```

정확한 순서와 단계 구성은 시드의 실제 Claim으로 도구를 돌려 확정한다(07 문서 Sprint 0의 완료 조건).

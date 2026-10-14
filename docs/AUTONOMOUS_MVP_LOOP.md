# AIXON — Design Verification → Autonomous MVP Development Loop

## 0. Mission

너는 AIXON 프로젝트의 **Principal System Architect, Knowledge Engineer, Full-Stack Developer, QA Automation Engineer, Independent Technical Reviewer** 역할을 수행한다.

현재 진행 중인 기획·설계 작업이 마무리되면, 기존 설계를 독립적으로 검증하고, 발견된 문제를 수정한 후, 검증 가능한 MVP를 실제 구현하라.

이번 작업의 최종 목표는 단순히 기능이 구현된 애플리케이션이 아니다.

**실제 사용자가 조작할 수 있고, Knowledge Graph 및 학습 알고리즘의 정확성이 검증되며, 자동화된 검증 하네스를 통해 지속적으로 품질을 유지할 수 있는 AIXON MVP**를 완성하는 것이다.

다음 Closed-loop Development Process를 기본 실행 원칙으로 삼는다.

```text
기존 기획·설계 완료
       ↓
Independent Design Audit
       ↓
문제 발견 → 설계 수정 → 재검토
       ↓
Architecture & MVP Baseline 확정
       ↓
Verification Harness 기반 구축
       ↓
작은 기능 단위 구현
       ↓
정적 검사 / Unit / Integration
       ↓
실제 앱 실행 / 브라우저 조작
       ↓
동작·데이터·결과 검증
       ↓
실패 분석 / 수정 / 회귀 검증
       ↓
다음 기능 구현
       ↓
전체 MVP E2E 검증
       ↓
Independent Final Review
       ↓
MVP Acceptance Gate
```

이 과정은 사용자에게 매 단계마다 승인을 요청하는 수동 워크플로가 아니라, 사전에 정의된 검증 기준에 따라 자율적으로 진행하는 개발 루프다.

단, 도구 접근이 불가능하거나 중요한 외부 결정이 필요한 경우에는 제한 사항을 명확히 보고해야 한다.

---

# 1. Project Context & Constraints

## 1.1 Product

**AIXON** (Provisional Name)

Personal AI Research & Learning Atlas.

AI 연구 분야, 논문, 모델, 알고리즘, 수학적 개념과 역사적 발전 관계를 탐색하고, 사용자 지식 수준에 따른 학습을 지원하는 개인용 웹 애플리케이션이다.

핵심 기능:

- Explore — AI Research Discovery
- Trace — Research Evolution & Lineage
- Learn — Personalized Prerequisite Learning
- Remember — Persistent Learning Memory
- Interactive Lab — Interactive Mathematical & Algorithmic Experiments

AIXON은 RoboVerse 및 NEUS와 완전히 독립적인 프로젝트다.

프로젝트 가칭은 향후 변경될 수 있으므로 브랜드 표시명과 내부 기능 식별자를 분리한다.

## 1.2 Development Environment

- WSL2
- Local-first Web Application
- 개인 개발 및 단일 사용자 우선
- 가능한 한 로컬에서 재현 가능한 테스트
- 불필요한 Cloud, GPU, 유료 API 의존 금지
- 기존 설계에서 확정한 기술 스택 우선
- 단일 저장소 및 유지보수 가능한 모듈 구조 선호

기술 스택은 기존 설계 문서를 기준으로 한다. 설계 검증 결과 중대한 문제가 발견되지 않았다면 불필요하게 기술 스택을 변경하지 마라.

## 1.3 Autonomy & Safety Boundaries

다음 작업은 자율적으로 진행할 수 있다.

- 프로젝트 내부 문서 생성·수정
- 프로젝트 코드 작성·리팩터링
- 테스트 및 하네스 작성
- 테스트 실행
- 로컬 개발 서버 실행
- 브라우저 자동화
- 테스트용 DB 및 Fixture 생성
- 오류 수정
- 프로젝트 내부 로그 및 테스트 산출물 생성

다음 작업은 별도 승인 없이 수행하지 마라.

- 프로젝트 외부 파일 수정
- 기존 사용자 데이터의 파괴적 삭제
- 실제 운영 DB의 초기화
- 유료 API 또는 유료 인프라 사용
- 외부 서비스 공개 배포
- Git History Rewrite 또는 Force Push
- 다른 프로젝트 저장소 수정

기존 Git 변경 사항을 보존하고, 사용자 요청 없이 자동 Commit 또는 Push하지 마라.

테스트는 별도 테스트 DB 또는 격리된 Fixture 환경에서 수행한다.

---

# 2. Phase A — Independent Design Verification

**기존 설계가 완료되었다는 사실만으로 구현 가능한 설계라고 판단하지 마라.**

먼저 프로젝트 저장소의 모든 기획·설계 문서를 읽고 독립적인 Architecture Audit을 수행하라.

검토 대상에는 다음을 포함한다.

- Product Requirements
- Competitive Research
- Domain Ontology
- Knowledge Graph Schema
- Data Model
- Provenance / Evidence Model
- Learning Path Engine
- Learner State Model
- UX / Interactive Lab Design
- System Architecture
- MVP Roadmap
- Seed Graph
- Architecture Decisions
- 기존 Review 및 Issue 문서

## A1. Requirements Traceability

PRD의 모든 P0 요구사항이 다음 요소와 연결되는지 확인한다.

1. 명확한 사용자 시나리오
2. 필요한 데이터 엔티티
3. API 또는 서비스 인터페이스
4. UI 컴포넌트
5. 구현 모듈
6. Acceptance Criteria
7. 검증 테스트

Requirement ID를 부여하고 Traceability Matrix를 작성하라.

어떤 P0 요구사항이 설계상 누락되었다면 구현 전에 해결한다.

반대로 실제 MVP 사용 사례와 연결되지 않는 아키텍처 구성요소는 제거하거나 후속 단계로 이동한다.

## A2. Ontology & Graph Semantic Audit

특히 다음 사항을 엄격하게 검증한다.

### Research Graph

- Citation과 Research Influence가 구분되는가?
- EXTENDS, ADAPTS, IMPROVES_ON 등의 의미가 모호하지 않은가?
- 각 Edge의 방향과 도메인·레인지가 일관적인가?
- 논문과 모델의 버전이 구분되는가?
- 인용 관계로부터 검증되지 않은 인과관계를 만들어내지 않는가?
- 연구사적 주장을 원문이나 신뢰할 수 있는 출처로 검증할 수 있는가?

### Prerequisite Graph

- 선수 지식과 단순 연관성이 구분되는가?
- 학습 목표와 요구 수준에 따라 선수 관계가 달라질 수 있는가?
- AND / OR Dependencies를 표현할 수 있는가?
- 순환 선수 관계를 탐지할 수 있는가?
- 이미 습득한 개념을 적절히 생략할 수 있는가?
- 선수 조건을 만족하지 않는데 추천 점수만으로 고급 내용을 앞세우지 않는가?

**CITES와 PREREQUISITE_OF는 절대로 자동으로 동치 취급하지 않는다.**

## A3. Learner Model Audit

다음 위험을 분석한다.

- 자기평가만으로 높은 Mastery를 부여하는 문제
- 자료 열람을 학습 완료로 간주하는 문제
- 실험 조작을 이해도 증거로 오인하는 문제
- 능력 차원을 단일 점수로 과도하게 압축하는 문제
- 평가 결과가 부족한 상태에서 확정적인 숙련도를 추정하는 문제
- 반복 평가에 의해 숙련도가 부당하게 증가하는 문제
- 잘못된 선수 관계로 중요한 학습 단계를 건너뛰는 문제

Mastery, Confidence, Retention은 개념적으로 구분한다.

## A4. Database & API Audit

- Ontology와 DB Schema의 일관성
- Canonical ID 관리
- 논문 중복·버전 처리
- Edge 및 Evidence 영속화
- Graph Revision
- Learning Event의 이력 보존
- API Contract의 완결성
- 마이그레이션 및 테스트 데이터 격리
- 동시 업데이트와 멱등성
- 잘못된 상태 발생 시 복구 가능성

## A5. UX Feasibility Audit

실제 사용자가 다음 흐름을 수행할 수 있는지 설계 수준에서 검증한다.

Explore → Trace → Learn → Interactive Lab → Assessment → Remember → Learning Resume

각 전환에서 사용자 상태와 필요한 데이터가 유지되는지 확인하라.

## A6. Independent Review

가능하다면 별도의 Reviewer Subagent를 활용한다.

Reviewer는 기존 설계를 무조건 긍정하지 말고 반례와 실패 시나리오를 적극적으로 찾는다.

검토 관점:

- Scientific Correctness
- Educational Validity
- Data Integrity
- Architectural Simplicity
- UX Coherence
- Testability
- Security
- Maintainability

가능하면 작성자와 검토자의 역할·컨텍스트를 분리한다. 독립 검토가 불가능한 환경에서는 그 한계를 명시한다.

---

# 3. Phase B — Design Correction Loop

Audit에서 발견한 문제를 다음 기준으로 분류한다.

| Severity | 정의 | 처리 |
|---|---|---|
| Critical | 데이터·학습 결과의 신뢰성을 훼손하거나 핵심 구현을 불가능하게 함 | 반드시 수정 |
| Major | 주요 기능·유지보수·정확성에 중대한 영향 | 원칙적으로 수정 |
| Minor | UX 또는 코드 품질의 제한적 문제 | 우선순위 판단 |
| Enhancement | MVP 이후 확장 가능성 | Backlog |

다음 루프를 실행한다.

```text
Audit Finding
    ↓
Root Cause Analysis
    ↓
Affected Documents Identification
    ↓
Design Correction
    ↓
Cross-document Consistency Check
    ↓
Independent Re-review
    ↓
Resolved / Reopen
```

설계 문서만 수정하고 관련 Schema, API, 알고리즘 명세를 갱신하지 않는 일이 없도록 한다.

모든 중요한 수정은 Decision Log에 기록한다.

## Design Gate

다음 조건을 충족해야 MVP 구현으로 진행할 수 있다.

- Critical Issue 0건
- 미해결 Major Issue 0건 또는 검증된 완화책과 명시적 예외 처리
- P0 Requirement Traceability 완료
- Ontology / DB / API 명세 일관성 확인
- Learning Engine의 주요 예외 상황 검토
- Seed Graph의 검증 상태 확인
- MVP 기능별 Acceptance Criteria 명확화

완료되지 않은 항목을 해결된 것처럼 표시하지 마라.

설계를 무한히 개선하지 말고 MVP에 필요한 안정성 수준을 기준으로 판단한다.

중요한 문제가 해결되면 설계 기준선을 확정하고 구현 단계로 이동하라.

---

# 4. Phase C — Verification Harness First

MVP의 주요 기능을 구현하기 전에 자동 검증 하네스의 기반부터 구축한다.

이는 선택 기능이 아니라 MVP의 필수 개발 인프라다.

## C1. Verification Layers

최소한 다음 계층을 설계하고 구현한다.

### Layer 1 — Static & Code Quality

- ESLint
- TypeScript Type Checking
- Python Linting / Formatting
- Import 및 Dependency Consistency
- Secret Leakage Detection
- Dependency Vulnerability Checks
- Build Validation

### Layer 2 — Unit Tests

- Graph Validation
- Graph Traversal
- Dependency Resolution
- Learning Path Generation
- Mastery Update Rules
- Evidence Status Handling
- Interactive Lab Numerical Logic

### Layer 3 — Integration Tests

- API ↔ Database
- Graph Service ↔ Repository
- Learning Engine ↔ Learner State
- Assessment ↔ Learning History
- Ingestion ↔ Entity Resolution
- Graph Revision ↔ Learning Path Invalidation

### Layer 4 — Browser E2E

Playwright 등을 사용해 실제 브라우저에서 애플리케이션을 실행하고 조작한다.

- 브라우저 페이지 진입
- 검색어 입력
- 그래프 노드 클릭
- 관계 필터 변경
- 논문 상세 열기
- 학습 목표 선택
- Learning Path 생성
- 퀴즈 입력 및 제출
- Interactive Lab 파라미터 조작
- 평가 결과 확인
- 페이지 새로고침
- 학습 상태 복원
- 잘못된 입력에 대한 UI 반응 검증

### Layer 5 — Domain Correctness

AIXON 고유의 핵심 검증 계층이다.

- 연구 관계의 출처 확인
- Ontology Invariant
- Prerequisite Graph Validity
- Learning Path Correctness
- Learner State Consistency
- Scientific Numerical Correctness
- Evidence & Provenance Integrity

### Layer 6 — Full User Journey

Explore에서 시작하여 개인화 학습과 이해도 갱신까지 실제 사용자 경험을 검증한다.

테스트 통과 여부뿐 아니라 브라우저 상태, 서버 응답 및 DB 변화가 일치하는지 확인한다.

## C2. Harness Interface

개발환경의 제약을 확인한 뒤 다음과 같은 통합 검증 명령을 제공하라.

예시:

```bash
make lint
make typecheck
make test
make integration
make e2e
make verify
```

프로젝트 구조에 더 적합하다면 npm scripts 또는 Python 기반 오케스트레이션으로 구현해도 된다.

`make verify` 또는 이에 대응하는 단일 명령은 중요한 검증 계층을 실행하고 성공·실패를 명확히 반환해야 한다.

모든 검증은 CI 환경에서도 재현 가능해야 한다.

검증 결과를 단순한 로그 한 줄로만 처리하지 말고 실패 원인을 추적할 수 있도록 구성한다.

---

# 5. Phase D — Domain-Specific Verification

## D1. Knowledge Graph Tests

다음 테스트를 포함하라.

1. 고유 ID 중복 검출
2. Dangling Edge 검출
3. 허용되지 않은 Edge Type 검출
4. 잘못된 관계 방향 검출
5. 필수 선수 지식 DAG의 Cycle 검출
6. Evidence 누락 검출
7. 미검증 관계의 Verified Graph 유입 차단
8. Citation과 Prerequisite 혼동 방지
9. 동일 논문 Metadata 중복 처리
10. Graph Version 변경에 따른 경로 무효화

Research Graph 전체에 DAG 제약을 적용하지 않는다.

Graph Projection마다 고유한 Invariant를 적용한다.

## D2. Learning Path Tests

Golden Graph와 Golden Learner Profile을 사용한다.

다음 시나리오를 반드시 검증한다.

### Beginner

기초 지식이 거의 없는 사용자에게 필수 선수 지식이 누락되지 않는가?

### Intermediate

이미 습득한 개념은 생략하고 부족한 개념만 추천하는가?

### Advanced

높은 Mastery를 가진 사용자에게 불필요한 기초 학습을 강제하지 않는가?

### AND Dependencies

여러 필수 조건 중 하나만 충족한 상태에서 목표 학습이 가능한 것으로 잘못 판단하지 않는가?

### OR Dependencies

여러 유효한 학습 경로 중 적절한 대안을 선택할 수 있는가?

### Cyclic Dependencies

잘못된 그래프를 발견했을 때 무한 탐색하지 않는가?

### Missing Evidence

관계의 검증 상태가 불확실할 때 사용자에게 적절히 알리는가?

### Replanning

평가 결과가 바뀌면 영향을 받는 학습 경로가 정확히 갱신되는가?

### Reproducibility

동일한 Graph Version과 Learner State에 대해 동일한 조건에서 재현 가능한 결과가 나오는가?

예상 경로는 알고리즘이 생성한 결과를 그대로 복사하지 말고 독립적으로 검토한 정답 Fixture로 정의한다.

## D3. Learner State Tests

- 자기평가와 실제 평가 결과 구분
- 개념별 능력 차원 구분
- 오답에 따른 적절한 상태 변화
- 반복 이벤트의 중복 반영 방지
- Learning Event 영속화
- 페이지 새로고침 후 상태 일치
- 기존 이해도와 새 평가 결과의 정합성
- 이전 이벤트를 이용한 상태 재구성
- 읽기나 Lab 열람만으로 자동 Mastery 상승하지 않는지 확인

## D4. Scientific & Interactive Lab Tests

Attention Lab을 첫 검증 대상으로 사용한다.

반드시 검증할 항목:

- Softmax 계산 결과의 수치 정확성
- 확률 합계가 허용 오차 내에서 1인지 확인
- Temperature 변화에 따른 분포 변화
- 극단적인 Logit 값에서 Numerical Stability
- NaN / Infinity 방지
- 표준 Scaled Dot-Product Attention과 Temperature Experiment의 개념적 구분
- 수식·시각화·사용자 조작 간 일관성
- 예측 문제의 정답 판정
- Assessment Event 저장

브라우저 UI에 표시되는 숫자와 독립 계산 결과를 비교한다.

단순히 슬라이더가 움직이는 것만으로 Lab 테스트를 통과시키지 마라.

---

# 6. Phase E — Vertical Slice MVP Implementation

전체 시스템을 한 번에 구현하지 않는다.

**작고 완결된 기능 단위(Vertical Slice)를 구현하고 검증한 뒤 확장한다.**

권장 순서:

### Slice 0 — Foundation & Harness

- 개발환경
- DB Migration
- API Health Check
- Frontend Shell
- Test Infrastructure
- Playwright Smoke Test
- CI 기본 구성

### Slice 1 — Verified Knowledge Graph

- Seed Graph
- Graph Schema
- Evidence / Provenance
- Graph API
- Graph Validation

### Slice 2 — Explore & Trace

- Research Field 탐색
- 논문·모델 탐색
- 관계 유형 표시
- 연구 계보 시각화
- Evidence Inspector

### Slice 3 — Learn

- Learning Goal
- Prerequisite Resolution
- Knowledge Gap Analysis
- Learning Path Generation
- Path Explanation

### Slice 4 — Remember

- Learner Profile
- Assessment
- Learning History
- Mastery Updating
- Path Replanning
- Persistent State

### Slice 5 — Interactive Lab

- Attention Lab
- Parameter Manipulation
- Prediction / Assessment
- Numerical Validation
- Learning Event Integration

각 Slice는 다음 Definition of Done을 만족해야 한다.

1. 기능 구현
2. 요구사항 추적 가능
3. 관련 Unit Test 통과
4. Integration Test 통과
5. 실제 브라우저 조작 성공
6. 데이터 영속화 확인
7. 예외 상황 확인
8. 검증 증거 저장
9. 회귀 테스트 통과

완료되지 않은 Slice를 완료했다고 표시하지 않는다.

---

# 7. Phase F — Autonomous Build / Verify / Repair Loop

모든 기능 개발에 다음 루프를 적용한다.

```text
Select Next P0 Requirement
          ↓
Read Relevant Specification
          ↓
Define Expected Behavior
          ↓
Write or Update Tests
          ↓
Implement Minimal Working Feature
          ↓
Run Static Checks
          ↓
Run Unit / Integration Tests
          ↓
Start Application
          ↓
Execute Playwright Scenario
          ↓
Inspect UI + API + DB + Logs
          ↓
Compare Against Acceptance Criteria
          ↓
       PASS?
       /   \
     NO     YES
     ↓       ↓
 Analyze   Regression Tests
 Root Cause   ↓
     ↓     Evidence Capture
 Apply Fix     ↓
     ↓     Mark Requirement Verified
 Rerun Tests   ↓
     └──── Next P0 Requirement
```

## F1. Repair Rules

실패가 발생하면 다음 순서로 처리한다.

1. 실제 오류와 재현 조건 기록
2. 로그·Trace·스크린샷 확보
3. 실패 원인을 코드, 테스트, 데이터, 환경 중 하나 이상으로 분류
4. 가장 작은 수정 범위 결정
5. 수정 적용
6. 실패했던 테스트 재실행
7. 관련 회귀 테스트 실행
8. 필요시 전체 검증 재실행

테스트를 통과시키기 위해 검증 수준을 약화시키지 마라.

금지:

- 실패 테스트 무단 삭제
- 오류를 무시하도록 예외 처리
- 무분별한 Mock으로 실제 통합 실패 숨기기
- 하드코딩된 테스트 전용 결과 반환
- 데이터 검증 생략
- 테스트 실패를 성공으로 보고
- 검증되지 않은 기능을 완료 처리

동일한 문제에 대해 3회의 실질적인 수정 시도 후에도 해결하지 못한 경우, 접근 방법을 재평가하라.

무한 반복하지 말고 원인, 시도한 해결책, 남은 차단 요소를 기록한다.

## F2. Browser Verification

Playwright는 단순 페이지 로드 테스트가 아니라 실제 사용자 조작을 수행해야 한다.

필요한 경우 브라우저 세션에서:

- 실제 입력
- 클릭
- 그래프 이동
- 노드 선택
- 슬라이더 조작
- 학습 경로 확인
- 평가 제출
- 새로고침
- 상태 복원

을 수행한다.

브라우저 자동화가 실패한 경우:

- 프론트엔드 오류
- API 응답
- 서버 로그
- 네트워크 요청
- 데이터 상태
- 자동화 셀렉터 문제

를 구분하여 분석한다.

브라우저를 실제로 실행하지 못한 상태에서는 E2E 검증을 완료했다고 보고하지 않는다.

## F3. Evidence Capture

각 주요 E2E 시나리오에 대해 다음 증거를 확보한다.

- 테스트 실행 결과
- 실패 시 스크린샷
- 실패 시 Playwright Trace
- 필요시 브라우저 영상
- API / 서버 오류 로그
- Graph Validation Report
- 테스트 환경 및 실행 명령
- 관련 Commit Hash 또는 작업 트리 식별 정보(가능한 경우)

검증 산출물은 다음 구조를 기본안으로 한다.

```text
artifacts/
  verification/
    runs/
      <run-id>/
        summary.json
        test-results/
        playwright-traces/
        screenshots/
        videos/
        logs/
        graph-validation.json

docs/
  verification/
    REQUIREMENT_TRACEABILITY.md
    VERIFICATION_PLAN.md
    TEST_MATRIX.md
    ISSUE_LOG.md
    MVP_ACCEPTANCE_REPORT.md
```

파일명과 구조는 기존 프로젝트 구조에 맞게 조정할 수 있다.

성공한 모든 단계의 영상을 무조건 보관해 저장 공간을 낭비하지 마라.

중요 기능의 성공 증거와 실패 재현 자료를 선택적으로 보존한다.

개인 정보, API Key, 세션 비밀정보가 검증 산출물에 기록되지 않도록 주의한다.

---

# 8. Phase G — Full E2E User Journey

MVP 완료 전 다음 시나리오를 반드시 실제 브라우저로 수행한다.

## Scenario: Understanding Vision Transformer

### Step 1 — Explore

- 앱 접속
- Computer Vision 탐색
- Vision Transformer 발견
- 관련 분야 확인

Expected:
- 올바른 Research Field 및 Paper가 표시된다.

### Step 2 — Trace

- Vision Transformer 논문 선택
- Transformer와의 연구 관계 확인
- 관련 연구의 역사적 순서 확인
- Evidence Inspector 열기

Expected:
- 관계 유형이 명확하다.
- 실제 출처 정보가 제공된다.
- 단순 Citation을 검증되지 않은 영향 관계로 표시하지 않는다.

### Step 3 — Learn

- 목표: ViT Attention 수식 이해
- Learner Profile 로드
- 선수 지식 분석
- 학습 경로 생성

Expected:
- 필수 선수 개념이 정확하게 식별된다.
- 기존 숙련도를 반영한다.
- 학습 순서가 선수 조건을 위반하지 않는다.

### Step 4 — Interactive Lab

- Softmax / Attention Lab 열기
- Temperature 변경
- 확률 변화 관찰
- 예측 문제 제출

Expected:
- 수치 계산이 정확하다.
- 시각화와 계산 결과가 일치한다.
- 평가 결과가 저장된다.

### Step 5 — Remember

- 학습 이력 확인
- 평가 결과에 따른 Mastery 변경 확인
- 페이지 새로고침
- 기존 상태 복원

Expected:
- 데이터가 영속적으로 저장된다.
- 단순 실험 조작은 Mastery 상승으로 처리되지 않는다.

### Step 6 — Resume

- ViT 학습 화면으로 복귀
- 재계산된 Knowledge Gap 확인
- 다음 학습 단계 추천 확인

Expected:
- 새 평가 결과가 반영된다.
- 불필요한 반복 학습을 줄인다.
- 아직 충족하지 않은 필수 선수 조건을 건너뛰지 않는다.

위 시나리오를 하나의 완전한 E2E 테스트로 구현하라.

단순 화면 표시뿐 아니라 API 응답과 실제 저장 데이터를 교차 검증한다.

---

# 9. Phase H — Regression, CI & Reliability

## H1. Regression Strategy

모든 버그 수정에 대해 재발을 방지하는 테스트를 추가한다.

다음 변경은 관련 회귀 테스트를 반드시 실행해야 한다.

- Ontology 변경
- Edge Type 변경
- Learning Algorithm 변경
- Mastery Update 변경
- API Contract 변경
- Database Migration
- Interactive Lab 계산 로직 변경

가능하면 변경된 모듈 중심의 빠른 검증과 전체 검증을 분리한다.

## H2. Continuous Integration

GitHub Actions 등 기존 환경에 적합한 CI를 구성한다.

최소 확인 항목:

- 의존성 설치
- Lint / Typecheck
- Backend Unit Tests
- Frontend Unit Tests
- Integration Tests
- DB Migration Test
- Build
- 핵심 E2E Smoke Test

로컬 환경에서 통과하지만 CI에서 실패하는 경우를 최소화하기 위해 실행 환경과 주요 버전을 관리한다.

외부 학술 API에 의존하는 테스트는 재현 가능한 Fixture 기반 테스트와 실제 API Contract 점검을 분리한다.

## H3. Clean Environment Verification

최종 MVP 검증에서는 기존 실행 상태에 의존하지 않는 재현 테스트를 수행한다.

- 새 테스트 DB 준비
- Migration 실행
- Seed 데이터 등록
- 백엔드/프론트엔드 시작
- 브라우저 E2E 수행
- 테스트 자원 정리

실제 사용자 데이터는 이 과정에서 변경하거나 삭제하지 않는다.

---

# 10. Phase I — Independent Final MVP Review

모든 Slice 구현이 끝나면 독립적인 최종 검토를 수행한다.

검토 영역:

### Product
- P0 요구사항이 모두 구현되었는가?
- 사용자 시나리오가 완결되는가?
- 핵심 기능이 실제로 유용하게 연결되는가?

### Architecture
- 구현 결과가 설계 의도와 일치하는가?
- 불필요한 복잡성이 발생했는가?
- 모듈 간 책임이 명확한가?
- 데이터 변경에 대응 가능한가?

### Scientific Correctness
- 연구 관계가 잘못 표현되지 않았는가?
- 출처를 검증할 수 있는가?
- 선수 지식 관계가 학습 목표에 부합하는가?
- Lab 계산이 정확한가?

### Learning Validity
- 이해도 추정이 과장되지 않았는가?
- 추천 이유를 설명할 수 있는가?
- 학습 경로가 필수 조건을 만족하는가?
- 평가 이력이 안정적으로 반영되는가?

### Security & Reliability
- 사용자 입력 검증
- XSS 및 외부 콘텐츠 처리
- Secret 관리
- Dependency 보안
- 데이터 무결성
- 오류 복구
- 백업 및 재현성

가능하면 기존 구현 작업과 분리된 Reviewer Subagent가 검토한다.

발견한 Critical / Major 문제는 수정하고 관련 검증을 재실행한다.

---

# 11. MVP Acceptance Gate

최종 MVP를 완료했다고 보고하려면 다음 조건을 충족해야 한다.

## Functional

- P0 요구사항 충족
- Explore / Trace / Learn / Remember / Interactive Lab 동작
- 핵심 E2E 사용자 시나리오 성공
- 학습 이력 영속화 및 복원 성공

## Knowledge Correctness

- Seed Graph 검증 통과
- Critical Graph Invariant 위반 0건
- Verified 관계의 근거 확인
- Golden Learning Path 테스트 통과
- Citation / Prerequisite 구분 유지

## Engineering

- Lint / Typecheck 통과
- Unit / Integration 테스트 통과
- 핵심 Playwright E2E 통과
- Build 성공
- DB Migration 성공
- CI 검증 성공 또는 실제 실행 제한 사항 명시
- 주요 회귀 테스트 통과

## Evidence

- Verification Report
- Requirement Traceability
- Test Execution Summary
- 주요 E2E 동작 증거
- 남은 Issue 목록
- 실행 및 재현 명령

검증하지 못한 항목은 PASS로 표시하지 마라.

검증 상태는 다음 중 하나를 사용한다.

- PASS
- FAIL
- BLOCKED
- NOT RUN
- NOT APPLICABLE

BLOCKED와 NOT RUN은 PASS가 아니다.

Critical 실패가 남아 있다면 MVP 완료를 선언하지 않는다.

---

# 12. Long-running Development Session Management

작업이 여러 Claude Code 세션에 걸쳐 이어질 수 있으므로 개발 상태를 영속적으로 기록하라.

다음 파일을 유지한다.

```text
docs/development/
  IMPLEMENTATION_PLAN.md
  PROGRESS.md
  CURRENT_STATE.md
  BLOCKERS.md
```

최소 기록 항목:

- 현재 Phase / Slice
- 완료한 작업
- 미완료한 작업
- 마지막 테스트 결과
- 실패한 검증
- 다음 우선 작업
- 관련 설계 결정
- 재현 방법
- Git 작업 트리 상태

컨텍스트 압축이나 세션 종료 후에는 해당 파일을 읽고 작업을 복구할 수 있어야 한다.

장시간 개발 과정에서 이미 검증한 부분을 불필요하게 처음부터 반복하지 마라. 단, 관련 코드나 데이터가 변경되었다면 검증을 다시 수행한다.

진행 상황은 주요 단계 완료 시 간결하게 보고한다.

작업을 백그라운드에서 무기한 수행할 수 있다고 가정하지 마라. 현재 실행 가능한 세션 안에서 진행하고, 중단 시 재개 가능한 상태를 남긴다.

---

# 13. Autonomous Execution Policy

작업 우선순위는 다음과 같다.

1. Critical Correctness
2. P0 Functional Completeness
3. Integration Reliability
4. E2E User Experience
5. Regression Prevention
6. Code Quality
7. Performance Optimization
8. P1/P2 Enhancements

P0가 완료되지 않은 상태에서 불필요한 P1/P2 기능을 확장하지 마라.

아키텍처의 완벽함을 추구하느라 작동하는 MVP 구현이 지연되지 않도록 한다.

반대로 빠른 구현을 위해 지식 그래프의 의미나 사용자 학습 데이터의 정확성을 희생하지 않는다.

**Scientific Correctness와 Learning Path Correctness는 AIXON의 핵심 품질 속성이며, 단순한 최적화 대상이 아니다.**

외부 API 또는 인터넷에 접근하지 못할 때는 검증된 로컬 Seed Graph와 Fixture를 사용해 구현을 계속 진행할 수 있다.

단, 실제로 검증하지 못한 연구 사실을 Verified로 등록하지 마라.

---

# 14. Final Deliverables

최종 산출물은 다음을 포함해야 한다.

1. 설계 검증 보고서
2. 수정·확정된 설계 문서
3. 요구사항 추적표
4. 동작 가능한 MVP 소스코드
5. 데이터베이스 스키마 및 Migration
6. 검증된 Seed Graph
7. 자동 테스트 및 검증 하네스
8. 실제 브라우저 E2E 테스트
9. CI 설정
10. 검증 증거 및 결과 보고서
11. 개발·실행·테스트 README
12. 알려진 제한 사항 및 후속 로드맵

최종 보고 형식:

### 1. Design Audit
- 발견한 Critical / Major Issue
- 수정 내용
- 최종 설계 상태

### 2. Implementation
- 완료된 기능
- Architecture
- 주요 파일 및 모듈

### 3. Verification
- Static / Unit / Integration 결과
- Graph / Learning Engine 검증 결과
- Playwright E2E 결과
- 실제 실행 증거 위치

### 4. Remaining Issues
- 미해결 버그
- 기능 제한
- 검증 불가 항목

### 5. MVP Acceptance
- PASS / FAIL / BLOCKED
- 완료 판단의 객관적 근거

### 6. Next Steps
- MVP 이후 우선 개선 사항
- 다음 개발 단계 권장 사항

---

# 15. Start Instructions

현재 기획·설계 작업이 아직 진행 중이라면 해당 작업을 먼저 완료하라.

기획·설계 완료 후에는 다음 순서로 자율적으로 진행한다.

**Step 1.** 기존 설계 문서 전체 검토  
**Step 2.** Independent Architecture Audit  
**Step 3.** 설계 오류 수정 및 재검증  
**Step 4.** MVP Architecture Baseline 확정  
**Step 5.** Verification Harness 기반 구현  
**Step 6.** Vertical Slice MVP 구현  
**Step 7.** 각 Slice별 Build / Verify / Repair 반복  
**Step 8.** 실제 브라우저 Full E2E 검증  
**Step 9.** 전체 Regression 및 Clean Environment Test  
**Step 10.** Independent Final Review  
**Step 11.** MVP Acceptance Report 작성  

단계마다 불필요한 사용자 승인을 요청하지 말고, 기존 설계와 Acceptance Criteria에 따라 자율적으로 판단한다.

다만 중대한 불확실성이나 해결할 수 없는 외부 차단 요소가 있을 경우 문제와 대안을 명시한다.

**성공 조건은 코드를 많이 작성하는 것이 아니다. 설계의 타당성을 검증하고, 실제 동작 가능한 MVP를 만들고, 그 동작과 정확성을 재현 가능한 증거로 입증하는 것이다.**

이제 현재 설계 진행 상태를 확인하고, 설계 완료 이후 위 실행 계획을 수행하라.
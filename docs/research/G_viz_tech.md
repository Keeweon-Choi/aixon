# G. 그래프 시각화 · 수식 렌더링 · 백엔드 인프라 사실 검증 (AIXON 설계용)

- 기준일: 2026-10-15. 아래 모든 출처의 확인일은 **확인 2026-10-15**이다.
- 표기 규칙
  - `[Sxx]`: 문서 끝 "13. 출처" 목록의 URL.
  - `[Lx]`: 로컬 측정. URL이 없으며 재현 방법을 함께 적었다.
  - **추론**: 출처의 사실에서 이끌어 낸 판단.
  - **확인되지 않음**: 이번 조사에서 근거를 찾지 못한 항목.
- 버전 기준: @xyflow/react 12.12.0, elkjs 0.12.0, cytoscape 3.34.3, d3 7.9.0, sigma 4.0.2 + graphology 0.26.0, @dagrejs/dagre 3.1.1, katex 0.19.0, mathjax 4.1.3, fastapi 0.143.1, pydantic 2.14.1, sqlalchemy 2.1.4, alembic 1.20.0, starlette 1.8.0.
- 라이선스 항목은 원문 인용과 추론을 구분해 적었다. 법률 자문이 아니다.

---

## 1. 그래프 라이브러리 비교표

| 항목 | React Flow (@xyflow/react 12.12.0) | ELK.js (elkjs 0.12.0) | Cytoscape.js 3.34.3 | D3 7.9.0 | Sigma.js 4.0.2 + graphology 0.26.0 | dagre (@dagrejs/dagre 3.1.1) |
|---|---|---|---|---|---|---|
| 성격 | React용 노드 기반 UI 컴포넌트 | 레이아웃 엔진 전용. 원문: "not a diagramming framework itself - it computes positions" [S20] | 그래프 렌더링과 분석 라이브러리. 헤드리스 실행 가능 [S31] | 저수준 툴박스. 원문: "not a charting library in the traditional sense" [S39] | WebGL 그래프 렌더러. 데이터 모델은 graphology [S42] | 방향 그래프 레이아웃 전용 [S52] |
| 렌더링 | 노드: HTML `div`. 엣지: SVG `<g>`. 미니맵: SVG [S06][S07][S09][S10] | 없음 (좌표만 계산) [S20] | 기본 Canvas 2D. 3.31부터 WebGL "preview" 모드 [S32][S33] | 개발자가 SVG·Canvas·WebGL 중 선택 [S39] | WebGL2 캔버스 1개. 4.0부터 라벨도 WebGL(SDF)로 그리고 WebGL1 지원 중단 [S43][S45] | 없음 |
| 레이아웃 | 내장 없음. dagre·d3-hierarchy·d3-force·elkjs 연동 예제만 제공 [S04] | layered(Sugiyama), stress, mrtree, radial, force, disco. box·fixed·random은 항상 포함 [S20] | 내장: null, random, preset, grid, circle, concentric, breadthfirst, cose. 확장: dagre, elk, klay, cola, fcose 등 [S31] | d3-force, d3-hierarchy(트리)만. 레이어드 DAG 모듈 없음 [S40] | graphology: random/circle, force, ForceAtlas2, noverlap. 레이어드 없음 [S50] | ranker(network-simplex, tight-tree, longest-path), rankdir, minlen 등 [S54] |
| 공식 성능 가이드·노드 수 | 성능 페이지 있음. 노드 수 권장치는 없음. 공식 Stress Test 예제는 15×30=450 노드 [S01][S12] | 수치 없음. 레이아웃은 "time-consuming job"이라 Web Worker 지원 [S20] | 문서에 Performance 절이 있다. 블로그 실측: 노드 약 1,200·엣지 16,000에서 Canvas 약 20 FPS, WebGL 100 FPS 이상 [S31][S32] | 확인되지 않음 | 원문: "smooth performance with tens of thousands of nodes and edges" [S43] | React Flow 문서 평: "a focus on speed over choosing the most optimal layout" [S04] |
| 뷰포트 컬링·경량화 옵션 | `onlyRenderVisibleElements`. 기본 false이며 "also adds an overhead" [S02] | 해당 없음 | `hideEdgesOnViewport`, `textureOnViewport`(문서: "now largely moot"), `pixelRatio` [S31] | 직접 구현 | `hideEdgesOnMove`, `hideLabelsOnMove`, `labelRenderedSizeThreshold` 등 [S48] | 해당 없음 |
| 커스텀 노드 | React 컴포넌트로 무엇이든 렌더 [S08] | 해당 없음 | 스타일시트로 지정. HTML 노드는 확장(html, dom-node, node-html-label) 필요 [S31] | 자유 (SVG·HTML을 직접 작성) | WebGL primitives(shape·layer)로 표현. HTML 오버레이는 수동 동기화 [S46][S47] | 해당 없음 |
| 엣지 라벨 | `label` prop, `<EdgeLabelRenderer />`(div 포털) [S06][S10] | 엣지 라벨 배치를 레이아웃에서 계산 [S23] | 스타일 `label`·`source-label`·`target-label`. WebGL 모드에서는 중앙 라벨 1개만 [S31][S32] | 직접 구현 | `renderEdgeLabels` 설정 [S48] | `labelpos`·`labeloffset` [S54] |
| 미니맵 | `<MiniMap />` 내장 [S07] | 해당 없음 | navigator 확장 [S31] | 직접 구현 | 공식 문서 사이트맵에 없음 [S49] | 해당 없음 |
| 그룹·서브플로우 | `parentId` 기반 sub flow. 원문: "not really a child markup-wise" [S05] | compound 그래프와 `hierarchyHandling` [S23][S24] | compound nodes, expand-collapse 확장 [S31] | 직접 구현 | 내장 그룹 없음. cluster-labels 쿡북 예제만 있음 [S49] | 클러스터. 3.1.0부터 클러스터별 rankdir 지정 [S53] |
| 접근성 | Tab·Enter·Space·Esc·화살표 키 조작. 기본 role="group", `ariaRole`·`domAttributes`·`ariaLabelConfig`(현지화), aria-live 제공 [S03] | 해당 없음 | 내장 기능 문서 없음. 메인테이너: "accessibility is something that needs to be built at the app level" [S35] | 공식 a11y 가이드는 확인되지 않음 | a11y 문서 없음 (사이트맵 기준) [S49] | 해당 없음 |
| 라이선스 | MIT. 저작자 표시를 숨기려면 Pro 구독 요청 (정책이며 법적 의무 아님) [S14][S15] | 0.12.0: `EPL-2.0 OR GPL-3.0-or-later`. 0.11.1 이하: `EPL-2.0` [S21][S56n] | MIT | ISC | MIT / MIT | MIT |
| 유지보수 (2026-10-15) | 12.12.0(2026-09-24). 13.0.0-next.0(2026-10-11, `next` 태그). ★38,665 [S17][S19][S89] | 0.12.0(2026-07-17). 0.11.1은 보안 릴리스(2026-03-03). ★2,817 [S21][S89] | 3.34.3(2026-09-07). ★11,237. v4 성능 재설계 이슈 진행 중 [S34][S38][S89] | d3 7.9.0(2024-03-12). d3-force 3.0.0(2021-06-05). ★113,751 [S40][S89] | sigma 4.0.0(2026-10-08) → 4.0.2(2026-10-14). graphology 0.26.0(2025-01-26) [S45][S56n] | 3.0.0(2026-03-22, TS 재작성) → 3.1.1(2026-08-08) [S53][S56n] |
| 번들 크기 (측정 [L3]) | dist/umd/index.js 188,484 B, gzip 약 59 KB. React 제외 | lib/elk.bundled.js 1,609,707 B, gzip 약 467 KB | dist/cytoscape.min.js 435,503 B, gzip 약 136 KB | dist/d3.min.js 279,706 B, gzip 약 92 KB | sigma.min.js 391,628 B(gzip 약 103 KB) + graphology 73,629 B(gzip 약 14 KB) | dist/dagre.min.js 48,956 B, gzip 약 17 KB |
| React 연동 | 네이티브. peer `react >=17`, 13-next는 `>=18` [S19] | 프레임워크 무관 | react-cytoscapejs 최신 2.0.0(2022-09-02) [S56n] | 직접 연동 | @react-sigma/core 5.0.6의 peer가 `sigma ^3.0.2`. v4 미지원 [S51] | 프레임워크 무관 |

---

## 2. React Flow (@xyflow/react)

### 2.1 렌더링 구조
- 노드 DOM 요소의 `domAttributes` 타입은 `Omit<HTMLAttributes<HTMLDivElement>, ...>`이다. 즉 노드는 HTML div로 그려진다 [S09].
- 엣지의 `domAttributes` 타입은 `Omit<SVGAttributes<SVGGElement>, ...>`이다 [S10].
- 엣지에 대한 원문: "Edges are SVG-based. If you want to render more complex labels you can use the `<EdgeLabelRenderer />` component to access a div based renderer." [S06]
- MiniMap에 대한 원문: "It renders each node as an SVG element and visualizes where the current viewport is in relation to the rest of the flow." [S07]

### 2.2 성능 가이드 [S01]
- 커스텀 노드·엣지 컴포넌트는 `React.memo`로 감싸거나 부모 컴포넌트 밖에 선언한다.
- 콜백은 `useCallback`, `defaultEdgeOptions`·`snapGrid` 같은 객체·배열은 `useMemo`로 메모이즈한다.
- 컴포넌트 안에서 `nodes`·`edges` 배열 전체를 구독하지 않는다. 예를 들어 선택된 노드 ID는 별도 상태 필드로 둔다.
- "Collapse large node trees": 노드의 `hidden` 속성을 토글해 펼친 노드만 렌더한다.
- 애니메이션·그림자·그라디언트 같은 복잡한 CSS를 줄인다.
- 노드 수 상한이나 권장 수치는 페이지에 없다.
- 공식 Stress Test 예제는 `initialElements(15, 30)`, 즉 450 노드를 사용한다 [S12].
- `onlyRenderVisibleElements` 원문: "instruct React Flow to only render nodes and edges that would be visible in the viewport. This might improve performance when you have a large number of nodes and edges but also adds an overhead." 기본값은 `false`이다 [S02].

### 2.3 레이아웃 연동 [S04]
- 원문: "We have not implemented our own layouting solution yet".
- 공식 비교표:

  | 라이브러리 | 동적 노드 크기 | Sub-flow 레이아웃 | 엣지 라우팅 |
  |---|---|---|---|
  | Dagre | Yes | Yes¹ | No |
  | D3-Hierarchy | No | No | No |
  | D3-Force | Yes | No | No |
  | ELK | Yes | Yes | Yes |

  ¹ dagre에 미해결 이슈가 있다. dagre#238은 2018-03-26에 열렸고 2026-10-15 현재도 OPEN이다 [S55].
- dagre에 대한 평: "If you need to organize your flows into a tree, we highly recommend dagre."
- elkjs에 대한 평: "We don't often recommend elkjs because it's complexity makes it difficult for us to support folks when they need it."
- elkjs는 레이아웃이 비동기로 실행되므로 hook으로 감싸야 한다.
- d3-hierarchy는 단일 루트를 전제하고 모든 노드에 같은 크기를 부여한다.
- 노드를 피해 가는 자동 엣지 라우팅은 Pro 예제(libavoid 사용)로만 제공된다.
- 공식 ELK 예제는 `elkjs/lib/elk.bundled.js`(메인 스레드 번들)를 import한다 [S13].

### 2.4 상호작용 기능
- **커스텀 노드**: 원문 "all you need to do is create a React component". React Flow가 선택·드래그·핸들 기능을 갖춘 래퍼로 감싼다 [S08].
- **Sub flows** [S05]
  - `parentId`를 쓴다 (11.11.0에서 `parentNode`에서 이름이 바뀌었다).
  - nodes 배열에서 부모 노드가 자식보다 앞에 와야 한다.
  - `extent: 'parent'`로 자식이 부모 밖으로 나가지 못하게 할 수 있다.
  - 원문: "The child node is not really a child markup-wise."
- **좌표계 정렬 요소**: `<ViewportPortal />`은 노드·엣지와 같은 좌표계에 컴포넌트를 렌더하며 줌·팬의 영향을 받는다 [S11]. 연도 축이나 눈금선에 쓸 수 있다 (**추론**).
- **팬 경계**: `translateExtent`로 viewport 경계를 지정한다 [S02].
- **노드 위치**: 노드의 `position: XYPosition`을 직접 지정한다 [S09].

### 2.5 접근성 [S03]
- 기본적으로 모든 노드와 엣지가 키보드로 포커스·조작 가능하다.
  - `nodesFocusable` 기본 true, `edgesFocusable` 기본 true [S02].
  - 원문: "These elements receive tabIndex={0} and, by default, role="group"".
- 키 조작: Enter·Space로 선택, Escape로 선택 해제, 화살표 키로 노드 이동(Shift를 누르면 빠르게).
- `disableKeyboardA11y`를 켜면 화살표 이동만 꺼진다.
- `autoPanOnNodeFocus`(기본 true): 포커스된 노드가 보이도록 자동으로 팬한다.
- `ariaLabelConfig`: 안내 문구를 현지화한다. 키 예: `node.a11yDescription.default`, `minimap.ariaLabel`.
- 노드 이동은 `aria-live="assertive"` 영역으로 알린다.
- 공식 문서의 자체 주장: "React Flow provides features that can help you meet key WCAG 2.1 AA criteria when properly implemented".
- 커스텀 노드 안에 인터랙티브 요소가 있으면 노드 자체에 `ariaRole: 'button'`을 주지 말라고 권고한다.
- 이력 (xyflow#3147, 마크업 접근성 요청) [S18]
  - 메인테이너 답변(2025-06-11): "In 12.7.0 we added `ariaRole` for nodes and edges and `domAttributes`".
  - 같은 답변: "For now we decided against an `as` prop".
  - 노드·엣지의 기본 role이 "group"으로 바뀌었다.

### 2.6 라이선스와 Pro
- 원문: "React Flow is open-source MIT-licensed software." [S14]
- 저작자 표시 정책 원문: "We can't legally require you to keep the attribution — React Flow is MIT-licensed ... attribution visible, no subscription needed; no attribution, please subscribe." [S15]
- React Flow Pro는 라이브러리가 아니라 구독 서비스다 [S14][S16].
  - 포함 항목: Pro 예제·템플릿, 이슈 우선 처리, 이메일 지원.
  - 가격 표기가 페이지마다 다르다. Starter "$169 per month", Professional "$289 per month"는 S14, "from €129"는 S16에 있다. 구매 전 재확인이 필요하다.
  - Pro 예제 목록에 AIXON 기능과 겹치는 항목이 있다: Auto Layout, Expand and Collapse(dagre 사용), Dynamic Layouting, Node Position Animation, Edge Routing(libavoid).
  - 학생·교육자·오픈소스 개발자는 Pro 예제를 무료로 받을 수 있다고 안내한다 [S16].

### 2.7 유지보수 [S17][S19][S89]
- 최근 릴리스: 12.11.3(2026-08-12), 12.11.4·12.11.5(2026-08-25), 12.11.6(2026-09-01), 12.12.0(2026-09-24).
- 13.0.0-next.0(2026-10-11)이 `next` dist-tag로 나와 있다.
  - peer: `react >=18`.
  - 의존성: `zustand ^5.0.0`, `react-compiler-runtime ^1.0.0`.
  - 12.x의 의존성은 `zustand ^4.4.0`이다.
- GitHub xyflow/xyflow: ★38,665, 마지막 push 2026-10-12.

---

## 3. ELK.js (elkjs)

### 3.1 정체와 Web Worker [S20]
- 원문: "ELK's flagship is a layer-based layout algorithm ... based on the ideas originally introduced by Sugiyama et al."
- 원문: "elkjs is not a diagramming framework itself".
- 파일 구성
  - `elk-api.js`: API만 담는다.
  - `elk-worker.js`: GWT로 Java에서 변환된 레이아웃 코드.
  - `elk.bundled.js`: 위 둘을 묶은 번들.
- Web Worker 원문: "Web Workers are supported out of the box". `new ELK({ workerUrl: ... })`로 켜고 `terminateWorker()`로 종료한다.
- Node.js에서는 `web-worker` 패키지가 필요하다. 없으면 경고를 내고 non-worker 버전으로 동작한다.
- 기본 알고리즘 배열: `[ 'layered', 'stress', 'mrtree', 'radial', 'force', 'disco' ]`. box·fixed·random은 항상 포함된다.
- README가 꼽는 반복 이슈
  - 이전 레이아웃 결과 반영과 노드·엣지의 증분 추가 (elkjs#100, elk#355, elk#627).
  - GWT 변환과 모듈 구조 때문에 react·webpack 환경에서 생기는 문제: "`g is not defined`", "`Can't resolve web-worker`".

### 3.2 ELK Layered 주요 옵션 (공식 Reference "current" [S23][S24], enum 설명은 ELK 소스 Javadoc [S25])

| 옵션 | ID | 값 | 기본값 | 비고 (원문 요약) |
|---|---|---|---|---|
| Node Layering Strategy | `org.eclipse.elk.layered.layering.strategy` | NETWORK_SIMPLEX, LONGEST_PATH, LONGEST_PATH_SOURCE, COFFMAN_GRAHAM(adv.), INTERACTIVE(adv.), STRETCH_WIDTH·MIN_WIDTH·BF_MODEL_ORDER·DF_MODEL_ORDER(experimental) | NETWORK_SIMPLEX | INTERACTIVE: "Nodes are put into layers according to their relative position. The actual positions as given in the input diagram are considered here." [S25] |
| Node Placement Strategy | `org.eclipse.elk.layered.nodePlacement.strategy` | SIMPLE, INTERACTIVE(adv.), LINEAR_SEGMENTS, BRANDES_KOEPF, NETWORK_SIMPLEX | BRANDES_KOEPF | INTERACTIVE: "Interactive node placer that leaves y coordinates of nodes untouched." [S25] |
| Crossing Minimization Strategy | `org.eclipse.elk.layered.crossingMinimization.strategy` | LAYER_SWEEP, MEDIAN_LAYER_SWEEP, INTERACTIVE(adv.), NONE | LAYER_SWEEP | NONE을 쓰려면 GreedySwitch도 꺼야 한다 [S25] |
| Semi-Interactive Crossing Minimization | `...crossingMinimization.semiInteractive` | boolean | false | 레이어 안 노드 순서를 `org.eclipse.elk.position`에서 가져와 유지한다 |
| Cycle Breaking Strategy | `org.eclipse.elk.layered.cycleBreaking.strategy` | GREEDY, DEPTH_FIRST, INTERACTIVE(adv.), MODEL_ORDER, GREEDY_MODEL_ORDER, SCC_CONNECTIVITY, SCC_NODE_TYPE, DFS_NODE_ORDER, BFS_NODE_ORDER | GREEDY | 역전된 엣지는 정방향과 반대쪽을 향한다 |
| Port Constraints | `org.eclipse.elk.portConstraints` | UNDEFINED, FREE, FIXED_SIDE, FIXED_ORDER, FIXED_RATIO, FIXED_POS | UNDEFINED | 노드에 적용 |
| Layer Constraint | `...layering.layerConstraint` | NONE, FIRST, FIRST_SEPARATE, LAST, LAST_SEPARATE | NONE | 노드에 적용 |
| Layer Choice Constraint | `...layering.layerChoiceConstraint` | Integer | null | 원문: "only evaluated as part of the InteractiveLayeredGraphVisitor, which must be applied manually or used via the `DiagramLayoutEngine." |
| Position Choice Constraint | `...crossingMinimization.positionChoiceConstraint` | Integer | null | Layer Choice Constraint와 같은 제약 |
| Consider Model Order | `...considerModelOrder.strategy` | NONE, NODES_AND_EDGES, PREFER_EDGES, PREFER_NODES | NONE | 입력 순서를 보존한다. 단 교차가 늘지 않는 한에서만 |
| Layout Partitioning | `org.eclipse.elk.partitioning.activate` / `.partition` | boolean / Integer | false / — | 원문: "the node with lower index is placed to the left of the other node (with left-to-right layout direction)". 단 "may only be guaranteed to work if all nodes have a layout partition configured, or at least if edges that cross partitions are not part of a partition-crossing cycle" |
| interactive Layout | `org.eclipse.elk.interactiveLayout` | boolean | false | "Whether the graph should be changeable interactively and by setting constraints" |
| Generate Position and Layer IDs | `...generatePositionAndLayerIds` | boolean | false | 출력 속성 `layerId`·`positionId`를 생성한다 |
| Hierarchy Handling | `org.eclipse.elk.hierarchyHandling` | INHERIT, INCLUDE_CHILDREN, SEPARATE_CHILDREN | INHERIT | 루트가 INHERIT이면 SEPARATE_CHILDREN으로 동작 |
| Direction | `org.eclipse.elk.direction` | UNDEFINED, RIGHT, LEFT, DOWN, UP | UNDEFINED | — |
| (기타) | Edge Routing 기본 ORTHOGONAL, Thoroughness 기본 7 | | | [S23] |

**고정 좌표와 부분 레이아웃**
- Fixed 알고리즘(`org.eclipse.elk.fixed`) 원문: "Keeps the current layout as it is, without any automatic modification. Optional coordinates can be given for nodes and edge bend points." 좌표는 `org.eclipse.elk.position`으로 준다 [S28][S24].
- layerChoiceConstraint에 대한 ELK 메인테이너 답변 (eclipse-elk/elk#908) [S26]
  - 원문: "layerChoiceConstraints are not directly supported by ELK but require postprocessing by the core.service package, which is eclipse dependent."
  - 대안 1: 노드 position을 지정하고 interactive 사이클 제거·레이어링 전략을 쓴다.
  - 대안 2: 연결되지 않은 서브그래프에도 일관된 레이어가 필요하면 partition을 쓴다.
- kieler/elkjs#116에서도 메인테이너가 layer partitions를 안내했고, 질문자가 `partitioning.activate`와 노드별 partition 번호로 해결했다 [S27].
- 0.12.0 번들에 옵션 문자열이 들어 있는지 확인했다 [L3]. `curl https://unpkg.com/elkjs@0.12.0/lib/elk-worker.min.js | grep`으로 다음이 모두 검출됐다.
  - `MEDIAN_LAYER_SWEEP`, `BF_MODEL_ORDER`, `partitioning.activate`, `semiInteractive`, `layerChoiceConstraint`, `InteractiveLayeredGraphVisitor`.
  - 문자열이 있다는 것만으로 elkjs에서 layerChoiceConstraint가 실제로 동작하는지는 알 수 없다 (**확인되지 않음**).

### 3.3 라이선스 (EPL-2.0 OR GPL-3.0-or-later)
- elkjs 0.12.0 릴리스 노트 원문: "Most notably elkjs 0.12.0 adds GPL-3.0 as a secondary license, allowing elkjs to be used in GPL-3.0 or later projects." [S21]
- npm license 필드: 0.12.0은 `EPL-2.0 OR GPL-3.0-or-later`, 0.11.1과 0.9.3은 `EPL-2.0` [S56n].
- LICENSE.md는 EPL-2.0 전문이다. Exhibit A의 Secondary License는 "GNU General Public License v3.0 or later"이다 [S22].
- EPL-2.0 조문 [S22]
  - "Distribute"의 정의: "distributing or b) making available in any manner that enables the transfer of a copy."
  - §3.1(a): 어떤 형태로 배포하든 Source Code로도 제공해야 하고, Source Code가 이 Agreement 아래 제공된다는 문구와 입수 방법을 함께 알려야 한다.
  - §3.3: 저작권·라이선스 고지를 삭제하거나 변경할 수 없다.
- Eclipse EPL-2.0 FAQ [S29]
  - 4.17 (수정 없이 컴파일해 상용 배포할 때 소스를 동봉해야 하는가): "No. But you do need to include a statement indicating where the source code is available and information on how to obtain it."
  - 4.22 (자신이 쓴 모듈을 함께 배포할 때 그 소스를 EPL로 공개해야 하는가): "No, as long as the module is not a Modified Work of the Program."
  - 4.5: "The EPL-2.0 continues to be a weak copyleft license."
  - 1.4: "The license is now suitable for scripting languages such as JavaScript"
  - 4.20: 수정했더라도 배포하지 않으면 수정본을 공개할 의무가 없다.
- 이 조문들을 수정하지 않은 elkjs를 웹앱에 번들하는 경우에 적용하면 다음과 같다 (**추론**).
  - GWT로 변환·minify된 JS는 "preferred form for making modifications"가 아니므로 비소스 형태로 볼 여지가 크다.
  - 따라서 배포 시에는 elkjs LICENSE와 고지, 그리고 소스 위치(github.com/kieler/elkjs)를 함께 제공하면 4.17의 요건을 충족한다.
  - AIXON 자체 코드는 4.22에 따라 EPL을 적용받지 않는다.
  - 로컬 단독 사용이라 제3자에게 전달하지 않으면 "Distribute"가 일어나지 않는다. 다만 웹으로 호스팅해 타인에게 JS를 제공하면 "making available ... transfer of a copy"에 해당할 수 있다.

### 3.4 유지보수 [S21][S89]
- 릴리스: 0.10.0(2025-03-13), 0.10.1(2025-06-25), 0.10.2(2025-07-22), 0.11.0(2025-09-15), 0.11.1(2026-03-03, "security release"), 0.12.0(2026-07-17).
- GitHub ★2,817, 마지막 push 2026-10-14.

---

## 4. Cytoscape.js

### 4.1 렌더링과 WebGL 상태
- 블로그 원문: "Under the hood it uses the browser's Canvas API to draw". 이어서 "Version 3.31 of Cytoscape.js contains a preview of a new WebGL renderer" [S32]. 3.31.0 릴리스 글은 2025-01-13자다.
- 같은 글: "The WebGL renderer is brand new and is available as a preview release in version 3.31. Any options or API being introduced are provisional and may change." [S32]
- 켜는 방법: `renderer: { name: 'canvas', webgl: true, ... }`. 원문: "It's more like a new mode for the Canvas renderer." [S32]
- 이슈 #3305 "Initial, experimental WebGL rendering support"(milestone 3.31.0) 원문: "until the WebGL rendering feature has been marked as final, the API and behaviour of the renderer will be subject to change." [S33]
- 2026-10-15 현재 상태
  - 공식 문서 js.cytoscape.org 본문에서 "webgl" 문자열이 한 번도 나오지 않는다 (curl과 grep 결과) [S31].
  - final로 표시됐다는 릴리스 노트도 찾지 못했다. 3.32~3.34의 GitHub 릴리스 본문은 "Release version vX" 한 줄뿐이다 [S38].
  - 그러므로 **"preview/experimental 상태 유지"로 보는 것이 타당하다 (추론)**.
- WebGL 모드의 제약 [S32]
  - 엣지는 straight, haystack, bezier만 지원한다.
  - dashed 선, overlay·underlay를 지원하지 않는다.
  - 엣지 라벨은 중앙 1개만 쓸 수 있다.
  - 화살표는 triangle만 지원한다.
  - 그라디언트를 쓸 수 없다.
- WebGL 관련 미해결 이슈: #3374(화살표가 항상 triangle), #3376(compound 노드 시각 불일치) [S33b].
- 성능 수치 [S32]: M1 MacBook Pro·Chrome에서 노드 약 1,200·엣지 16,000일 때 Canvas 약 20 FPS, WebGL 100 FPS 이상이었다. 원문: "most applications that use Cytoscape.js probably don't need the WebGL renderer."
- v4 계획: 이슈 #3486 "Cytoscape.js v4 performance redesign"(2026-07-13, OPEN)이 GPU 중심 데이터 모델, WebGPU, typed-array 저장 등을 검토하고 있다. 원문: "This would be worth a breaking change, a v4." [S34]

### 4.2 성능 가이드 [S31]
- 원문: "Performance is a function of graph size".
- 비용이 큰 요소: 라벨과 엣지. 대안으로 haystack 엣지, 실선, 화살표 생략, `min-zoomed-font-size` 지정을 제시한다.
- compound 노드도 스타일 계산과 렌더링 비용을 늘린다.
- 조정 옵션: `pixelRatio: 1`, `hideEdgesOnViewport`, `textureOnViewport`. 앞의 두 옵션은 "only very, very large graphs"에서만 효과가 있다고 적혀 있다.

### 4.3 레이아웃
- 내장: null, random, preset, grid, circle, concentric, breadthfirst, cose [S31].
- preset 원문: "The preset layout puts nodes in the positions you specify manually." [S31]
- 확장
  - cytoscape-dagre 4.0.1(2026-08-28): "Dagre v3 is bundled into the distributed extension files" [S36].
  - cytoscape-elk 2.3.0(2024-11-26): 의존성이 `elkjs ^0.9.3`이다 [S37]. npm caret 규칙상 0.9.x에 고정되므로 최신 0.12.0을 쓰지 못한다 (**추론**).
  - cytoscape-klay 3.1.4(2020-10-07): `klayjs ^0.4.1`에 의존한다. klayjs README 원문: "**Deprecated: Use elkjs**" [S37].

### 4.4 상호작용과 접근성
- compound nodes 원문: "A compound node contains a number of child nodes, similar to how a HTML DOM element can contain a number of child elements." [S31]
- UI 확장: expand-collapse, navigator("A bird's eye view widget of the graph"), html, dom-node, node-html-label, popper [S31].
- 접근성: 메인테이너 maxkfranz의 #3091 답변 [S35]
  - 원문: "Is it acceptable to force users to tab through potentially thousands of elements to get to the one they want?"
  - 원문: "Generally, accessibility is something that needs to be built at the app level ... Cytoscape generally shouldn't, and can't, make those decisions for you."
- 키보드 이벤트: 메인테이너 답변 원문 "keyboard events are emitted only for widgets like text boxes." (#2710) [S35b]
- Canvas 안의 노드는 DOM 요소가 아니어서 스크린리더가 개별 노드에 접근하려면 별도의 병렬 DOM(또는 Data Navigator 같은 레이어)이 필요하다 (**추론**).

### 4.5 유지보수
- 릴리스: 3.33.0(2025-07-28), 3.34.0(2026-06-02), 3.34.3(2026-09-07) [S38].
- GitHub ★11,237, 마지막 push 2026-10-14 [S89].

---

## 5. D3 (+ d3-dag)
- 원문: "D3 is a low-level toolbox", "not a charting library in the traditional sense" [S39].
- 원문: "you use D3 directly with web standards such as SVG and Canvas" [S39]. 직접 차트를 만드는 경우를 두고 "(or even WebGL)"라고도 적었다 [S39].
- 공식 페이지는 고수준 대안으로 Observable Plot을 권한다 [S39].
- d3 7.9.0에 포함된 모듈 중 그래프 관련은 d3-force, d3-hierarchy, d3-zoom, d3-drag, d3-scale, d3-axis이다. 레이어드 DAG 레이아웃 모듈은 없다 [S40].
- 릴리스: d3 7.9.0(2024-03-12), d3-force 3.0.0(2021-06-05), d3-hierarchy 3.1.2(2022-04-02) [S40]. GitHub d3/d3의 마지막 push는 2026-05-28이다 [S89].
- d3-dag(외부, MIT) [S41]
  - 원문: "Lightweight, TypeScript-first DAG layout for the web", "provides layered graph layout algorithms for directed acyclic graphs".
  - 원문: "Works with React Flow - drop-in replacement for dagre as a layout engine".
  - 1.2.0(2026-04-13), 1.2.2(2026-07-05).
  - README는 elkjs를 "~500KB transpiled Java"라고 비교한다. 이는 d3-dag 측 주장이다.
- D3 공식 문서에서 접근성 전용 가이드는 **확인되지 않음**.

---

## 6. Sigma.js + graphology
- 원문: "A WebGL-powered JavaScript library for interactive graph visualization, built on graphology." [S42]
- 원문: "Sigma.js uses WebGL to render graphs efficiently, achieving smooth performance with tens of thousands of nodes and edges." [S43]
- 라벨은 "Labels are rendered on the GPU using an SDF-based text atlas"이다 [S43].
- DOM은 WebGL 캔버스(stage)와 마우스 이벤트용 투명 div 두 개뿐이다. 노드 판별은 GPU picking으로 한다 [S43].
- 4.0.0(2026-10-08) 주요 변경 [S45][S46]
  - 원문: "complete rewrite of the programs system".
  - 노드·엣지 라벨을 WebGL(SDF)로 옮겼다.
  - 원문: "Drops WebGL 1 support in favor of WebGL 2".
  - 선언형 styles·primitives API를 도입했다.
  - 노드 드래그를 내장했다.
  - parallel edge와 self-loop를 기본 처리한다.
  - `hidden`·`forceLabel`이 `visibility`·`labelVisibility`로 바뀌었다 (breaking).
- 성능 가이드 [S44]
  - 원문: "with hundreds of thousands of edges, some choices start to matter a lot".
  - `antialiasEdges: false`가 GPU 렌더 전체를 "up to x5" 빠르게 할 수 있다.
  - 반투명은 비싸다.
  - `enableEdgeEvents`는 기본 false다.
- HTML·SVG 요소를 쓰려면 `graphToViewport()`와 `afterRender`로 오버레이를 직접 동기화해야 한다 [S47].
- 공식 사이트맵에는 accessibility와 minimap 페이지가 없다 [S49].
- graphology 표준 라이브러리 [S50]
  - 레이아웃: layout(random, circle 등), layout-force, layout-forceatlas2, layout-noverlap.
  - dag: "cycle detection, topological sorting etc."
  - 레이어드 레이아웃은 없다.
- React 바인딩 @react-sigma/core 5.0.6은 peer가 `sigma ^3.0.2`이고 2025-12-01 이후 갱신되지 않았다 [S51]. v4가 나온 지 1주일이라 생태계가 아직 따라오지 못한 상태다.

---

## 7. dagre (@dagrejs/dagre)
- README 원문: "There are 2 versions on NPM, but only the one in the DagreJs org is receiving updates right now." [S52]
- 레거시 npm `dagre`의 최신은 0.8.5다 [S56n].
- changelog [S53]
  - 3.0.0: "Full TypeScript Rewrite", 타입 내장, ESM·CJS export 정비.
  - 3.1.0: "Per-Cluster Direction Support"(클러스터별 rankdir·ranksep·nodesep·align).
  - 3.1.0: "Dynamic Graph Layout Support ... `useDynamic` and `corePath` ... persistent node ordering and layout stability when modifying graph structures."
- npm 릴리스: 2.0.1(2025-12-01), 3.0.0(2026-03-22), 3.1.0(2026-08-02), 3.1.1(2026-08-08). `latest`는 3.1.1이다 [S56n].
- GitHub Releases 페이지는 v2.0.0(2025-11-23)까지만 있다. 태그는 v3.1.1까지 있다 [S52].
- 의존성은 `@dagrejs/graphlib 4.0.5` 하나다 [S56n].
- 설정 [S54]
  - 그래프: `rankdir`(TB/BT/LR/RL), `align`, `nodesep`, `edgesep`, `ranksep`, `acyclicer`(greedy), `ranker`(network-simplex/tight-tree/longest-path).
  - 엣지: `minlen`("The number of ranks to keep between the source and target of the edge."), `weight`, `labelpos`, `labeloffset`.
- GitHub ★5,826, 마지막 push 2026-08-08 [S89].
- dagre에는 노드의 rank를 절대값으로 고정하는 옵션이 설정 표에 없다 (wiki 표 기준) [S54]. 연도별 열 정렬은 `minlen`으로 근사하거나 후처리로 x를 덮어써야 한다 (**추론**).

---

## 8. KaTeX vs MathJax v4

| 항목 | KaTeX 0.19.0 | MathJax 4.1.3 (v4) |
|---|---|---|
| 라이선스 | MIT [S56n][S57] | Apache-2.0 [S63] |
| 속도 | 자체 주장: "The fastest math typesetting library for the web." 원문: "KaTeX renders its math synchronously and doesn't need to reflow the page." 홈페이지 비교 애니메이션에는 MathJax 버전과 수치가 없다 [S57] | v4는 Speech Rule Engine(SRE)을 성능 개선을 위해 재작성했고, 음성 생성을 web worker로 옮겨 "the page will remain responsive" [S61] |
| 독립 벤치마크 | **확인되지 않음** | **확인되지 않음** |
| 출력과 접근성 | `output`: `html`, `mathml`, `htmlAndMathml`(기본). 원문: "includes MathML for accessibility" [S58]. 번들 확인 결과 `.katex-html`에 `aria-hidden="true"`, `.katex-mathml`은 1px·clip-path로 시각적으로 숨긴다 [S60] | expression explorer를 기본으로 켠다. SRE가 만든 음성 문자열을 `aria-label`·`aria-braille-label`로 노출한다. 수식에 포커스할 수 있고 화살표 키로 탐색한다. assistive MathML은 combined 컴포넌트에서 뺐다(메뉴에서 켤 수 있음) [S61] |
| 한국어 | 해당 정보 없음 | 원문: "There is a new Korean and Afrikaans locales for speech output." [S61]. 음성 품질은 **확인되지 않음** |
| 숨김 MathML 방식에 대한 평가 | — | MathJax 문서 원문: "a stop-gap measure that was both clunky and somewhat fragile, and changes in screen readers often rendered it ineffective (e.g., the current VoiceOver version doesn't read the mathematics and skips it entirely, while Windows screen readers indicate clickable math, but then fail to read it)" [S61] |
| 테스트 범위 | — | "13 browser/os/screen-reader combinations" (VoiceOver, NVDA, JAWS, Orca) [S61] |
| 릴리스·변경 | 0.19.0(2026-10-01) BREAKING: 누락된 문자 metric을 `strict`로 보고한다 (에러 코드 symbolNotInFont) [S59] | 4.0.0(2025-08-04), 4.1.3(npm, 2026-07). v4는 "opt-in update"이며 "potentially breaking changes"가 있다 [S62][S63] |
| 크기 (측정 [L3]) | katex.min.js 272,868 B(gzip 약 76 KB), katex.min.css 24,793 B(gzip 약 3.5 KB). 폰트는 별도 | tex-chtml.js 997,445 B(gzip 약 281 KB). 폰트와 SRE worker의 추가 로드량은 **확인되지 않음** |

- KaTeX의 `htmlAndMathml`은 MathJax 문서가 "fragile"이라고 평가한 숨김 MathML과 같은 계열의 방식이다. 스크린리더 지원이 중요하면 실제 VoiceOver·NVDA로 비교 테스트할 필요가 있다 (**추론**).

---

## 9. 복잡한 그래프·네트워크 시각화 접근성 권고 (핵심 4가지)

### R1. 두 부분 텍스트 대안 제공: 짧은 설명 + 긴 설명 [S64]
- W3C WAI Images Tutorial "Complex Images"는 적용 대상에 "graphs and charts, including flow charts and organizational charts" 및 diagrams를 포함한다.
- 원문: "a two-part text alternative is required. The first part is the short description to identify the image ... The second part is the long description – a textual representation of the essential information conveyed by the image."
- 원문: "Make long descriptions available to everyone".

### R2. 데이터 표 제공과 구조 기반 탐색 [S66]
Chartability(Frank Elavsky)는 POUR+CAF 7원칙과 50개 휴리스틱으로 구성되며, 그중 14개가 critical이다 [S65][S66].
- "No table (critical)" 원문: "A table must be provided that contains a human-readable version of the data the chart is based on."
- 같은 항목은 표만으로는 부족하다고도 쓴다. 원문: "chart structures can represent relationships that are non-tabular."
- "Information cannot be navigated according to narrative or structure" 원문: "Keyboard navigation must be comparable to the data structure (including cases where the data structure is novel) as well as provide linear or tabular navigation (like in a table or list)."
- 키보드 커서 이동(focus)은 마우스 hover와, Enter·Space는 클릭과 같은 동작을 해야 한다 ("Interaction modality only has one input type (critical)").
- 조작 안내문을 제공해야 한다 ("No interaction cues or instructions (critical)").

### R3. 탭 정지 수 제한과 roving tabindex [S66][S67]
- Chartability 원문: "Every interactive chart element must NOT have its own tab stop unless the chart is small or the tabs are programmatically revealed (such as having a single tab stop at the root of a chart and then a way to enter further layers or sections of the chart using keyboard controls)."
- WAI-ARIA APG의 roving tabindex 원문: "the element that is to be included in the tab sequence has tabindex="0" and all other focusable elements contained in the composite have tabindex="-1"". 같은 문서는 Tree View, Grid, Treegrid 같은 composite 패턴을 예시로 든다 [S67].

### R4. 색만으로 정보를 전달하지 않기 [S68][S66]
- WCAG 2.2 SC 1.4.1 원문: "Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element."
- Chartability: 대비 기준은 텍스트 4.5:1, 차트 도형 3:1이다. 텍스트는 12px/9pt 이상이어야 한다 [S66].

### 연구 근거
- **Data Navigator** (Elavsky, Nadolskis, Moritz; IEEE VIS 2023 / TVCG 2024) [S69]
  - 원문: "a system built on a dynamic graph structure, enabling developers to construct navigable lists, trees, graphs, and flows".
  - 화면 위에 의미론적 HTML 접근성 레이어를 얹는 방식이다.
  - npm `data-navigator` 3.0.0, MIT.
- **TADA** (CHI 2024, Honourable Mention) [S70]
  - 시각장애·저시력 사용자가 node-link 다이어그램을 탐색하도록 돕는다.
  - 기능: 특정 노드 검색, 노드에서 노드로 이동, 정보 필터링.
  - 인터뷰 15명, 평가 25명.
- **Benthic** (ASSETS 2025) [S71]
  - 스크린리더 탐색 구조를 시각 구조와 일치시킨다("perceptually congruent").
  - hypergraph 기반으로 계층(포함)과 인접(연결) 관계를 함께 다룬다.
  - 시각장애 참가자 15명 연구.

---

## 10. 백엔드·인프라

### 10.1 SQLite FTS5 trigram
- 3.34.0(2020-12-01) 원문: "Enhanced FTS5 to support trigram indexes." [S73]
- 공식 문서 4.3.4 [S72]
  - 원문: "a query or phrase token may match any sequence of characters within a row, not just a complete token."
  - 옵션 `case_sensitive`(기본 0)와 `remove_diacritics`(기본 0). 둘 다 1로 설정하면 오류다.
  - `remove_diacritics`를 켜지 않으면 LIKE·GLOB에도 인덱스를 쓴다. `case_sensitive 1`이면 GLOB에만 쓴다.
  - **최소 길이** 원문: "Substrings consisting of fewer than 3 unicode characters do not match any rows when used with a full-text query. If a LIKE or GLOB pattern does not contain at least one sequence of non-wildcard unicode characters, FTS5 falls back to a linear scan of the entire table."
  - `detail=none`이나 `detail=column`이면 full-text 쿼리 토큰을 3글자 이하로 제한한다.
  - LIKE에 ESCAPE 절이 있으면 인덱스를 쓰지 못한다.
- **[L1] 로컬 실험**
  - 환경: Python 3.12.7, 내장 sqlite3(SQLite 3.45.3), `:memory:` DB.
  - `MATCH '"검색"'`(2음절) → 0건. `MATCH '"어텐션"'`(3음절) → 일치. `MATCH '"검색 알"'`(공백 포함 4글자) → 일치.
  - `LIKE '%검색%'` → 결과는 정상 반환.
    - 20만 행 기준 2음절 LIKE: 약 34 ms. 같은 데이터의 일반 테이블 LIKE 스캔: 약 23 ms.
    - 3음절 `LIKE '%어텐션%'`: 약 0.1 ms.
    - 따라서 2음절 LIKE는 선형 스캔으로 동작하는 것으로 보인다 (**추론**).
  - `unicode61` 토크나이저 비교: "어텐션을 사용한다" 행에서 `MATCH '어텐션'`은 0건, `MATCH '어텐션*'`은 1건이다. 조사가 붙은 어절이 하나의 토큰이 되기 때문이다.
  - 재현 방법: python3 -c로 FTS5 테이블 2개(unicode61, trigram)를 만들고 위 질의를 실행하면 된다.
- 한국어·CJK 적합성 (**추론**)
  - trigram은 형태소 분석 없이 부분 문자열로 일치시켜 조사·어미 문제를 피한다.
  - 대신 2음절 이하 질의(예: "검색", "모델")는 MATCH로 찾지 못한다. LIKE 스캔이나 별도 처리가 필요하다.
  - 단일 사용자의 소규모 코퍼스라면 스캔 비용은 수십 ms 수준이다 ([L1]).

### 10.2 SQLite JSON
- 원문: "built into SQLite by default, as of SQLite version 3.38.0 (2022-02-22)". 끄려면 `-DSQLITE_OMIT_JSON`을 쓴다 [S74].
- JSONB: "Beginning with version 3.45.0 (2024-01-15)". 원문: "intended for internal use by SQLite only"이며 PostgreSQL JSONB와 바이너리 호환되지 않는다 [S74].
- `->`와 `->>` 연산자는 3.38.0부터 [S73], JSON5 읽기는 3.42.0부터 [S74], 표현식 인덱스는 3.9.0부터 지원한다 [S74b].
- 최신 SQLite는 3.54.0(2026-10-09)이다 [S73].
- 3.53.0부터 `ALTER TABLE ... ALTER COLUMN ... SET/DROP NOT NULL`을 지원한다 [S76]. DROP COLUMN은 3.35.0, RENAME COLUMN은 3.25.0부터다 [S73].

### 10.3 SQLite WAL 동시성 [S75]
- 원문: "WAL provides more concurrency as readers do not block writers and a writer does not block readers. Reading and writing can proceed concurrently."
- 원문: "since there is only one WAL file, there can only be one writer at a time."
- 원문: "All processes using a database must be on the same host computer; WAL does not work over a network filesystem."
- 원문: "WAL does not work well for very large transactions. For transactions larger than about 100 megabytes, traditional rollback journal modes will likely be faster."
- WSL에 대한 Microsoft 권고 원문: "For the fastest performance speed, store your files in the WSL file system if you are working in a Linux command line" [S88]. 현재 프로젝트 경로 /home/choi/projects/aixon은 Linux 파일시스템에 있다.

### 10.4 sqlite-vec / pgvector
- **sqlite-vec** [S77]
  - README 원문: "`sqlite-vec` is a pre-v1, so expect breaking changes!"
  - "Written in pure C, no dependencies". `vec0` 가상 테이블에 float·int8·binary 벡터를 저장한다.
  - Mozilla Builders 프로젝트다.
  - 라이선스: 저장소에 LICENSE-MIT와 LICENSE-APACHE가 있다. npm 표기는 "MIT OR Apache"다.
  - PyPI 최신 안정판은 0.1.9이고, GitHub 최신은 v0.1.10-alpha.4(2026-05-18, pre-release)다.
- **pgvector** [S78]
  - 최신 0.8.7(2026-10-01).
  - META.json의 license는 "PostgreSQL"이다.
  - 원문: "supports Postgres 13+". PostgreSQL 서버의 확장이다.

### 10.5 Python stdlib graphlib [S79]
- `graphlib.TopologicalSorter`는 "Added in version 3.9."
- CycleError 원문: "Subclass of ValueError raised by TopologicalSorter.prepare() if cycles exist in the working graph."
- 사이클 정보 원문: "The detected cycle can be accessed via the second element in the args attribute ... the first and the last node will be the same".
- **[L2] 로컬 확인**
  - `{'a':{'b'},'b':{'a'}}`로 CycleError를 일으키면 `args[1] == ['a','b','a']`다.
  - `get_ready()`로 받은 배치를 모두 `done()`한 뒤 다시 `get_ready()`를 호출하면 배치가 출발점 기준 최장 경로 레이어가 된다. 예: `[['A'], ['B','C','F'], ['D'], ['E']]`.
  - 레이어드 DAG의 rank 계산에 바로 쓸 수 있다 (**추론**).

### 10.6 Next.js 16 static export vs Vite SPA + FastAPI
- **Next.js `output: 'export'`**: 공식 문서(Last updated 2026-08-09)의 "Unsupported Features" [S80]
  - Dynamic Routes with `dynamicParams: true`
  - Dynamic Routes without `generateStaticParams()`
  - Route Handlers that rely on Request
  - Cookies, Rewrites, Redirects, Headers, Proxy
  - Incremental Static Regeneration
  - Image Optimization with the default loader
  - Draft Mode, Server Actions, Intercepting Routes
  - 원문: "Attempting to use any of these features with `next dev` will result in an error".
  - Server Components는 빌드 시 실행된다. 클라이언트 라우팅은 원문 "behaves like a traditional SPA" [S80].
- **FastAPI `app.frontend()`** [S81][S84]
  - 0.138.0(2026-06-20)에 추가됐다. 사용법: `app.frontend("/", directory="dist")`.
  - 기본 `fallback="auto"`
    - 디렉터리에 `404.html`이 있으면 그 파일을 404로 응답한다.
    - 없으면 HTML을 요청하는 GET·HEAD 탐색 요청에 `index.html`을 응답한다. 클라이언트 라우팅용이다.
  - 원문: "Missing files like JavaScript, CSS, and images still return 404." 일반 path operation이 항상 우선한다.
  - 원문: "It does not run server-side rendering."
  - 이후 버전에서 의존성 지원(0.139.0), GET·HEAD 외 메서드에 404 반환(0.138.2), `check_dir="auto"`(0.141.0)가 추가됐다.
  - FastAPI Static Files 문서 원문: "If you need to host a frontend, use app.frontend() instead" [S82].
- **Starlette `StaticFiles(html=True)`** [S83]
  - 원문: "Automatically loads index.html for directories if such file exist."
  - 원문: "In HTML mode if 404.html file exists it will be shown as 404 response."
  - 즉 임의 경로에 대한 SPA index.html fallback은 하지 않는다.

### 10.7 FastAPI 2025–2026 breaking changes [S84][S85]
| 버전(날짜) | 내용 |
|---|---|
| 0.119.0 (2025-10-11) | v2 모델과 `pydantic.v1` 모델을 한 앱에서 임시로 함께 지원. Pydantic v1 지원을 deprecated 처리 |
| 0.125.0 (2025-12-17) | Python 3.8 지원 중단 |
| 0.126.0 (2025-12-20) | Pydantic v1 지원 중단. Pydantic v2의 `pydantic.v1`만 잠시 유지 |
| 0.127.0 (2025-12-21) | `pydantic.v1` 사용 시 deprecation 경고 |
| 0.128.0 (2025-12-27) | `pydantic.v1` 지원 중단 |
| 0.129.0 (2026-02-12) | Python 3.9 지원 중단 |
| 0.130.0 (2026-02-22) | Pydantic(Rust)로 JSON 응답을 직렬화. 원문: "2x (or more) performance increase" |
| 0.131.0 (2026-02-22) | `ORJSONResponse`·`UJSONResponse` deprecated |
| 0.132.0 (2026-02-23) | `strict_content_type` 기본 활성. JSON 요청에 유효한 `Content-Type`이 없으면 거부. 끄려면 `strict_content_type=False` |
| 0.137.0 (2026-06-14) | `router.routes`가 평면 리스트에서 트리로 변경(내부 구현 세부사항) |
| 0.143.0 (2026-10-08) | OpenTelemetry exporter 자동 설정을 opt-in으로 전환. 유지하려면 `FASTAPI_OTEL_AUTO_CONFIGURE=true` |

- 현재 0.143.1(2026-10-14)의 요구사항 (PyPI): `requires_python >=3.10`, `pydantic>=2.9.0`, `starlette>=0.46.0`, `opentelemetry-api>=1.44.0` [S85].
- 관련 패키지 (PyPI) [S85]
  - pydantic 2.14.1: `>=3.10`.
  - starlette 1.8.0: `>=3.11`, BSD-3-Clause.
  - alembic 1.20.0: `>=3.10`, `SQLAlchemy>=2.0`.

### 10.8 SQLAlchemy 2.1 주요 변경 [S86][S85]
- 원문: "Python version compatibility starts at version 3.11". 이어서 "Python 3.10 is dropped as of August, 2026 in preparation for Python 3.10 EOL in October of 2026." 2.1.4의 `requires_python`도 `>=3.11`이다.
- greenlet을 더 이상 기본 설치하지 않는다. asyncio를 쓰려면 `[asyncio]` extra가 필요하다.
- Session autoflush가 무조건 동작한다. `text()` 같은 Core 문 실행에서도 flush된다.
- ORM Mapped Dataclasses의 기본값이 `__dict__`가 아니라 descriptor로 전달된다.
- `Row`가 각 컬럼 타입을 직접 표현한다.
- `filter_by()`가 모든 FROM 엔티티를 검색한다.
- SQLite용 JSONB 타입을 추가했다 (SQLite 3.45+).
- PostgreSQL 기본 드라이버가 psycopg 3로 바뀌었다.

### 10.9 Alembic batch mode (SQLite) [S87]
- 원문: "it has almost no support for the ALTER statement which relational schema migrations rely upon".
- "move and copy" 절차: 새 구조로 임시 테이블 생성 → "INSERT from SELECT"로 데이터 복사 → 원래 테이블 drop → 임시 테이블 rename. `op.batch_alter_table()`로 실행한다.
- 기본적으로 SQLite에서만, 그리고 `add_column` 외의 지시문이 있을 때만 move-and-copy가 일어난다.
- autogenerate가 batch 형식을 만들게 하려면 `env.py`에 `render_as_batch=True`를 설정한다. 원문: "This mode is safe to use in all cases".
- SQLite는 이름 없는 제약을 허용하므로 `drop_constraint`를 쓰려면 `naming_convention`이 필요하다.
- 원문: "batch table operations do not work with foreign keys that enforce referential integrity". `PRAGMA foreign_keys`를 켰다면 작업 중에는 꺼야 한다.
- CHECK 제약은 `table_args`로 직접 옮겨야 한다.

---

## 11. Recommendation inputs

### 11.1 사실 (출처 있음)
- **F1 (규모)**
  - React Flow: 노드 수 상한 문서 없음, 공식 Stress Test 450 노드 [S01][S12].
  - Cytoscape Canvas: 1,200노드/16,000엣지에서 약 20 FPS [S32].
  - Sigma: "tens of thousands" [S43].
  - AIXON의 일반 표시량은 노드 200개 이하다.
- **F2 (접근성 내장)**
  - 키보드·ARIA·live region·라벨 현지화를 문서화한 것은 React Flow뿐이다 [S03].
  - Cytoscape는 앱 레벨 구현이 필요하다 [S35].
  - Sigma 4는 라벨까지 WebGL 텍스처로 렌더한다 [S43][S45].
  - D3는 SVG·HTML을 직접 다룬다 [S39].
- **F3 (React Flow 기본 포커스)**: `nodesFocusable`·`edgesFocusable` 기본 true, 모든 요소가 `tabIndex={0}` [S02][S03].
- **F4 (레이아웃)**
  - React Flow에는 내장 레이아웃이 없다 [S04].
  - dagre: MIT, gzip 약 17 KB, 2026년에 TS 재작성과 동적 레이아웃 안정성 옵션 추가 [S53][L3].
  - ELK: partitioning·interactive 전략 등 제약 옵션이 풍부하다. 대신 gzip 약 467 KB이고, React Flow 팀은 지원 난이도 때문에 "don't often recommend"라고 밝혔다 [S04][S24][L3].
  - d3-dag: dagre를 그대로 대체할 수 있다는 자체 주장 [S41].
- **F5 (연도 고정 배치 수단)**
  - React Flow 노드는 `position`을 직접 받는다 [S09].
  - ELK는 `partitioning.partition`에서 낮은 인덱스를 왼쪽에 둔다 [S24]. `layerChoiceConstraint`는 코어에서 직접 지원하지 않는다 (메인테이너) [S26].
  - Cytoscape는 `preset` 레이아웃을 쓴다 [S31].
  - dagre 설정 표에는 절대 rank 고정 옵션이 없다 [S54].
- **F6 (라이선스)**
  - elkjs 0.12.0: `EPL-2.0 OR GPL-3.0-or-later` [S21].
  - EPL FAQ 4.17·4.22 [S29], 고지 유지 조항 §3.3 [S22].
  - React Flow: MIT, 저작자 표시는 정책상 요청 [S15].
- **F7 (수식)**
  - MathJax v4: SRE 음성을 aria-label로 노출, 한국어 locale, explorer 기본 활성 [S61].
  - KaTeX: 기본 `htmlAndMathml`, MathML 시각적 숨김 [S58][S60].
  - MathJax는 숨김 MathML 방식을 "fragile"이라고 평가했다 [S61].
- **F8 (검색)**
  - trigram MATCH는 3 유니코드 문자 이상만 일치한다 [S72].
  - 로컬 실험: 2음절 MATCH 0건, LIKE는 결과를 반환하지만 스캔 수준의 시간이 걸렸다 [L1].
- **F9 (DB 동시성)**: WAL은 writer를 한 번에 하나만 허용하고 reader와 writer가 서로를 막지 않는다. 네트워크 파일시스템에서는 동작하지 않는다 [S75].
- **F10 (서빙)**
  - FastAPI ≥0.138.0의 `app.frontend()`는 SPA fallback을 기본 제공한다 [S81][S84].
  - `StaticFiles(html=True)`는 SPA fallback을 하지 않는다 [S83].
  - Next.js static export는 Server Actions, 요청 기반 Route Handlers, `generateStaticParams` 없는 동적 라우트를 지원하지 않는다 [S80].
- **F11 (Python 버전)**
  - SQLAlchemy 2.1과 Starlette 1.8.0은 ≥3.11, FastAPI 0.143.1은 ≥3.10을 요구한다 [S85][S86].
  - 로컬 python3는 3.12.7이다 [L1].
- **F12 (위상정렬)**: graphlib CycleError가 사이클 경로를 제공한다 [S79]. `get_ready` 배치가 최장 경로 레이어가 된다 [L2].
- **F13 (벡터)**: sqlite-vec는 pre-v1 [S77]. pgvector 0.8.7은 PostgreSQL 13+의 확장이다 [S78].
- **F14 (전환기)**
  - React Flow 13.0.0-next.0(peer React ≥18, zustand 5) [S19].
  - Sigma 4.0.0이 1주 전 출시됐고, React 바인딩은 아직 v3 peer다 [S45][S51].
  - Cytoscape v4 재설계가 진행 중이다 [S34].
  - Cytoscape WebGL은 preview/experimental이다 [S32][S33].

### 11.2 추론
- **I1. 렌더러 선택**
  - 200노드 규모에서는 WebGL(Sigma, Cytoscape WebGL)의 성능 이점이 필요하지 않다.
  - 반대로 Canvas·WebGL에서는 요소별 DOM이 없어 접근성 비용이 크다.
  - 따라서 DOM·SVG 기반인 React Flow(또는 D3+SVG)가 두 뷰의 요구(커스텀 노드 배지, KaTeX 라벨, 키보드 탐색)에 더 부합한다.
- **I2. 레이아웃 분리**
  - 계보 그래프: x를 `연도 → 픽셀`로 직접 계산하고, 레이아웃 엔진은 같은 연도 안의 y 순서와 교차 최소화만 맡긴다. 필요하면 ELK `partitioning`(partition=연도 인덱스, direction=RIGHT)을 쓴다.
  - 선수지식 DAG: dagre로 충분할 가능성이 높다. rank는 백엔드 graphlib 레이어 결과와 맞출 수 있다.
  - ELK는 partition·interactive 제약이 꼭 필요할 때만 도입하고 Web Worker로 실행한다.
- **I3. 키보드 탐색 설계**
  - React Flow 기본값이면 노드와 엣지 수만큼 탭 정지가 생긴다. 200노드 이상이면 수백 개다.
  - Chartability R3에 따라 `edgesFocusable=false`로 끄고, 그래프 진입점은 하나만 둔다.
  - 그 안에서 화살표 키로 선행·후행 노드를 따라가는 구조적 탐색(roving tabindex)을 구현하고, 동기화된 목록·트리 대체 뷰를 함께 둔다(R1, R2).
- **I4. 엣지 타입과 검증 배지**
  - EXTENDS·ADAPTS·IMPROVES_ON과 검증 배지는 색만으로 구분하지 않는다(R4). 텍스트 라벨, 아이콘, 선 패턴을 함께 쓴다.
  - React Flow의 `EdgeLabelRenderer`(HTML)와 엣지 `ariaLabel`로 구현할 수 있다.
- **I5. 수식 렌더러**
  - 한국어 스크린리더 지원을 우선하면 MathJax v4를 먼저 검토한다.
  - 번들 크기와 동기 렌더 속도를 우선하면 KaTeX가 낫다.
  - 결정 전에 실제 스크린리더 테스트가 필요하다.
- **I6. 한국어 검색**
  - FTS5 trigram을 기본으로 쓰고, 2음절 이하 질의는 LIKE 스캔으로 처리한다. 단일 사용자·소규모 데이터에서는 허용 가능한 비용이다.
  - SQLite 버전 요구: trigram은 ≥3.34, JSONB는 ≥3.45.
  - Python 빌드마다 내장 SQLite 버전이 다르므로 기동 시 `sqlite3.sqlite_version`을 확인한다.
- **I7. 프런트엔드 서빙**
  - 사용자 데이터에서 동적으로 생기는 노드 상세 경로를 Next.js static export로 처리하려면 `generateStaticParams`가 필요하다.
  - 로컬 앱에서는 Vite SPA + FastAPI `app.frontend("/", directory="dist")`가 더 단순하다.
  - 프런트엔드는 JSON 요청에 `Content-Type: application/json`을 반드시 보내야 한다(0.132.0).
- **I8. Python 버전**: Python 3.11 이상으로 고정한다. 3.10은 2026-10에 EOL이다.
- **I9. ELK 배포 고지**: ELK를 쓰고 AIXON을 외부에 배포하거나 호스팅하면 elkjs LICENSE·고지·소스 위치를 함께 제공한다. 로컬 단독 사용에서는 배포 의무가 생기지 않는다 (법률 자문 아님).
- **I10. 벡터 검색**
  - sqlite-vec는 버전을 고정하고 실험적 기능으로 다룬다.
  - pgvector는 PostgreSQL 서버 운영이 필요해 local-first 단순성과 맞지 않는다.
- **I11. 메이저 전환기 대응**: React Flow 12.x를 고정하고 13 정식 출시 뒤 마이그레이션한다. Sigma와 Cytoscape는 메이저 전환기라 지금 채택하면 재작업 위험이 있다.
- **I12. Cytoscape+ELK 제약**: Cytoscape를 고른다면 cytoscape-elk가 elkjs 0.9.x에 묶여 있고 klay는 deprecated다. ELK 최신 기능(0.12)을 쓰려면 어댑터를 직접 작성해야 한다.

### 11.3 확인되지 않음
- React Flow·D3의 공식 노드 수 가이드 (문서에 없음).
- Cytoscape.js WebGL 렌더러의 final·stable 전환 여부. 3.34.3 기준 근거 없음.
- KaTeX와 MathJax v4의 독립 성능 벤치마크. MathJax v4의 전체 로드량(폰트, SRE worker). MathJax 한국어 음성의 품질.
- elkjs(JS)에서 `layerChoiceConstraint`가 실제로 동작하는지. 문서와 메인테이너 발언은 코어 미지원이다.
- FTS5 trigram이 2글자 LIKE에 인덱스를 쓰는지. 문서 문구가 모호하며 로컬 타이밍은 스캔을 시사한다 ([L1]).
- Sigma.js의 접근성 기능 (문서 없음).

---

## 12. 로컬 측정 상세
- **[L1]** `python3 -I -c` 인라인 스크립트로 실행했다 (Python 3.12.7, SQLite 3.45.3, `:memory:`).
  - FTS5 `tokenize='trigram'` 테이블과 `tokenize='unicode61'` 테이블을 만들고 한국어 행을 넣었다.
  - MATCH와 LIKE 결과를 비교하고, 무작위 한글 40자 행 20만 개로 `time.perf_counter` 시간을 쟀다.
- **[L2]** `graphlib.TopologicalSorter`로 측정했다.
  - CycleError 예제와 `get_ready()`·`done()` 배치 루프를 실행했다.
  - 입력 `{'D':{'B','C'},'C':{'A'},'B':{'A'},'E':{'A','D'},'F':{'A'}}`의 출력은 `[['A'],['B','C','F'],['D'],['E']]`였다.
- **[L3]** `curl -sL <unpkg URL> | gzip -9 -c | wc -c`로 측정했다. 대상 URL은 다음과 같다. elk-worker.min.js는 grep 검사용이다.
  - https://unpkg.com/@xyflow/react@12.12.0/dist/umd/index.js
  - https://unpkg.com/elkjs@0.12.0/lib/elk.bundled.js
  - https://unpkg.com/elkjs@0.12.0/lib/elk-worker.min.js (1,595,334 B)
  - https://unpkg.com/cytoscape@3.34.3/dist/cytoscape.min.js
  - https://unpkg.com/d3@7.9.0/dist/d3.min.js
  - https://unpkg.com/sigma@4.0.2/dist/sigma.min.js
  - https://unpkg.com/graphology@0.26.0/dist/graphology.umd.min.js
  - https://unpkg.com/@dagrejs/dagre@3.1.1/dist/dagre.min.js
  - https://unpkg.com/katex@0.19.0/dist/katex.min.js
  - https://unpkg.com/katex@0.19.0/dist/katex.min.css
  - https://unpkg.com/mathjax@4.1.3/tex-chtml.js

---

## 13. 출처 (모두 확인 2026-10-15)

**React Flow**
- [S01] https://reactflow.dev/learn/advanced-use/performance
- [S02] https://reactflow.dev/api-reference/react-flow
- [S03] https://reactflow.dev/learn/advanced-use/accessibility
- [S04] https://reactflow.dev/learn/layouting/layouting
- [S05] https://reactflow.dev/learn/layouting/sub-flows
- [S06] https://reactflow.dev/api-reference/components/edge-label-renderer
- [S07] https://reactflow.dev/api-reference/components/minimap
- [S08] https://reactflow.dev/learn/customization/custom-nodes
- [S09] https://reactflow.dev/api-reference/types/node
- [S10] https://reactflow.dev/api-reference/types/edge
- [S11] https://reactflow.dev/api-reference/components/viewport-portal
- [S12] https://reactflow.dev/examples/nodes/stress
- [S13] https://reactflow.dev/examples/layout/elkjs
- [S14] https://reactflow.dev/remove-attribution (동일 내용: https://reactflow.dev/learn/troubleshooting/remove-attribution)
- [S15] https://reactflow.dev/api-reference/types/pro-options
- [S16] https://reactflow.dev/pro/examples
- [S17] https://github.com/xyflow/xyflow/releases
- [S18] https://github.com/xyflow/xyflow/issues/3147
- [S19] https://www.npmjs.com/package/@xyflow/react (`npm view`: version, dist-tags, peerDependencies, dependencies, time)

**ELK**
- [S20] https://github.com/kieler/elkjs (README)
- [S21] https://github.com/kieler/elkjs/releases (0.12.0, 0.11.1 등)
- [S22] https://github.com/kieler/elkjs/blob/master/LICENSE.md
- [S23] https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-layered.html
- [S24] ELK 옵션 레퍼런스 페이지들. 접두사는 https://eclipse.dev/elk/reference/options/
  - org-eclipse-elk-layered-layering-strategy.html
  - org-eclipse-elk-layered-nodePlacement-strategy.html
  - org-eclipse-elk-layered-crossingMinimization-strategy.html
  - org-eclipse-elk-layered-crossingMinimization-semiInteractive.html
  - org-eclipse-elk-layered-crossingMinimization-positionChoiceConstraint.html
  - org-eclipse-elk-layered-cycleBreaking-strategy.html
  - org-eclipse-elk-portConstraints.html
  - org-eclipse-elk-layered-layering-layerConstraint.html
  - org-eclipse-elk-layered-layering-layerChoiceConstraint.html
  - org-eclipse-elk-layered-considerModelOrder-strategy.html
  - org-eclipse-elk-partitioning-activate.html
  - org-eclipse-elk-partitioning-partition.html
  - org-eclipse-elk-interactiveLayout.html
  - org-eclipse-elk-layered-generatePositionAndLayerIds.html
  - org-eclipse-elk-layered-layering-layerId.html
  - org-eclipse-elk-hierarchyHandling.html
  - org-eclipse-elk-direction.html
  - org-eclipse-elk-position.html
- [S25] ELK 소스 Javadoc. 접두사는 https://github.com/eclipse-elk/elk/blob/master/plugins/org.eclipse.elk.alg.layered/src/org/eclipse/elk/alg/layered/options/
  - LayeringStrategy.java
  - NodePlacementStrategy.java
  - CrossingMinimizationStrategy.java
- [S26] https://github.com/eclipse-elk/elk/issues/908
- [S27] https://github.com/kieler/elkjs/issues/116
- [S28] https://eclipse.dev/elk/reference/algorithms/org-eclipse-elk-fixed.html
- [S29] https://www.eclipse.org/legal/documents/html/epl-2.0-faq.html (렌더 페이지: https://www.eclipse.org/legal/epl-2.0/faq/)

**Cytoscape.js**
- [S31] https://js.cytoscape.org/ (Performance, Extensions, Layouts, Compound nodes, Core initialisation 절)
- [S32] https://blog.js.cytoscape.org/2025/01/13/webgl-preview/
- [S33] https://github.com/cytoscape/cytoscape.js/issues/3305
- [S33b] https://github.com/cytoscape/cytoscape.js/issues/3374 , https://github.com/cytoscape/cytoscape.js/issues/3376
- [S34] https://github.com/cytoscape/cytoscape.js/issues/3486
- [S35] https://github.com/cytoscape/cytoscape.js/issues/3091
- [S35b] https://github.com/cytoscape/cytoscape.js/issues/2710
- [S36] https://github.com/cytoscape/cytoscape.js-dagre (README)
- [S37] https://www.npmjs.com/package/cytoscape-elk , https://www.npmjs.com/package/cytoscape-klay , https://github.com/kieler/klayjs (README)
- [S38] https://github.com/cytoscape/cytoscape.js/releases

**D3**
- [S39] https://d3js.org/what-is-d3
- [S40] https://www.npmjs.com/package/d3 (7.9.0 dependencies와 time), https://www.npmjs.com/package/d3-force , https://www.npmjs.com/package/d3-hierarchy
- [S41] https://github.com/erikbrinkman/d3-dag (README), https://www.npmjs.com/package/d3-dag

**Sigma.js / graphology**
- [S42] https://www.sigmajs.org/
- [S43] https://www.sigmajs.org/concepts/rendering/
- [S44] https://www.sigmajs.org/how-to/technical/performance/
- [S45] https://github.com/jacomyal/sigma.js/releases/tag/sigma@4.0.0
- [S46] https://www.sigmajs.org/how-to/technical/migration-v3-v4/
- [S47] https://www.sigmajs.org/how-to/layers/sync-html-svg/
- [S48] https://www.sigmajs.org/api/sigma/settings/interfaces/settings/
- [S49] https://www.sigmajs.org/sitemap-0.xml
- [S50] https://graphology.github.io/standard-library/
- [S51] https://www.npmjs.com/package/@react-sigma/core

**dagre**
- [S52] https://github.com/dagrejs/dagre (README, Releases·Tags)
- [S53] https://github.com/dagrejs/dagre/blob/master/changelog.md
- [S54] https://github.com/dagrejs/dagre/wiki#configuring-the-layout
- [S55] https://github.com/dagrejs/dagre/issues/238

**npm 레지스트리 공통**
- [S56n] `npm view <pkg> version license time dist-tags dependencies peerDependencies`. 대상 페이지:
  - https://www.npmjs.com/package/elkjs
  - https://www.npmjs.com/package/sigma
  - https://www.npmjs.com/package/graphology
  - https://www.npmjs.com/package/@dagrejs/dagre
  - https://www.npmjs.com/package/dagre
  - https://www.npmjs.com/package/katex
  - https://www.npmjs.com/package/react-cytoscapejs
  - https://www.npmjs.com/package/cytoscape
  - https://www.npmjs.com/package/sqlite-vec

**수식**
- [S57] https://katex.org/
- [S58] https://katex.org/docs/options
- [S59] https://github.com/KaTeX/KaTeX/blob/main/CHANGELOG.md
- [S60] https://unpkg.com/katex@0.19.0/dist/katex.min.css , https://unpkg.com/katex@0.19.0/dist/katex.min.js
- [S61] https://docs.mathjax.org/en/latest/upgrading/whats-new-4.0/explorer.html
- [S62] https://docs.mathjax.org/en/latest/upgrading/whats-new-4.0.html
- [S63] https://www.npmjs.com/package/mathjax (4.0.0 2025-08-04, 4.1.3, Apache-2.0)

**접근성**
- [S64] https://www.w3.org/WAI/tutorials/images/complex/
- [S65] https://chartability.fizz.studio/
- [S66] https://chartability.github.io/POUR-CAF/
- [S67] https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/
- [S68] https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- [S69] https://arxiv.org/abs/2308.08475 , https://www.npmjs.com/package/data-navigator
- [S70] https://arxiv.org/abs/2311.04502
- [S71] https://vis.csail.mit.edu/pubs/benthic/

**백엔드·인프라**
- [S72] https://www.sqlite.org/fts5.html (4.3.4 The Trigram Tokenizer)
- [S73] https://www.sqlite.org/changes.html
- [S74] https://www.sqlite.org/json1.html
- [S74b] https://www.sqlite.org/expridx.html
- [S75] https://www.sqlite.org/wal.html
- [S76] https://www.sqlite.org/lang_altertable.html
- [S77] https://github.com/asg017/sqlite-vec (README, LICENSE-MIT, LICENSE-APACHE, Releases), https://pypi.org/project/sqlite-vec/
- [S78] https://github.com/pgvector/pgvector/blob/master/CHANGELOG.md , https://github.com/pgvector/pgvector/blob/master/META.json , https://github.com/pgvector/pgvector (README)
- [S79] https://docs.python.org/3/library/graphlib.html
- [S80] https://nextjs.org/docs/app/guides/static-exports
- [S81] https://fastapi.tiangolo.com/tutorial/frontend/
- [S82] https://fastapi.tiangolo.com/tutorial/static-files/
- [S83] https://starlette.dev/staticfiles/
- [S84] https://fastapi.tiangolo.com/release-notes/
- [S85] PyPI JSON API:
  - https://pypi.org/pypi/fastapi/json
  - https://pypi.org/pypi/pydantic/json
  - https://pypi.org/pypi/sqlalchemy/json
  - https://pypi.org/pypi/alembic/json
  - https://pypi.org/pypi/starlette/json
- [S86] https://docs.sqlalchemy.org/en/21/changelog/migration_21.html
- [S87] https://alembic.sqlalchemy.org/en/latest/batch.html
- [S88] https://learn.microsoft.com/en-us/windows/wsl/filesystems
- [S89] GitHub REST API `https://api.github.com/repos/{owner}/{repo}` (stargazers_count, pushed_at). 대상 저장소:
  - xyflow/xyflow, kieler/elkjs
  - cytoscape/cytoscape.js, d3/d3
  - jacomyal/sigma.js, graphology/graphology
  - dagrejs/dagre, erikbrinkman/d3-dag
  - KaTeX/KaTeX, mathjax/MathJax
  - asg017/sqlite-vec, pgvector/pgvector

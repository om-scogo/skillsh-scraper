# Figure Patterns — Layout

Structure & flow patterns (15): Comparison, Flow, Timeline, Concept, Architecture, Interaction, State, Schema, Hierarchy, Matrix, Journey, Funnel, Loop, Storyboard, Terminal.

All use `assets/figure.css`. **핵심 원칙**: 텍스트는 최소한으로. 색상과 면적으로 구조 전달. 모바일 25% 축소에서도 인식 가능.

## TOC

- 1. Comparison
- 2. Flow
- 3. Timeline
- 4. Concept
- 5. Architecture
- 6. Interaction
- 7. State
- 8. Schema
- 9. Hierarchy
- 10. Matrix
- 11. Journey
- 12. Funnel
- 13. Loop
- *(14. Data Viz → patterns-dataviz-static.md)*
- 15. Storyboard
- 16. Terminal

---

## 1. Comparison (좌우 비교)

Best for: X vs Y, 나쁜 예시 vs 좋은 예시, 이전 vs 이후

Key classes: `.split`, `.split-left`, `.split-right`, `.vs-badge`, `.section-label`, `.quote-card`, `.data-card`

Max: 양쪽 각 2~3개 카드

```html
<body>
  <div class="split relative" style="height:74%">
    <div class="vs-badge">VS</div>
    <div class="split-left bg-info">
      <div class="section-label" style="background:var(--info-accent)">말하는 것</div>
      <div class="flex flex-col gap-3" style="width:100%;flex:1;justify-content:center">
        <div class="quote-card" style="padding:2rem;font-size:2rem">"좋은데요!"</div>
        <div class="quote-card" style="padding:2rem;font-size:2rem">"써볼게요"</div>
      </div>
    </div>
    <div class="split-right bg-bad">
      <div class="section-label" style="background:var(--bad-accent)">실제 행동</div>
      <div class="flex flex-col gap-3" style="width:100%;flex:1;justify-content:center">
        <div class="data-card" style="padding:1.75rem 2.5rem">가입 <span style="font-size:3.5rem">0건</span></div>
        <div class="data-card" style="padding:1.75rem 2.5rem">결제 <span style="font-size:3.5rem">0건</span></div>
      </div>
    </div>
  </div>
</body>
```

Notes: 카드 내 텍스트는 키워드만. 문장 금지. 양쪽 카드 컨테이너는 동일하게 구성(대칭)하되, `flex:1` + `justify-content:center`로 남는 세로 공간에서 카드를 수직 중앙 정렬해 패널을 균형 있게 채운다. **핵심 수치("0건")는 카드에서 가장 큰 요소**(라벨보다 크게, `.data-card`의 white 900 상속)로 — 유색 강조면 위에 같은 계열 accent 텍스트(`.text-bad` 등)를 올리면 대비가 무너진다(Red600 `--bad-card` 위 `--bad-accent` = 1.9:1). accent 텍스트 색은 흰색·tint(`--bad-bg`) 배경 전용, 600 강조면 위는 white만.

---

## 2. Flow (수직 플로우 비교)

Best for: 프로세스 비교, 단계별 차이, 방법론 대비

Key classes: `.flow-card`, `.flow-card.bad`, `.flow-card.good`, `.arrow-down`

Max: **3단계**. 설명 텍스트 생략 — 제목만 사용.

```html
<body>
  <div class="split relative" style="height:auto;min-height:78%">
    <div class="split-left bg-bad">
      <div class="section-label" style="background:var(--bad-accent)">나쁜 방법</div>
      <div class="flex flex-col items-center" style="flex:1;justify-content:center;width:100%">
        <div class="flow-card bad" style="padding:1.75rem 2rem"><strong>아이디어 설명</strong></div>
        <div class="arrow-down" style="height:52px"></div>
        <div class="flow-card bad" style="padding:1.75rem 2rem"><strong>평가 요청</strong></div>
        <div class="arrow-down" style="height:52px"></div>
        <div class="flow-card bad" style="padding:1.75rem 2rem;border-color:var(--bad-accent)"><strong style="color:var(--bad-accent)">착각</strong></div>
      </div>
    </div>
    <div class="split-right bg-good">
      <div class="section-label" style="background:var(--good-accent)">좋은 방법</div>
      <div class="flex flex-col items-center" style="flex:1;justify-content:center;width:100%">
        <div class="flow-card good" style="padding:1.75rem 2rem"><strong>맥락 확인</strong></div>
        <div class="arrow-down" style="height:52px"></div>
        <div class="flow-card good" style="padding:1.75rem 2rem"><strong>사례 복기</strong></div>
        <div class="arrow-down" style="height:52px"></div>
        <div class="flow-card good" style="padding:1.75rem 2rem;border-color:var(--good-accent)"><strong style="color:var(--good-accent)">니즈 발견</strong></div>
      </div>
    </div>
  </div>
</body>
```

Notes: Flow는 split 없이 단일 칼럼으로도 사용 가능. 설명 텍스트(`<span>`) 대신 제목(`<strong>`)만 사용할 것.

---

## 3. Timeline (수평 타임라인)

Best for: 시간 배분, 단계 순서, 비율 시각화

Key classes: `.timeline`, `.tl-block`, `.tl-label`, `.tl-time`

Max: **3블록**. `.tl-annotations` 사용 자제 — 쓸 경우 키워드 1개만.

```html
<body>
  <div class="timeline" style="min-height:460px">
    <div class="tl-block" style="flex:3;background:var(--tl-blue);color:var(--white)">
      <div class="tl-label">맥락</div><div class="tl-time">3분</div>
    </div>
    <div class="tl-block" style="flex:5;background:var(--tl-lime)">
      <div class="tl-label">사례 복기</div><div class="tl-time">5분</div>
    </div>
    <div class="tl-block" style="flex:4;background:var(--tl-orange)">
      <div class="tl-label">비용 확인</div><div class="tl-time">4분</div>
    </div>
  </div>
</body>
```

Notes: `flex` 비율로 시간 비율을 직관적으로 표현. 색상은 `--tl-*` 토큰 사용. annotation 생략이 기본. 얇은 띠가 캔버스 중앙에 뜨지 않도록 `.timeline`에 `min-height:460px`를 줘 블록을 세로로 키운다(블록은 stretch로 함께 커진다).

---

## 4. Concept (개념도)

Best for: 관계도, 벤 다이어그램 스타일, 개념 비교

Key classes: `.concept-block`, absolute positioning, z-index

```html
<body>
  <div style="position:relative;width:940px;height:560px">
    <div class="concept-block" style="position:absolute;left:0;top:90px;width:310px;height:380px;background:var(--yellow);z-index:1">
      <div class="text-4xl">TDD</div>
      <div class="text-xl">테스트 중심</div>
    </div>
    <div class="concept-block" style="position:absolute;left:270px;top:0;width:400px;height:560px;background:var(--orange);z-index:3">
      <div class="text-4xl">IDD</div>
      <div class="text-xl">인터뷰 중심</div>
    </div>
    <div class="concept-block" style="position:absolute;right:0;top:90px;width:310px;height:380px;background:var(--info-accent);color:white;z-index:2">
      <div class="text-4xl">SDD</div>
      <div class="text-xl">스펙 중심</div>
    </div>
  </div>
</body>
```

Notes: `z-index`로 겹침 순서 제어 — **중앙(강조) 블록이 항상 최상위**, 좌우 블록은 그 아래로 대칭이 되게 둔다(한쪽은 중앙 위·다른쪽은 중앙 아래인 비대칭 z-order 금지). 블록 내 텍스트는 약어+한줄 키워드만.

---

## 5. Architecture (시스템 구성도)

Best for: 시스템 아키텍처, 컴포넌트 관계, 레이어 구조

Key classes: `.arch`, `.arch-layer`, `.arch-label`, `.arch-nodes`, `.arch-node`

Max: **3레이어, 레이어당 3노드** (2노드면 빈약해 보임)

```html
<body>
  <div class="arch">
    <div class="arch-layer">
      <div class="arch-label" style="background:var(--tl-blue);color:var(--white)">Client</div>
      <div class="arch-nodes">
        <div class="arch-node">Web</div>
        <div class="arch-node">Mobile</div>
        <div class="arch-node">CLI</div>
      </div>
    </div>
    <div class="arch-layer">
      <div class="arch-label" style="background:var(--tl-lime)">Service</div>
      <div class="arch-nodes">
        <div class="arch-node">API</div>
        <div class="arch-node">Auth</div>
        <div class="arch-node">Analytics</div>
      </div>
    </div>
    <div class="arch-layer">
      <div class="arch-label" style="background:var(--tl-orange)">Data</div>
      <div class="arch-nodes">
        <div class="arch-node">PostgreSQL</div>
        <div class="arch-node">Redis</div>
        <div class="arch-node">S3</div>
      </div>
    </div>
  </div>
</body>
```

Notes: 노드 텍스트는 단어 1~2개. `figure-title` 생략 — 컨텐츠가 자명하면 불필요.

---

## 6. Interaction (시퀀스 다이어그램)

Best for: 요청/응답, 사용자-시스템 상호작용, API 플로우

Key classes: `.seq-entity`(액터 헤더 카드), `.seq-msg-label`(메시지 라벨). 라이프라인·화살표는 컬럼 센터에 맞춘 절대 위치 인라인 요소로 그린다.

```html
<body>
  <div class="relative" style="width:1180px;height:620px">
    <!-- 액터 헤더 (컬럼 센터 x: 150 / 590 / 1030) -->
    <div class="seq-entity" style="position:absolute;left:50px;top:0;width:200px;background:var(--tl-blue);color:var(--white)">사용자</div>
    <div class="seq-entity" style="position:absolute;left:490px;top:0;width:200px;background:var(--tl-lime)">API</div>
    <div class="seq-entity" style="position:absolute;left:930px;top:0;width:200px;background:var(--tl-orange)">DB</div>
    <!-- 라이프라인 (각 액터 아래 점선 세로선) -->
    <div style="position:absolute;left:148px;top:78px;height:512px;border-left:3px dashed var(--dark)"></div>
    <div style="position:absolute;left:588px;top:78px;height:512px;border-left:3px dashed var(--dark)"></div>
    <div style="position:absolute;left:1028px;top:78px;height:512px;border-left:3px dashed var(--dark)"></div>
    <!-- msg1: 사용자 → API (요청·실선) -->
    <div class="seq-msg-label" style="position:absolute;left:370px;top:128px;transform:translateX(-50%)">로그인 요청</div>
    <div style="position:absolute;left:150px;top:178px;width:440px;height:6px;background:var(--dark)"></div>
    <div style="position:absolute;left:570px;top:168px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark)"></div>
    <!-- msg2: API → DB (요청·실선) -->
    <div class="seq-msg-label" style="position:absolute;left:810px;top:248px;transform:translateX(-50%)">사용자 조회</div>
    <div style="position:absolute;left:590px;top:298px;width:440px;height:6px;background:var(--dark)"></div>
    <div style="position:absolute;left:1010px;top:288px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark)"></div>
    <!-- msg3: DB → API (응답·점선) -->
    <div class="seq-msg-label" style="position:absolute;left:810px;top:368px;transform:translateX(-50%)">조회 결과</div>
    <div style="position:absolute;left:590px;top:420px;width:440px;height:0;border-top:6px dashed var(--dark)"></div>
    <div style="position:absolute;left:590px;top:410px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-right:20px solid var(--dark)"></div>
    <!-- msg4: API → 사용자 (응답·점선) -->
    <div class="seq-msg-label" style="position:absolute;left:370px;top:488px;transform:translateX(-50%)">토큰 반환</div>
    <div style="position:absolute;left:150px;top:540px;width:440px;height:0;border-top:6px dashed var(--dark)"></div>
    <div style="position:absolute;left:150px;top:530px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-right:20px solid var(--dark)"></div>
  </div>
</body>
```

Notes: 액터 헤더를 상단에 고정하고 각 컬럼 센터(예: 150·590·1030)에 점선 **라이프라인**을 내린다(라이프라인은 보조 가이드선이라 3px 유지). 메시지 화살표는 **인접 액터 컬럼 사이만** 연결한다 — 요청은 →(왼쪽→오른쪽), 응답은 ←. **요청은 실선, 응답은 점선**으로 구분하고 라벨은 화살표 바로 위 중앙(`translateX(-50%)`)에 둔다. 메시지 라인은 **6px**, 화살촉은 **26×20px**(head top = line 세로 중심 − 13px)로 커넥터 최소 두께 규칙을 지킨다. 엔티티 **3개 기본**, 메시지 **4개**로 세로 리듬을 채운다.

---

## 7. State (상태 머신)

Best for: 상태 전이, 라이프사이클, 워크플로우 상태

Key classes: `.state-chain`, `.state-node`, `.state-node.active/.initial/.final`, `.state-transition`, `.arrow-right`, `.arrow-label`

```html
<body>
  <div class="state-chain" style="width:90%;justify-content:space-between">
    <div class="state-node initial" style="min-width:210px;padding:2.5rem 2.5rem">
      <strong>발견</strong>
      <span class="text-sm">문제 인지</span>
    </div>
    <div class="state-transition">
      <div class="arrow-label">인터뷰</div>
      <div class="arrow-right" style="width:80px"></div>
    </div>
    <div class="state-node" style="min-width:210px;padding:2.5rem 2.5rem">
      <strong>정의</strong>
      <span class="text-sm">가설 정리</span>
    </div>
    <div class="state-transition">
      <div class="arrow-label">구현</div>
      <div class="arrow-right" style="width:80px"></div>
    </div>
    <div class="state-node active" style="min-width:210px;padding:2.5rem 2.5rem">
      <strong>검증</strong>
      <span class="text-sm">활성 확인</span>
    </div>
    <div class="state-transition">
      <div class="arrow-label">반복</div>
      <div class="arrow-right" style="width:80px"></div>
    </div>
    <div class="state-node final" style="min-width:210px;padding:2.5rem 2.5rem">
      <strong>확장</strong>
      <span class="text-sm">재방문 유도</span>
    </div>
  </div>
</body>
```

Notes: 수평 체인이 기본. **상태 4개**가 가장 안정적이고, 각 상태에 **짧은 보조 설명 1줄**을 붙이면 카드 면적이 커져 모바일에서도 더 잘 읽힌다. `.initial`(시작), `.active`(강조), `.final`(종료) 변형 사용.

---

## 8. Schema (데이터 스키마)

Best for: DB 테이블 구조, 데이터 모델, 엔티티 관계

Key classes: `.schema-container`, `.schema-table`, `.schema-header`, `.schema-field`, `.schema-pk`, `.schema-fk`

Max: **3테이블, 테이블당 3~4필드**

```html
<body>
  <div style="position:relative;width:100%;display:flex;justify-content:center">
    <div class="schema-container" style="width:88%;gap:1.75rem;justify-content:space-between;align-items:stretch">
      <div class="schema-table" style="min-width:300px;flex:1">
        <div class="schema-header" style="background:var(--tl-blue);color:var(--white)">User</div>
        <div class="schema-field"><span>id</span> <span class="schema-pk">PK</span></div>
        <div class="schema-field"><span>email</span></div>
        <div class="schema-field"><span>plan_id</span> <span class="schema-fk">FK</span></div>
        <div class="schema-field"><span>status</span></div>
      </div>
      <div class="schema-table" style="min-width:300px;flex:1">
        <div class="schema-header" style="background:var(--tl-lime)">Plan</div>
        <div class="schema-field"><span>id</span> <span class="schema-pk">PK</span></div>
        <div class="schema-field"><span>name</span></div>
        <div class="schema-field"><span>price</span></div>
        <div class="schema-field"><span>cycle</span></div>
      </div>
      <div class="schema-table" style="min-width:300px;flex:1">
        <div class="schema-header" style="background:var(--tl-orange)">Invoice</div>
        <div class="schema-field"><span>id</span> <span class="schema-pk">PK</span></div>
        <div class="schema-field"><span>user_id</span> <span class="schema-fk">FK</span></div>
        <div class="schema-field"><span>amount</span></div>
        <div class="schema-field"><span>paid_at</span></div>
      </div>
    </div>
  </div>
</body>
```

Notes: 필드명 + PK/FK 뱃지만 유지하고 타입 표기는 기본적으로 생략한다. **3테이블까지**는 1440px 캔버스에서 안정적으로 읽히며, 관계를 이해시키는 핵심 FK만 남기면 된다. 작은 중앙 배지보다 **좌우로 넓게 펼친 테이블 배치**가 더 잘 읽힌다.

---

## 9. Hierarchy (계층 구조)

Best for: 조직도, 트리 구조, 분류 체계, 상속 관계

Key classes: `.tree`, `.tree-node`, `.tree-level`, `.tree-branch`, `.tree-vline`, `.tree-hline`

```html
<body>
  <div class="tree" style="width:1200px;gap:0.35rem">
    <div class="tree-node" style="background:var(--yellow);min-width:260px;padding:1.5rem 3rem">Platform</div>
    <div class="tree-vline" style="height:56px"></div>
    <div class="tree-hline" style="width:860px"></div>
    <div class="tree-level" style="gap:1rem;width:100%;justify-content:space-between;align-items:flex-start">
      <div class="tree-branch" style="width:340px">
        <div class="tree-vline" style="height:48px"></div>
        <div class="tree-node" style="background:var(--tl-blue);color:var(--white);min-width:200px;flex-direction:column;gap:0.25rem">
          <span>Product</span>
          <span class="mono" style="font-size:1.25rem;color:var(--white)">core UX</span>
        </div>
        <div class="tree-vline" style="height:44px"></div>
        <div class="tree-level" style="gap:0.75rem">
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">온보딩</div>
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">리텐션</div>
        </div>
      </div>
      <div class="tree-branch" style="width:340px">
        <div class="tree-vline" style="height:48px"></div>
        <div class="tree-node" style="background:var(--tl-lime);min-width:200px;flex-direction:column;gap:0.25rem">
          <span>Growth</span>
          <span class="mono" style="font-size:1.25rem;color:var(--dark)">top funnel</span>
        </div>
        <div class="tree-vline" style="height:44px"></div>
        <div class="tree-level" style="gap:0.75rem">
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">획득</div>
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">활성화</div>
        </div>
      </div>
      <div class="tree-branch" style="width:340px">
        <div class="tree-vline" style="height:48px"></div>
        <div class="tree-node" style="background:var(--tl-orange);min-width:200px;flex-direction:column;gap:0.25rem">
          <span>Revenue</span>
          <span class="mono" style="font-size:1.25rem;color:var(--dark)">monetization</span>
        </div>
        <div class="tree-vline" style="height:44px"></div>
        <div class="tree-level" style="gap:0.75rem">
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">업그레이드</div>
          <div class="tree-node" style="background:var(--white);min-width:140px;padding:1.1rem 1.4rem">확장</div>
        </div>
      </div>
    </div>
  </div>
</body>
```

Notes: **깊이 3단계**까지는 안전하다. 루트 1개 + 상위 카테고리 3개 + 하위 노드 2개씩 구성이 가장 읽기 쉽고, 세로 리듬도 살아난다. 상위 노드에는 짧은 보조 라벨을 붙이고, 하위 노드는 흰색 카드로 통일하면 계층이 빨리 구분된다. **유색 노드 위 텍스트는 면과 같은 색 계열 금지** — `--muted-fg`는 유색 면 위에서 사실상 안 보인다(흰/연회색 배경 전용). 노드 면이 `--tl-green/orange` 등 밝은 hue면 본문·보조 라벨 모두 `--dark`, `--tl-blue/purple` 진한 hue면 모두 `--white`(dark는 4.1/3.1:1 미달).

---

## 10. Matrix (매트릭스)

Best for: 2x2 분석, 의사결정 매트릭스, 기능 비교표

Key classes: `.matrix`, `.matrix-header`, `.matrix-cell`, `.matrix-corner`, `.matrix-label-x`, `.matrix-label-y`

```html
<body>
  <div class="matrix" style="grid-template-columns:180px 1fr 1fr;grid-template-rows:auto 1fr 1fr;width:82%;height:580px;background:var(--dark);gap:3px">
    <div class="matrix-corner" style="background:var(--white)"></div>
    <div class="matrix-label-x" style="background:var(--good-card);color:var(--white);border:none">높은 임팩트</div>
    <div class="matrix-label-x" style="background:var(--info-card);color:var(--white);border:none">낮은 임팩트</div>
    <div class="matrix-label-y" style="background:var(--white);border:none">쉬움</div>
    <div class="matrix-cell" style="background:var(--good-bg)">
      <div class="text-xl"><strong>Quick Win</strong></div>
    </div>
    <div class="matrix-cell" style="background:var(--info-bg)">
      <div class="text-xl"><strong>채워넣기</strong></div>
    </div>
    <div class="matrix-label-y" style="background:var(--white);border:none">어려움</div>
    <div class="matrix-cell" style="background:var(--good-bg)">
      <div class="text-xl"><strong>Big Bet</strong></div>
    </div>
    <div class="matrix-cell" style="background:var(--info-bg)">
      <div class="text-xl"><strong>하지 말것</strong></div>
    </div>
  </div>
</body>
```

Notes: 셀 내 텍스트는 **키워드 1~2단어**만. **열별 색상 통일** — 1열과 2열은 서로 다른 색상 계열, 같은 열 내 셀은 동일 색상. 헤더는 진한 톤, 셀은 연한 톤. **코너·행라벨은 흰색**. **구분선은 grid gap 기법**: `.matrix`에 `background:var(--dark);gap:3px` 적용, 개별 셀 border 제거.

---

## 11. Journey (사용자 여정)

Best for: 사용자 경험 흐름, 터치포인트 맵, 온보딩 과정

Key classes: `.journey`, `.journey-line`, `.journey-step`, `.journey-dot`, `.journey-label`, `.journey-desc`

Max: **4단계**

```html
<body>
  <div class="journey" style="width:92%;align-items:stretch;gap:1.25rem;padding:0 1rem">
    <div class="journey-line" style="top:67px;left:6%;right:6%"></div>
    <div class="journey-step" style="background:var(--white);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);padding:2rem 1.25rem 2.25rem;min-height:540px">
      <div class="journey-dot" style="background:var(--info-bg);width:76px;height:76px;font-size:2.25rem">1</div>
      <div class="journey-label" style="font-size:1.75rem;margin-top:1.25rem">발견</div>
      <div class="journey-desc">서비스 인지</div>
      <div class="mono" style="margin-top:auto;font-size:3rem;font-weight:900">68%</div>
    </div>
    <div class="journey-step" style="background:var(--white);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);padding:2rem 1.25rem 2.25rem;min-height:540px">
      <div class="journey-dot" style="background:var(--info-bg);width:76px;height:76px;font-size:2.25rem">2</div>
      <div class="journey-label" style="font-size:1.75rem;margin-top:1.25rem">가입</div>
      <div class="journey-desc">빠른 시작</div>
      <div class="mono" style="margin-top:auto;font-size:3rem;font-weight:900">42%</div>
    </div>
    <div class="journey-step" style="background:var(--white);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);padding:2rem 1.25rem 2.25rem;min-height:540px">
      <div class="journey-dot" style="background:var(--info-bg);width:76px;height:76px;font-size:2.25rem">3</div>
      <div class="journey-label" style="font-size:1.75rem;margin-top:1.25rem">활성화</div>
      <div class="journey-desc">첫 경험</div>
      <div class="mono" style="margin-top:auto;font-size:3rem;font-weight:900">31%</div>
    </div>
    <div class="journey-step" style="background:var(--white);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);padding:2rem 1.25rem 2.25rem;min-height:540px">
      <div class="journey-dot" style="background:var(--accent);color:var(--white);width:76px;height:76px;font-size:2.25rem">4</div>
      <div class="journey-label" style="font-size:1.75rem;margin-top:1.25rem">재방문</div>
      <div class="journey-desc">습관 형성</div>
      <div class="mono" style="margin-top:auto;font-size:3rem;font-weight:900">11%</div>
    </div>
  </div>
</body>
```

Notes: `.journey-desc`는 짧은 한 줄 설명을 허용하되 **12자 내외**로 유지한다. **핵심 수치(%)가 카드에서 가장 큰 시각 요소** — `margin-top:auto`로 카드 하단에 앵커하고 3rem·900·`--dark`로 찍는다(강조 역전 금지: 수치를 muted·20px로 넣으면 정보 위계가 뒤집힌다). **단계 dot은 단일 계열(연한 tint)로 통일하고 강조 1색만** — 순서는 위치·번호가 이미 전달하므로 단계마다 다른 hue를 입히면 색이 가짜 범주를 만든다(색은 인코딩 수단). 핵심 단계(예: 마지막 11%)만 `--accent`+white로 강조한다. 카드에 `min-height:540px`를 줘 810px 캔버스 세로를 채운다 — 240px짜리 얕은 카드 띠는 축소 시 떠 보인다. **4단계**를 같은 폭으로 균등 분배하고, `.journey` 폭을 92% 정도로 잡아 양 끝 카드가 캔버스 모서리에 붙지 않게 한다. journey-line(6px)의 `top`은 카드 padding-top + dot 반지름에 맞춘다(예: 32px + 38px → 67px).

---

## 12. Funnel (퍼널)

Best for: 전환율, 단계별 감소, 마케팅 퍼널, 파이프라인

Key classes: `.funnel`, `.funnel-row`, `.funnel-stage`(색 바 — 텍스트 없음), `.funnel-out`(바 오른쪽 라벨·수치 블록), `.funnel-label`, `.funnel-value`

Max: **4단계**

```html
<body>
  <!-- 폭 = 값 정비례 (방문 10,000 → 1200px 기준: 384/86/22px). 라벨·수치는 전 행 공통으로 바 오른쪽 바깥 -->
  <div class="funnel" style="width:auto;gap:8px">
    <div class="funnel-row">
      <div class="funnel-stage" style="width:1200px;padding:0;background:var(--accent)"></div>
      <div class="funnel-out" style="margin-left:16px;display:flex;flex-direction:column;gap:0.25rem">
        <span class="funnel-label" style="font-size:1.75rem">방문</span>
        <span class="funnel-value mono" style="font-size:1.5rem">10,000 · 100%</span>
      </div>
    </div>
    <div class="funnel-row">
      <div class="funnel-stage" style="width:384px;padding:0;background:var(--accent);border-top:3px solid var(--dark)"></div>
      <div class="funnel-out" style="margin-left:16px;display:flex;flex-direction:column;gap:0.25rem">
        <span class="funnel-label" style="font-size:1.75rem">가입</span>
        <span class="funnel-value mono" style="font-size:1.5rem">3,200 · 32%</span>
      </div>
    </div>
    <div class="funnel-row">
      <div class="funnel-stage" style="width:86px;padding:0;background:var(--accent);border-top:3px solid var(--dark)"></div>
      <div class="funnel-out" style="margin-left:16px;display:flex;flex-direction:column;gap:0.25rem">
        <span class="funnel-label" style="font-size:1.75rem">첫 사용</span>
        <span class="funnel-value mono" style="font-size:1.5rem">720 · 7.2%</span>
      </div>
    </div>
    <div class="funnel-row">
      <div class="funnel-stage" style="width:22px;padding:0;background:var(--accent);border-top:3px solid var(--dark)"></div>
      <div class="funnel-out" style="margin-left:16px;display:flex;flex-direction:column;gap:0.25rem">
        <span class="funnel-label" style="font-size:1.75rem">결제</span>
        <span class="funnel-value mono" style="font-size:1.5rem">180 · 1.8%</span>
      </div>
    </div>
  </div>
</body>
```

Notes: **폭 = 값 정비례가 이 패턴의 존재 이유 — 최소폭 클램프 금지**(방문 10,000 = 1200px 기준: 3,200 → `384px`, 720 → `86px`, 180 → `22px` 그대로). 모든 바는 **좌측 정렬**(공통 베이스라인 = 왼쪽 변)로 쌓아 감소가 한 축에서 형태로 읽히게 한다. **좁은 스테이지의 라벨·수치는 바 안에 욱여넣지 말고 바 오른쪽 외부에 단다(같은 행)** — 모든 행을 [색 바][16px][라벨·수치] 구조로 통일해 넓은 1행도 같은 자리에서 읽힌다(라벨은 `--dark` 900, 수치는 `.mono`). **라벨 %는 첫 스테이지 대비 누적**(100 → 15 → 3 → 0.9%) — 폭이 누적 비례를 인코딩하므로, 원문이 단계 전환율(15·20·30%)로 주어져도 라벨은 자기 기하와 일치시킨다. **바는 단색(`--accent`)** — 스테이지는 위치·순서로 이미 구분되므로 단계마다 hue를 바꾸면 색이 가짜 범주를 만든다(색 문법 ③). 급락 지점을 색으로 강조하고 싶으면 그 바 하나만 `--bad-card`로. **전환 손실이 형태로 보여야 한다** — 1.8%는 실처럼 보이는 게 정답이다. **스테이지는 시간 순서 유지 — 값 크기로 재정렬 금지.** 바 높이는 `.funnel-stage` 기본 110px, 행 간 8px. 바에 텍스트가 없으므로 `padding:0`으로 기본 좌우 패딩을 제거한다(border-box에서 패딩이 좁은 바의 최소폭처럼 작동해 비례를 깬다). 8px 간격 스택에서는 2행부터 `border-top:3px solid var(--dark)`를 인라인으로 복원한다(기본 규칙은 맞닿은 스택용으로 top border를 지운다). 마지막 행 아래 잔여 공간이 커도 body 기본 정렬이 퍼널 전체를 세로 중앙에 앉힌다.

---

## 13. Loop (순환 루프)

Best for: 피드백 루프, PDCA 사이클, 반복 프로세스

Key classes: `.loop-node`, `.loop-center` + 링(둥근 사각 보더 6px) + 코너 화살촉(absolute 배치)

```html
<body>
  <div class="relative" style="width:1080px;height:640px">
    <!-- 순환 링: 6px 보더 + 큰 corner radius가 회전 궤도를 형태로 보여준다 -->
    <div style="position:absolute;left:60px;right:60px;top:50px;bottom:50px;border:6px solid var(--dark);border-radius:120px"></div>
    <!-- 시계방향 화살촉 4개 — 코너 정점(45°)에 배치, 각 코너의 진행 방향으로 회전 -->
    <div style="position:absolute;left:973px;top:74px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark);transform:rotate(45deg)"></div>
    <div style="position:absolute;left:973px;top:540px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark);transform:rotate(135deg)"></div>
    <div style="position:absolute;left:87px;top:540px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark);transform:rotate(225deg)"></div>
    <div style="position:absolute;left:87px;top:74px;width:0;height:0;border-top:13px solid transparent;border-bottom:13px solid transparent;border-left:20px solid var(--dark);transform:rotate(315deg)"></div>
    <!-- 노드 4개: 링의 상/우/하/좌 변 중앙에 올라탄다 (시계방향 순서) -->
    <div class="loop-node" style="position:absolute;left:50%;top:50px;transform:translate(-50%,-50%);background:var(--tl-blue);color:var(--white);min-width:260px;padding:1.75rem 2rem">문제 정의</div>
    <div class="loop-node" style="position:absolute;left:1020px;top:50%;transform:translate(-50%,-50%);background:var(--tl-lime);min-width:260px;padding:1.75rem 2rem">인터뷰</div>
    <div class="loop-node" style="position:absolute;left:50%;top:590px;transform:translate(-50%,-50%);background:var(--tl-orange);min-width:260px;padding:1.75rem 2rem">빌드</div>
    <div class="loop-node" style="position:absolute;left:60px;top:50%;transform:translate(-50%,-50%);background:var(--tl-purple);color:var(--white);min-width:260px;padding:1.75rem 2rem">검증</div>
    <!-- 중앙 허브 -->
    <div class="loop-center" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:2.35rem;background:var(--yellow);border:3px solid var(--dark);width:150px;height:150px;border-radius:999px;box-shadow:4px 4px 0px var(--dark);text-align:center;line-height:1.15">학습<br>루프</div>
  </div>
</body>
```

Notes: 직선 화살표 4개는 25% 축소에서 순환으로 읽히지 않는다 — **링(6px 보더 + `border-radius:120px`) 위에 노드 4개를 올리고, 코너 정점에 시계방향 화살촉(26×20px)**을 얹어 회전이 형태 자체로 보이게 한다. 화살촉 좌표: 코너 아크 중심에서 45° 지점(반지름 R이면 코너 모서리에서 안쪽으로 약 0.29R). 노드는 링의 네 변 중앙에 `translate(-50%,-50%)`로 정확히 올라타고, 시계방향 진행 순서(상→우→하→좌)로 배치한다. 컨테이너는 **가로 1000px 이상**(예: 1080×640)으로 캔버스를 채운다.

---

## 15. Storyboard (스토리보드)

Best for: 시나리오 설명, 단계별 장면, 사용자 시나리오, 기능 소개

Key classes: `.storyboard`, `.story-panel`, `.story-number`, `.story-caption`, `.story-desc`

Max: **4패널 (2×2)**

```html
<body>
  <div class="storyboard" style="grid-template-columns:repeat(2,1fr);width:96%">
    <div class="story-panel" style="min-height:250px;justify-content:flex-start">
      <div class="story-number">1</div>
      <div style="width:100%;height:92px;background:var(--muted);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);margin-top:0.75rem;position:relative">
        <div style="position:absolute;left:14px;right:14px;top:14px;height:10px;background:var(--white)"></div>
        <div style="position:absolute;left:14px;right:44px;top:34px;height:10px;background:var(--white)"></div>
        <div style="position:absolute;left:14px;right:24px;top:54px;height:10px;background:var(--white)"></div>
      </div>
      <div class="story-caption">앱 열기</div>
      <div class="story-desc">알림 확인</div>
    </div>
    <div class="story-panel" style="min-height:250px;justify-content:flex-start">
      <div class="story-number">2</div>
      <div style="width:100%;height:92px;background:var(--muted);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);margin-top:0.75rem;position:relative">
        <div style="position:absolute;left:14px;top:14px;width:60px;height:60px;background:var(--white)"></div>
        <div style="position:absolute;left:90px;right:14px;top:18px;height:10px;background:var(--white)"></div>
        <div style="position:absolute;left:90px;right:34px;top:40px;height:10px;background:var(--white)"></div>
      </div>
      <div class="story-caption">내역 확인</div>
      <div class="story-desc">금액 검토</div>
    </div>
    <div class="story-panel" style="min-height:250px;justify-content:flex-start">
      <div class="story-number">3</div>
      <div style="width:100%;height:92px;background:var(--muted);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);margin-top:0.75rem;position:relative">
        <div style="position:absolute;left:14px;right:14px;top:14px;bottom:14px;border:3px solid var(--white)"></div>
        <div style="position:absolute;left:50%;top:50%;width:44px;height:44px;border-radius:999px;background:var(--white);transform:translate(-50%,-50%)"></div>
      </div>
      <div class="story-caption">결제 승인</div>
      <div class="story-desc">슬라이드</div>
    </div>
    <div class="story-panel" style="min-height:250px;justify-content:flex-start">
      <div class="story-number">4</div>
      <div style="width:100%;height:92px;background:var(--muted);border:3px solid var(--dark);box-shadow:4px 4px 0px var(--dark);margin-top:0.75rem;position:relative">
        <div style="position:absolute;left:18px;top:16px;width:58px;height:58px;border-radius:999px;background:var(--white)"></div>
        <div style="position:absolute;left:94px;right:18px;top:22px;height:10px;background:var(--white)"></div>
        <div style="position:absolute;left:94px;right:40px;top:46px;height:10px;background:var(--white)"></div>
      </div>
      <div class="story-caption">완료</div>
      <div class="story-desc">영수증 표시</div>
    </div>
  </div>
</body>
```

Notes: `grid-template-columns`로 열 수 조정. **2×2 기본**. 각 패널에 **장면 placeholder 영역**을 먼저 두면 스토리보드다운 밀도가 생기고 하단 공백이 크게 줄어든다.

---

## 16. Terminal (터미널 UI)

Best for: CLI 도구 시각화, 터미널 명령어 시퀀스, AskUserQuestion UI, 개발자 도구 데모

Key classes: `.terminal`, `.terminal-card`, `.terminal-card-header`, `.terminal-card-tag`, `.terminal-option`, `.terminal-radio`, `.terminal-answer`

Max: **3 Step 카드 (가로)**, 카드당 옵션 **2개 (max 3)**

```html
<body>
<div class="terminal">
  <div style="margin-bottom:20px">
    <div class="terminal-path"><span style="color:var(--t-good)">~</span> /project</div>
    <div class="terminal-prompt">
      <span style="color:var(--t-good);font-weight:700">&#10095;</span>
      <span style="color:var(--t-accent);font-weight:600">@SPEC.md</span>를 읽고
      <span style="color:var(--t-purple);font-weight:600">AskUserQuestionTool</span>로 인터뷰해 주세요.
    </div>
  </div>

  <div class="terminal-tool">
    <span class="terminal-dot" style="background:var(--t-accent)"></span>
    <span>Read</span>
    <span style="color:var(--muted-fg)">SPEC.md</span>
  </div>

  <div class="terminal-text">핵심 결정 인터뷰</div>

  <div class="terminal-steps">
    <div class="terminal-card">
      <div class="terminal-card-header">
        <span>Step 1 / 3</span>
        <span class="terminal-card-tag">성공 기준</span>
      </div>
      <div class="terminal-card-question">성공 기준은?</div>
      <div class="flex flex-col" style="gap:10px;margin-bottom:18px">
        <div class="terminal-option selected">
          <span class="terminal-radio checked"></span>
          <span>WAU 활성만</span>
        </div>
        <div class="terminal-option">
          <span class="terminal-radio"></span>
          <span>결제 전환만</span>
        </div>
      </div>
      <hr class="terminal-divider">
      <div class="terminal-answer">
        <span style="font-weight:700;flex-shrink:0">✔</span>
        <span>WAU 활성만</span>
      </div>
    </div>

    <div class="terminal-connector">&#8250;</div>

    <div class="terminal-card">
      <div class="terminal-card-header">
        <span>Step 2 / 3</span>
        <span class="terminal-card-tag">좌절 관리</span>
      </div>
      <div class="terminal-card-question">좌절 관리법?</div>
      <div class="flex flex-col" style="gap:10px;margin-bottom:18px">
        <div class="terminal-option selected">
          <span class="terminal-radio checked"></span>
          <span>실시간 가이드</span>
        </div>
        <div class="terminal-option">
          <span class="terminal-radio"></span>
          <span>숫자 숨기기</span>
        </div>
      </div>
      <hr class="terminal-divider">
      <div class="terminal-answer">
        <span style="font-weight:700;flex-shrink:0">✔</span>
        <span>실시간 가이드</span>
      </div>
    </div>

    <div class="terminal-connector">&#8250;</div>

    <div class="terminal-card">
      <div class="terminal-card-header">
        <span>Step 3 / 3</span>
        <span class="terminal-card-tag">목표 재정의</span>
      </div>
      <div class="terminal-card-question">진짜 목표는?</div>
      <div class="flex flex-col" style="gap:10px;margin-bottom:18px">
        <div class="terminal-option selected">
          <span class="terminal-radio checked"></span>
          <span>첫 매출</span>
        </div>
        <div class="terminal-option">
          <span class="terminal-radio"></span>
          <span>단계적 접근</span>
        </div>
      </div>
      <hr class="terminal-divider">
      <div class="terminal-answer">
        <span style="font-weight:700;flex-shrink:0">✔</span>
        <span>첫 매출</span>
      </div>
    </div>
  </div>

  <div style="margin-top:28px">
    <div class="terminal-tool" style="margin:0">
      <span class="terminal-dot" style="background:var(--t-good)"></span>
      <span style="color:var(--t-good)">Write</span>
      <span style="color:var(--muted-fg)">SPEC-v2.md</span>
    </div>
  </div>
  <div class="terminal-text" style="color:var(--t-good);margin-top:8px;margin-bottom:0">
    ✔ 인터뷰 완료
  </div>
</div>
</body>
```

Notes: figure.css 기반이므로 외부 @import 없이 동작. 다크 테마는 `.terminal` 클래스가 body 대신 적용. 질문 텍스트에 `<br>` 사용 금지 — `.terminal-card-question`의 `text-wrap: balance`가 자동으로 균등 줄바꿈 처리. 질문은 **max 12자, 1줄 권장**. 옵션은 **max 8자**.

---

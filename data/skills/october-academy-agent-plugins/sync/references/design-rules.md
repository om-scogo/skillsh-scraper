# Design Rules Reference

HTML 구현 시 반드시 참고할 디자인 제약 모음. SKILL.md Workflow 4단계에서 읽어라.

---

## Core Rules

- **Size**: 1440×810 (16:9)
- **Border**: 3px solid #0a0a0a
- **Shadow**: Npx Npx 0px #0a0a0a (no blur ever)
- **Title font**: Noto Sans KR 900 (headings/labels only)
- **Body font**: Noto Sans KR, weight 700 (bold default). Use 400 only for minor annotations
- **Code/number font**: JetBrains Mono (`.mono`, `.code`, `.tag`)
- **Colors**: CSS variables only — never hardcode hex in HTML (Canvas/D3 패턴은 JS 내 hex 허용).
  팔레트는 AGENTIC v1.2 — 면·텍스트·선 조합은 [색 문법](#색-문법--agentic-v12-면텍스트-조합-ssot) 참조
- **Contrast**: 유색 면 위 텍스트는 `--dark` 기본 — 단 **Blue·Purple 500 면과 600 강조면(`--good-card`/`--bad-card`/`--info-card`) 위는 `--white`**. `--muted-fg`는 흰·연회색 배경 전용 — [색상 대비](#색상-대비--금지-조합) 참조
- **Connectors**: 화살표·연결선 샤프트 ≥6px + 화살촉 ≥20px — [커넥터](#커넥터--화살표연결선-두께) 참조
- **No**: gradients, blur shadows, soft edges

## 시각 패턴 (Isometric, IconDiagram, Network, Graph) 참고

- **SVG 패턴** (Isometric, IconDiagram): `<svg>` 인라인. 정밀한 좌표 배치. figure.css 색상 변수 사용 가능.
- **Canvas 패턴** (Network): `<canvas>` + JS. `document.fonts.ready.then()`으로 폰트 로드 후 렌더링. retina 2x (`width=2880, height=1620, style width=1440px`).
- **D3 패턴** (Graph): `<script src="https://d3js.org/d3.v7.min.js">`. 시뮬레이션 동기 실행: `for(let i=0;i<300;i++) sim.tick(); sim.stop();`
- **공통**: dot grid 배경 (`<pattern>` SVG 또는 Canvas 루프), 모노스페이스 섹션 라벨, 텍스트 최소화 — 도형과 연결선으로 구조 전달

## SVG/Canvas/D3 인라인 font-size 규칙

| 역할 | 최소 px | 비고 |
|------|---------|------|
| 콘텐츠 라벨 | 24px | `font-size="24"`, `ctx.font = '${24*S}px ...'` |
| 보조 라벨 (축 눈금, 순위 등) | 20px | 18px 이하 금지 |

## 텍스트 버짓 — 절대 한도

**Figure는 글의 설명을 대체하지 않는다. 시각적 앵커를 제공할 뿐이다.**

| 컴포넌트 | 최대 텍스트 | 예시 |
|---------|-----------|------|
| `.flow-card` | **제목 2~4단어**. 설명 생략 또는 max 6자 | "맥락 확인", "사례 복기" |
| `.quote-card` | **max 8자** (핵심 키워드만) | "좋은데요!", "0건" |
| `.section-label` | **max 6자** | "나쁜 예시", "좋은 방법" |
| `.tl-anno` | **사용 자제**. 쓸 경우 max 4자 키워드 | "맥락", "사례" |
| `.journey-desc` | **max 6자** | "서비스 인지" |
| `.story-desc` | **max 6자** | "결제 확인" |
| `.bar-label` | **max 4단어** | "React", "설문 응답률" |
| `.terminal-card-question` | **max 12자, 1줄 권장** (`<br>` 금지, balance 자동 줄바꿈) | "성공 기준은?" |
| `.terminal-option` | **max 8자** | "WAU 활성만" |
| `.terminal-answer` | **max 8자** | "첫 매출" |
| `.schema-field` | **필드명 max 8자. 타입 주석 생략** | "user_id FK" |
| `.matrix-corner` | **max 4자 또는 빈칸** | "" |
| Figure 전체 | **max 20단어** (Terminal 예외: 35단어) | — |

## 컴포넌트 수량 제한

**적은 수의 큰 컴포넌트 > 많은 수의 작은 컴포넌트.** 이 표가 컴포넌트 캡의 SSoT다 —
`validate_figure.py`도 여기 명시된 수량으로 캡을 검사한다.

| 패턴 | 최대 수량 | 이유 |
|------|---------|------|
| Flow | **3단계** | 3개면 비교 충분, 5개면 텍스트 덩어리 |
| Timeline | **3블록** | 블록 크기↑, 라벨 가독성↑ |
| Storyboard | **4패널 (2×2)** | 패널 크기 2배 확보 |
| Bar chart | **4행** | 바 높이 충분히 확보 |
| Architecture | **3레이어, 레이어당 3노드** (2노드면 너무 빈약) | 시스템 구조의 풍부함 |
| Split 비교 | **양쪽 각 2~3카드** | 카드 크기 유지 |
| Journey | **4단계** | dot 간 여백 확보 |
| Loop | **4노드 + 중앙 허브 1** | 노드는 링 네 변 중앙에 1개씩 — 5노드부터는 변 중앙 배치가 깨진다 |
| Schema | **3테이블, 테이블당 3~4필드** | 글자 크기 유지 |
| Terminal | **3카드, 카드당 옵션 2개 (max 3)** | 질문 max 12자 1줄, `<br>` 금지 |
| Matrix | **2×2 (셀 max 4). 코너 4자 이내 또는 빈칸** | 축 라벨이 의미 전달 |
| Waffle | **1 grid (10x10), 2 카테고리 (범례 2)** | 총 ~8단어 (범례 포함) |
| Typographic | **1 primary text (max 8단어)** | attribution max 4단어 |
| Slope | **max 5항목, 2시점** | 항목명 1단어 |
| Treemap | **max 6~8 cells** | **위계(그룹⊃항목) 데이터 전용 — flat 비율은 바 차트 권장.** 그룹=hue·자식=명도 스텝. 라벨 1단어. 작은 잔여 항목은 "기타"로 병합 — 무라벨 색면 금지 |
| Radar | **max 5축, 1~2 series** | 축 라벨 1단어 |
| Dumbbell | **max 5 rows** | 라벨 max 3단어 |
| Heatmap | **max 7x5 grid (35 cells)** | 셀 ~110x90px |
| Bullet | **max 3~4 charts** | 범위 3단계 + 타겟 마커 |
| Sparkline Grid | **max 6 sparklines (3x2)** | 항목당 라벨 1단어 + 값 1개 |
| Waterfall | **max 6~8 bars** | 라벨 1~2단어, 시작/합계 포함 |

## 최소 폰트 크기 — 2-tier 시스템

1440px 캔버스에서 **1.25rem(20px) 미만 절대 금지**.
콘텐츠 텍스트(읽어야 하는 키워드)는 **1.5rem(24px) 이상**.

| Tier | 최소 크기 | 25% 환산 | 해당 요소 |
|------|---------|---------|----------|
| 콘텐츠 | 1.5rem (24px) | 6px | `.flow-card`, `.bar-label`, `.state-node`, `.arch-node`, `.schema-field`, `.arrow-label`, `.journey-desc`, `.story-desc`, `.tl-anno`, `.matrix-corner`, `.terminal-prompt`, `.terminal-card-question` |
| 장식 마커 | 1.25rem (20px) | 5px | `.tag`, `.badge`, `.schema-pk`, `.schema-fk` |
| 섹션 헤딩 | 2rem (32px) | 8px | `.section-label` |
| Figure 제목 | 3rem (48px) | 12px | `.figure-title` |

**장식 전용 클래스** (`.sticker`, `.sticker-sm`, `.code`)는 콘텐츠 용도 사용 금지.
**Terminal 보조 텍스트** (`.terminal-option`, `.terminal-answer` 등)는 1.4rem(22px) 허용.
**SVG/Canvas 인라인**: `font-size` 최소 20px. 18px 이하 금지.

## Weight Hierarchy

| Role | Weight | Example |
|------|--------|---------|
| 모든 텍스트 기본값 | 700 | body default, `.flow-card`, `.journey-desc` |
| 부연/보조 (드물게 사용) | 400 | 긴 설명이 불가피할 때만 |
| Display titles | Noto Sans KR 900 | `.figure-title`, `.section-label` |

**v1.2 타이포 컨셉 이식** (폰트 교체 아님 — Domaine/Geist/Departure Mono는 한글 미지원):
- **48px+ 대형 타이틀은 음수 트래킹** — `.figure-title`/`.text-4xl`(−0.01em),
  `.text-5xl`(−0.015em)에 내장돼 있다. 인라인 대형 텍스트를 만들 때도 동일하게 적용
- **영문 마이크로 라벨(eyebrow)은 `.micro-label`** — JetBrains Mono·uppercase·자간 0.08em.
  v1.2의 Departure Mono 대문자 라벨 문법의 이식. 한글에는 uppercase가 무의미하므로
  영문 보조 라벨("STEP 1", "BEFORE/AFTER" 등)에만 쓴다

## 색 문법 — AGENTIC v1.2 면·텍스트 조합 (SSoT)

토큰 출처: AGENTIC DESIGN SYSTEM v1.2 (Figma `Bq6kNw42yQEA8swB5Vpa6c` →
`agentic30-greenfield/docs/design/agentic-ui-v1.2/tokens.css`). figure.css의 `:root`가
이 팔레트의 스냅샷이고, **면·텍스트 조합 규칙은 이 섹션이 SSoT다.** (WCAG 실측 수치 병기)

| 역할 | 스텝 조합 | 실측 대비 | figure.css 토큰 |
|------|----------|----------|----------------|
| 배지·워시 면 | **200 면 + 700 텍스트** | 7.9~16.8:1 | `--good-bg`+`--good-accent` 등 |
| 카테고리 채움면 | **500 면 + `--dark`** (예외: Blue·Purple 500은 `--white`) | 4.3~11.8:1 | `--tl-*` |
| 강조면 (경고·성공 카드) | **600 면 + `--white`** | 4.7~9.6:1 (전 hue 통과) | `--bad-card`/`--good-card` |
| 선(stroke) | Blue·Pink·Purple·Red는 **500**, Green·Orange·Teal은 **600 승급** | ≥3.6:1 | 아래 선 팔레트 |
| 보조 텍스트 | `--muted-fg`(#616161)는 **흰·연회색 배경 전용** | 6.2:1 on white | — |
| 형광펜·하이라이트 | **Yellow300 `--highlight` 등 연면 전용 + `--dark`** — 선·글자색 금지 | 15.9:1 | `--highlight`, `.mark-*` |

**색은 인코딩 수단이다 — 장식이 아니다.** 색을 칠하기 전에 "이 색이 어떤 데이터 차이를
인코딩하는가"에 답하라:

- **위치·길이가 이미 구분하는 단일 계열**(바 차트의 행, Funnel 스테이지, Journey 단계,
  Flow 순서)에는 **단색 + 강조 1색**만 쓴다. 항목마다 다른 hue를 입히면 존재하지 않는
  범주를 발명하는 것이다. 강조 1색은 "어디를 봐야 하는가"에만 쓴다.
- **다색은 실제 범주 구분이 있을 때만** — 서로 다른 시리즈(Slope·Sparkline의 항목),
  위계 그룹(Treemap), 시맨틱(good/bad). 이때도 4 hue 이내로 제한하고, 같은 대상은
  figure 세트 전체에서 같은 색을 유지한다(같은 항목 = 같은 색).
- **good/bad 병치는 색에만 의존 금지** — Green600 vs Red600은 명도가 사실상 같아(1.09:1)
  적록 색각이상에서 hue가 죽으면 구분이 소멸한다. 반드시 아이콘(✓/✗)·라벨·위치·방향
  같은 비색채 채널을 병행하라. 200 tint 쌍(Green200/Red200)은 정상 시각에서도 서로
  1.13:1이라 나란히 두면 안 된다.
- **카테고리 다색의 CVD 인접 금지 쌍**: Blue500↔Purple500, Green500↔Red500↔Orange500은
  deuteranopia에서 가장 먼저 뭉개진다(ΔE 10~16). 3~4색만 쓸 때는 **Blue → Orange →
  Green(선은 600) → Pink** 순서로 뽑으면 CVD 거리가 가장 멀다.

## 색상 대비 — 금지 조합

25% 축소에서 살아남는 것은 대비뿐이다. WCAG 실측 기준으로 지킬 것:

- **유색 면 위 `--muted-fg` 금지.** `--muted-fg`(#616161)는 `--white`/`--card`/`--muted` 같은
  흰·연회색 배경 전용이다. 유색 카드·노드 위 보조 텍스트는 `--dark`가 기본이고, 배경이
  Blue·Purple 계열(500+)이거나 600 강조면·`--dark`일 때만 `--white`를 쓴다.
  실측: Blue500 #0968F6 위 muted-fg = **1.27:1** — 사실상 안 보인다.
- **accent 텍스트 색(`.text-bad`/`.text-good`/`.text-info`)은 흰색·tint(200) 배경 전용.** 같은
  계열 강조면 위에 올리면 무너진다 — `--bad-card`(Red600) 위 `--bad-accent`(Red700) = **1.9:1**.
- **Yellow(#FFE58A·#EEBB04)와 밝은 500(Green #3CC14E·Teal #1BBFCA)은 선(stroke)·글자색 금지.**
  연회색 배경(#f5f5f5) 위 1.7~2.2:1이라 선이 통째로 사라진다. 이들은 **채움면 + `--dark`
  텍스트** 조합 전용(8.9~16.8:1). **선 팔레트**: Blue500 #0968F6 · Pink500 #DE458E ·
  Purple500 #583AEE · Red500 #F02D2D · Green600 #288034 · Orange600 #C15100 ·
  Teal600 #006F93 (Orange500 #EC7303은 2.79:1, Teal500 #1BBFCA는 2.06:1 미달 —
  선은 600 승급. 더 필요하면 `--dark`).
- **핵심 수치는 가장 큰 시각 무게.** Content Brief의 강조점(예: "0건", 전환 %)은 figure에서
  가장 크고 진해야 한다 — 크게 + `--dark` 900 (어두운 면 위면 `--white` 900). 핵심 수치가
  라벨보다 작거나 muted로 들어가는 **강조 역전 금지** — Journey의 %, Comparison의 대비 수치가
  대표 사례다.
- **다크 배경(Terminal)은 스텝을 승급한다**: muted-fg→Neutral500 #8F8F8F, accent→Blue400
  #70A9FF, good→Green500 #3CC14E — figure.css `.terminal` 블록이 재정의를 갖고 있다.

## 커넥터 — 화살표·연결선 두께

3px 보더 시스템과 균형을 맞춘다: 정보를 나르는 커넥터는 25% 축소 후에도 1.5px 이상 남아야 한다.

- **샤프트 최소 6px, 화살촉 최소 20px.** figure.css의 `.arrow-*`, `.journey-line`,
  `.tree-vline`/`.tree-hline`, `.seq-msg-line`이 이 기본값이다 — 인라인 스타일로 얇게 덮어쓰지 마라.
- **SVG 커넥터도 동일**: `stroke-width` ≥ 6(점선 보조 커넥터는 ≥5), 화살촉 `<marker>`는
  `markerUnits="userSpaceOnUse"` + 20px 이상. 기본 markerUnits는 stroke 굵기에 비례해
  화살촉이 왜곡된다.
- **보조 가이드선·데이터 마크는 예외**: 축·눈금·베이스라인·라이프라인처럼 구조 배경인 선은
  1.5~3px를 유지하고, Slope·Sparkline의 데이터 선은 흐름 커넥터가 아니라 마크라 예제 기본
  3px을 따른다(강조 항목만 6~8px 승급) — 커넥터와의 두께 위계가 오히려 정보를 만든다.
- **순환(Loop)은 직선 4개 금지에 준한다**: 링(6px 보더 + 큰 corner radius) 또는 코너 곡선 +
  방향 화살촉으로 회전이 형태 자체로 보이게 하라 (patterns-layout.md §13).

## Composition — 정형화 피하기

- `.figure-title` + `.insight-box`를 **매번 넣지 마라**. 컨텐츠만으로 의미가 전달되면 생략
- 제목이 필요하면 `.figure-title` 대신 패턴 내부에 자연스럽게 포함
- 하단 요약이 필요하면 `.insight-box` 대신 `.callout`이나 `.mark`로 변주
- 같은 블로그 포스트 내 여러 Figure는 각각 다른 구성을 사용할 것

## 캔버스 활용

콘텐츠는 1440×810 캔버스를 **균형 있게** 채워야 한다. 상단에 몰리고 하단이 텅 비는 배치는
축소 시 "떠 있는" 인상을 준다.

- **수직 채움**: 본문 컨테이너를 세로 중앙 정렬(`justify-content: center`)하거나 flex로 남은
  공간을 흡수(`flex: 1`)해 810px 높이를 고르게 쓴다. 상단 몰림 + 하단 공백 금지
- **가장자리 여백**: 요소가 캔버스 모서리에 붙거나 잘리지 않게 좌우(그리고 상하) 여백을
  **균등하게** 준다. 한쪽만 붙는 비대칭 배치 금지
- **면적으로 말하기**: 빈 공간이 남으면 컴포넌트를 늘리지 말고(수량 캡 유지) 기존 컴포넌트의
  크기·여백을 키워 캔버스를 채운다 — 모바일 축소에서 구조가 더 잘 잡힌다

## 아이콘/이모지 원칙

- **텍스트만으로 충분하면 아이콘 생략**. `.icon` 원형은 선택 사항
- `.flow-card`는 아이콘 없이 `<strong>제목</strong>`만으로 충분. 설명 텍스트 최소화
- 이모지는 카테고리 구분이 반드시 필요할 때만 (예: `.arch-label`, `.journey-dot`)
- 장식용 이모지/아이콘 금지

## 패턴별 레이아웃 규칙

모바일 축소 상태에서도 구조가 한눈에 잡히려면, 각 패턴의 정렬과 색상 사용이 일관되어야 한다.

**Comparison (Split)**
- 양쪽 카드는 **동일한 상단 시작점**에서 시작. `margin-top` 등으로 한쪽만 아래로 밀지 마라
- `.split-left`와 `.split-right`에 `justify-content: flex-start`를 명시하고, 카드 컨테이너의 구조를 동일하게 유지

**Matrix (2×2)**
- **열별 색상 통일**: 1열은 하나의 색상 계열, 2열은 다른 색상 계열. 같은 열의 셀은 모두 동일 색상
- **헤더 ≠ 셀**: 헤더(`.matrix-label-x`)는 진한 톤(`--good-card`, `--info-card`) + **`--white` 텍스트**(600 강조면), 본문 셀은 연한 톤(`--good-bg`, `--info-bg`) + `--dark` 텍스트
- **셀 구분선**: `.matrix`에 `background:var(--dark);gap:3px` 적용 (grid gap 기법). 개별 셀에 border 넣지 마라 — 이중 테두리가 생긴다
- 예: 1열 헤더 `--good-card` → 1열 셀 `--good-bg`, 2열 헤더 `--info-card` → 2열 셀 `--info-bg`
- **코너(좌상단)는 흰색**: `background:var(--white)`. 검은색 금지

**Architecture**
- 레이어당 노드 **최소 3개**. 2개만 넣으면 레이어 영역 대비 노드가 빈약해 보인다
- 프롬프트에 2개만 명시되어 있어도, 맥락상 추가 가능한 노드를 보충하라 (예: Client 레이어에 Web, Mobile 외 CLI 추가)

**Funnel**
- 각 스테이지 폭은 **값에 정비례**한다 — 비례가 이 패턴의 존재 이유다(proportional ink).
  **최소폭 클램프 금지**: 1.8%가 26% 폭으로 그려지면 figure가 데이터에 대해 거짓말을 한다.
  1.8%는 실처럼 가늘게 보이는 것이 정답이고, 그 가늘어짐이 전달하려는 충격이다
- 라벨·수치는 **바 내부가 아니라 바 오른쪽 바깥에** 단다(같은 행). 좁은 스테이지도 라벨이
  온전히 읽히고, 모든 행의 라벨 시작점이 정렬돼 비교가 쉬워진다
- 스테이지는 **좌측 정렬**로 쌓는다(공통 베이스라인 = 왼쪽 변) — 폭 비교의 기준선이 생긴다.
  순서는 시간·단계 순서 유지, 값 크기로 재정렬 금지

**Waffle (SVG)**
- 제목은 **한국어**로, 그리드 상단 또는 좌측에 배치. 영문 부제목/서브타이틀 금지
- **분리형 범례 금지 — 직접 라벨**: 그리드 우측에 스와치 + **큰 수치(40px 900) + 짧은
  한국어 라벨**을 한 덩어리로 밀착시켜, 범례가 아니라 "숫자가 주인공인 직접 라벨"로 읽히게
  한다. 채움 색과 수치가 한 시선에 붙어 있어야 왕복이 없다

**Typographic Statement (SVG)**
- 인용문은 캔버스(1440×810) 기준 **수직·수평 모두 중앙 정렬**
- SVG의 viewBox를 `0 0 1440 810`으로 설정하고, 텍스트 블록의 y 좌표를 중앙에 맞춰라

## Textures & Decorations

- `.bg-dots`, `.bg-lines`, `.bg-grid`, `.bg-crosshatch` — 시각적 깊이
- `.tape`, `.sticker`, `.stamp`, `.mark` — 수제 느낌
- `.bg-*`, `.p-*`, `.m-*`, `.badge`, `.tag` — inline style 최소화

## File Naming

```
web/public/blog/images/{blog-slug}/{blog-slug}-{figure-name}.png
```

Repo root(`agentic30-greenfield`) 기준 상대 경로다 (2026-07-05 web/ 통합 — 구경로
`blog/public/…`은 폐기). 실행 중인 리포에 이 디렉터리가 없으면 임의로 추측하지 말고
사용자에게 저장 위치를 물어라.

## MDX Usage

```mdx
<Figure src="/blog/images/{slug}/{filename}.png" alt="..." caption="..." />
```

## Output Spec

- **해상도**: 출력 PNG는 2880×1620 (1440×810의 retina 2x)이 표준. retina 캡처가 불가능한
  폴백 경로(Playwright — deviceScaleFactor 지정 불가)에서는 1440×810(1x)을 최후 수단으로 허용
- **용량 가이드**: 300KB를 넘으면 압축을 고려하라 — 단, 압축은 해상도를 보존해야 한다.
  `sips -Z 1440` 같은 리샘플은 해상도를 절반(1440×810)으로 낮춰 규격을 깨므로 최종 산출물에
  쓰지 마라
  - PNG 팔레트 압축(해상도 유지, 평면 단색 다이어그램에 효과적): `pngquant --force --quality=65-80 input.png -o output.png`
    (quality 하한 미달 시 exit 99로 파일을 저장하지 않는다 — 그땐 무손실 압축으로 폴백)
  - 완전 무손실: `oxipng -o max input.png`
  - 사진/스크린샷 성격 한정: `cwebp -q 80 input.png -o output.webp`
  - 위 도구는 별도 설치가 필요할 수 있다 — 없으면 압축을 건너뛰고 사용자에게 고지하라
- 사진/스크린샷 성격의 콘텐츠는 WebP를 고려할 수 있다. 다이어그램(도형·텍스트 위주)은
  선명도 손실을 피하기 위해 PNG를 유지하라

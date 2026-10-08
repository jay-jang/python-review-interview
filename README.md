# python-review-interview

Python 코드 리뷰 인터뷰를 준비하기 위한 한국어 학습 자료입니다. Junior부터 Intermediate, Expert까지 문법, 스타일, 흔한 실수, 실무 설계, 고급 기능을 다루며, 코드 예제와 해설이 있는 실전 문제를 제공합니다.

현재 Claude, Codex, AGY 세 버전의 HTML 프레젠테이션을 포함합니다. 각 버전은 브라우저에서 바로 열 수 있는 독립 실행 파일입니다.

## GitHub Pages에서 보기

| 버전 | 페이지 경로 | 바로가기 | 저장소 문서 |
| --- | --- | --- | --- |
| Claude | `/python-review-interview/claude/` | [Claude 프레젠테이션 열기](https://jay-jang.github.io/python-review-interview/claude/) | [claude/README.md](claude/README.md) |
| Codex | `/python-review-interview/codex/` | [Codex 프레젠테이션 열기](https://jay-jang.github.io/python-review-interview/codex/) | [codex/README.md](codex/README.md) |
| AGY | `/python-review-interview/agy/` | [AGY 프레젠테이션 열기](https://jay-jang.github.io/python-review-interview/agy/) | [agy/README.md](agy/README.md) |

GitHub Pages의 기본 주소는 `https://jay-jang.github.io/python-review-interview/`입니다. 위 링크에서 원하는 버전으로 바로 접근할 수 있습니다.

## 현재 프로젝트에 포함된 내용

| 항목 | Claude | Codex | AGY |
| --- | --- | --- | --- |
| 분량 | 102장 | 123장 | 38장 |
| 주요 내용 | Python 핵심 모델, Pythonic 관용구, 스타일 가이드, 흔한 실수, Best Practice, 고급 기능, Python 3.8~3.14 변화, 레벨별 리뷰 체크리스트 | Junior 핵심, 스타일과 계약, Intermediate 실무, 타입과 추상화, Expert 객체 모델, 동시성과 실행 모델, 운영 품질, 고급 기능과 종합 | 레벨별 평가 루브릭과 이슈 심각도(P0~P3), 흔한 실수 12가지(Before/After/Diff), Python 3.10~3.12+ 고급 기능(패턴 매칭, except*, TaskGroup, 디스크립터, ExitStack) |
| 실전 문제 | 출력 예측 16문항, 코드 리뷰 12문항 | 해설·수정안·회귀 테스트·채점 기준을 포함한 리뷰 문제 24문항 | 레벨별 실전 코드 리뷰 9문항(PR 코드, 리뷰 포인트, 모범 리뷰, 리팩토링 코드) |
| 학습 기능 | 목차, 슬라이드/스크롤 보기, 다크 모드 | 발표/학습 모드, 목차 검색·난이도 필터, 상세 해설, 코드 복사, 답안 저장·내보내기, 인쇄, 실행 예제 다운로드 | 슬라이드 개요 그리드, 목차, 전체 화면, 다크/라이트 테마, Before/After 나란히·탭 비교, 터치 스와이프 |

공통으로 다음과 같은 리뷰 포인트를 학습할 수 있습니다.

- 가변 기본 인자, 이름 바인딩, 객체의 동일성과 동등성 등 Python의 핵심 동작
- 컴프리헨션, 제너레이터, 컨텍스트 매니저와 예외 처리
- 네이밍, 타입 힌트, 문서화, 함수·클래스 설계와 테스트
- 데코레이터, 디스크립터, 상속과 MRO 등 고급 객체 모델
- 비동기 코드, 동시성, 캐시와 성능 관련 실수 및 개선 방향
- 문제의 영향과 우선순위, 수정안, 검증할 테스트를 설명하는 리뷰 연습

## 프로젝트 구조

```text
python-review-interview/
├── README.md                 # 프로젝트 개요와 GitHub Pages 링크
├── .nojekyll                 # GitHub Pages에서 정적 파일을 그대로 제공
├── claude/
│   ├── README.md             # Claude 버전 안내
│   ├── index.html            # 102장 프레젠테이션
│   └── source/
│       ├── build.py          # 코드 하이라이팅 및 HTML 생성
│       ├── template.html     # 화면 스타일과 프레젠테이션 기능
│       └── src/*.html        # 주제별 슬라이드 원본
├── codex/
│   ├── README.md             # Codex 버전 안내
│   ├── index.html            # 123장 프레젠테이션
│   └── python_review_lab.py  # 표준 라이브러리 실행 예제와 27개 테스트
└── agy/
    ├── README.md             # AGY 버전 안내
    ├── index.html            # 38장 프레젠테이션
    └── verify_agy.py         # 오프라인·구조·콘텐츠 검증 스크립트
```

## 로컬에서 보기

저장소를 내려받은 뒤 `claude/index.html`, `codex/index.html`, `agy/index.html` 중 하나를 브라우저에서 열면 됩니다. 프레젠테이션 열람에는 별도 패키지 설치가 필요하지 않습니다.

```bash
git clone https://github.com/jay-jang/python-review-interview.git
cd python-review-interview
```

로컬 HTTP 서버로도 볼 수 있습니다.

```bash
python3 -m http.server 8000
```

- Claude: <http://localhost:8000/claude/>
- Codex: <http://localhost:8000/codex/>
- AGY: <http://localhost:8000/agy/>

### 조작 방법

- Claude: `←` / `→` 이동, `T` 목차, `S` 슬라이드/스크롤 보기 전환, `D` 다크 모드
- Codex: `←` / `→` / `Space` 이동, `T` 목차·검색, `N` 상세 해설, `A` 문제 해설, `F` 전체 화면, `Home` / `End` 처음·끝 이동. 답안 저장·내보내기와 실행 예제 다운로드를 지원합니다.
- AGY: `←` / `→` / `Space` 이동, `G` 전체 슬라이드 보기, `T` 목차, `F` 전체 화면, `D` 다크/라이트 테마

## Claude 프레젠테이션 다시 빌드하기

Claude 버전의 내용은 `claude/source/src/*.html`에서, 스타일과 화면 기능은 `claude/source/template.html`에서 수정합니다. 다음 명령은 저장소 루트에서 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pygments
python3 claude/source/build.py claude/index.html
```

Codex 버전은 별도 빌드 스크립트 없이 `codex/index.html`을 직접 수정합니다.

## GitHub Pages 배포

현재 GitHub Pages는 `main` 브랜치의 루트(`/`)를 게시 대상으로 사용합니다. 변경 사항을 `main`에 push하면 GitHub Pages 빌드를 거쳐 `/claude/`, `/codex/`, `/agy/` 경로에 반영됩니다.

# Python 코드 리뷰 인터뷰 대비

Python 코드 리뷰 인터뷰 준비용 프레젠테이션(한국어, 102장)입니다. Junior부터 Expert 수준까지의 리뷰 포인트, 스타일 가이드, 흔한 실수, best practice, 고급 기능, 최신 Python 변화, 실전 문제(출력 예측 16문항, 코드 리뷰 12문항)를 담고 있습니다.

- `index.html`: 외부 의존성 없는 단일 HTML 파일. 브라우저로 바로 열 수 있습니다.
- 조작: `←` `→` 이동, `T` 목차, `S` 슬라이드/스크롤 보기 전환, `D` 다크 모드

## 다시 빌드하기

```bash
pip install pygments
python3 source/build.py index.html   # claude/ 폴더 안에서 실행
```

슬라이드 원본은 `source/src/*.html`에 있고, `<py bad|good ln cap="...">` 태그가 하이라이팅된 코드 블록으로 변환됩니다.

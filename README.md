# vibe_sdd

간단한 오늘의 할 일 웹 애플리케이션입니다.

## 실행 방법

1. 의존성 설치
   - `pip install -r requirements.txt`
   - `pip install jinja2`
2. 환경 변수 설정
   - `.env.example`을 복사해 `.env`를 생성합니다.
   - 필요하면 `DATABASE_URL`을 수정합니다.
3. 서버 실행
   - `uvicorn app.main:app --reload`
4. 브라우저 접속
   - `http://127.0.0.1:8000/`

## 테스트 실행

- `pytest -q`

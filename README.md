# CLIP AI Backend

FastAPI 기반 이미지 분류 API  
Render에 배포 가능 (Python 3.10 기준)

## 실행

```bash
uvicorn app.main:app --reload
```

## 주요 경로

- `POST /classify` - 이미지 테마 분류
- `GET /ping` - 상태 확인

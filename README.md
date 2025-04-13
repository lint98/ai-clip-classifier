# CLIP AI Backend

FastAPI 기반 이미지 분류 API  
Render에 배포 가능 (Python 3.10 기준)

1️⃣ ImageMagick 설치
아래 링크로 이동
👉 https://imagemagick.org/script/download.php#windows

최신 Q16 x64 DLL 버전 다운로드
예시: ImageMagick-7.1.1-30-Q16-HDRI-x64-dll.exe

C:\Program Files\ImageMagick-7.1.1-Q16-HDRI
이 경로가 환경 변수 PATH에 포함되어야 함.
convert.exe가 있는지 확인.

convert -version
정상적으로 동작하면 ImageMagick 버전 정보가 나와야 해.

설치할 때 꼭 아래 체크

✅ Install legacy utilities (e.g., convert)

✅ Add application directory to your system path

## 실행

venv환경접속
.\.venv\Scripts\Activate.ps1

```bash
uvicorn app.main:app --reload
```

## api

- `POST /classify` - 이미지 테마 분류
- `GET /ping` - 상태 확인

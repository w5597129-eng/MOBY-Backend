from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. 우리가 만든 'api' 폴더에서 모든 라우터 파일들을 가져옵니다.
# (아직 이 파일들이 비어있어도 괜찮습니다. 미리 연결만 해둡니다.)
from backend.api import auth, users, facilities, alerts, reports, admin

# 2. FastAPI '본체' 앱을 생성합니다.
app = FastAPI(
    title="MOBY IoT Platform API",
    description="MOBY 프로젝트를 위한 실시간 설비 모니터링 API입니다.",
    version="0.1.0",
)

# 3. CORS 미들웨어 설정 (필수!)
# React(포트 3000)에서 FastAPI(포트 8000)로 보내는
# '교차 출처' API 요청을 허용하기 위한 설정입니다.
origins = [
    "http://localhost",  # 로컬 개발 환경
    "http://localhost:3000",  # React 개발 서버 주소 (프론트엔드)
    # TODO: 나중에 실제 배포할 프론트엔드 도메인을 여기에 추가하세요.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 이 출처들에서의 요청을 허용
    allow_credentials=True,  # 쿠키/인증 정보 허용
    allow_methods=["*"],  # 모든 HTTP 메소드(GET, POST 등) 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 4. 각 라우터(팔, 다리)들을 '본체'에 조립합니다.
# (A 개발자 담당)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(facilities.router, prefix="/facilities", tags=["Facilities"])

# (B 개발자 담당)
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


# 5. (테스트용) 루트 엔드포인트
@app.get("/")
async def read_root():
    return {"message": "Welcome to MOBY IoT Platform API"}

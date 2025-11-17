from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# 1. 방금 만든 config.py 파일에서 settings 객체를 가져옵니다.
from backend.core.config import settings

# 2. '연결 통로' (Engine) 생성
# create_async_engine: FastAPI 같은 비동기 앱을 위한 SQLAlchemy 엔진입니다.
# settings.DATABASE_URL: .env 파일에서 읽어온 "postgresql+asyncpg://..." 주소
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # echo=True로 설정하면, 실행되는 SQL 쿼리가 터미널에 로그로 찍힙니다. (개발 시 유용)
)

# 3. '안내 창구' (Session Maker) 생성
# DB와 실제 대화를 나누는 '세션'을 만드는 공장(factory)입니다.
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 커밋 후에도 객체를 계속 사용할 수 있게 설정
)


# 4. '모델의 기반' (Base) 클래스 생성
# backend/models/ 폴더 안의 모든 모델(User, Facility 등)이
# 이 'Base' 클래스를 상속받아야 합니다.
class Base(DeclarativeBase):
    pass


# 5. API를 위한 'DB 세션 제공' 함수 (가장 중요!)
# FastAPI의 '의존성 주입(Dependency Injection)' 시스템을 위한 함수입니다.
async def get_db() -> AsyncSession:
    """
    API 엔드포인트에 DB 세션을 주입(제공)하는 의존성 함수입니다.
    요청이 시작될 때 세션을 열고, 요청이 끝나면(성공/실패 무관) 세션을 닫습니다.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  # 비동기 쿼리를 위한 select

# 1. DB 모델 (DB와 대화)
from backend.models.user import User

# 2. API 스키마 (데이터 형식)
from backend.schemas.user import UserCreate

# 3. 보안 로직 (비밀번호 해싱)
from backend.core.security import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    이메일을 기준으로 DB에서 사용자를 1명 조회합니다.

    :param db: (get_db 함수로부터 주입된) 비동기 DB 세션
    :param email: 조회할 이메일
    :return: User 모델 객체 (없으면 None)
    """
    # 쿼리 생성: "SELECT * FROM users WHERE users.email = [email]"
    query = select(User).where(User.email == email)

    # 쿼리 실행 (비동기)
    result = await db.execute(query)

    # 쿼리 결과에서 첫 번째 항목을 가져옵니다. (없으면 None)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    새로운 사용자를 DB에 생성합니다.

    :param db: (get_db 함수로부터 주입된) 비동기 DB 세션
    :param user: (API로부터 받은) UserCreate 스키마 (순수 비밀번호 포함)
    :return: 생성된 User 모델 객체
    """

    # 1. (보안) 순수 비밀번호를 해시값으로 변환합니다.
    hashed_password = get_password_hash(user.password)

    # 2. UserCreate 스키마를 User DB 모델 객체로 변환합니다.
    #    (주의: password 필드에는 해시된 값을 넣어줍니다.)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        # is_active 등 다른 필드는 DB 모델의 default 값을 따릅니다.
    )

    # 3. DB 세션에 '추가' (아직 DB에 저장된 것은 아님)
    db.add(db_user)

    # 4. DB에 '커밋' (실제 저장 실행) (비동기)
    await db.commit()

    # 5. DB에 방금 생성된 객체의 정보(예: 새로 생성된 id)를 '새로고침' (비동기)
    await db.refresh(db_user)

    return db_user

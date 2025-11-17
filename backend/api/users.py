from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# 1. '핏줄': DB 세션을 가져오는 공통 함수
from backend.database import get_db

# 2. '데이터 명세서': API가 받을(Create) 데이터와 응답할(Read) 데이터
from backend.schemas.user import UserCreate, UserRead

# 3. '실행 로직': 실제 DB 작업을 수행하는 함수들
from backend.services import user_service

# 'APIRouter'는 main.py의 '심장(app)'에 연결될 '팔다리'입니다.
router = APIRouter()


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserCreate,  # (1) 요청 Body를 UserCreate 스키마로 검증/받음
    db: AsyncSession = Depends(get_db),  # (2) get_db 함수가 DB 세션을 '주입'
):
    """
    회원가입 API 엔드포인트입니다.

    :param user: (Request Body) UserCreate 스키마 (email, password)
    :param db: (Dependency) DB 세션
    :return: UserRead 스키마 (id, email, is_active) - 비번 제외!
    """

    # 1. (서비스 로직) 이메일이 이미 존재하는지 확인
    db_user = await user_service.get_user_by_email(db, email=user.email)
    if db_user:
        # 이미 존재하면 400 에러 발생
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # 2. (서비스 로직) 존재하지 않으면, 새 사용자 생성
    #    (이 함수 내부에서 비밀번호 해싱이 일어남)
    new_user = await user_service.create_user(db=db, user=user)

    # 3. (응답) UserRead 스키마에 맞춰서 응답 (비밀번호 자동 제외됨)
    return new_user

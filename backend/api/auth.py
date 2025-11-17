from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

# 1. '핏줄': DB 세션
from backend.database import get_db

# 2. '데이터 명세서': 응답할 토큰 모양
from backend.schemas.auth import Token

# 3. '실행 로직': DB에서 사용자 조회
from backend.services import user_service

# 4. '보안 로직': 비밀번호 검증, 토큰(출입증) 생성
from backend.core import security

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    # (1) 'form-data'로 "username"과 "password"를 받음
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    로그인 API 엔드포인트입니다.
    'username' 필드에 이메일을, 'password' 필드에 비밀번호를 받아
    JWT Access Token(출입증)을 발급합니다.
    """

    # 1. (서비스 로직) 'username' 필드(즉, 이메일)로 사용자를 찾습니다.
    user = await user_service.get_user_by_email(db, email=form_data.username)

    # 2. 사용자가 없거나, 비밀번호가 틀리면 401 에러 발생
    # (보안을 위해 "이메일이 틀렸습니다" / "비번이 틀렸습니다"라고
    #  구체적으로 알려주지 않는 것이 좋습니다.)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},  # 표준 응답 헤더
        )

    # 3. (보안 로직) 로그인 성공! '출입증(Access Token)'을 생성합니다.
    #    토큰의 '주인(sub)'은 사용자의 이메일입니다.
    access_token = security.create_access_token(data={"sub": user.email})

    # 4. (응답) Token 스키마에 맞춰서 토큰을 반환합니다.
    return {"access_token": access_token, "token_type": "bearer"}

from pydantic import BaseModel, EmailStr
from typing import Optional


# --- 로그인 시 사용할 스키마 (API 입력용) ---
class LoginRequest(BaseModel):
    """
    /auth/login (로그인) API로 요청(Request)할 때 사용될 스키마입니다.
    (OAuth2 사양에서는 username, password를 쓰지만, 우린 email을 username으로 사용)
    """

    # HTML form에서 username 필드에 email을 담아 보낼 것을 가정합니다.
    # 만약 JSON으로 email, password를 받는다면 아래와 같이 정의합니다.
    # email: EmailStr
    # password: str

    # FastAPI의 OAuth2PasswordRequestForm
    # (HTML <form> 태그)를 기준으로 합니다.
    # 이 경우 username 필드에 이메일을 담아 보냅니다.
    username: EmailStr
    password: str


# --- 토큰 응답 시 사용할 스키마 (API 출력용) ---
class Token(BaseModel):
    """
    로그인 성공 시 /auth/login API가 응답(Response)할 때 사용될 스키마입니다.
    """

    access_token: str
    token_type: str  # (보통 "bearer"라는 고정 문자열이 들어갑니다)


# --- 토큰 내부 데이터 스키마 (보안용) ---
class TokenData(BaseModel):
    """
    JWT 토큰 '내부'에 저장될 데이터의 형식을 정의합니다. (예: "sub": "user@email.com")
    """

    email: Optional[EmailStr] = None

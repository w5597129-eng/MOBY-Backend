from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext  # 비밀번호 해싱
from jose import JWTError, jwt  # JWT 생성 및 검증

# 1. Phase 0에서 만든 config.py 파일에서 settings 객체를 가져옵니다.
from backend.core.config import settings

# 2. Phase 1에서 만든 auth.py 스키마에서 TokenData를 가져옵니다.
from backend.schemas.auth import TokenData

# --- 1. 비밀번호 해싱 설정 ---

# CryptContext: 사용할 해싱 알고리즘을 지정합니다. (bcrypt 사용)
# deprecated="auto": 구형 해시를 자동으로 최신으로 업그레이드합니다.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 비밀번호(plain)와 DB의 해시된 비밀번호(hashed)를 비교합니다.

    :param plain_password: 사용자가 입력한 순수 비밀번호
    :param hashed_password: DB에 저장된 해시된 비밀번호
    :return: 일치하면 True, 아니면 False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    순수 비밀번호를 받아 bcrypt 해시값으로 변환합니다.

    :param password: 사용자가 입력한 순수 비밀번호
    :return: 해시된 비밀번호 문자열
    """
    return pwd_context.hash(password)


# --- 2. JWT 토큰(출입증) 생성 및 검증 ---

# .env 파일에서 읽어온 설정값들
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 만료 시간 (예: 30분)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT Access Token (출입증)을 생성합니다.

    :param data: 토큰 내부에 저장할 데이터 (예: {"sub": "user@email.com"})
    :param expires_delta: 토큰 만료 시간 (지정하지 않으면 기본 30분)
    :return: 인코딩된 JWT 토큰 문자열
    """
    to_encode = data.copy()

    # 만료 시간 설정
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    # JWT 토큰 생성
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> TokenData:
    """
    (보너스) JWT 토큰을 '검증'하는 함수입니다.
    이 함수는 나중에 API 접근 권한을 확인할 때 (dependencies.py) 사용됩니다.
    """
    try:
        # 토큰 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # 토큰에서 'sub' (주체) 필드를 꺼냅니다.
        email: str = payload.get("sub")
        if email is None:
            # 주체가 없으면 유효하지 않은 토큰
            raise credentials_exception

        # TokenData 스키마로 검증
        token_data = TokenData(email=email)
    except JWTError:
        # JWT 파싱/검증 중 에러 발생 (예: 만료, 잘못된 서명)
        raise credentials_exception

    return token_data

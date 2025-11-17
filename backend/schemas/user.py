from pydantic import BaseModel, EmailStr


# --- 기본 스키마 ---
class UserBase(BaseModel):
    """
    User 모델의 공통 필드를 정의하는 기본 스키마입니다.
    (DB 모델의 'email' 컬럼과 이름이 같아야 합니다.)
    """

    # EmailStr 타입은 Pydantic이 자동으로 이메일 형식을 검증해줍니다.
    email: EmailStr


# --- 회원가입 시 사용할 스키마 (API 입력용) ---
class UserCreate(UserBase):
    """
    /users/signup (회원가입) API로 요청(Request)할 때 사용될 스키마입니다.
    UserBase를 상속받아 'password' 필드를 추가로 받습니다.
    """

    password: str


# --- 사용자 정보 응답 시 사용할 스키마 (API 출력용) ---
class UserRead(UserBase):
    """
    /users/{id} (사용자 정보 조회) API가 응답(Response)할 때 사용될 스키마입니다.
    """

    id: int
    is_active: bool

    # Pydantic v2부터는 ConfigDict를 사용합니다.
    # (Pydantic v1의 경우: class Config: orm_mode = True)
    class ConfigDict:
        # 이 설정을 True로 해야, SQLAlchemy의 DB 모델(User) 객체를
        # Pydantic 스키마(UserRead)가 읽을 수 있게 됩니다. (매우 중요!)
        from_attributes = True

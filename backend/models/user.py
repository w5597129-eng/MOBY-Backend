from sqlalchemy import Column, Integer, String, Boolean

# Phase 0에서 만든 '공통 기반' Base 클래스를 가져옵니다.
from backend.database import Base


class User(Base):
    """
    User 모델 (DB 테이블)
    모든 모델은 우리가 database.py에서 만든 Base 클래스를 상속받아야 합니다.
    """

    # __tablename__은 PostgreSQL에 생성될 실제 테이블의 이름을 지정합니다.
    __tablename__ = "users"

    # --- 테이블의 컬럼(Column)들을 정의합니다 ---

    # id 컬럼:
    # Integer: 정수 타입
    # primary_key=True: 이 테이블의 고유 식별자(PK)로 지정
    # index=True: 검색 속도를 높이기 위해 인덱스 설정
    id = Column(Integer, primary_key=True, index=True)

    # email 컬럼:
    # String: 문자열(VARCHAR) 타입
    # unique=True: 이메일은 중복될 수 없음
    # index=True: 이메일로 사용자를 찾는 경우가 많으므로 인덱스 설정
    # nullable=False: 이 값은 비어있을(NULL) 수 없음
    email = Column(String, unique=True, index=True, nullable=False)

    # hashed_password 컬럼:
    # String: 문자열 타입
    # nullable=False: 비밀번호는 비어있을 수 없음
    # (실제 비밀번호가 아닌, 해시(암호화)된 값을 저장합니다.)
    hashed_password = Column(String, nullable=False)

    # is_active 컬럼: (선택 사항이지만 유용합니다)
    # Boolean: 참/거짓(True/False) 타입
    # default=True: 기본값은 '활성' 상태
    is_active = Column(Boolean, default=True)

    # TODO: 나중에 '설비(Facility)' 모델과 관계를 맺을 때
    # facilities = relationship("Facility", back_populates="owner")

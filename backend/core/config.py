from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일의 경로를 명시적으로 지정
# 이 config.py 파일은 core/ 안에 있으므로, .env 파일은 부모의 부모 폴더에 있습니다.
# (backend/core/ -> backend/ -> .env)
# 하지만 main.py가 backend/에서 실행될 것을 가정하고 경로를 설정합니다.
# 가장 확실한 방법은 load_dotenv()를 호출하는 것입니다.
load_dotenv()


class Settings(BaseSettings):
    """
    애플리케이션 설정을 관리하는 클래스
    .env 파일에서 환경 변수를 읽어옵니다.
    """

    # .env 파일에서 읽어올 변수들을 타입과 함께 선언합니다.
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        # .env 파일의 경로를 직접 지정할 수도 있습니다.
        # env_file = ".env"
        # env_file_encoding = 'utf-8'
        pass


# Settings 클래스의 인스턴스를 생성합니다.
# 다른 파일에서는 이 'settings' 객체를 import하여 설정값에 접근합니다.
settings = Settings()

# --- 테스트용 ---
# 이 파일이 잘 작동하는지 확인하려면
# 터미널에서 python backend/core/config.py 를 실행해보세요.
if __name__ == "__main__":
    print("설정값 로드 테스트:")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    print(f"JWT_SECRET_KEY: {settings.JWT_SECRET_KEY}")

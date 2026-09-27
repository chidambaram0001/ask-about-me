from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    port:int = 9000
    API_KEY:str = ''
    DATABASE_URL:str = ''
    INGEST_DOC_PATH:str = '../assets/chidambaram_resume_rag.txt'
    embedding_dimension:int = 768
    INGEST_DOC_KEY:str = ''
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8"
    )
settings = Settings()
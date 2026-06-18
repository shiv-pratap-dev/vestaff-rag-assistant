from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Global configurations for VeStaff. 
    Automatically loads the .env vars

    """
    # HuggingFace:
    HF_TOKEN:str = Field(..., description = 'HuggingFace API Token')
    HF_API_BASE_URL: str = Field(
        default="https://router.huggingface.co/v1",
    )

    # Models:
    EMBEDDING_MODEL: str = Field(
        default = "sentence-transformers/all-MiniLM-L6-v2"
    )

    LLM_MODEL: str = Field(
        default="meta-llama/Llama-3.1-8B-Instruct"
    )

    # Retrieval:
    TOP_K: int = Field( default = 6)
    SIMILARITY_THRESHOLD: float = Field(default=0.45)

    #File Path
    FILE_PATH: str = Field(..., description= "contains the path of input file"
    )

    # database path
    DB_PATH: str = Field(
    default="query_logs.db"
)
    VECTOR_STORE_PATH: str = Field(
    default="vectorstores"
)

    # App
    APP_NAME : str = "AWS Agreement"
    ENV: str = Field(default = "development")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

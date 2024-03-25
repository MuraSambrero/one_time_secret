from pydantic import BaseModel, Field

class Secret(BaseModel):
    secret_data: str = Field(min_length=5)
    code_phrase: str = Field(min_length=8)
    ttl: int = Field(ge=5, le=3600*7*24, default=60, alias="ttl_seconds")


class SecretResponse(BaseModel):
    code_phrase: str
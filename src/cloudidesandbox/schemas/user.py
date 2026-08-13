from pydantic import BaseModel, Field


class UserSchema(BaseModel):

    password: str = Field(min_length=8, max_length=128)
    login: str = Field(min_length=8, max_length=50)

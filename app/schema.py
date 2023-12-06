import pydantic
from typing import Optional, Type


# pip install pydantic Через эту библиотеку очень хорошо валидировать данные по определённому шаблону
# Различие create от update в том, что в update - все поля опциональны (from typing import Optional)

class AbstractUser(pydantic.BaseModel):
    name: str
    password: str

    @pydantic.field_validator("name")
    @classmethod  # Особенность библиотеки pydantic
    def name_length(cls, v: str) -> str:
        if len(v) > 100:
            raise ValueError("Maxima length of name is 100")  # Доп. проверка на длину имени
        return v

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError(f"Minimal length of password is 8")
        return v

class CreateUser(AbstractUser):
    name: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str]
    password: Optional[str]


SCHEMA_CLASS = Type[CreateUser | UpdateUser]  # Создаём тип данных для передачи классов
SCHEMA = CreateUser | UpdateUser

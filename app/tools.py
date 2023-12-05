from schema import SCHEMA_CLASS
from pydantic import ValidationError
from errors import HttpError


def validate(schema_cls: SCHEMA_CLASS, json_data: dict | list):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
        # Создаём экземпляр класса схемы, которую мы валидируем и извлекаем из неё словарь
        # Так как в UpdateUser поля опциональны, по умолчанию pydantic создаст эти поля в словаре,
        # который мы получаем на выходе и подставит туда None. То есть появятся ключи. Чтобы этого не происходило
        # параметр exclude_unset=True
    except ValidationError as er:
        error = er.errors()[0]  # Метод errors возвращает список ошибок
        error.pop("ctx", None)  # Удаляем свойство ctx, т.к. там инф-ция, которую мы не хотим передавать пользователю
        raise HttpError(400, error)

# Если мы будем импортировать из server.py, то может получиться цикличный импорт. Поэтому создадим отдельный модуль, в
# котором будем хранить ошибки (errors.py)
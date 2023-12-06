import flask
from errors import HttpError
from flask import views, jsonify, request  # Импортируем глобальную переменную request
# jsonify берёт словарь или список, превращает в корректный http-ответ.
from flask_bcrypt import Bcrypt
from models import Session, User
from schema import CreateUser, UpdateUser
from sqlalchemy.exc import IntegrityError  # Для проверки на уникальность (юзера)
from tools import validate

app = flask.Flask("app")  # Создаём экземпляр класса Flask. Это по сути WEB-server
bcrypt = Bcrypt(app)
# Создаём экземпляр класса Bcrypt, передаём туда в качестве аргумента приложение, которое мы создали

def hash_password(password: str):
    password = password.encode()  # Преобразовываем строчку в байты
    return bcrypt.generate_password_hash(password).decode()  # Обратно преобразовываем в строку. Можно записывать в базу

def check_password(password: str, hashed_password: str):
    # Принимает пароль, который отправляет пользователь. И пароль, который лежит в базе.
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)

@app.before_request
def before_request():
    session = Session()  # Создаём сессию
    request.session = session  # Привязываем к объекту request. Делаем сессию свойством запроса

@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response

# @app.errorhandler(404)
@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    # jsonify берёт словарь или список, превращает в корректный http-ответ.
    response.status_code = error.status_code
    return response

def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user

def add_user(user: User):  # Принимает самого юзера (ORM-модель) и добавляет в базу
    try:  # Проверка на уникальность юзера
        request.session.add(user)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description="user already exists")


# Очень удобно будет передавать id usera задавать в самом URL в качестве переменной. Flask такое умеет

class UserView(views.MethodView):

    @property
    def session(self) -> Session:
        return request.session  # Возвращается объект сессии

    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data = validate(CreateUser, request.json)  # Валидируем входящий json
        user_data["password"] = hash_password(user_data["password"])  # Хешируем пароль
        user = User(**user_data)  # Создаём экземпляр класса User.
        #  В Python операторы * и ** используются, чтобы упаковывать и распаковывать итерабельные объекты и словари.
        #  Эти операторы обеспечивают гибкий способ обработки аргументов функций и позволяют писать функции,
        #  которые могут принимать переменное количество аргументов.
        add_user(user)  # Добавляем в БД
        return jsonify({"id": user.id})

    def patch(self, user_id: int):
        user = get_user(user_id)
        user_data = validate(UpdateUser, request.json)  # Валидируем входящий json
        if 'password' in user_data:  # Если пароль есть в user_data
            user_data['password'] = hash_password(user_data['password'])  # То хешируем пароль
        # Нужно проитерироваться по парам: ключ - значение, которые есть в user_data
        for key, value in user_data.items():
            setattr(user, key, value)  # Устанавливаем в поля аттрибуты
            add_user(user)  # Вызываем add_user для того, чтобы изменения записались в базу
        return jsonify({"id": user.id})  # Возвращаем id юзера, которого мы создали

    def delete(self, user_id: int):
        user = get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return jsonify({"status": "ok"})



user_view = UserView.as_view("user_view")
# В "user_view" передаётся метаинформация. В принципе можно в круглые скобки написать что угодно. Но принято писать то,
# что подходит по смыслу

app.add_url_rule(rule="/users/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"])
app.add_url_rule(rule="/users", view_func=user_view, methods=["POST"])
# Говорим, что здесь будет переменная типа int (<user_id:int>)
# У самого апликэйшена Flask есть метод add_url_rule для привязки url
# (певый аргумент - сам url, второй - функция
# А также мы может передать сюда список методов, по которым эта view будет доступна )
# Нам нужно преобразовать UserView в совместимый объект с view_func. Для этого есть метод as_view


if __name__ == '__main__':
    app.run(debug=True)  # "debug=True" <- При ошибках будет выдаваться доп. debug-информация

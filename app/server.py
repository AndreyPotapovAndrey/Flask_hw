import flask
from errors import HttpError
from flask import jsonify, request, views
from flask_bcrypt import Bcrypt
from models import Session, Ads
from schema import CreateAds, UpdateAds
from sqlalchemy.exc import IntegrityError  # Для проверки на уникальность (юзера)
from tools import validate

app = flask.Flask("app")  # Создаём экземпляр класса Flask. Это по сути WEB-server
bcrypt = Bcrypt(app)
# Создаём экземпляр класса Bcrypt, передаём туда в качестве аргумента приложение, которое мы создали


@app.before_request
def before_request():
    session = Session()  # Создаём сессию
    request.session = (
        session  # Привязываем к объекту request. Делаем сессию свойством запроса
    )


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


def get_ads(ads_id: int):
    ads = request.session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, "ads not found")
    return ads


def add_ads(ads: Ads):  # Принимает само объявление (ORM-модель) и добавляет в базу
    try:  # Проверка на уникальность объявления
        request.session.add(ads)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(status_code=409, description="ads already exists")


class AdsView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session  # Возвращается объект сессии

    def get(self, ads_id: int):
        ads = get_ads(ads_id)
        return jsonify(ads.dict)

    def post(self):
        ads_data = validate(CreateAds, request.json)  # Валидируем входящий json
        ads = Ads(**ads_data)  # Создаём экземпляр класса Ads.
        return jsonify({"id": ads.id})

    def patch(self, ads_id: int):
        ads = get_ads(ads_id)
        ads_data = validate(UpdateAds, request.json)  # Валидируем входящий json
        for key, value in ads_data.items():
            setattr(ads, key, value)  # Устанавливаем в поля аттрибуты
            add_ads(ads)  # Вызываем add_ads для того, чтобы изменения записались в базу
        return jsonify({"id": ads.id})  # Возвращаем id объявления, которого мы создали

    def delete(self, ads_id: int):
        ads = get_ads(ads_id)
        self.session.delete(ads)
        self.session.commit()
        return jsonify({"status": "ok"})


ads_view = AdsView.as_view("ads_view")


app.add_url_rule(
    rule="/ads/<int:ads_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule(rule="/ads", view_func=ads_view, methods=["POST"])
# Говорим, что здесь будет переменная типа int (<ads_id:int>)
# У самого апликэйшена Flask есть метод add_url_rule для привязки url
# (певый аргумент - сам url, второй - функция
# А также мы может передать сюда список методов, по которым эта view будет доступна )
# Нам нужно преобразовать AdsView в совместимый объект с view_func. Для этого есть метод as_view


if __name__ == "__main__":
    app.run(
        debug=True
    )  # "debug=True" <- При ошибках будет выдаваться доп. debug-информация

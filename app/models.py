import datetime
import os

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# func - объект, который позволяет использовать функции на стороне БД (дата и время создания записи)

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# Адрес DSN, который будем передавать при подключении
engine = create_engine(
    PG_DSN
)  # Такая фабрика подключений, которая создаёт много подключений внутри себя, управляет
# ими и выдаёт их для сессии
Session = sessionmaker(
    bind=engine
)  # Создаём базовый класс для сессии. Указываем, чтобы подключение брал из engine


class Base(DeclarativeBase):
    pass


class Ads(Base):
    __tablename__ = "ads_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner:  Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "registration_time": self.registration_time.isoformat(),
            "owner": self.owner
        }


Base.metadata.create_all(bind=engine)

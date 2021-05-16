from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.dialects.firebird import CHAR
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Model(Base):  # type: ignore  # noqa
    __abstract__ = True
    __mapper_args__ = {
        "eager_defaults": True,
    }


class Chenal(Model):
    __tablename__ = "repost_chenal"

    id = Column(Integer, primary_key=True)
    id_chenal = Column(BIGINT, unique=True)
    chenel_name = Column(Text)


class User(Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    state_auth = Column(Integer)
    number_post = Column(BIGINT)


class Word(Model):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    zap_word = Column(Text)

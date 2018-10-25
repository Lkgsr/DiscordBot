from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session


class DataBase:
    def __init__(self):
        self.Base = declarative_base()
        self.engine = create_engine("sqlite:///data.db", echo=False)
        self.session = scoped_session(sessionmaker())
        self.session.remove()
        self.session.configure(bind=self.engine, autoflush=False, expire_on_commit=False)

    def create_data_base(self):
        self.Base.metadata.create_all(self.engine)


db = DataBase()


class User(db.Base):

    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    nick_name = Column(String)
    last_played_game = Column(String)
    highest_role = Column(String)
    level = Column(Integer)
    current_exp = Column(Float)

    def __init__(self, id, username, nickname, lastplayedgame, highestrole, level=0, currentexp=0, prestige=0):
        self.id = id
        self.user_name = username
        self.nick_name = nickname
        self.last_played_game = lastplayedgame
        self.highest_role = highestrole
        self.level = level
        self.current_exp = currentexp
        self.prestige = prestige

    async def commit(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    async def find_by_username(cls, username):
        return db.session.query(cls).filter_by(usern_name=username).first()

    @classmethod
    async def find_by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()

    @classmethod
    async def get_all(cls):
        return db.session.query(cls).all()




db.create_data_base()

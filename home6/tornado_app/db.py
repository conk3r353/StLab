from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Message(Base):
    __tablename__ = 'message'

    def __repr__(self):
        return f'Message {self.text} by {self.name}'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(Text)
    room = Column(Integer)


class DbController:
    conn = 'postgresql://test_user:Test_Password@localhost:5432/tornado_app'
    engine = create_engine(conn)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    @staticmethod
    def db_setup():
        Base.metadata.create_all()

    @classmethod
    def add_message(cls, name, text, room):
        cls.session.add(Message(name=name, text=text, room=room))
        cls.session.commit()

    @classmethod
    def clear_room(cls, room):
        items = cls.session.query(Message).filter(Message.room == room).all()
        for item in items:
            cls.session.delete(item)
        cls.session.commit()

    @classmethod
    def get_room_messages(cls, room):
        return cls.session.query(Message).order_by(Message.id).filter(Message.room == room).all()


DbController.db_setup()

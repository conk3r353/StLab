from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shops'

    def __repr__(self):
        return f'Shop {self.name}'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    staff_amount = Column(Integer)


class Department(Base):
    __tablename__ = 'departments'

    def __repr__(self):
        return f'Department {self.sphere}'

    id = Column(Integer, primary_key=True)
    sphere = Column(String)
    staff_amount = Column(Integer)
    shop_id = Column(Integer, ForeignKey('shops.id'))
    shops = relationship(Shop, backref='departments')


class Item(Base):
    __tablename__ = 'items'

    def __repr__(self):
        return f'Item {self.name}'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    price = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
    departments = relationship(Department, backref='items')

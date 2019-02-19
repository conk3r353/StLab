from models import Base, Shop, Department, Item
from sqlalchemy import create_engine, or_, select, literal, and_
from sqlalchemy.orm import sessionmaker, join
from sqlalchemy.sql import func


class AlchemyManager:
    conn_str = 'postgresql://test_user:Test_Password@localhost:5432/home4_alchemy'
    engine = create_engine(conn_str)
    Base.metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    def create_tables(self):
        Base.metadata.create_all()

    def insert_data(self):
        self.session.add_all([Shop(id=1, name='Auchan', address=None, staff_amount=250),
                              Shop(id=2, name='IKEA', address='Street Žirnių g. 56, Vilnius, Lithuania.',
                                   staff_amount=500),
                              Department(id=1, sphere='Furniture', staff_amount=250, shop_id=1),
                              Department(id=2, sphere='Furniture', staff_amount=300, shop_id=2),
                              Department(id=3, sphere='Dishes', staff_amount=200, shop_id=2),
                              Item(id=1, name='Table', description='Cheap wooden table', price=300, department_id=1),
                              Item(id=2, name='Table', description=None, price=750, department_id=2),
                              Item(id=3, name='Bed', description='Amazing wooden bed', price=1200, department_id=2),
                              Item(id=4, name='Cup', description=None, price=10, department_id=3),
                              Item(id=5, name='Plate', description='Glass plate', price=20, department_id=3)])
        self.session.commit()

    def update_data(self):
        self.session.query(Item).filter(
            or_(Item.name.ilike('b%'), Item.name.ilike('%e'))
        ).update({Item.price: Item.price + 100}, synchronize_session='fetch')
        self.session.commit()

    def select_data(self, task):
        if task == 1:
            return self.session.execute(select([Item]).select_from(Item).where(Item.description != 'None')).fetchall()

        elif task == 2:
            return [department[0] for department in
                    self.session.query(Department.sphere).filter(Department.staff_amount > 200).distinct().all()]

        elif task == 3:
            return self.session.execute(select([Shop.address]).select_from(Shop).where(
                Shop.name.ilike('i%'))).fetchall()

        elif task == 4:
            return self.session.query(Item).join(Department).filter(Department.sphere == 'Furniture').all()

        elif task == 5:
            return self.session.query(Shop).join(Department, Item).filter(Item.description.isnot(None)).all()

        elif task == 6:
            return self.session.query(Item, Department, Shop).join(Department, Shop).all()

        elif task == 7:
            return self.session.query(Item).group_by(Item.name, Item.id).limit(2).offset(2).all()

        elif task == 8:
            return self.session.query(Item, Department).join(Department).all()

        elif task == 9:
            return self.session.query(Item, Department).join(Department, isouter=True).all()

        elif task == 10:
            return self.session.query(Department, Item).join(Item, isouter=True).all()

        elif task == 11:
            return self.session.query(Item, Department).join(Department, full=True).all()

        elif task == 12:
            return self.session.query(Item, Department).join(Department, literal(True)).all()

        elif task == 13:
            return self.session.execute(select(
                [func.count(Item.id),
                 func.sum(Item.price),
                 func.max(Item.price),
                 func.min(Item.price),
                 func.avg(Item.price)]
                ).select_from(join(Item, join(Department, Shop))).having(func.count(Item.id) > 1)).fetchall()

        elif task == 14:
            return self.session.execute(select(
                [Shop.name,
                 func.array_agg(Item.name)]
            ).select_from(join(Item, join(Department, Shop))).group_by(Shop.name)).fetchall()

    def delete_data(self, task):
        if task == 1:
            self.session.query(Item).filter(and_(Item.price > 500, Item.description.is_(None))).delete()
            self.session.commit()

        elif task == 2:
            items = self.session.query(Item).join(Department, Shop).filter(Shop.address.is_(None)).all()
            for item in items:
                self.session.delete(item)
            self.session.commit()

        elif task == 3:
            items = self.session.query(Item).join(Department).\
                filter(Item.id.in_(self.session.query(Department.id).filter(or_(
                           Department.staff_amount > 275,
                           Department.staff_amount < 225))
                       ))
            for item in items:
                self.session.delete(item)
            self.session.commit()

        elif task == 4:
            self.session.query(Item).delete()
            self.session.query(Department).delete()
            self.session.query(Shop).delete()
            self.session.commit()

    def drop_tables(self):
        Base.metadata.drop_all()

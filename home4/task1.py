import psycopg2


class SQLManager:
    try:
        conn = psycopg2.connect(dbname='home4', user='test_user', host='localhost', password='Test_Password')
    except psycopg2.Error:
        raise SystemExit('Unable to connect to the database.')

    curr = conn.cursor()

    def create_tables(self):

        self.curr.execute("""
        create table if not exists Shops(
          id int primary key,
          name varchar,
          address varchar null,
          staff_amount int)
        """)

        self.curr.execute("""
        create table if not exists Departments(
          id int primary key,
          sphere varchar,
          staff_amount int,
          shop_id int,
          foreign key (shop_id) references Shops (id) 
        )
        """)

        self.curr.execute("""
        create table if not exists Items(
          id int primary key,
          name varchar,
          description text null,
          price int,
          department_id int,
          foreign key (department_id) references Departments (id)
        )
        """)

        self.conn.commit()

    def insert_data(self):

        self.curr.execute("""
        insert into shops values
          (1, 'Auchan', null, 250),
          (2, 'IKEA', 'Street Žirnių g. 56, Vilnius, Lithuania.', 500);
        """)

        self.curr.execute("""
        insert into departments values 
          (1, 'Furniture', 250, 1),
          (2, 'Furniture', 300, 2),
          (3, 'Dishes', 200, 2)
        """)

        self.curr.execute("""
        insert into items values 
          (1, 'Table', 'Cheap wooden table', 300, 1),
          (2, 'Table', null, 750, 2),
          (3, 'Bed', 'Amazing wooden bed', 1200, 2),
          (4, 'Cup', null, 10, 3),
          (5, 'Plate', 'Glass plate', 20, 3)
        """)
        self.conn.commit()

    def update_data(self):
        self.curr.execute("""
        update items 
        set price = price + 100
        where name ilike 'b%' or name ilike '%e'
        """)
        self.conn.commit()

    def select_data(self, task):
        if task == 1:
            self.curr.execute("select * from items where description is not null")
            return self.curr.fetchall()

        elif task == 2:
            self.curr.execute("select distinct sphere from departments where staff_amount > 200")
            return [item[0] for item in self.curr.fetchall()]

        elif task == 3:
            self.curr.execute("select address from shops where name ilike 'i%'")
            return [item[0] for item in self.curr.fetchall()]

        elif task == 4:
            self.curr.execute("""
             select i.name
             from items i join departments d on i.department_id = d.id 
             where d.sphere = 'Furniture'
             """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 5:
            self.curr.execute("""
            select name
            from shops
            where id in 
              (select distinct d.id from departments d join items i on d.id = i.department_id
               where i.name is not null)
            """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 6:
            self.curr.execute("""
            select i.name, i.description, i.price,
              concat('department_id ', i.department_id), concat('department_sphere ', d.sphere),
              concat('department_staff_amount ', d.staff_amount), concat('department_shop_id ', d.shop_id),
              concat('shop_name ', s.name), concat('shop_address ', s.address),
              concat('shop_staff_amount ', s.staff_amount)
            from (items i join departments d on i.department_id = d.id) join shops s on d.shop_id = s.id
            """)
            return self.curr.fetchall()

        elif task == 7:
            self.curr.execute("""
            select id
            from items
            order by name
            offset 2 limit 2
            """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 8:
            self.curr.execute("""
            select i.name, d.sphere
            from items i inner join departments d on i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 9:
            self.curr.execute("""
            select i.name, d.sphere
            from items i left join departments d on i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 10:
            self.curr.execute("""
            select i.name, d.sphere
            from items i right join departments d on i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 11:
            self.curr.execute("""
            select i.name, d.sphere
            from items i full join departments d on i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 12:
            self.curr.execute("""
            select i.name, d.sphere
            from items i cross join departments d
            """)
            return self.curr.fetchall()

        elif task == 13:
            self.curr.execute("""
            select count(i.id), sum(i.price), max(i.price), min(i.price), avg(i.price)
            from (items i join departments d on i.department_id = d.id) join shops s on d.shop_id = s.id
            having count(i.name) > 1
            """)
            return self.curr.fetchall()

        elif task == 14:
            self.curr.execute("""
            select s.name, array_agg(i.name)
            from (items i join departments d on i.department_id = d.id) join shops s on d.shop_id = s.id
            group by s.name
            """)
            return self.curr.fetchall()

    def delete_data(self, task):
        if task == 1:
            self.curr.execute("""
            delete from items
            where price > 500 and description is null
            """)
            self.conn.commit()

        elif task == 2:
            self.curr.execute("""
            delete from items
            where department_id = (
              select d.id 
              from departments d join shops s on d.shop_id = s.id
              where s.address is null )
            """)
            self.conn.commit()

        elif task == 3:
            self.curr.execute("""
            delete from items
            where id in (
              select id
              from departments
              where staff_amount < 225 or staff_amount > 275)
            """)
            self.conn.commit()

        elif task == 4:
            self.curr.execute("delete from items")
            self.curr.execute("delete from departments")
            self.curr.execute("delete from shops")
            self.conn.commit()

    def drop_tables(self):
        self.curr.execute("drop table items")
        self.curr.execute("drop table departments")
        self.curr.execute("drop table shops")
        self.conn.commit()

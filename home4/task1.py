import psycopg2


class SQLManager:
    try:
        conn = psycopg2.connect(dbname='home4', user='test_user', host='localhost', password='Test_Password')
    except psycopg2.Error:
        raise SystemExit('Unable to connect to the database.')

    curr = conn.cursor()

    def create_tables(self):

        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS Shops(
          id INT PRIMARY KEY,
          name VARCHAR,
          address VARCHAR NULL,
          staff_amount int)
        """)

        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS Departments(
          id INT PRIMARY KEY,
          sphere VARCHAR,
          staff_amount INT,
          shop_id INT,
          FOREIGN KEY (shop_id) REFERENCES Shops (id) 
        )
        """)

        self.curr.execute("""
        CREATE TABLE IF NOT EXISTS Items(
          id INT PRIMARY KEY,
          name VARCHAR,
          description TEXT NULL,
          price INT,
          department_id INT,
          FOREIGN KEY (department_id) REFERENCES Departments (id)
        )
        """)

        self.conn.commit()

    def insert_data(self):

        self.curr.execute("""
        INSERT INTO shops VALUES 
          (1, 'Auchan', NULL, 250),
          (2, 'IKEA', 'Street Žirnių g. 56, Vilnius, Lithuania.', 500);
        """)

        self.curr.execute("""
        INSERT INTO departments VALUES 
          (1, 'Furniture', 250, 1),
          (2, 'Furniture', 300, 2),
          (3, 'Dishes', 200, 2)
        """)

        self.curr.execute("""
        INSERT INTO items VALUES 
          (1, 'Table', 'Cheap wooden table', 300, 1),
          (2, 'Table', NULL, 750, 2),
          (3, 'Bed', 'Amazing wooden bed', 1200, 2),
          (4, 'Cup', NULL, 10, 3),
          (5, 'Plate', 'Glass plate', 20, 3)
        """)
        self.conn.commit()

    def update_data(self):
        self.curr.execute("""
        UPDATE items 
        SET price = price + 100
        WHERE name ILIKE 'b%' OR name ILIKE '%e'
        """)
        self.conn.commit()

    def select_data(self, task):
        if task == 1:
            self.curr.execute("SELECT * from items where description is not null")
            return self.curr.fetchall()

        elif task == 2:
            self.curr.execute("SELECT DISTINCT sphere FROM departments WHERE staff_amount > 200")
            return [item[0] for item in self.curr.fetchall()]

        elif task == 3:
            self.curr.execute("SELECT address FROM shops WHERE name ILIKE 'i%'")
            return [item[0] for item in self.curr.fetchall()]

        elif task == 4:
            self.curr.execute("""
             SELECT i.name
             FROM items i JOIN departments d ON i.department_id = d.id 
             WHERE d.sphere = 'Furniture'
             """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 5:
            self.curr.execute("""
            SELECT name
            FROM shops
            WHERE id IN 
              (SELECT DISTINCT d.id FROM departments d JOIN items i ON d.id = i.department_id
               WHERE i.name IS NOT NULL)
            """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 6:
            self.curr.execute("""
            SELECT i.name, i.description, i.price,
              CONCAT('department_id ', i.department_id), CONCAT('department_sphere ', d.sphere),
              CONCAT('department_staff_amount ', d.staff_amount), CONCAT('department_shop_id ', d.shop_id),
              CONCAT('shop_name ', s.name), CONCAT('shop_address ', s.address),
              CONCAT('shop_staff_amount ', s.staff_amount)
            FROM (items i JOIN departments d ON i.department_id = d.id) JOIN shops s ON d.shop_id = s.id
            """)
            return self.curr.fetchall()

        elif task == 7:
            self.curr.execute("""
            SELECT id
            FROM items
            ORDER BY name
            OFFSET 2 LIMIT 2
            """)
            return [item[0] for item in self.curr.fetchall()]

        elif task == 8:
            self.curr.execute("""
            SELECT i.name, d.sphere
            FROM items i INNER JOIN departments d ON i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 9:
            self.curr.execute("""
            SELECT i.name, d.sphere
            FROM items i LEFT JOIN departments d ON i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 10:
            self.curr.execute("""
            SELECT i.name, d.sphere
            FROM items i RIGHT JOIN departments d ON i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 11:
            self.curr.execute("""
            SELECT i.name, d.sphere
            FROM items i FULL JOIN departments d ON i.department_id = d.id
            """)
            return self.curr.fetchall()

        elif task == 12:
            self.curr.execute("""
            SELECT i.name, d.sphere
            FROM items i CROSS JOIN departments d
            """)
            return self.curr.fetchall()

        elif task == 13:
            self.curr.execute("""
            SELECT COUNT(i.id), SUM(i.price), MAX(i.price), MIN(i.price), AVG(i.price)
            FROM (items i JOIN departments d ON i.department_id = d.id) JOIN shops s ON d.shop_id = s.id
            HAVING COUNT(i.name) > 1
            """)
            return self.curr.fetchall()

        elif task == 14:
            self.curr.execute("""
            SELECT s.name, ARRAY_AGG(i.name)
            FROM (items i JOIN departments d ON i.department_id = d.id) JOIN shops s ON d.shop_id = s.id
            GROUP BY s.name
            """)
            return self.curr.fetchall()

    def delete_data(self, task):
        if task == 1:
            self.curr.execute("""
            DELETE FROM items
            WHERE price > 500 AND description IS NULL
            """)
            self.conn.commit()

        elif task == 2:
            self.curr.execute("""
            DELETE FROM items
            WHERE department_id = (
              SELECT d.id 
              FROM departments d JOIN shops s ON d.shop_id = s.id
              WHERE s.address IS NULL)
            """)
            self.conn.commit()

        elif task == 3:
            self.curr.execute("""
            DELETE FROM items
            WHERE id IN (
              SELECT id
              FROM departments
              WHERE staff_amount < 225 or staff_amount > 275)
            """)
            self.conn.commit()

        elif task == 4:
            self.curr.execute("DELETE FROM items")
            self.curr.execute("DELETE FROM departments")
            self.curr.execute("DELETE FROM shops")
            self.conn.commit()

    def drop_tables(self):
        self.curr.execute("DROP TABLE items")
        self.curr.execute("DROP TABLE departments")
        self.curr.execute("DROP TABLE shops")
        self.conn.commit()

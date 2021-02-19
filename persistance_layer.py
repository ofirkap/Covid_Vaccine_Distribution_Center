import sqlite3


# The DTOs of the database
class Vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


# Generic DAO
class Dao:
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        q_marks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, column_names, q_marks)

        self._conn.execute(stmt, params)

    def find(self, **key_values):
        column_names = key_values.keys()
        params = list(key_values.values())

        stmt = 'SELECT * FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, params)
        return self._dto_type(*c.fetchall()[0])

    # returns the first item in a table sorted by 'column'
    def find_first_by_order(self, column):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {} ORDER BY {} ASC LIMIT 1'.format(self._table_name, column))
        return self._dto_type(*c.fetchall()[0])

    def delete(self, **key_values):
        column_names = key_values.keys()
        params = list(key_values.values())

        stmt = 'DELETE FROM {} WHERE {}'.format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))

        c = self._conn.cursor()
        c.execute(stmt, params)

    # adds 'value' to the 'column' of the item given by 'id'
    def increment(self, column, value, id):
        self._conn.execute(
            'UPDATE {} SET {} = {} + {} WHERE id = {}'.format(self._table_name, column, column, value, id))


# The Repository
class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.create_tables()
        self.vaccines = Dao(Vaccine, self._conn)
        self.suppliers = Dao(Supplier, self._conn)
        self.clinics = Dao(Clinic, self._conn)
        self.logistics = Dao(Logistic, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS vaccines (
            id              INTEGER     PRIMARY KEY AUTOINCREMENT NOT NULL,
            date            DATE        NOT NULL,
            supplier        INT         NOT NULL,
            quantity        INT         NOT NULL,
            FOREIGN KEY(supplier)       REFERENCES suppliers(row_id)
        );
        
        CREATE TABLE IF NOT EXISTS suppliers (
            id              INT         PRIMARY KEY NOT NULL,
            name            TEXT        NOT NULL,
            logistic        INT         NOT NULL,
            FOREIGN KEY(logistic)       REFERENCES logistics(id)
        );

        CREATE TABLE IF NOT EXISTS clinics (
            id              INT         PRIMARY KEY NOT NULL,
            location        TEXT        NOT NULL,
            demand          INT         NOT NULL,
            logistic        INT         NOT NULL,
            FOREIGN KEY(logistic)       REFERENCES logistics(id)
        );
        
        CREATE TABLE IF NOT EXISTS logistics (
            id              INT         PRIMARY KEY NOT NULL,
            name            TEXT        NOT NULL,
            count_sent      INT         NOT NULL,
            count_received  INT         NOT NULL
        );
    """)


# the repository singleton
repo = _Repository()

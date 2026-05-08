import sqlite3 as sql

# class Database:
#     def __init__(self):
#         self.connection = sql.connect('src\database\log.db')
#         # self.table = table
#         # self.prim_key = prim_key
#         # self.columns = columns or []
        
#         self.cursor = self.connection.cursor()
        
#         # cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({prim_key} INTEGER)')
#         # cursor.execute(f'INSERT INTO {table} VALUES (2)')
        
#         # self.connection.commit()
        
#         # cursor.execute(f'SELECT {prim_key} from {table}')
#         # print(cursor.fetchall())
#         # self.connection.close()
        
#     def create_table(self, table, prim_key, columns=None):
#         """Adds new table to database

#         Args:
#             table (str): name of the table
#             prim_key (int): primary key for the table_
#             columns (str, str): name and data type for each column (e.g. [[f_name, TEXT], [age, INTEGER]]). Defaults to None.
#         """
#         columns = columns or []
#         cursor = self.connection.cursor()
#         cursor.execute(f'CREATE TABLE IF NOT EXISTS {table} ({prim_key} INTEGER)')
        
#         for column in columns:
#             cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column[0]} {column[1]}")

# # database = Database()
# # database.create_table("band", "id", [["hello", "TEXT"], ["age", "INTEGER"]])
# # print(database.cursor.fetchall())

# class Table:
#     def __init__(self, database, table=None, prim_key=None, columns=None):
#         self.connection =sql.connect(database)
#         self.cursor = self.connection.cursor()
#         self.table = table
#         self.prim_key = prim_key
#         self.columns = columns or []
        
#     def create_table(self, table, prim_key):
#         """Adds new table to database

#         Args:
#             table (str): name of the table
#             prim_key (int): primary key for the table_
#             columns (str, str): name and data type for each column (e.g. [[f_name, TEXT], [age, INTEGER]]). Defaults to None.
#         """
#         #columns = columns or []
#         #cursor = self.connection.cursor()
#         self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table} ({prim_key} INTEGER)') 
        
#     def add_column(self, name, type):
#         self.cursor.execute(f"ALTER TABLE {self.table} ADD COLUMN {name} {type}")
        
#     def output(self):
#         print(self.cursor.fetchall())
        
# database = Table(database='src\Database\log.db')
# database.create_table("people", "f_name")
# database.add_column('age', 'INTEGER')
# database.add_column('hello', 'TEXT')
         
class Users():
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY CHECK(length(user_id)=6),
            password TEXT,
            salt TEXT,
            f_name TEXT NOT NULL,
            l_name TEXT NOT NULL,
            access_level INTEGER NOT NULL CHECK(access_level BETWEEN 1 AND 5),
            group_id INTEGER
            )''')  
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT user_id, password, salt, f_name, l_name, access_level, group_id FROM users'):
            print(row)
        
    def create_user(self, user_id, f_name, l_name, password=None, salt=None, access_level=1, group_id=None):
        self.cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?)', (user_id, password, salt, f_name, l_name, access_level, group_id))
        
    def fetch_password(self, user_id):
        """fetch hashed password and salt
        Args:
            user_id (Int): User unique id
        Raises:
            Exception: User not found
        Returns:
            tuple: password, salt
        """     
        results = self.cursor.execute('''SELECT password, salt 
                                      FROM users 
                                      WHERE user_id = ?''', (user_id,))
        row = results.fetchone()
        if row:
            password, salt = row
            return password, salt
        else:
            raise Exception("User not found")


        
class Groups():
    def __init__(self, database):
        self.connection =sql.connect(database)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            group_name TEXT
            )''') 

class PrinterModels:
    def __init__(self, database):
        self.connection =sql.connect(database)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS printer_models (
            model_id INTEGER PRIMARY KEY,
            model_name TEXT
            )''') 

class Printers:
    def __init__(self, database):
        self.connection =sql.connect(database)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS printers (
            printer_id INTEGER PRIMARY KEY,
            )''') 

class Filaments:
    def __init__(self, database):
        self.connection =sql.connect(database)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            )''') 

class Logs:
    def __init__(self, database):
        self.connection =sql.connect(database)
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            print_id INTEGER PRIMARY KEY,
            user_id TEXT,
            print_name TEXT,
            gcode TEXT,
            duration INTEGER,
            weight INTEGER,
            date_time TEXT,
            printer_id INTEGER,
            filament_id INTEGER,
            approval BOOLEAN,
            approver_id INTEGER
            successful BOOLEAN
            )''') 
        
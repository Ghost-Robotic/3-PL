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
        for row in self.cursor.execute('SELECT * FROM users'):
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
        
    def fetch_auth(self, user_id):
        results = self.cursor.execute('''SELECT access_level 
                                      FROM users
                                      WHERE user_id = ?''',(user_id,))
        row = results.fetchone()
        if row:
            return int(row[0])
        else:
            raise Exception("User not found")
        
    def fetch_name(self, user_id):
        result = self.cursor.execute('''SELECT f_name, l_name 
                                     FROM users 
                                     WHERE user_id =?''',(user_id,))
        
        row = result.fetchone()
        name = row[0][0].upper()+row[0][1:]+ " " + row[1][0].upper()+row[1][1:]
        return name.title()
    
    def fetch_table(self):
        rows = []
        for row in self.cursor.execute('SELECT user_id, access_level, f_name, l_name FROM users'):
            columns = []
            name = row[2][0].upper()+row[2][1:]+ " " + row[3][0].upper()+row[3][1:]
            
            columns.append(row[0])
            columns.append(name)
            columns.append(row[1])
            rows.append(columns)
        return rows 

        
class Groups():
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            group_name TEXT
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM groups'):
            print(row)
            
    def add_group(self, group_name):
         self.cursor.execute('INSERT INTO groups VALUES (?,?)',(None,group_name))

class PrinterModels:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS printer_models (
            model_id INTEGER PRIMARY KEY,
            model_name TEXT,
            brand TEXT,
            multimaterial BOOLEAN,
            filament_id
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM printer_models'):
            print(row)
            
    def add_printer_model(self, model_name, brand, multimaterial=False, filament_id=None):
         self.cursor.execute('INSERT INTO printer_models VALUES (?,?,?,?,?)',(None,model_name,brand,multimaterial,filament_id))
         
    def fetch_all(self):
        rows = []
        for row in self.cursor.execute('SELECT * FROM printer_models'):
            rows.append(row)
        return rows  
         
    def fetch_name_brand(self):
        models = {}
        for row in self.cursor.execute('SELECT model_id, model_name, brand FROM printer_models ORDER BY brand ASC'):
            id = row[0]
            name = row[2] +" "+ row[1]
            models.update({name:id})
        return models
    
    def fetch_id(self, name):
        row = self.cursor.execute('SELECT model_id FROM printer_models WHERE model_name = ?',(name,))
        model = self.cursor.fetchone()
        if model[0] != None:
            return model[0]
        else:
            raise Exception("Model not found")
        
    def fetch_name(self, id):
        row = self.cursor.execute('SELECT brand, model_name FROM printer_models WHERE model_id = ?',(id,))
        result = row.fetchone()
        name = result[0] +" "+ result[1]
        return name
    

class Printers:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS printers (
            printer_id INTEGER PRIMARY KEY,
            model_id INTEGER,
            group_id INTEGER
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM printers'):
            print(row)
            
    def add_printer(self, model_id, group_id=None):
         self.cursor.execute('INSERT INTO printers VALUES (?,?,?)',(None,model_id,group_id))
         


class Filaments:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS filaments (
            filament_id INTEGER PRIMARY KEY,
            material TEXT,
            weight INTEGER,
            amount INTEGER
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM filaments'):
            print(row)
            
    def add_filament(self, material, weight=1000, amount=0):
         self.cursor.execute('INSERT INTO filaments VALUES (?,?,?,?)', (None,material,weight,amount))
         
    def fetch_all(self):
        rows = []
        for row in self.cursor.execute('SELECT * FROM filaments'):
            rows.append(row)
        return rows  
         
    def fetch_names(self):
        materials = {}
        for row in self.cursor.execute('SELECT filament_id,material FROM filaments ORDER BY material ASC'):
            materials.update({row[1]:row[0]})
        return materials
    
    def fetch_name(self, id):
        row = self.cursor.execute('SELECT material FROM filaments WHERE filament_id = ?',(id,))
        result = row.fetchone()
        name = result[0]
        return name

class Logs:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA forgeign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            print_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            successful BOOLEAN,
            
            FOREIGN KEY (user_id)
                REFERENCES users (user_id),
                
            FOREIGN KEY (model_id)
                REFERENCES printer_models (model_id),
                
            FOREIGN KEY (filament_id)
                REFERENCES filaments (filament_id),
                
            FOREIGN KEY (approver_id)
                REFERENCES users (user_id)
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM users'):
            print(row)
            
    def add_log(self, user_id, print_name, gcode, duration, weight, printer_id, filament_id, approval=None, approver_id=None, successful=None):
        datetime = self.get_datetime()
        
        self.cursor.execute('INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',(None,user_id,print_name,gcode,duration,weight,datetime,printer_id,filament_id,approval,approver_id,successful))
    
    def get_datetime(self):
        self.cursor.execute('SELECT datetime("now","localtime")')
        datetime = self.cursor.fetchone()
        return datetime[0]
    
    def fetch_table(self):
        rows = []
        for row in self.cursor.execute('SELECT print_id, user_id, print_name, duration, weight, printer_id, filament_id, date_time FROM logs'):
            columns = []
            columns.append(str(row[0]))
            
            name = accounts.fetch_name(row[1])
            columns.append(name)
            
            columns.append(row[2])

            hours = row[3]//60
            mins = row[3]%60
            columns.append(str(hours)+"hrs "+str(mins)+"mins")

            columns.append(row[4])
            
            columns.append(printer_models.fetch_name(row[5]))
            columns.append(filaments.fetch_name(row[6]))
            
            datetime = row[7].split()
            columns.append(datetime[1])
            columns.append(datetime[0])
            
            rows.append(columns)
        return rows 
        
    
accounts = Users(r"src\database\log.db")
logs = Logs(r"src\database\log.db")
printer_models = PrinterModels(r"src\database\log.db")
printers = Printers(r"src\database\log.db")
filaments = Filaments(r"src\database\log.db")
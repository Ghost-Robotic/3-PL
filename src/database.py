import sqlite3 as sql
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

database = resource_path(r"database/log.db")
    
class Users():
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA foreign_keys = ON')
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
        
    def create_user(self, user_id, f_name, l_name, password, salt, access_level=1, group_id=None):
        self.cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?)', (user_id, password, salt, f_name, l_name, access_level, group_id))
        
    def change_password(self, id, password, salt):
        self.cursor.execute('UPDATE users SET password=?, salt=? WHERE user_id=?', (password,salt,id))
        
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
        return row[0].title(), row[1].title() # fname,lname
    
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
    
    def fetch_all_id(self):
        id = []
        for row in self.cursor.execute('SELECT user_id FROM users'):
            id.append(row[0])
        return id
    
    def fetch_all_accounts(self):
        account = []
        for row in self.cursor.execute('SELECT user_id, f_name, l_name FROM users'):
            account.append([row[0],f"{row[1].title()} {row[2].title()}"])
        return account
    
    def edit_user(self, user_id, f_name, l_name, access_level):
        self.cursor.execute('UPDATE users SET f_name=?, l_name=?, access_level=? WHERE user_id=?', (f_name,l_name,access_level,user_id))
        
class Groups():
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA foreign_keys = ON')
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
        self.connection.execute('PRAGMA foreign_keys = ON')
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
    
    def fetch_all_names(self):
        rows = []
        for row in self.cursor.execute('SELECT model_name FROM printer_models'):
            rows.append(row[0].lower())
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
    
    def edit_model(self):
        pass
    

class Printers:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA foreign_keys = ON')
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
        self.connection.execute('PRAGMA foreign_keys = ON')
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
    
    def edit_filament(self):
        pass

class Logs:
    def __init__(self, database):
        self.connection =sql.connect(database, autocommit=True)
        self.connection.execute('PRAGMA foreign_keys = ON')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            print_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user TEXT,
            print_name TEXT,
            gcode TEXT,
            duration INTEGER,
            model_weight INTEGER,
            date_time TEXT,
            id_model INTEGER,
            id_filament INTEGER,
            approval BOOLEAN,
            approver_id INTEGER,
            successful BOOLEAN,
            
            FOREIGN KEY (id_user)
                REFERENCES users (user_id),
                
            FOREIGN KEY (id_model)
                REFERENCES printer_models (model_id),
                
            FOREIGN KEY (id_filament)
                REFERENCES filaments (filament_id),
                
            FOREIGN KEY (approver_id)
                REFERENCES users (user_id)
            )''') 
        
    def view_table(self):
        """prints entire table
        """
        for row in self.cursor.execute('SELECT * FROM logs'):
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
        for row in self.cursor.execute("""SELECT l.print_id, u.f_name, u.l_name, l.print_name, l.duration, l.model_weight, pm.brand, pm.model_name, f.material, l.date_time 
                                       FROM logs AS l
                                       JOIN users AS u ON l.id_user = u.user_id
                                       JOIN printer_models AS pm ON l.id_model = pm.model_id
                                       JOIN filaments AS f ON l.id_filament = f.filament_id"""):
            columns = []
            columns.append(str(row[0]))
            
            fname = str(row[1])
            lname = str(row[2])
            
            name = f"{fname} {lname}"
            columns.append(name.title())
            
            columns.append(row[3])

            hours = row[4]//60
            mins = row[4]%60
            columns.append(str(hours)+"hrs "+str(mins)+"mins")

            columns.append(row[5])
            
            columns.append(f"{str(row[6])} {str(row[7])}")
            columns.append(str(row[8]))
            
            datetime = row[9].split()
            columns.append(datetime[1])
            columns.append(datetime[0])
            
            rows.append(columns)
        return rows 
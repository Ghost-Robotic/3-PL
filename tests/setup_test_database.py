import sys
sys.path.append("../3_PL")
from src.database import Users, Logs, PrinterModels, Printers, Filaments
import random
import src.helpers.hash_utils as hsh

accounts = Users(r"src\database\log.db")
logs = Logs(r"src\database\log.db")
printer_models = PrinterModels(r"src\database\log.db")
printers = Printers(r"src\database\log.db")
filaments = Filaments(r"src\database\log.db")

# accounts
salt = hsh.generate_salt()
accounts.create_user(user_id=123456, password=hsh.hash("admin", salt), salt=salt,f_name="john", l_name="doe", access_level=5)
accounts.create_user(user_id=654321, password=hsh.hash("password", salt), salt=salt,f_name="bob", l_name="builder", access_level=1)
accounts.view_table()

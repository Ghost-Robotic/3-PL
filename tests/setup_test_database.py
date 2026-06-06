from operator import mul
import sys
sys.path.append("../3_PL")
from src.database import Users, Logs, PrinterModels, Printers, Filaments
import random
import src.helpers.hash_utils as hsh

accounts = Users(r"database\log.db")
logs = Logs(r"database\log.db")
printer_models = PrinterModels(r"database\log.db")
printers = Printers(r"database\log.db")
filaments = Filaments(r"database\log.db")

# setup sample database
salt = hsh.generate_salt()
accounts.create_user(user_id=123456, password=hsh.hash("admin", salt), salt=salt,f_name="john", l_name="doe", access_level=5)
accounts.create_user(user_id=654321, password=hsh.hash("password", salt), salt=salt,f_name="bob", l_name="builder", access_level=1)
accounts.create_user(user_id=987654, password=hsh.hash("123456", salt), salt=salt,f_name="thomas", l_name="smith", access_level=4)
accounts.view_table()

filament_types = ["PLA", "PETG", "ABS", "ASA", "TPU-95A","TPU-90A","TPU-85A", "PCCF", "PC", "PEEK", "PLA-CF", "PETG-CF", "PCTG", "ABS-CF", "PPS-CF", "PPA-CF", "PET-CF", "Nylon", "Nylon-GF", "PETG-GF","PC-GF","ABS-GF", "HTPLA","PLA Silk", "Brass filled HTPLA", "Iron filled PLA", "Bronze filled PLA", "Static Dissipative PLA", "Matte PLA", "PLA+", "Matte PETG","PA12CF","PA6CF","Wood PLA", "Marble PLA"]

for i in filament_types:
    filaments.add_filament(material=i)
filaments.view_table()

printer_types = [("CORE One L","Prusa",False),("CORE One","Prusa",False),("XL 5 Tool","Prusa",True),("HT90","Prusa",False),("H2D","Bambu Lab",True),("P1S","Bambu Lab",False),("U1","Snapmaker",True),("Omni TECH+","Omni3D",False),("FUSE 1+","formlabs",False),("Form 4L","formlabs",False)]

for i in printer_types:
    printer_models.add_printer_model(model_name=i[0],brand=i[1],multimaterial=i[2])
printer_models.view_table()
import sys
sys.path.append("../3_PL")
from src.app import App

# test login page, currently redundant as it performs the same func as main.py

app = App()

app.start()
app.display_page(list(app.frames)[0])
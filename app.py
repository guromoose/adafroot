from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Potlog

# Kobler til / lager en session til db
engine = create_engine("mysql://root:toor@localhost/tmp_db", echo=True)
Session =  sessionmaker(bind=engine)

# Initialiserer flasken
app = Flask(__name__)

# setter opp ruten til flasken
@app.route('/')
def index():
	# setter session her nede for å refreshe riktig
	session = Session()
	# Henter data fra bordet 'potlog' fra databasen
	potdata = session.query(Potlog).all() 
	
	return render_template('index.html', potdata=potdata)

# Vrooom!
app.run(debug=True)
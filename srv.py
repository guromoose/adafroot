from flask import Flask, render_template
from sqq import Potlog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

engine = create_engine("mysql://root:toor@localhost/tmp_db", echo=True)
Session =  sessionmaker(bind=engine)

app = Flask(__name__)

@app.route('/')
def index():
	session = Session()
	potdata = session.query(Potlog).all() 
	
	return render_template('index.html', potdata=potdata)

app.run(debug=True)
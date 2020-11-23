"""
Kommuniserer med db, adafruit, og arduino
"""

import time
import datetime
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Potlog

# Kobler til / lager en session til db
engine = create_engine("mysql://root:toor@localhost/tmp_db")
Session =  sessionmaker(bind=engine)
session = Session()

# Adafruit konto-info og init
ADAFRUIT_IO_USERNAME = "hankeson"
ADAFRUIT_IO_KEY = "aio_regS57Cc7c8atquEXUzGvKjSCHGE"
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Kobler til arduino med pyfirmata
board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()
# Finner pins til arduino
digital_output = board.get_pin('d:10:o') # led pin
analog_input = board.get_pin('a:0:o') # pot pin

# Funksjon som initialiserer mater fra adafruit
def initfeeds(feedname):
	try:
		feede = aio.feeds(feedname)
		return feede
	except RequestError:
		feed = Feed(name=feedname)
		feede = aio.create_feed(feed)
		return feede

digital = initfeeds('digital')
initfeeds('analog')
initfeeds('counter')

last_potval = 0
run_count = 0

while True:
	# Sender counter verdi til feed 'counter'
	print('Run Count:', run_count)
	aio.send_data('counter', run_count)
	run_count += 1

	# leser og runder av potmeter verdien og legger den 
	# inn i databasen om den ikke er det samme som forige verdi
	potval = round(analog_input.read(), 2)
	if potval != last_potval:
		print(potval)
		aio.send_data('analog', potval)
		
		potentry = Potlog(
			value=str(potval),
			time=datetime.datetime.now()
		)
		session.add(potentry)
		session.commit()
		time.sleep(5)
	else:
		time.sleep(1)
	last_potval = potval

	# Får dataen (On eller Off) fra adafruit
	data = aio.receive(digital.key)
	print('Data: ', data.value)
	# Setter LED til arduino
	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

import time
import datetime
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqq import Potlog

engine = create_engine("mysql://root:toor@localhost/tmp_db")
Session =  sessionmaker(bind=engine)
session = Session()

ADAFRUIT_IO_USERNAME = "hankeson"
ADAFRUIT_IO_KEY = "aio_ZMDi59gL4CGqneSYvykZIzDJCkEO"

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

digital_output = board.get_pin('d:10:o')
analog_input = board.get_pin('a:0:o')

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
	print('Sending count:', run_count)
	aio.send_data('counter', run_count)
	run_count += 1

	data = aio.receive(digital.key)
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

	print('Data: ', data.value)

	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)

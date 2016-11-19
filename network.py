
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from datetime import datetime, date, time
import threading
import json
import serial
cron="0"
text = ""
URL = 'https://5da31d11.ngrok.io'
GPGLL=""
def parseUart(data):
        print(data)
	try:
		dataArray = data.split(',')
		print(dataArray[1]+' '+dataArray[3])
		latitude=dataArray[1].split('.')
		logitude=dataArray[3].split('.')
		print(requests.post(URL + '/api/ward/geo', {"latitude": latitude[0]+','+latitude[1], "longitude": logitude[0]+','+logitude[1], "timestamp": datetime.now(), "isAlert": True}))
	except:
		print('eroor')
		print(requests.post(URL + '/api/ward/geo', {"latitude": 60000.462960, "longistude": 03022.40263, "timestamp": 45435, "isAlert": True}))



def timer2():
	with serial.Serial('/dev/ttyS0', 9600, timeout=0.05) as ser:
		data = ser.readline()
		if data!='':
			if data[2]=='P':
				if data[5]=='L':
					global GPGLL
					GPGLL=data
        t = threading.Timer(0.05, timer2)
        t.start()
timer2()


def tick():
        subprocess.Popen(["espeak", "-v", "en","-s", "100",'hel' + text])
	print('( .Y. )')



def timer1():
	response = requests.get(URL + '/api/schedule/event')
	#print(response.content)
	parsed_string = json.loads(response.content)
	ID_NUM=1
	print(parsed_string[ID_NUM]["cron"])
	global cron
	global text
	text=parsed_string[ID_NUM]["message"]
	cron=parsed_string[ID_NUM]["cron"]
	if cron == '1 4 8 8 * *': 
		tick()
	print(cron)
	#print(datetime.now())

	
	
	parseUart(GPGLL)

	#print(requests.post(URL + '/api/ward/geo', {"latitude": 3, "longistude": 5, "timestamp": 45435, "isAlert": True}))
	t = threading.Timer(10.0, timer1)
	t.start()
timer1()


#ser.write(data)
#ser.close()

scheduler = BlockingScheduler()
scheduler.add_executor('processpool')
arrayCron=cron.split(' ')
print(arrayCron)
if cron != '1 4 8 8 * *':
	print('cron is correct')
	scheduler.add_job(tick, 'cron', second=arrayCron[0], minute=arrayCron[1],hour=arrayCron[2], day=arrayCron[3],day_of_week=arrayCron[4],month=arrayCron[5])
scheduler.start()


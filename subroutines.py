import traceback, time, datetime
from user_agents import parse
import json,re, requests

def getCurrentTime():
	currTime=datetime.datetime.now()
	currTime=str(currTime)
	return currTime

def user_log(db,mongo_db,session_st_end,username,ip,userAgent,sessionType,geo,referer):
	try:
		user_agent=parse(userAgent)
		browser = str(user_agent.browser.family)+', version: '+user_agent.browser.version_string
		os = str(user_agent.os.family)+', version: '+user_agent.os.version_string
		device = str(user_agent.device.family)
	except Exception, e:
		browser = ""
		os = ""
		device = ""

	currTime=getCurrentTime()
	if session_st_end=="session_start":
		gps_url= 'http://maps.google.com/maps/api/geocode/json?latlng='+geo.strip('()')+'&sensor=false'
		resp = requests.get(gps_url)
		response = str(resp.text).replace('\n','')
		resTxt=json.loads(response)
		addr=str(resTxt['results'][0]['formatted_address'])
		addrList=addr.split(',')
		country=(addrList[len(addrList)-1]).strip()
		city= (addrList[len(addrList)-3]).strip()
		state= (addrList[len(addrList)-2]).strip()
		pin=re.findall('\d+', state)
		state=state[:state.find(pin[0])].strip()
		

		ins_val={
					'referer':referer,
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					session_st_end:currTime,
					'date':str(time.strftime('%Y-%m-%d')),
					'time':str(time.strftime('%H:%M:%S')),
					'session_type':sessionType,
					'geolocation':geo,
					"country":country,
					"city":city,
					"state":state,
					"device_type":device,
					"os":os,
					"browser":browser
				}
		db.insert_db(mongo_db,"user_activity",ins_val)

	else:
		ins_val={
					session_st_end:currTime,
					'date':str(time.strftime('%Y-%m-%d')),
					'time':str(time.strftime('%H:%M:%S'))					
				}
		query = {
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					'geolocation':geo,
					'referer':referer
				}
		db.update_db(mongo_db,"user_activity",ins_val,query)
	
	return "200"


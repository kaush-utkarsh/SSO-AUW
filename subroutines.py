import traceback, time, datetime

def getCurrentTime():
	currTime=datetime.datetime.now()
	currTime=str(currTime)
	return currTime

def user_log(db,mongo_db,session_st_end,username,ip,userAgent,sessionType,geo):

	currTime=getCurrentTime()
	if session_st_end=="session_start":
		ins_val={
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					session_st_end:currTime,
					'session_type':sessionType,
					'geolocation':geo
				}
		db.insert_db(mongo_db,"user_activity",ins_val)

	else:
		ins_val={
					session_st_end:currTime
				}
		query = {
					'username':username,
					'ipAdd':ip,
					'user_agent':userAgent,
					'geolocation':geo
				}
		db.update_db(mongo_db,"user_activity",ins_val,query)
	
	return "200"


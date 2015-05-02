########################################################################################
#########	 Schema Definition for the mongo database to be used for SSO     ###########
########################################################################################

auw_schema={
			"user_data":{
							"id":"",
							"name":"",
							"username":"",
							"password":"",
							"email":"",
							"phone":"",
							"native_country":"",
							"native_city":"",
							"current_country":"",
							"current_city":"",
							"profession":"",
							"interests":"",
							"active_status":"",
							"signup_type":"",
							"fb_id":"",
							"twt_id":"",
							"lnkd_id":"",
							"google_id":"",
							"timestamp":""
			},
			"admin_user":{
							"id":"",
							"name":"",
							"username":"",
							"password":"",
							"email":"",
							"phone":"",
							"native_country":"",
							"native_city":"",
							"current_country":"",
							"current_city":"",
							"profession":"",
							"interests":"",
							"active_status":"",
							"signup_type":"",
							"fb_id":"",
							"twt_id":"",
							"lnkd_id":"",
							"google_id":"",
							"timestamp":""
			},
			"countries":{
							"country_iso":"",
							"country_name":"",
							"country_other_name":""
			},
			"cities":{
							"city_iso":"",
							"city_name":"",
							"city_other_name":"",
							"country_iso":""
			},
			"signup_types":{
							"type_code":"",
							"type_name":""
			},
			"user_activity":{
							"username":"",
							"ipAdd":"",
							"session_start":"",
							"session_end":"",
							"session_type":"",
							"geolocation":"",
							"country":"",
							"city":"",
							"state":"",
							"user_agent":"",
							"device_type":"",
							"os":"",
							"browser":"",
							"referer":""
			},			
			"entity_brief":{
							"entity_id":"",
							"entity_type":"",
							"entity_name":""
			},			
			"device_log":{
							"device":"",
							"browser":"",
							"os":"",
							"date":"",
							"count":""
			},			
			"city_counters":{
							"city":"",
							"state":"",
							"country":"",
							"date":"",
							"morning":"",	# 00:00-10:00
							"office":"",	# 10:00-19:00
							"evening":"",	# 19:00-23:59
							"total":""					
			},			
			"date_day_split":{
							"date":"",
							"02AM":"",	# 00:00 - 02:00
							"04AM":"",	# 02:00 - 04:00
							"06AM":"",	# 04:00 - 06:00
							"08AM":"",	# 06:00 - 08:00
							"10AM":"",	# 08:00 - 10:00
							"12AM":"",	# 10:00 - 12:00
							"14AM":"",	# 12:00 - 14:00
							"16AM":"",	# 14:00 - 16:00
							"18AM":"",	# 16:00 - 18:00
							"20AM":"",	# 18:00 - 20:00
							"22AM":"",	# 20:00 - 22:00
							"24AM":"",	# 22:00 - 24:00
							"total":""
			}
}
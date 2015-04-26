from pymongo import MongoClient
import os, traceback, datetime, re
import mongo_schema

# include the db schema so as to use throughout the db updates
auw_schema=mongo_schema.auw_schema 

class dbHandler:
	def dbConn(self,hst,prt,poolSize,queueMultiple,queueTimeOut,dtbs):
		try:
			client = MongoClient()
			db = client.get_database(dtbs)
			return db
		except Exception,e:
			print traceback.format_exc()

	def select_db(self,db,coll,query):
		try:
			collection = db.get_collection(coll)
			rows=collection.find(query)
			data=[]
			for row in rows:
				datum={}
				for r in row.keys():
					datum[r]=row[r]
				data.append(datum)
			return data
		except Exception,e:
			print traceback.format_exc()
			data=[]
			return data

	def update_db(self,db,coll,set_update,query):
		try:
			collection = db.get_collection(coll)
			db.collection.update(query,set_update,False )
		except Exception,e:
			print traceback.format_exc()

	def insert_db(self,db,coll,ins_values):
		try:
			collection = db.get_collection(coll)
			curr=auw_schema[coll]
			row={}
			for c in curr.keys():
				if c  in ins_values.keys():
					row[c]=ins_values[c]
				else:
					row[c]=curr[c]
			collection.insert(row)
		except Exception,e:
			print traceback.format_exc()

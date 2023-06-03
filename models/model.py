from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as db
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import math

class MainModel():
    #mysql+pymysql://cameras:[@980AC].z.*@50.123.16.124/portal
	#mysql+pymysql://root:0n3sh0t3@localhost/portal
	engine = db.create_engine('mysql+pymysql://cameras:[@980AC].z.*@50.123.16.124/camserver')
	connection = engine.connect()
	metadata = db.MetaData()
	#Declare all the tables here
	cameras = db.Table('cameras', metadata, autoload=True, autoload_with=engine)
	#GlobalSettings = db.Table('settings_global', metadata, autoload=True, autoload_with=engine)

	def statuses():
		return ["Pending","Active","On Hold","Closed","Approved","Denied"]

	def Paginate(perpage,qry):
		ResultProxy = MainModel.connection.execute(qry)
		ResultSet = ResultProxy.fetchall()
		total = len(ResultSet)
		return math.ceil(int(total)/int(perpage))

	def Getuser(uid):
		#Equivalent to 'SELECT * FROM profile'
		query = db.select([MainModel.profile]).where(MainModel.profile.c.id == uid)
		ResultProxy = MainModel.connection.execute(query)
		ResultSet = ResultProxy.fetchall()
		#print(ResultSet)
		return ResultSet

	def GetUserLogin(email):
		query = db.select([MainModel.profile]).where(MainModel.profile.c.email == email)
		ResultProxy = MainModel.connection.execute(query)
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet

	def GetUsers(limit = 5):
		query = db.select([MainModel.profile]).order_by("id ASC")
		query.limit(limit)
		ResultProxy = MainModel.connection.execute(query)
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet

	def GetUsersByDepartment(did):
		ResultProxy = MainModel.connection.execute("SELECT firstname,lastname,email FROM profile WHERE deptid = '"+did+"'")
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		return ResultSet

	def GetDepartmentDropdown():
		ResultProxy = MainModel.connection.execute("SELECT id,title FROM departments")
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		return ResultSet

	def GetWorkOrderDropDown():
		ResultProxy = MainModel.connection.execute("SELECT id,subject FROM requests WHERE type = 1")
		ResultSet = ResultProxy.fetchall()
		#print(ResultSet)
		if len(ResultSet) <= 0:
			return None
		return ResultSet

	def GetUserDropdown():
		ResultProxy = MainModel.connection.execute("SELECT id,firstname,lastname FROM profile")
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		return ResultSet

	def GetVendorDropDown():
		ResultProxy = MainModel.connection.execute("SELECT id,name FROM vendors")
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		return ResultSet

	def DeleteRecord(table,id):
		s = True
		try:
			if table == "logs":
				MainModel.connection.execute("DELETE FROM "+table+" WHERE task_log_id = "+str(id))
			else:
				MainModel.connection.execute("DELETE FROM "+table+" WHERE id = "+str(id))
		except Exception as e:
			print(e)
			s=False
		return s

	# Utility function
	def convertHtmlToPdf(sourceHtml, outputFilename):
		#from xhtml2pdf import pisa    
		f = open("templates/requests/pdf.html", "r")
		temp = f.read

		print(f.read())
		# convert HTML to PDF
		#pisaStatus = pisa.CreatePDF(
		#		sourceHtml,                # the HTML to convert
		#		dest=resultFile)           # file handle to recieve result

		# close output file
		#resultFile.close()                 # close output file

		# return True on success and False on errors
		return true  #pisaStatus.err

	def PrintRequest(data):   
		f = open("templates/requests/pdf.html", "r")
		temp = f.readlines()
		temp = str(temp)
		statuses = MainModel.statuses()
		temp = temp.replace("RID", str(data.id))
		temp = temp.replace("CREATED_AT", str(data.created_at))
		temp = temp.replace("SUBJECT", data.subject)
		temp = temp.replace("CREATED_BY", data.firstname + " "+ data.lastname)
		temp = temp.replace("STATUS", statuses[data.status])
		temp = temp.replace("MESSAGE", data.message)
		temp = temp.replace("['", "")
		temp = temp.replace("']", "")
		#print(str(temp))
		return temp  #pisaStatus.err
		
	def Cleaninput(data):
		output = data.replace("'","\\'")
		output = output.replace('\"','\\"')
		output = output.replace('^',' ')
		output = output.replace('&','amp;')
		output = output.replace('^',' ')
		#print("***************CLEANUP OUTPUT***************")
		#print(output)
		return output

def FTP_Request(address,un,pw,path):
	import ftplib
	ftp = ftplib.FTP(address)
	ftp.login(un, pw)
	ftp.cwd(path)
	data = []
	ftp.dir(data.append)
	ftp.quit()
	return data
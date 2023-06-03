from models import model
from datetime import datetime

class Surveillance(model.MainModel):
	def List(p=0,perpage=10,type=1):
		ResultProxy = Surveillance.connection.execute("SELECT * FROM cameras LIMIT "+str(p)+","+str(perpage))
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet

	def Filter(p,perpage,id,fltr):
		if fltr == "status":
			ResultProxy = Surveillance.connection.execute("SELECT surveillance.*, profile.firstname, profile.lastname, departments.title FROM surveillance LEFT JOIN profile ON surveillance.task_log_creator=profile.id LEFT JOIN departments ON surveillance.task_log_department=departments.id WHERE (surveillance.task_log_status = '"+id+"') ORDER BY surveillance.task_log_date DESC LIMIT "+str(p)+","+str(perpage))
		if fltr == "department":
			ResultProxy = Surveillance.connection.execute("SELECT surveillance.*, profile.firstname, profile.lastname, departments.title FROM surveillance LEFT JOIN profile ON surveillance.task_log_creator=profile.id LEFT JOIN departments ON surveillance.task_log_department=departments.id WHERE (surveillance.task_log_department = '"+id+"') ORDER BY surveillance.task_log_date DESC LIMIT "+str(p)+","+str(perpage))
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet		

	def Search(p,perpage=15,q=None):
		ResultProxy = Surveillance.connection.execute("SELECT surveillance.*, profile.firstname, profile.lastname, departments.title FROM surveillance LEFT JOIN profile ON surveillance.task_log_creator=profile.id LEFT JOIN departments ON surveillance.task_log_department=departments.id ORDER BY surveillance.task_log_date DESC LIMIT "+str(p)+","+str(perpage))
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet

	def Get(id):
		ResultProxy = Surveillance.connection.execute("SELECT * FROM surveillance WHERE task_log_id = "+str(id))
		ResultSet = ResultProxy.fetchall()
		if len(ResultSet) <= 0:
			return None
		#print(ResultSet)
		return ResultSet[0]
		
	def Update(data,SendMail=False):
		s = True
		print(data)
		try:
			Surveillance.connection.execute("UPDATE surveillance SET task_log_workorder = '"+data['task_log_workorder']+"'\
				, task_log_name = '"+model.MainModel.Cleaninput(data['task_log_name'])+"',\
				task_log_description = '"+model.MainModel.Cleaninput(data['task_log_description'])+"',\
				task_log_creator = '"+data['task_log_creator']+"',task_log_department = '"+data['task_log_department']+"',\
				task_log_status = '"+data['task_log_status']+"', task_log_hours = '"+data['task_log_hours']+"' WHERE task_log_id = "+str(data['id']))
		except Exception as e:
			print("**********ERROR:task log update **********")
			print(e)
			s=False
		return s
		
	def Insert(data,SendMail):
		s = True
		try:
			Surveillance.connection.execute("INSERT INTO surveillance(task_log_workorder,task_log_name ,task_log_description ,task_log_creator, task_log_date, task_log_department) \
			 values('"+data['task_log_workorder']+"', '"+model.MainModel.Cleaninput(data['task_log_name'])+"', '"+model.MainModel.Cleaninput(data['task_log_description'])+"', '"+data['task_log_creator']+"' \
				 , '"+datetime.today().strftime('%Y-%m-%d')+"', '"+data['task_log_department']+"')")
		except Exception as e:
			print("**********ERROR: task log insert**********")
			print(e)
			s=False
		return s



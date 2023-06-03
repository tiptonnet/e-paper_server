import mysql.connector
from mysql.connector import Error

def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host='50.123.16.124',
                                       database='camserver',
                                       user='cameras',
                                       password='[@980AC].z.*')
        if conn.is_connected():
            print('Connected to MySQL database')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            return conn



def GetData(qry):
	cnx = connect()
	cursor = cnx.cursor()
	query = (qry)
	cursor.execute(query)
	data = []
	for d in cursor:
		#print(d[10]+", "+d[9])
		data.append(d)
	cursor.close()
	cnx.close()
	return data

def InsertData(qry):
	pass

def UpdateDate(qry):
	pass

def DeleteData(qry):
	pass

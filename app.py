from flask import *
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_bootstrap import Bootstrap
#from flask_nav import Nav
#from flask_nav.elements import *
from dominate.tags import img

app = Flask(__name__)

@app.errorhandler(404) 
def invalid_route(e):
	return render_template(
		'404.html',
		username = session.get("name"),
		acl = 0,
		uid = 0
	)

# Defining our custom login required decorator
def RequireLogIn(function): 
	@wraps(function)
	def wrapper(*args, **kwargs):
		if not session.get('logged_in'):
			return render_template(
				'login.html',
				location = request.cookies.get('location')
			)
		return function(*args, **kwargs)
	return wrapper

def CalculatePagination(p,query,path,perpage):
	from models import model
	total_pages = model.MainModel.Paginate(perpage,query)
	total_pages = total_pages*perpage
	prev = p - perpage
	nxt = p + perpage
	if prev < 0:
		prev = 0
	if nxt >= total_pages:
		nxt = p
	i = 0
	prev_path = ""
	for PT in path:
		#print(i)
		if i > 0:
			if i == 2:
				prev_path = str(prev_path) + "/" + str(prev)
			else:
				prev_path = prev_path + "/" + PT
		i = i + 1
	#print(prev_path)
	next_path = ""
	i = 0
	for PT in path:
		if i > 0:
			if i == 2:
				next_path = str(next_path) + "/" + str(nxt)
			else:
				next_path = next_path + "/" + PT
		i = i + 1
	#print(next_path)	
	PageData =[prev_path,next_path]
	#print(PageData)
	return PageData

app = Flask(__name__)


@app.route('/<int:p>')
def index(p):
    #from models import surveillance
    #PageData = CalculatePagination(p,"SELECT * FROM cameras",request.path.split("/"),15)
    #data = surveillance.Surveillance.List(0,10,1)
    return render_template(
		'index.html'
	)

@app.route('/forward')
def forward():

    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
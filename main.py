from flask import *
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
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


app = Flask(__name__)


@app.route('/<int:p>')
def index(p):
    from models import surveillance
    PageData = CalculatePagination(p,"SELECT * FROM cameras",request.path.split("/"),15)
    data = surveillance.Surveillance.List(0,10,1)
    return render_template(
		'list.html',
		path=request.path.split("/"),
		p = p,

		prev_path = PageData[0], 
		next_path = PageData[1], 
		data = data  

	)

@app.route('/forward')
def forward():

    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
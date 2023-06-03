from flask import *
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_bootstrap import Bootstrap
#from flask_nav import Nav
#from flask_nav.elements import *
from dominate.tags import img
import xml.etree.ElementTree as ET

app = Flask(__name__)

def GetConfig():
  
    # create element tree object
    tree = ET.parse('static/config.xml')
    #print(tree)
    # get root element
    root = tree.getroot()
    #print(root)
    #print(root[0].tag)
    # create empty list for config items
    config = []
    for x in root[0]:
        config.append(x.text)
        #print(x.text)
    return config

config = GetConfig()
print(config)

@app.errorhandler(404) 
def invalid_route(e):
	return render_template(
		'404.html',
		username = session.get("name"),
		acl = 0,
		uid = 0
	)

app = Flask(__name__)

@app.route('/<int:p>')
def index(p):
    return render_template(
		'index.html'
	)

@app.route('/forward')
def forward():

    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
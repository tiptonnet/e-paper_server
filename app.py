from flask import *
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from PIL import Image
#import epd12in48b_V2
import time
#from html2image import Html2Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from PIL import Image
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
    config = GetConfig()
    return render_template(
		'index.html',
        config=config,
        local=p
	)

@app.route('/forward')
def forward():

    return "Hello"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
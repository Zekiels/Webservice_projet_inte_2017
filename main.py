from flask import Flask, request
from flask_cors import CORS, cross_origin
from pprint import pprint
import random 
import json

app = Flask(__name__)
app.debug = True
CORS(app)
identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']

@app.route("/", methods=["GET"])
def getDefault():
	global identifiant
	print identifiant
	return json.dumps(identifiant),200,{'Content-Type':'application/json'}

@app.route("/retour", methods=["GET"])
def getTest():
	global identifiant
	print identifiant
	return json.dumps(identifiant),200,{'Content-Type':'application/json'}


@app.route("/rdm", methods=["GET"])
def getRdm():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}

@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}


@app.route("/sales",methods=["POST"])
def postSales():
	global  postSales
	postSales = request.get_json()
	print postSales
	return json.dumps(postSales),200,{'Content-Type':'application/json'}

@app.route("/idPost",methods=["POST"])
def postId():
	global  identifiant
	tmp = request.get_json()
	#tmp = json.loads(tmp)
	identifiant.append(tmp)
	print identifiant
	return json.dumps(identifiant),200,{'Content-Type':'application/json'}

@app.route("/idGet",methods=["GET"])
def idGet():
	return "test"

if __name__ == "__main__":
	app.run()	

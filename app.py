from flask import Flask, request
from flask_cors import CORS, cross_origin
from pprint import pprint
import random 
import json
import os
from db import Db


app = Flask(__name__)
app.debug = True
CORS(app)

os.environ['DATABASE_URL'] = "postgres://tsnflmvlizgvjx:066dedf141326dcdc78db46c4d30036bb0405f74cd06d5880e8dfbf87add1176@ec2-107-22-250-33.compute-1.amazonaws.com:5432/dcj4s31ubdp85s"

identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']
 
weather = []
 
@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}

@app.route("/GET/metrology", methods=["GET"])
def getWeather():
	tmp={"weather":"sunny"}
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/map", methods=["GET"])
def getmap():
	#tmp={"map"{"region":"perpignan","ranking":["Kevin","adam"],"itemsByPlayer":{"kind":"shop","owner":"Jack336","location":coordinate{"latitude":0.6,"longitude":5.7},"influance":10.8},"PlayerInfo":{"jean"{"cash":3000.50,"sales":80,"profit":100.8,"drinksOffered":["name":"Mojito","price":5.80,"hasAlcohol":True,"isCold":True]}}}}
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/", methods=["GET"])
def getBD():
	db = Db()
	db.execute("""SELECT * FROM player, ingredient, recipe;""")
	tmp = db.cur.fetchall()
	db.close()
	return json.dumps(tmp),200,{'Content-Type':'application/json'}
 
 
@app.route("/sales",methods=["POST"])
def postSales():
 	global  postSales
 	postSales = request.get_json()
 	print postSales

 
@app.route("/idPost",methods=["POST"])
def postId():
 	global  identifiant
 	#tmp = request.get_json()
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	identifiant.append(tmp)
 	print identifiant
 	return json.dumps(identifiant),200,{'Content-Type':'application/json'}
 
@app.route("/idIsValide",methods=["POST"])
def postIdIsValide():
 	global  identifiant
 	idvalide= request.get_data()
 	idvalide = json.loads(tmp)
 	for x in identifiant:
 		if idvalide in identifiant:
 			return json.dumps(idvalide),200,{'Content-Type':'application/json'}
 		else :continue
 	
 	print identifiant
 
@app.route("/POST/meterology", methods=["POST"])
def postWheather():
 	global weather
 	tmp = request.get_data()
 	weather.append(tmp)
 	print weather
 	return json.dumps(weather),200,{'Content-Type':'application/json'}
 		
 
#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"
 
if __name__ == "__main__":
 	app.run() 
from flask import Flask, request
from flask_cors import CORS, cross_origin
from pprint import pprint
import random 
import json
import os
from db import Db

os.environ['DATABASE_URL'] = "postgres://tsnflmvlizgvjx:066dedf141326dcdc78db46c4d30036bb0405f74cd06d5880e8dfbf87add1176@ec2-107-22-250-33.compute-1.amazonaws.com:5432/dcj4s31ubdp85s"

app = Flask(__name__)
app.debug = True
CORS(app)

identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']

CurrentWeather = []
PrevisoinWeather = []

@app.route("/GET/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}





@app.route("/GET/metrology", methods=["GET"])
def getWeather():
	db = Db()
	db.execute("""SELECT map_time FROM map;""")
	tmp = db.cur.fetchall()
	db.close()
	json={"timestamp":1,"weather":"sunny", "test":{"key1":0.5,"key2":"[tao,toa,tia]"}}

	#Temps{ "timestamp":int, "weather":["dfn":int, "weather":"sunny"] }

	return tmp,200,{'Content-Type':'application/json'}


@app.route("/GET/map", methods=["GET"])
def getmap():
	#tmp={"map"{"region":"perpignan","ranking":["Kevin","adam"],"itemsByPlayer":{"kind":"shop","owner":"Jack336","location":coordinate{"latitude":0.6,"longitude":5.7},"influance":10.8},"PlayerInfo":{"jean"{"cash":3000.50,"sales":80,"profit":100.8,"drinksOffered":["name":"Mojito","price":5.80,"hasAlcohol":True,"isCold":True]}}}}
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

	


@app.route("/GET/ingredients", methods=["GET"])
def getIngredienst():
	# TODO


	return json.dumps(),200,{'Content-Type':'application/json'}

@app.route("/GET/map/<PlayerName>", methods=["GET"])
def getMapPlayer():
	# TODO

@app.route("/", methods=["GET"])
def getBD():
	db = Db()
	db.execute("""SELECT * FROM player, ingredient, recipe;""")
	tmp = db.cur.fetchall()
	db.close()
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

#################################                   POST   						 #######################################################
 
	return json.dumps(),200,{'Content-Type':'application/json'}

@app.route("/POST/quitter", methods=["POST"])
def postquitter():
	# TODO

	
	return json.dumps(),200,{'Content-Type':'application/json'}
 

@app.route("/POST/rejoindre", methods=["POST"])
def postRejoindre():
	# TODO

	
	return json.dumps(),200,{'Content-Type':'application/json'}
 
 
 
@app.route("/POST/sales",methods=["POST"])
def postSales():
 	global  postSales
 	postSales = request.get_json()
 	print(postSales)


 
@app.route("/POST/idPost",methods=["POST"])
def postId():
 	global  identifiant
 	#tmp = request.get_json()
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	identifiant.append(tmp)
 	print(identifiant)
 	return json.dumps(identifiant),200,{'Content-Type':'application/json'}
 
@app.route("/POST/idIsValide",methods=["POST"])
def postIdIsValide():
 	global  identifiant
 	idvalide= request.get_data()
 	idvalide = json.loads(tmp)
 	for x in identifiant:
 		if idvalide in identifiant:
 			return json.dumps(idvalide),200,{'Content-Type':'application/json'}
 		else :continue

 	print(identifiant)

@app.route("/POST/meterology", methods=["POST"])
def postWheather():
 	global weather
 	tmp = request.get_data()
 	weather.append(tmp)
 	print(weather)
 	return json.dumps(weather),200,{'Content-Type':'application/json'}

@app.route("/POST/actions/<PlayerName>", methods=["POST"])
def postAction():
	# TODO

	
	return json.dumps(),200,{'Content-Type':'application/json'}
 		
#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"

if __name__ == "__main__":
 	app.run()

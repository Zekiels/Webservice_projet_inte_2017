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

#variable de test
identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']

CurrentWeather = []
PrevisoinWeather = []

@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}


@app.route("/metrology", methods=["GET"])
def getWeather():
	db = Db()
	db.execute("""SELECT map_time FROM map;""")
	tmp = db.cur.fetchall()
	db.close()
	#json={"timestamp":1,"weather":"sunny", "test":{"key1":0.5,"key2":"[tao,toa,tia]"}}

	#Temps{ "timestamp":int, "weather":["dfn":int, "weather":"sunny"] }

	return json.dumps(tmp),200,{'Content-Type':'application/json'}


@app.route("/map", methods=["GET"])
def getmap():
	#tmp={"map"{"region":"perpignan","ranking":["Kevin","adam"],"itemsByPlayer":{"kind":"shop","owner":"Jack336","location":coordinate{"latitude":0.6,"longitude":5.7},"influance":10.8},"PlayerInfo":{"jean"{"cash":3000.50,"sales":80,"profit":100.8,"drinksOffered":["name":"Mojito","price":5.80,"hasAlcohol":True,"isCold":True]}}}}
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/ingredients", methods=["GET"])
def getIngredienst():
	db = Db()
	tmp = db.select("""SELECT * FROM ingredient;""")
	db.close()
	# {"ingredients":["name":string, "cost":float, "hasAlcohol":bool, "isCold":bool]}

	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/map/<PlayerName>", methods=["GET"])
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

@app.route("/quitter", methods=["POST"])
def postquitter():
	# TODO
	
	return json.dumps(),200,{'Content-Type':'application/json'}
 

@app.route("/rejoindre", methods=["POST"])
def postRejoindre():
	# Récupère le contenu de la requette
	rejoindre = request.get_json()

	#Vérifie si elle contient les infos nécésaire
	if "name" not in rejoindre or len(rejoindre["name"]) == 0:
    	return json_response({ "error" : "Missing name" }, 400)
	
	#Création d'un nouveau joueur
	db = Db()
	db.execute("""SELECT pre_value FROM preference WHERE pre_name = "budget";""")
	budget = db.cur.fetchall()

	db.execute("""
	INSERT INTO player VALUES (@(name), "", """+budget+""", 0);
	""", rejoindre)
	db.close()
	
	#{"name": string, "location":[latitude:float, longitude:float] ,"info":[cash:float, sales:int, profit:float, drinkOffered:[name:string, price:float, hasAlcohol:bool, isCold:bool]]}
	return json.dumps(),200,{'Content-Type':'application/json'}
 
 
 
@app.route("/sales",methods=["POST"])
def postSales():
 	global  postSales
 	postSales = request.get_json()
 	print(postSales)


 
@app.route("/idPost",methods=["POST"])
def postId():
 	global  identifiant
 	#tmp = request.get_json()
 	tmp = request.get_data()
 	tmp = json.loads(tmp)
 	identifiant.append(tmp)
 	print(identifiant)
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

 	print(identifiant)

@app.route("/meterology", methods=["POST"])
def postWheather():
 	global weather
 	tmp = request.get_data()
 	weather.append(tmp)
 	print(weather)
 	return json.dumps(weather),200,{'Content-Type':'application/json'}

@app.route("/actions/<PlayerName>", methods=["POST"])
def postAction():
	# TODO

	
	return json.dumps(),200,{'Content-Type':'application/json'}
 		
#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"

if __name__ == "__main__":
 	app.run()

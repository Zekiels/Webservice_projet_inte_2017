from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask import render_template
from pprint import pprint
import random
import json
from db import Db

#os.environ['DATABASE_URL'] = S3Connection(os.environ['DATABASE_URL'])

app = Flask(__name__, static_folder='HTML')
app.debug = True
CORS(app)

#variable de test
identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']

CurrentWeather = []
PrevisoinWeather = []
weather = []

@app.route('/HTML/jeu.html')
def jeu():
	return render_template('/HTML/jeu.html')

@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}


@app.route("/metrology", methods=["GET"])
def getWeather():
	db = Db()
	tmp = db.select("""SELECT map_time FROM map;""")
	db.close()
	#json={"timestamp":1,"weather":"sunny", "test":{"key1":0.5,"key2":"[tao,toa,tia]"}}

	#Temps{ "timestamp":int, "weather":["dfn":int, "weather":"sunny"] }

	return json.dumps(tmp),200,{'Content-Type':'application/json'}


@app.route("/ingredients", methods=["GET"])
def getIngredienst():
	db = Db()
	tmp = db.select("""SELECT * FROM ingredient;""")
	db.close()
	# {"ingredients":["name":string, "cost":float, "hasAlcohol":bool, "isCold":bool]}

	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/map", methods=["GET"])
def getMapPlayer():
	JSONitemsByPlayer=[]
	itemsByPlayer=[]
	playerInfo=[]
	db = Db()
	player = db.select("""SELECT pla_name from player;""")
	day = db.select("""SELECT map_day_nb from map;""")
	day_tmp = day.pop()
	print(day_tmp)
	for i in player:

		itemsByPlayer = (db.select("""
			SELECT mit_type, mit_pla_name, mit_longitude, mit_lattitude, mit_influence
			FROM map_item
			WHERE mit_pla_name = '{0}';
			""".format(i.get("pla_name"))))
		print (itemsByPlayer)

		#for element in itemsByPlayer:
			#JSONitemsByPlayer.append("""{{"kind":{0},"owner":{1},"location":{{"coordinates":{{"lattitude":{2},"longitude":{3}}}}}"influence":{4}}}""".format(element.get("mit_type"),element.get("mit_pla_name"),element.get("mit_lattitude"),element.get("mit_longitude"),element.get("mit_influence")))

		#budget
		playerInfo.append(db.select("""
			SELECT pla_cash
			FROM player
			WHERE pla_name = '{0}';
			""".format(i.get("pla_name"))))
		#qty vendu
		playerInfo.append(db.select("""
			SELECT SUM (sal_qty)
			FROM sale
			INNER JOIN player ON player.pla_name = sale.sal_pla_name
			WHERE sal_day_nb = {1}
			AND sal_pla_name = '{0}';
			""".format(i.get("pla_name"), day_tmp.get("map_day_nb"))))
		#profit
		playerInfo.append(db.select("""
			SELECT
				(SELECT SUM (sal_qty * sal_price)
				FROM sale
				INNER JOIN player ON player.pla_name = sale.sal_pla_name
				WHERE sal_day_nb = {1}
				AND sal_pla_name = '{0}'
				)
				-
				(SELECT SUM (pro_qty * pro_cost_at_that_time)
				FROM production
				INNER JOIN player ON player.pla_name = production.pro_pla_name
				WHERE pro_day_nb = {1}
				AND pro_pla_name = '{0}'
				);
			""".format(i.get("pla_name"), day_tmp.get("map_day_nb"))))
		#liste des types de boissons preparee
		playerInfo.append(db.select("""
			SELECT pro_rcp_name
			FROM production
			INNER JOIN player ON player.pla_name = production.pro_pla_name
			WHERE pro_day_nb = {1}
			AND pro_pla_name = '{0}';
		""".format(i.get("pla_name"), day_tmp.get("map_day_nb"))))

	db.close()
	json_retour = """
	{
		"region":{},
		"ranking":[
			{}
		],
		"itemsByPlayer":

	}"""
	print(playerInfo)
	return JSONitemsByPlayer,200,{'Content-Type':'application/json'}
	#tmp={"map"{"region":"perpignan","ranking":["Kevin","adam"],"itemsByPlayer":{"kind":"shop","owner":"Jack336","location":coordinate{"latitude":0.6,"longitude":5.7},"influance":10.8},"PlayerInfo":{"jean"{"cash":3000.50,"sales":80,"profit":100.8,"drinksOffered":["name":"Mojito","price":5.80,"hasAlcohol":True,"isCold":True]}}}}

@app.route("/", methods=["GET"])
def getBD():
	db = Db()
	tmp = db.select("""SELECT * FROM player;""")
	db.close()
	return json.dumps(tmp),200,{'Content-Type':'application/json'}

#################################                   POST   						 #######################################################

@app.route("/quitter", methods=["POST"])
def postquitter():
	# TODO

	return json.dumps(),200,{'Content-Type':'application/json'}


@app.route("/rejoindre", methods=["POST"])
def postRejoindre():
	# Recupere le contenu de la requette
	rejoindre = request.get_json()

	#Verifie si elle contient les infos necesaire
	if "name" not in rejoindre or len(rejoindre["name"]) == 0:
		return json_response({ "error" : "Missing name" }, 400)

	#Creation d'un nouveau joueur
	db = Db()
	budget = db.select("""SELECT pre_value FROM preference WHERE pre_name = "budget";""")

	db.execute("""
	INSERT INTO player VALUES (@(name), "", """+budget+""", 0);
	""", rejoindre)
	db.close()

	#{"name": string, "location":[latitude:float, longitude:float] ,"info":[cash:float, sales:int, profit:float, drinkOffered:[name:string, price:float, hasAlcohol:bool, isCold:bool]]}
	return json.dumps(),200,{'Content-Type':'application/json'}



@app.route("/sales",methods=["POST"])
def postSales():
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
 		else :
 			continue

 	print(identifiant)

@app.route("/metrology", methods=["POST"])
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

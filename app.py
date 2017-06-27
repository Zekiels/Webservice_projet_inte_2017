from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask import render_template
from pprint import pprint
import random
import json
from db import Db

#os.environ['DATABASE_URL'] = S3Connection(os.environ['DATABASE_URL'])

app = Flask(__name__, static_folder='static')
app.debug = True
CORS(app)

#variable de test
identifiant=['adrien']
postSales=[]
nombre = ['toto','tata','titi']

CurrentWeather = []
PrevisoinWeather = []
weather = {"timestamp":20,"weather":[{"dfn":0,"weather":"cloudy"},{"dfn":1,"weather":"sunny"}]}

def json_response(data="OK", status=200):
  return json.dumps(data), status, { "Content-Type": "application/json" }

@app.route('/jeu.html')
def jeu():
	return render_template('jeu.html')

@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}


@app.route("/metrology", methods=["GET"])
def getWeather():
	#db = Db()
	#tmp = db.select("""SELECT map_time FROM map;""")
	#db.close()
	#json={"timestamp":1,"weather":"sunny", "test":{"key1":0.5,"key2":"[tao,toa,tia]"}}

	#Temps{ "timestamp":int, "weather":["dfn":int, "weather":"sunny"] }

	return json.dumps(weather),200,{'Content-Type':'application/json'}


@app.route("/ingredients", methods=["GET"])
def getIngredienst():
	db = Db()
	tmp = db.select("""SELECT * FROM ingredient;""")
	db.close()
	# {"ingredients":["ing_name":string, "ing_current_cost":float, "ing_hasAlcohol":bool, "ing_isCold":bool]}

	return json.dumps(tmp),200,{'Content-Type':'application/json'}

@app.route("/map", methods=["GET"])
def getMapPlayer():
	Map = {}
	JSONitemsByPlayer=[]
	itemsByPlayer={}
	playerInfo=[]
	
	db = Db()
	region_tmp = db.select("""SELECT map_longitude, map_lattitude, map_longitude_span, map_lattitude_span from map where map_id = 0;""")
	region = region_tmp[0]

	Map.update({"region":{"center":{"latitude":region.get("map_lattitude"), "longitude":region.get("map_longitude")}, "span":{"latitudeSpan":region.get("map_lattitude_span"), "longitudeSpan":region.get("map_longitude_span")}}})
	print(Map)

	playerCash_tmp = db.select("""SELECT pla_name, pla_cash from player order by pla_cash DESC;""")
	playerCash = playerCash_tmp[0]
	print(playerCash)
	Map.update({"ranking":{}})
	for element in playerCash:
		Map["ranking"] = {element.get("pla_name"):playerCash.index(element)}
	print(Map)
	player = db.select("""SELECT pla_name from player;""")
	day = db.select("""SELECT map_day_nb from map;""")
	day_tmp = day[0]

	for i in player:

		itemsByPlayer.append(db.select("""
			SELECT mit_type, mit_pla_name, mit_longitude, mit_lattitude, mit_influence
			FROM map_item
			WHERE mit_pla_name = '{0}';
			""".format(i.get("pla_name"))))

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
		profit
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

	for element in itemsByPlayer:
			print(element)
			#JSONitemsByPlayer.append("""{{"kind":{0},"owner":{1},"location":{{"coordinates":{{"lattitude":{2},"longitude":{3}}}}}"influence":{4}}}""".format(element["mit_type"],element.get("mit_pla_name"),element.get("mit_lattitude"),element.get("mit_longitude"),element.get("mit_influence")))

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
	return json.dumps("ok"),200,{'Content-Type':'application/json'}
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
 	sales = request.get_json()
 	print(sales)

	if "quantity" not in sales :
		return json_response({ "error" : "Missing quantity" }, 400)
	if "player" not in sales :
		return json_response({ "error" : "Missing player" }, 400)
	if "item" not in sales :
		return json_response({ "error" : "Missing item" }, 400)


	db = Db()
	day = db.select("""SELECT map_day_nb from map;""")
	day_tmp = day.pop()
 	db.execute("""
 		INSERT INTO sale VALUES ({0}, @(quantity), 0, @(player), @(item));
 	""".format(day_tmp.get("map_day_nb")), sales)
 	db.close()

 	return json.dumps("ok"),200,{'Content-Type':'application/json'}


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
  	weather = tmp
	print(weather)
	#weather = request.get_json()
	#print(weather)

	#if "timestamp" not in weather or len(weather["timestamp"]) == 0:
		#return json_response({ "error" : "Missing timestamp" }, 400)
	#if weather["weather"]["dfn"] not in weather:
		#return json_response({ "error" : "Missing dfn"}, 400)
	#if weather["weather"]["weather"] not in weather:
		#return json_response({ "error" : "Missing weather"}, 400)

	#if weather["weather"]["dfn"] == 0:
		#currentWeather = weather["weather"]["weather"]
	#if weather["weather"]["dfn"] == 1:
		#previsionWeather = weather["weather"]["weather"]

	#db = Db()
	#db.execute("""
		#UPDATE map
		##SET map_time = @(timestamp)
		#SET map_prevision_weather = previsionWeather
		#SET map_current_weather = currentWeather
		#WHERE map_id = 0;
#""")
	#db.close()
 	return json.dumps("ok"),200,{'Content-Type':'application/json'}

@app.route("/actions/<PlayerName>", methods=["POST"])
def postAction(PlayerName):
	actions = request.get_json()
 	print(actions.items())
 	print(actions.values())
 	print(actions["actions"]["prepare"].values())

	if "actions" not in actions or len(actions["actions"]) == 0:
		return json_response({ "error" : "Missing player" }, 400)
	if actions["actions"]["kind"] == "drinks":
		db = Db()
		day = db.select("""SELECT map_day_nb from map;""")
		day_tmp = day.pop()

		db.execute("""
	    INSERT INTO production VALUES ({0}, {1}, {2}, {3}, {4});
	 	""".format(day_tmp.get("map_day_nb")), actions["actions"]["prepare"].values(), actions["actions"]["price"].values(), PlayerName, actions["actions"]["prepare"].items())
		db.close()

		return json.dumps("ok"),200,{'Content-Type':'application/json'}
	if actions["actions"]["kind"] == "recipe":
		print("NON")
	if actions["actions"]["kind"] == "ad":
		print("NON")




	return json.dumps("ok"),200,{'Content-Type':'application/json'}

#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"

if __name__ == "__main__":
 	app.run()

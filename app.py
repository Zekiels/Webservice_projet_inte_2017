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
dicoAction = {}

def json_response(data="OK", status=200):
  return json.dumps(data), status, { "Content-Type": "application/json" }

@app.route('/jeu.html')
def jeu():
	return render_template('jeu.html')

@app.route('/connexion.html')
def connect():
	return render_template('connexion.html')

@app.route("/reset", methods=["GET"])
def getReset():
	global nombre
	temp = random.choice(nombre)
	return json.dumps(temp),200,{'Content-Type':'application/json'}


@app.route("/metrology", methods=["GET"])
def getWeather():
	db = Db()
	tmp = db.select("""SELECT map_time, map_current_weather, map_prevision_weather FROM map;""")
	db.close()
	weather = {"timestamp":tmp[0]["map_time"],"weather":[{"dfn":0,"weather":tmp[0]["map_current_weather"]},{"dfn":1,"weather":tmp[0]["map_prevision_weather"]}]}

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
	Ranking = []
	itemsByPlayer = []
	playerInfo = {}
	listItems = []
	realItemsByPlayer = {}

	db = Db()
	region_tmp = db.select("""SELECT map_longitude, map_lattitude, map_longitude_span, map_lattitude_span from map where map_id = 0;""")
	region = region_tmp[0]

	Map.update({"region":{"center":{"latitude":region.get("map_lattitude"), "longitude":region.get("map_longitude")}, "span":{"latitudeSpan":region.get("map_lattitude_span"), "longitudeSpan":region.get("map_longitude_span")}}})

	playerCash = db.select("""SELECT pla_name, pla_cash from player order by pla_cash DESC;""")

	Map.update({"ranking":{}})
	for element in playerCash:
		Ranking.append(element.get("pla_name"))
	Map.update({"ranking":Ranking})

	player = db.select("""SELECT pla_name from player;""")
	day = db.select("""SELECT map_day_nb from map;""")
	day_tmp = day[0]


	#itemsByPlayer
	for i in player:
		row = None
		db.select("""
			SELECT mit_type, mit_pla_name, mit_longitude, mit_lattitude, mit_influence
			FROM map_item
			WHERE mit_pla_name = '{0}';
			""".format(i.get("pla_name")))

		row = db.fetchone()
		print(row)

		listItems = {"kind":row.get("mit_type"), "owner":row.get("mit_pla_name"), "location":{"lattitude":row.get("mit_lattitude"), "longitude":row.get("mit_longitude")},"influence":row.get("mit_influence")}

		realItemsByPlayer.update({i.get("pla_name"):listItems})

	Map.update({"itemsByPlayer":realItemsByPlayer})
	print(Map)
	#playerInfo
	for i in player:
		#budget
		playerCash_tmp = db.select("""
			SELECT pla_cash
			FROM player
			WHERE pla_name = '{0}';
			""".format(i.get("pla_name")))
		playerCash = playerCash_tmp[0]
		print(playerCash)
		#qty vendu
		playerSales_tmp = db.select("""
			SELECT SUM (sal_qty) AS vendu
			FROM sale
			INNER JOIN player ON player.pla_name = sale.sal_pla_name
			WHERE sal_day_nb = {1}
			AND sal_pla_name = '{0}';
			""".format(i.get("pla_name"), day_tmp.get("map_day_nb")))
		playerSales = playerSales_tmp[0]
		#profit
		#du jour meme ? ou du jour precedent ?
		playerProfit_tmp = db.select("""
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
				) AS profit;
			""".format(i.get("pla_name"), day_tmp.get("map_day_nb")))
		playerProfit = playerProfit_tmp[0]

		#drinksByPlayer
		#playerDoableDrinks = db.select("""
		#SELECT rcp_name,
		#(SELECT  SUM (ing_current_cost * compose.com_quantity)
		#FROM ingredient
		#INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name
		#INNER JOIN recipe ON recipe.rcp_name = compose.com_rcp_name
		#WHERE compose.com_rcp_name = rcp_name) AS cost,
		#rcp_is_cold,
		#(SELECT ingredient.ing_has_alcohol
		#FROM ingredient
		#INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name
		#INNER JOIN recipe ON recipe.rcp_name = compose.com_rcp_name
		#WHERE ingredient.ing_has_alcohol = TRUE
		#AND recipe.rcp_name = rcp_name) AS hasAlcohol
		#FROM recipe
		#INNER JOIN access ON access.acc_rcp_name = recipe.rcp_name
		#INNER JOIN player ON access.acc_pla_name = player.pla_name
		#WHERE player.pla_name ='{0}';
		#	""".format(i.get("pla_name")))


		playerInfo.update({i.get("pla_name"):{"cash":playerCash.get("pla_cash"),"sales":playerSales.get("vendu"),"profit":playerProfit.get("profit"),"drinksOffered":playerDoableDrinks}})

		#Ajouter laliste des boissons vendue
	Map.update({"playerInfo":playerInfo})

	#drinksByPlayer
	for i in player:
		#liste des types de boissons preparee
		playerDrinks = db.select("""
			SELECT pro_rcp_name, (pro_cost_at_that_time * pro_qty) AS cost, recipe.rcp_is_cold, (SELECT ingredient.ing_has_alcohol FROM ingredient INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name INNER JOIN recipe ON recipe.rcp_name = compose.com_rcp_name WHERE ingredient.ing_has_alcohol = TRUE AND recipe.rcp_name = pro_rcp_name) AS hasAlcohol
			FROM production
			INNER JOIN player ON player.pla_name = production.pro_pla_name
			INNER JOIN recipe ON recipe.rcp_name = production.pro_rcp_name
			WHERE pro_day_nb = {1}
			AND pro_pla_name = '{0}';
		""".format(i.get("pla_name"), day_tmp.get("map_day_nb")))
		print(playerDrinks)

	Map.update({"drinksByPlayer":playerDrinks})

	print(Map)
	db.close()

	return json.dumps(Map),200,{'Content-Type':'application/json'}
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


@app.route("/player", methods=["POST"])
def postRejoindre():
	rejoindre = request.get_json()
	name = rejoindre["name"]
	db = Db()
	sql = "SELECT pla_name FROM player;"
	joueur = db.select(sql)
	print (sql)
	db.close()
	#print(joueur)
	#if joueur = []:
	#	coordX = random.randrange(330,670,1)
    #	coordY = random.randrange(130,470,1)
	#	db = Db()
    #	budget = db.select("""SELECT pre_value FROM preference WHERE pre_name = 'budget';""")
    #	db.execute("""INSERT INTO Player VALUES ('{0}', 'abcd', {1}, 0);""".format(name,budget[0]["pre_value"]))
    #	db.close()
    return json_response()

@app.route("/sales",methods=["POST"])
def postSales():
 	sales = request.get_json()
 	player = sales['player']
  	item = sales['item']
  	quantity = sales['quantity']
 	print(sales)
 	for i in dicoTest:
 		if i == player:
 			for j in dicoTest[i]['actions']:
 				if j['kind'] == 'drinks':
 					recette = j['prepare']
 					if item in recette:
 						if recette[item] != 0:
 							if quantity > recette[item]:
								quantity = recette[item]
							else: 
								recette[item] = recette[item] - quantity

							prixVente = j['price'][item]

							db = Db()
							#get jour
							day = db.select("""SELECT map_day_nb from map;""")
							day_tmp = day.pop()
							#get budget player
							sqlGetBudget = "SELECT pla_cash FROM player WHERE pla_name = '"+ player +"';"
							budget = db.select(sqlGetBudget)[0]['pla_cash']
							print quantity
							print prixVente
							calBudget = budget + (quantity*prixVente)
							print calBudget
							#update budget
							sqlBudget = "UPDATE player SET (pla_cash) = ('"+ str(calBudget) +"') WHERE pla_name = '" + player + "';"
							db.execute(sqlBudget)
							#insert vente (0,10,12,'Toto','limonade')
							sql = "INSERT INTO sale VALUES('" + str(day_tmp) + "','" + str(quantity) + "','" + str(prixVente) + "','" + str(player) + "','" + str(item) + "');"
							db.execute(sql)
							db.close()
	#if "quantity" not in sales :
	#	return json_response({ "error" : "Missing quantity" }, 400)
	#if "player" not in sales :
	#	return json_response({ "error" : "Missing player" }, 400)
	#if "item" not in sales :
	#	return json_response({ "error" : "Missing item" }, 400)

	#db = Db()
	#day = db.select("""SELECT map_day_nb from map;""")
	#day_tmp = day.pop()
 	#db.execute("""
 	#	INSERT INTO sale VALUES ({0}, {1},{2}, '{3}', '{4}');
 	#""".format(day_tmp['map_day_nb'],sales['quantity'],sales['price'],sales['player'],sales['item']))
    #    db.close()

 	return json.dumps("ok"),200,{'Content-Type':'application/json'}


@app.route("/metrology", methods=["POST"])
def postWheather():
	weather = request.get_json()
	print(weather)

	if "timestamp" not in weather:
		return json_response({ "error" : "Missing timestamp" }, 400)
	if "dfn" not in weather["weather"][0]:
		return json_response({ "error" : "Missing dfn"}, 400)
	if "weather" not in weather["weather"][0]:
		return json_response({ "error" : "Missing weather"}, 400)
	if  weather["timestamp"] != 0 :
		timestamp = weather["timestamp"]
	if weather["weather"][0]["dfn"] == 0:
		currentWeather = weather["weather"][0]["weather"]
	if weather["weather"][1]["dfn"] == 1:
		previsionWeather = weather["weather"][1]["weather"]

	db = Db()
	db.execute("""
		UPDATE map
		SET map_time = {0}, map_prevision_weather = '{1}', map_current_weather =  '{2}'
		WHERE map_id = 0;
	""".format(timestamp ,previsionWeather, currentWeather))
	db.close()
 	return json.dumps("ok"),200,{'Content-Type':'application/json'}

@app.route("/actions/<PlayerName>", methods=["POST"])
def postAction(PlayerName):
	actions = request.get_json()
	dicoAction[PlayerName] = actions
	return json_response(dicoAction)




	return json.dumps("ok"),200,{'Content-Type':'application/json'}

#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"

if __name__ == "__main__":
 	app.run()

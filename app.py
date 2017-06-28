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

	itemsByPlayer={}
	playerInfo={}
	drinksByPlayer={}

	db = Db()
	coordinate_tmp = db.select("SELECT map_longitude AS longitude, map_lattitude AS lattitude from map;")
	coordinate = coordinate_tmp[0]

	coordinate_span_tmp = db.select("SELECT  map_longitude_span AS longitude_span, map_lattitude_span AS lattitude_span from map;")
	coordinate_span = coordinate_span_tmp[0]

	print (coordinate)
	print (coordinate_tmp)

	regionCoord = {"region": {"center": coordinate, "span" : coordinate_span}}
	rank = db.select("SELECT pla_name AS name, pla_cash AS cash from player order by pla_cash DESC;")

	day_tmp = db.select("SELECT map_day_nb from map;")
	day = day_tmp[0]
	db.close()

	
	for i in rank:
		db = Db()

		#playerInfo
		#budget
		playerCash_tmp = db.select("SELECT pla_cash AS cash FROM player WHERE pla_name = \'"+ i.get("name") + "\';")
		playerCash = playerCash_tmp[0]["cash"]

		#qty vendu
		playerSales_tmp = db.select("SELECT SUM (sal_qty) AS sales FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}';".format(i.get("name"), day_tmp.get("map_day_nb")))
		playerSales = playerSales_tmp[0]["sales"]
		
		#profit
		#du jour meme ? ou du jour precedent ?
		playerProfit_tmp = db.select("SELECT (SELECT SUM (sal_qty * sal_price) FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} ND sal_pla_name = '{0}') - (SELECT SUM (pro_qty * pro_cost_at_that_time) AS profit FROM production INNER JOIN player ON player.pla_name = production.pro_pla_name WHERE pro_day_nb = {1} AND pro_pla_name = '{0}' ) AS profit; ".format(i.get("name"), day_tmp.get("day")))
		playerProfit = playerProfit_tmp[0]["profit"]

		#drinksByPlayer	
		playerDoableDrinks = db.select("SELECT rcp_name, (SELECT  SUM (ing_current_cost * compose.com_quantity) FROM ingredient INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name WHERE compose.com_rcp_name = rcp_name) AS price, rcp_is_cold AS isVold, rcp_has_alcohol AS hasAlcohol FROM recipe INNER JOIN access ON access.acc_rcp_name = recipe.rcp_name WHERE access.axx_pla_name ='{0}';".format(i.get("name")))	

		db.close()
		info = {"cash": playerCash, "sales":playerSales, "profit":playerProfit, "drinksOffered":playerDoableDrinks}
		playerInfo[i['name']] = info

		db = Db()
		#itemsByPlayer
		oneItem = db.select("SELECT mit_type AS kind, mit_pla_name AS owner, mit_longitude AS longitude, mit_lattitude AS lattitude, mit_influence AS influence FROM map_item WHERE mit_pla_name =\'" + rank.get("name")+ "\';")
		listItems = {"kind":oneItem["kind"], "owner":oneItem["owner"], "location":{"lattitude":oneItem["lattitude"], "longitude":oneItem["longitude"]},"influence":oneItem["influence"]}
		itemsByPlayer[i['name']] = listItems
		db.close()
		
		db = Db()
		#drinksByPlayer
		#liste des types de boissons preparee*
		listDrinks = db.select("SELECT pro_rcp_name AS name, (pro_cost_at_that_time * pro_qty) AS price, recipe.rcp_is_cold AS isCold, recipe.rcp_has_alcohol AS hasAlcohol FROM production  INNER JOIN recipe ON recipe.rcp_name = production.pro_rcp_name WHERE pro_day_nb = {1} AND pro_pla_name = '{0}';".format(i.get("name"), day_tmp.get("map_day_nb")))
		drinksByPlayer[i['name']] = listDrinks
		db.close()

	Map = {"region":regionCoord, "ranking":rank, "itemsByPlayer":itemsByPlayer, "playerInfo":playerInfo, "drinksByPlayer":drinksByPlayer}
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
	name = rejoindre['name']
	db = Db()
	sql = "SELECT pla_name FROM player WHERE pla_name = '"+ name +"';"
	joueur = db.select(sql)
	print (joueur)
	db.close()
	if joueur == []:
		coordX = random.randrange(330,670,1)
		coordY = random.randrange(130,470,1)
		db = Db()
		budget = db.select("""SELECT pre_value FROM preference WHERE pre_name = 'budget';""")
		db.execute("""INSERT INTO Player VALUES ('{0}', 'abcd', {1}, 0);""".format(name,budget[0]["pre_value"]))
		db.close()
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

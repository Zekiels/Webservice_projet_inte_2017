from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask import render_template
from pprint import pprint
import random
import json
from db import Db
from math import *

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

day = 0

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

# Fonction pour la route /map/<player_name> avec GET
# Recupere les details d'une partie
@app.route('/map/<playerName>', methods=['GET'])
def getMapPlayer(playerName):
	#create 
	db = Db()
	sql = "SELECT b_nom as boisson, b_alcool as hasAlcool, b_chaud as isHot, i_nom as ingredient, i_prix as ingPrix, r_qte as quantite FROM ingredient INNER JOIN recette ON recette.i_id = ingredient.i_id INNER JOIN boisson ON boisson.b_id = recette.b_id WHERE boisson.b_id IN (SELECT b_id FROM boisson WHERE j_id = (SELECT j_id FROM joueur WHERE j_pseudo = '" + playerName +"'));"
	ingredients = db.select(sql)
	db.close()

	db = Db()
	sql = "SELECT m_centreX as latitude, m_centreY as longitude FROM map;"
	coordinates = db.select(sql)[0]
	sqlSpan = "SELECT m_coordX as latitudeSpan, m_coordY as longitudeSpan FROM map;"
	coordinatesSpan = db.select(sqlSpan)[0]
	sqlRank = "SELECT j_pseudo FROM JOUEUR ORDER BY j_budget DESC;"
	ranking = db.select(sqlRank)
	db.close()

	region = {"center": coordinates, "span": coordinatesSpan}

	mapInfo = {"region" : region, "ranking" : ranking}
	print region
	db = Db()
	sqlCoord = "SELECT z_centerX as latitude, z_centerY as longitude FROM zone WHERE j_id = (SELECT j_id FROM joueur WHERE j_pseudo = '" + player_name + "');"
	sqlBudget = "SELECT j_budget FROM joueur WHERE j_pseudo = '"+ player_name +"';"
	sqlSales = "SELECT COALESCE(0,SUM(v_qte)) as nbSales FROM ventes WHERE j_id = (SELECT j_id FROM joueur WHERE j_pseudo = '"+ player_name +"');"
	sqlDrinks = "SELECT b_nom as name, b_prixprod as price, b_alcool as hasAlcohol, b_chaud as isHot FROM boisson WHERE j_id = (SELECT j_id FROM joueur WHERE j_pseudo = '" + player_name +"');"
	coord = db.select(sqlCoord)[0]
	budgetBase = db.select(sqlBudget)[0]['j_budget']
	nbSales = db.select(sqlSales)[0]['nbsales']
	drinksInfo = db.select(sqlDrinks)
	db.close()

	profit = budgetBase - budget_depart;
	info = {"cash": budgetBase, "sales": nbSales, "profit": profit, "drinksOffered": drinksInfo}

	message = {"availableIngredients": ingredients, "map": mapInfo, "playerInfo": info}
	return json_response(message)

@app.route("/map", methods=["GET"])
def getMap():

	itemsByPlayer={}
	playerInfo={}
	drinksByPlayer={}
	rankNoKeys = []
	drinksOffered = []

	db = Db()
	coordinate_tmp = db.select("SELECT map_longitude AS longitude, map_latitude AS latitude from map;")
	coordinate = coordinate_tmp[0]

	coordinate_span_tmp = db.select("SELECT  map_longitude_span AS longitudeSpan, map_latitude_span AS latitudeSpan from map;")
	coordinate_span = coordinate_span_tmp[0]

	regionCoord = {"center": coordinate, "span" : coordinate_span}
	rank = db.select("SELECT pla_name AS name, pla_cash AS cash from player order by pla_cash DESC;")

	day_tmp = db.select("SELECT map_day_nb from map;")
	day = day_tmp[0]
	db.close()

	
	for i in rank:
		db = Db()
		rankNoKeys.append(i.get("name"))
		#playerInfo
		#budget
		playerCash_tmp = db.select("SELECT pla_cash AS cash FROM player WHERE pla_name = \'"+ i.get("name") + "\';")
		playerCash = playerCash_tmp[0]["cash"]

		#qty vendu
		playerSales_tmp = db.select("SELECT SUM (sal_qty) AS sales FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}';".format(i.get("name"), day.get("map_day_nb")))
		playerSales = playerSales_tmp[0]["sales"]
		
		#profit
		playerProfit_tmp = db.select("SELECT (SELECT SUM (sal_qty * sal_price) FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}') - (SELECT SUM (pro_qty * pro_cost_at_that_time) AS profit FROM production INNER JOIN player ON player.pla_name = production.pro_pla_name WHERE pro_day_nb = {1} AND pro_pla_name = '{0}' ) AS profit; ".format(i.get("name"), day.get("map_day_nb")))
		playerProfit = playerProfit_tmp[0]["profit"]

		#drinksByPlayer	
		playerDoableDrinks = db.select("SELECT rcp_name AS name, (SELECT  SUM (ing_current_cost * compose.com_quantity) FROM ingredient INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name WHERE compose.com_rcp_name = rcp_name) AS price, rcp_is_cold AS isCold, rcp_has_alcohol AS hasAlcohol FROM recipe INNER JOIN access ON access.acc_rcp_name = recipe.rcp_name WHERE access.acc_pla_name ='{0}';".format(i.get("name")))	
		drinksOffered.append({"name":playerDoableDrinks['name'], "price":playerDoableDrinks['price'], "hasAlcohol":playerDoableDrinks['hasalcohol'],"iscold":playerDoableDrinks['iscold']})


		db.close()
		info = {"cash": playerCash, "sales":playerSales, "profit":playerProfit, "drinksOffered":drinksOffered}


		playerInfo[i['name']] = info

		db = Db()
		#itemsByPlayer)
		oneItem_temp = db.select("SELECT mit_type AS kind, mit_pla_name AS owner, mit_longitude AS longitude, mit_latitude AS latitude, mit_influence AS influence FROM map_item WHERE mit_pla_name =\'" + i.get("name")+ "\';")
		if len(oneItem_temp) > 0 :
			oneItem = oneItem_temp[0]
			listItems = {"kind":oneItem["kind"], "owner":oneItem["owner"], "location":{"latitude":oneItem["latitude"], "longitude":oneItem["longitude"]},"influence":oneItem["influence"]}	
		else:
			oneItem = oneItem_temp
			listItems = oneItem

		itemsByPlayer[i['name']] = listItems
		db.close()
		
		db = Db()
		#drinksByPlayer
		#liste des types de boissons preparee*
		listDrinks = db.select("SELECT pro_rcp_name AS name, (pro_cost_at_that_time * pro_qty) AS price, recipe.rcp_is_cold AS isCold, recipe.rcp_has_alcohol AS hasAlcohol FROM production  INNER JOIN recipe ON recipe.rcp_name = production.pro_rcp_name WHERE pro_day_nb = {1} AND pro_pla_name = '{0}';".format(i.get("name"), day.get("map_day_nb")))
		drinksByPlayer[i['name']] = listDrinks
		db.close()

	Map = {"map":{"region":regionCoord, "ranking":rankNoKeys, "itemsByPlayer":itemsByPlayer, "playerInfo":playerInfo, "drinksByPlayer":drinksByPlayer}}
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

@app.route("/players/<playerName>", methods=["POST"])
def postquitter():
	quitter = request.get_son()
	print (quitter)

	return json.dumps("pas ok"),200,{'Content-Type':'application/json'}


@app.route("/player", methods=["POST"])
def postRejoindre():
	rejoindre = request.get_json()
	name = rejoindre['name']
	print(name)
	db = Db()
	sql = "SELECT pla_name FROM player WHERE pla_name = '"+ name +"';"
	joueur = db.select(sql)
	db.close()
	if joueur == []:
		longitude = random.randrange(0,600)
		latitude = random.randrange(0,600)
		db = Db()
		budget = db.select("""SELECT pre_value FROM preference WHERE pre_name = 'budget';""")
		sqlPLayer = ("""INSERT INTO Player VALUES ('{0}', 'abcd', {1}, 0);""".format(name,budget[0]["pre_value"]))
		db.execute(sqlPLayer)
		sqlMapItem = (""" INSERT INTO Map_Item(mit_type,  mit_influence, mit_longitude, mit_latitude, mit_pla_name, mit_map_id) VALUES('stand' ,10.0 ,{0} ,{1} ,'{2}', 0);""".format(longitude, latitude ,name))
		db.execute(sqlMapItem)
		sqlVente = (""" INSERT INTO Sale VALUES('{0}', 0, 0, 'limonade' '{1}');""".format(day,name))
		db.execute(sqlVente)
		sqlProd = (""" INSERT INTO production VALUES('{0}', 0, 0.82, 'limonade' '{1}');""".format(day,name))
		db.execute(sqlProd)
		db.close()

	#coord = db.select(""" SELECT mit_longitude,mit_latitude FROM Map_Item WHERE mit_pla_name ='{0}';""".format(name))
	#print(coord)
	#sqlDrinksInfo = (""" SELECT * FROM recipe WHERE rcp_name = 'limonade';""")
	#drinksInfo = db.execute(sqlDrinksInfo);
	#prixVente = (""" SELECT sal_price FROM Sale WHERE pla_name ='"+ name + "' rcp_name = 'limonade' sal_day_nb = '"+ day +"';""")
	#prixProd = (""" SELECT pro_cost_at_that_time FROM production WHERE pla_name ='"+ name + "' rcp_name = 'limonade' pro_day_nb = '"+ day +"';""")
	
	#reponse = {"name": name,
	return json_response()

@app.route("/sales",methods=["POST"])
def postSales():
 	sales = request.get_json()
 	player = sales['player']
  	item = sales['item']
  	quantity = sales['quantity']
 	print(sales)
 	print(dicoAction)
 	for i in dicoAction:
 		if i == player:
 			for j in dicoAction[i]['actions']:
 				if j['kind'] == 'drinks':
 					recette = j['prepare']
 					if item in recette:
 						if recette[item] != 0:
 							if quantity > recette[item]:
								quantity = recette[item]
							else: 
								recette[item] = recette[item] - quantity

							prixVente = j['price'][item]
							print("start request")
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
							print("request execute")
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

	day = timestamp%24

	db = Db()
	db.execute("""
		UPDATE map
		map_day_nb = {0}, SET map_time = {1}, map_prevision_weather = '{2}', map_current_weather =  '{3}'
		WHERE map_id = 0;
	""".format(day, timestamp ,previsionWeather, currentWeather))
	db.close()
 	return json.dumps("ok"),200,{'Content-Type':'application/json'}

@app.route("/actions/<PlayerName>", methods=["POST"])
def postAction(PlayerName):
	actions = request.get_json()
	dicoAction[PlayerName] = actions
	return json_response(dicoAction)

#@app.route("/idGet",methods=["GET"])
#def idGet():
#	return "test"

if __name__ == "__main__":
 	app.run()

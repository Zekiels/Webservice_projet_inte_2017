from flask import Flask, request, redirect, url_for
from flask_cors import CORS, cross_origin
from flask import render_template
from pprint import pprint
import random
import json
from db import Db
from math import *

app = Flask(__name__, static_folder='static')
app.debug = True
CORS(app)

def json_response(data="OK", status=200):
  return json.dumps(data), status, { "Content-Type": "application/json" }

@app.route('/jeu.html')
def jeu():
	return render_template('jeu.html')

@app.route('/connexion.html')
def connect():
	return render_template('connexion.html')

#######################################################################################################################################
#################################                   GET   						#######################################################
#######################################################################################################################################

@app.route("/day", methods=["GET"])
def getDay():
	db = Db()
	day = db.select("SELECT map_day_nb FROM map;")[0]["map_day_nb"] 
	db.close()
	return json.dumps(day),200,{'Content-Type':'application/json'}

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

# Fonction pour la route /map/<playerName> avec GET
# Recupere les details d'une partie
@app.route('/map/<playerName>', methods=['GET'])
def getMapPlayer(playerName):
	#info de boisson du joueur
	db = Db()
	day_tmp = db.select("SELECT map_day_nb from map;")
	day = day_tmp[0]

	sql = "SELECT ing_name as name, ing_has_alcohol as hasAlcool, ing_is_cold as isCold, ing_current_cost as cost FROM ingredient INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name INNER JOIN recipe ON recipe.rcp_name = compose.com_rcp_name WHERE recipe.rcp_name IN (	SELECT acc_rcp_name FROM access WHERE acc_pla_name = (SELECT pla_name FROM player WHERE pla_name = '{0}'));"
	ingredients = db.select(sql.format(playerName))
	db.close()

	db = Db()
	#emplacement map centre
	sql = "SELECT map_latitude as latitude, map_longitude as longitude FROM map;"
	coordinates = db.select(sql)[0]
	
	#emplacement map span
	sqlSpan = "SELECT map_latitude_span as latitudeSpan, map_longitude_span as longitudeSpan FROM map;"
	coordinatesSpan = db.select(sqlSpan)[0]
	
	#ranking
	rank = db.select("SELECT pla_name AS name from player order by pla_cash DESC;")
	rankNoKeys = []
	for i in rank:
		rankNoKeys.append(i.get("name"))
	db.close()

	region = {"center": coordinates, "span": coordinatesSpan}
	
	#ajouter Mapitem
	mapInfo = {"region" : region, "ranking" : rankNoKeys}
	print(region)
	db = Db()
	
	#infoPlayer
	
	#joueur stand
	sqlCoord = """	SELECT mit_latitude as latitude, mit_longitude as longitude 
					FROM map_item 
					WHERE mit_pla_name = (SELECT pla_name FROM player WHERE pla_name = '{0}');"""
	
	#info joueur profit
	playerProfit_tmp = """
						SELECT
							(SELECT COALESCE(0,SUM (sal_qty * sal_price)) 
							FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name 
							WHERE sal_day_nb = {1} AND sal_pla_name = '{0}') 
							- 
							(SELECT COALESCE(0,SUM (pro_qty * pro_cost_at_that_time)) 
							FROM production 
							INNER JOIN player ON player.pla_name = production.pro_pla_name 
							WHERE pro_day_nb = {1} 
							AND pro_pla_name = '{0}') AS profit;"""
	
	#info joueur budget
	sqlBudget = """	SELECT pla_cash as cash 
					FROM player 
					WHERE pla_name = '{0}';"""
	
	#info nb vente
	sqlSales = """	SELECT COALESCE(0, SUM(sal_qty)) as sales 
					FROM sale 
					WHERE sal_pla_name = '{0}';"""
	
	#info joueur drinkOffered
	sqlDrinks = """	SELECT rcp_name, 
							(SELECT  SUM (ing_current_cost * compose.com_quantity) 
							FROM ingredient 
							INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name 
							WHERE compose.com_rcp_name = rcp_name) AS price, 
							rcp_is_cold AS isCold, 
							rcp_has_alcohol AS hasAlcohol 
					FROM recipe 
					INNER JOIN access ON access.acc_rcp_name = recipe.rcp_name 
					WHERE access.acc_pla_name ='{0}';"""
	
	coord = db.select(sqlCoord.format(playerName))[0]
	print(coord)
	budgetBase = db.select(sqlBudget.format(playerName))[0]['cash']
	print(budgetBase)
	profit = db.select(playerProfit_tmp.format(playerName, day.get("map_day_nb")))[0]["profit"]
	print(profit)
	nbSales = db.select(sqlSales.format(playerName))[0]['sales']
	print(nbSales)
	drinksInfo = db.select(sqlDrinks.format(playerName))
	print(drinksInfo)
	db.close()

	info = {"cash": budgetBase, "sales": nbSales, "profit": profit, "drinksOffered": drinksInfo}

	message = {"availableIngredients": ingredients, "map": mapInfo, "playerInfo": info}
	return json_response(message)

############################
############################
#ROUTE GET /MAP
############################
############################
@app.route("/map", methods=["GET"])
def getMap():

	itemsByPlayer={}
	playerInfo={}
	drinksByPlayer={}
	rankNoKeys = []

	db = Db()

	##############
	#Coordonnee map
	##############
	coordinate_tmp = db.select("SELECT map_longitude AS longitude, map_latitude AS latitude from map;")
	coordinate = coordinate_tmp[0]

	coordinate_span_tmp = db.select("SELECT  map_longitude_span AS longitudeSpan, map_latitude_span AS latitudeSpan from map;")
	coordinate_span = coordinate_span_tmp[0]

	coordinate_span['latitudeSpan'] = coordinate_span['latitudespan']
	del coordinate_span['latitudespan']
	coordinate_span['longitudeSpan'] = coordinate_span['longitudespan']
	del coordinate_span['longitudespan']

	regionCoord = {"center": coordinate, "span" : coordinate_span}

	##############
	#Joueurs classes
	##############
	rank = db.select("SELECT pla_name AS name, pla_cash AS cash from player order by pla_cash DESC;")

	##############
	#Jour actuel
	##############
	day_tmp = db.select("SELECT map_day_nb from map;")
	day = day_tmp[0]


	for i in rank:
		rankNoKeys.append(i.get("name"))
		
		############################
		#playerInfo
		############################

		##############
		#Budget
		##############
		playerCash_tmp = db.select("""
			SELECT pla_cash AS cash 
			FROM player 
			WHERE pla_name = '{0}';
		""".format(i.get("name")))
		playerCash = playerCash_tmp[0]["cash"]
		print(playerCash_tmp)

		##############
		#Qty vendu
		##############
		playerSales_tmp = db.select("""
			SELECT COALESCE (0,SUM (sal_qty)) AS sales 
			FROM sale 
			INNER JOIN player ON player.pla_name = sale.sal_pla_name 
			WHERE sal_day_nb = {1} 
			AND sal_pla_name = '{0}';
		""".format(i.get("name"), day.get("map_day_nb")))
		playerSales = playerSales_tmp[0]["sales"]

		##############
		#Profit
		##############
		playerProfit_tmp = db.select("""
			SELECT
				(SELECT COALESCE(0,SUM (sal_qty * sal_price)) 
				FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name 
				WHERE sal_day_nb = {1} AND sal_pla_name = '{0}') 
				- 
				(SELECT COALESCE(0,SUM (pro_qty * pro_cost_at_that_time)) 
				FROM production 
				INNER JOIN player ON player.pla_name = production.pro_pla_name 
				WHERE pro_day_nb = {1} 
				AND pro_pla_name = '{0}') AS profit; 
			""".format(i.get("name"), day.get("map_day_nb")))
		print(playerProfit_tmp)
		playerProfit = playerProfit_tmp[0]["profit"]

		##############
		#drinksByPlayer
		##############
		playerDoableDrinks = db.select("SELECT rcp_name AS name, (SELECT  SUM (ing_current_cost * compose.com_quantity) FROM ingredient INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name WHERE compose.com_rcp_name = rcp_name) AS price, rcp_is_cold AS isCold, rcp_has_alcohol AS hasAlcohol FROM recipe INNER JOIN access ON access.acc_rcp_name = recipe.rcp_name WHERE access.acc_pla_name ='{0}';".format(i.get("name")))
		for j in playerDoableDrinks:
			j["isCold"] = j["iscold"]
			del j["iscold"]
			j["hasAlcohol"] = j["hasalcohol"]
			del j["hasalcohol"]

		info = {"cash": playerCash, "sales":playerSales, "profit":playerProfit, "drinksOffered":playerDoableDrinks}


		playerInfo[i['name']] = info

		##############
		#itemsByPlayer
		##############
		oneItem_temp = db.select("SELECT mit_type AS kind, mit_pla_name AS owner, mit_longitude AS longitude, mit_latitude AS latitude, mit_influence AS influence FROM map_item WHERE mit_pla_name =\'" + i.get("name")+ "\';")
		if len(oneItem_temp) > 0 :
			oneItem = oneItem_temp[0]
			listItems = [{"kind":oneItem["kind"], "owner":oneItem["owner"], "location":{"latitude":oneItem["latitude"], "longitude":oneItem["longitude"]},"influence":oneItem["influence"]}]	
			#Atention je triche vu qu'on a qu'un seul map_item, en vrai il faudrait utiliser des list.append()
		else:
			oneItem = oneItem_temp
			listItems = oneItem

		itemsByPlayer[i['name']] = listItems

		############################
		#drinksByPlayer
		############################
		#liste des types de boissons preparee

		listDrinks = db.select("SELECT sal_rcp_name AS name, sal_price AS price, recipe.rcp_is_cold AS isCold, recipe.rcp_has_alcohol AS hasAlcohol FROM sale  INNER JOIN recipe ON recipe.rcp_name = sale.sal_rcp_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}';".format(i.get("name"), day.get("map_day_nb")))
		for j in listDrinks:
			j["isCold"] = j["iscold"]
			del j["iscold"]
			j["hasAlcohol"] = j["hasalcohol"]
			del j["hasalcohol"]

		drinksByPlayer[i['name']] = listDrinks

	##############
	#Construction du JSON de retour
	##############
	Map = {"map":{"region":regionCoord, "ranking":rankNoKeys, "itemsByPlayer":itemsByPlayer, "playerInfo":playerInfo, "drinksByPlayer":drinksByPlayer}}
	print(Map)
	db.close()

	return json.dumps(Map),200,{'Content-Type':'application/json'}
	

##############
#ROUTE GET /
##############
@app.route("/", methods=["GET"])
def getIndex():
	return redirect(url_for('connect'))

##############
#ROUTE GET /reset
##############
@app.route("/reset", methods=["GET"])
def getReset():
	db=Db()
	db.execute("""
		DELETE
		FROM player;
		""")

	#Non synchroniser avec l'arduino donc on fait pas
	#db.execute("""
 	#	UPDATE map
	#	SET map_day_nb = 0,
	#	map_time = 0,
	#	map_prevision_weather = '',
	#	map_current_weather = ''
	#	WHERE map_id = 0
	#	""")
	db.close()
	return json.dumps("Done"),200,{'Content-Type':'application/json'}

#######################################################################################################################################
#################################                   POST   						#######################################################
#######################################################################################################################################

@app.route("/players/<playerName>", methods=["POST"])
def postquitter(playerName):
	quitter = request.get_json()
	if playerName == '':
		return json_response({ "error" : "playerName is empty" }, 400)

	db.execute("""
		DELETE FROM player 
		WHERE pla_name = {0};
		""".format(playerName)
	)
	return redirect(url_for('connect'))

@app.route("/players", methods=["POST"])
def postRejoindre():
	rejoindre = request.get_json()
	name = rejoindre['name']
	db = Db()
	#on recupere le jour dans la bdd
	day = db.select("SELECT map_day_nb FROM map;")[0]["map_day_nb"] 
	#variable temporaire pour verifier si le joueur existe
	joueur = db.select("SELECT pla_name FROM player WHERE pla_name = '"+ name +"';")
	#verifi si le joueur existe ou pas si jamais il n existe pas on lui creer les tables qui sont lie au joueur
	if joueur == []: 
		longitude = random.randrange(50,950)
		latitude = random.randrange(50,950)
		budget = db.select("""SELECT pre_value FROM preference WHERE pre_name = 'budget';""")
		sqlPLayer = ("""INSERT INTO Player VALUES ('{0}', 'abcd', {1}, 0);""".format(name,budget[0]["pre_value"]))
		db.execute(sqlPLayer)
		sqlMapItem = (""" INSERT INTO Map_Item(mit_type,  mit_influence, mit_longitude, mit_latitude, mit_pla_name, mit_map_id) VALUES('stand' ,10.0 ,{0} ,{1} ,'{2}', 0);""".format(longitude, latitude ,name))
		db.execute(sqlMapItem)
		sqlVente = (""" INSERT INTO Sale VALUES('{0}', 0, 0,'{1}','limonade');""".format(day, name))
		db.execute(sqlVente)
		sqlProd = (""" INSERT INTO production VALUES('{0}', 0, 0,'{1}', 'limonade');""".format(day, name))
		db.execute(sqlProd)
		sqlRecette = (""" INSERT INTO access VALUES ('limonade', '{0}')""".format(name))
		db.execute(sqlRecette)

	#recuperation des coord longitude et latitude
	coord = db.select(""" SELECT mit_longitude,mit_latitude FROM Map_Item WHERE mit_pla_name = '{0}' ;""".format(name))[0]
	coordx=coord["mit_longitude"]
	coordy=coord["mit_latitude"]
	coordinates = {"latitude":coordx, "longitude":coordy}

	#drinkInfo qui recupere les information pour formater le message drink
	drink = db.select("""SELECT * FROM recipe WHERE rcp_name ='limonade'; """)[0]
	prod = db.select("""SELECT pro_cost_at_that_time FROM production WHERE pro_rcp_name = 'limonade' and pro_pla_name = '{0}' ;""".format(name))[0]
	drinkInfo = {"name":drink["rcp_name"], "price":prod["pro_cost_at_that_time"], "hasAlcohol":drink["rcp_has_alcohol"], "isCold":drink["rcp_is_cold"]}
	
	#player cash qui genere l'argent dispo sur le compte du joueur
	playerCash_tmp = db.select("SELECT pla_cash AS cash FROM player WHERE pla_name ='{0}';".format(name))
	playerCash = playerCash_tmp[0]["cash"]

	#qty vendu recupere les vente du joueur
	playerSales_tmp = db.select("SELECT SUM (sal_qty) AS sales FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}';".format(name, day))
	playerSales = playerSales_tmp[0]["sales"]

	#profit rcorrespond au profit sur les ventes du joueur
	playerProfit_tmp = db.select("SELECT (SELECT SUM (sal_qty * sal_price) FROM sale INNER JOIN player ON player.pla_name = sale.sal_pla_name WHERE sal_day_nb = {1} AND sal_pla_name = '{0}') - (SELECT SUM (pro_qty * pro_cost_at_that_time) AS profit FROM production INNER JOIN player ON player.pla_name = production.pro_pla_name WHERE pro_day_nb = {1} AND pro_pla_name = '{0}' ) AS profit; ".format(name, day))
	playerProfit = playerProfit_tmp[0]["profit"]
	db.close()

	#on concataine dans la reponse finale
	playerInfo = {"cash":playerCash, "sales":playerSales,"profit":playerProfit, "drinksOffered": drinkInfo}
	reponse = {"name": name, "location": coordinates, "info":playerInfo}

	return json_response(reponse) #on retourne le message au client web

@app.route("/sales",methods=["POST"])
def postSales():
 	sales = request.get_json()
 	
	if "quantity" not in sales :
		return json_response({ "error" : "Missing quantity" }, 400)
	if "player" not in sales :
		return json_response({ "error" : "Missing player" }, 400)
	if "item" not in sales :
		return json_response({ "error" : "Missing item" }, 400)

	db = Db()
	#get day
	day_tmp = db.select("SELECT map_day_nb from map;")
	day = day_tmp[0]["map_day_nb"]
	
	prod = db.select("""SELECT pro_qty, pro_rcp_name 
						FROM production 
						WHERE pro_pla_name = '{0}' 
						AND pro_day_nb = {1};
					""".format(sales["player"], day))[0]

	if sales["item"] == prod["pro_rcp_name"]:
		if sales["quantity"] <= prod["pro_qty"]:

			#mise a jour budget joueur
			cash = db.select("""SELECT pla_cash from player WHERE pla_name = '{0}';""".format(sales['player']))[0]
			price = db.select("""SELECT sal_price from sale WHERE  sal_rcp_name = '{0}' AND sal_pla_name = '{1}' AND sal_day_nb = {2};""".format(sales['item'],sales['player'], day))[0]
			print(cash["pla_cash"])
			print(float(sales['quantity']))
			print(price["sal_price"])
			budget = cash["pla_cash"] + (float(sales['quantity'])*price["sal_price"])
			print(budget)
			db.execute("""
		 		UPDATE player SET pla_cash = {0} WHERE  pla_name = '{1}';
		 	""".format(budget, sales['player']))

			#mise a jour sale
		 	db.execute("""
		 		UPDATE sale SET sal_qty = {0} WHERE  sal_rcp_name = '{1}' AND sal_pla_name = '{2}' AND sal_day_nb = {3};
		 	""".format(sales['quantity'], sales['item'],sales['player'], day))
			return json.dumps("ok"),200,{'Content-Type':'application/json'}
		else:
			return json.dumps("quantity error"),400,{'Content-Type':'application/json'}
	else:
		return json.dumps("item error"),400,{'Content-Type':'application/json'}		
	db.close()


@app.route("/metrology", methods=["POST"])
def postWheather():
	weather = request.get_json()

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
	day = db.select("SELECT map_day_nb FROM map;")[0]["map_day_nb"]
	if (timestamp%24) == 0:
		day = day + 1 
		db.execute("""UPDATE map SET  map_day_nb = {0} WHERE map_id = 0;""".format(day))
		createTab()
	if(timestamp<23):
		day = 0
		db.execute("""UPDATE map SET  map_day_nb = {0} WHERE map_id = 0;""".format(day))
		print('bonjour')

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
	print(actions)
	if "actions" not in actions or len(actions["actions"]) == 0:
		return json_response({ "error" : "Missing actions" }, 400)

	for action in actions["actions"]:
		if action["kind"] == "drinks":
			db = Db()
			#get day
			day = db.select("""SELECT map_day_nb from map;""")
			day_tmp = day.pop()
			print(action["prepare"].items()[0][0])
			print(action["prepare"].values()[0])
			print(action["price"].values()[0])
			#get price
			price = db.select("""	SELECT  SUM (ing_current_cost * compose.com_quantity) 
												FROM ingredient 
												INNER JOIN compose ON compose.com_ing_name = ingredient.ing_name 
												WHERE compose.com_rcp_name = '{0}';""".format(action["prepare"].items()[0][0]))[0]
			print(price)
			#create production
			db.execute("""
			    UPDATE production
				SET pro_qty = {0}, pro_cost_at_that_time = {1}
				WHERE  pro_rcp_name = '{2}'
				AND pro_pla_name = '{3}'
				AND pro_day_nb = {4};
		 	""".format(action["prepare"].values()[0], price["sum"], action["prepare"].items()[0][0], PlayerName, day_tmp.get("map_day_nb")))

			#mise a jour budget joueur
			cash = db.select("""SELECT pla_cash from player WHERE pla_name = '{0}';""".format(PlayerName))[0]
			print(cash["pla_cash"])
			print(float(action["prepare"].values()[0]))
			print(price["sum"])
			
			budget = cash["pla_cash"] - (float(action["prepare"].values()[0])*price["sum"])
			print(budget)
			db.execute("""
		 		UPDATE player SET pla_cash = {0} WHERE  pla_name = '{1}';
		 	""".format(budget, PlayerName))

			#create sale
			db.execute("""
				UPDATE sale
				SET sal_price = {0}
				WHERE  sal_rcp_name = '{1}'
				AND sal_pla_name = '{2}'
				AND sal_day_nb = {3};
			""".format(action["price"].values()[0], action["prepare"].items()[0][0], PlayerName, day_tmp.get("map_day_nb")))

			db.close()
			return json.dumps("ok"),200,{'Content-Type':'application/json'}
		if action["kind"] == "recipe":
			print("NON")
			return json.dumps("No implement"),400,{'Content-Type':'application/json'}
		if action["kind"] == "ad":
			radiusToAdd = action["radius"]

			#Verifier le type
			if radius >= 15 :
				sizeType = "pub_grand"
			elif radius >=10 :
				sizeType = "pub_moyen"
			else : 
				sizeType = "pub_petit"
			
			db=Db()
			
			#Mettre a jour l influence du stand
			db.execute("""
				UPDATE map_item
				SET mit_influence = mit_influense + {0}
				WHERE mit_pla_name = '{1}'
			""".format(radiusToAdd, PlayerName))

			#mettre a jour le cash et le profit du joueur
			#apparement on peut soustraire par None, on est pas cense tomber dans le cas
			db.execute("""
				UPDATE player
				SET pla_cash = pla_cash - (SELECT pre_value FROM preference WHERE pre_name = {0}),
				pla_profit = pla_profit - (SELECT pre_value FROM preference WHERE pre_name = {0})
				WHERE pla_name = '{1}';
			""".format(sizeType,PlayerName))
			db.close()

	return json.dumps("ok"),200,{'Content-Type':'application/json'}


#fonction qui permet de creer une pable vide pour chaque joueur a chaque fois q un nouveau jour commence 
def createTab():
	db = Db()
	name = db.select("SELECT pla_name FROM player;")
	day = db.select("SELECT map_day_nb FROM map;")[0]["map_day_nb"] 

	for i in name:
		print(i["pla_name"])
		sqlVente = (""" INSERT INTO Sale VALUES('{0}', 1, 0,'{1}','limonade');""".format(day, i["pla_name"]))
		db.execute(sqlVente)
		sqlProd = (""" INSERT INTO production VALUES('{0}', 1, 0,'{1}', 'limonade');""".format(day, i["pla_name"]))
		db.execute(sqlProd)
	db.close()

#######################################################################################################################################

#######################################################################################################################################

if __name__ == "__main__":
 	app.run()

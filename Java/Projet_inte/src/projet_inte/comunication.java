/**
 * @date 21/06/2017
 * @author Adrien Corre
 *
 */
/**
 * import necessaire au bon fonctionnement du programme.
 */
package apiJavaProjetInte;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.Iterator;

import org.codehaus.jackson.map.ObjectMapper;
import org.codehaus.jackson.type.TypeReference;
import org.json.JSONArray;
import org.json.JSONObject;
import apiJavaProjetInte.Coordinates;
import apiJavaProjetInte.*;

/**
 * 
 * @author Adrien Corre
 * Déclaration de la classe communication
 */
public class comunication {
	
	private final String USER_AGENT = "Mozilla/5.0"; 					/**Parametre pris en compte pour les requête http */
	
	
	
	
	/**
	 * Définitionn de la fonction sendGet()
	 * @throws Exception capture les exeptions qui peuvent apparaitre et envoie un message qui est directement pris de la classe mere
	 * int responseCode variable qui récupère le code retour émise par le serveur lors de la requête
	 */
	private void sendGet() throws Exception {

			String url = "http://limonade-equipe7.herokuapp.com/rdm";    	 /** url utilisé plus loin pour les requêtes prend le sting url */
			URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
			con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
			con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
			int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
			
			System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
			System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
			
			
			BufferedReader in = new BufferedReader(
			        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
			
			String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
			StringBuffer response = new StringBuffer();
			
			while ((inputLine = in.readLine()) != null) { 
				response.append(inputLine);
			}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
			in.close();

			
			System.out.println(response.toString());						/** Affiche le resultat en string de 'response'*/
	
	
	
	
		}
	
	/**
	 * Définitionn de la fonction Getmap()
	 * @throws Exception capture les exeptions qui peuvent apparaitre et envoie un message qui est directement pris de la classe mere
	 * int responseCode variable qui récupère le code retour émise par le serveur lors de la requête
	 */
	public void Getmap() throws Exception {

			String url = "http://limonade-equipe7.herokuapp.com/map";    	 /** url utilisé plus loin pour les requêtes prend le sting url */
			URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
			con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
			con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
			int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
			
			System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
			System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
			
			
			BufferedReader in = new BufferedReader(
			        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
			
			String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
			StringBuffer response = new StringBuffer();
			
			while ((inputLine = in.readLine()) != null) { 
				response.append(inputLine);
			}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
			in.close();
			
			JSONObject jsonmap= new JSONObject(response.toString());
			ArrayList rank = new ArrayList();
			ArrayList map = new ArrayList();
			
			
			map.add(jsonmap.getJSONObject("region").getJSONObject("center").getDouble("latitude"));
			map.add(jsonmap.getJSONObject("region").getJSONObject("center").getDouble("longitude"));
			map.add(jsonmap.getJSONObject("region").getJSONObject("span").getDouble("latitudeSpan"));
			map.add(jsonmap.getJSONObject("region").getJSONObject("span").getDouble("longitudeSpan"));
			
			for (int i = 0; i < jsonmap.getJSONArray("ranking").length(); i++) {
				
				map.add(jsonmap.getJSONArray("ranking").getString(i));
				rank.add(jsonmap.getJSONArray("ranking").getString(i));
				
			}
			for(int i = 0;i<rank.size();i++){
				for(int j =0;j<jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).length();j++){
				
				map.add(jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getString("kind"));	
				map.add(jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getString("owner"));
				map.add(jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("latitude"));
				map.add(jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("longitude"));
				map.add(jsonmap.getJSONObject("itemsByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("influence"));
				}
			}	
			
			for(int i = 0;i<rank.size();i++){
				
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getDouble("cash"));
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getInt("sales"));
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getDouble("profit"));
				
				for(int j=0;j<jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getJSONArray("drinksOffered").length();j++){
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getJSONArray("drinksOffered").getJSONObject(j).getString("name"));
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getJSONArray("drinksOffered").getJSONObject(j).getDouble("Price"));
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getJSONArray("drinksOffered").getJSONObject(j).getBoolean("hasAlcohol"));
				map.add(jsonmap.getJSONObject("playerInfo").getJSONObject(jsonmap.getJSONArray("ranking").getString(i)).getJSONArray("drinksOffered").getJSONObject(j).getBoolean("isCold"));
				}
			}
				
				for(int i = 0;i<rank.size();i++){
					for (int j =0;j<jsonmap.getJSONObject("drinksByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).length();j++){
					map.add(jsonmap.getJSONObject("drinksByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getString("name"));
					map.add(jsonmap.getJSONObject("drinksByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("price"));
					map.add(jsonmap.getJSONObject("drinksByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getBoolean("hasAlcohol"));
					map.add(jsonmap.getJSONObject("drinksByPlayer").getJSONArray(jsonmap.getJSONArray("ranking").getString(i)).getJSONObject(j).getBoolean("isCold"));
					
					}
					
					
				}
				
				
			
			
	}

	
	private ArrayList GetQuitter() throws Exception {

		String url = "http://limonade-equipe7.herokuapp.com/DELETE/players/<PlayerName>";    	 /** url utilisé plus loin pour les requêtes prend le sting url */
		URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
		con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
		con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
		int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
		
		System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
		System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
		
		
		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
		
		String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
		StringBuffer response = new StringBuffer();
		
		while ((inputLine = in.readLine()) != null) { 
			response.append(inputLine);
		}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
		in.close();

		JSONObject IdToDelete= new JSONObject(response.toString());
		ArrayList name = new ArrayList();
		
		name.add( IdToDelete.getString("name"));
		System.out.println(response.toString());						/** Affiche le resultat en string de 'response'*/
			return name;



	}

	
	private ArrayList GetReset() throws Exception {

		String url = "http://limonade-equipe7.herokuapp.com/reset";    	 /** url utilisé plus loin pour les requêtes prend le sting url */
		URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
		con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
		con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
		int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
		
		System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
		System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
		
		
		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
		
		String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
		StringBuffer response = new StringBuffer();
		
		while ((inputLine = in.readLine()) != null) { 
			response.append(inputLine);
		}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
		in.close();

		JSONObject resetable= new JSONObject(response.toString());
		ArrayList reset = new ArrayList();
		
		reset.add( resetable.getBoolean("reset"));
		System.out.println(response.toString());						/** Affiche le resultat en string de 'response'*/
			return reset;



	}

	
	 ArrayList Getplayers() throws Exception {

		String url = "http://localhost:5000/GET/player";    	 /** url utilisé plus loin pour les requêtes prend le sting url */
		URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
		HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
		con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
		con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
		int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
		
		System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
		System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
		
		
		BufferedReader in = new BufferedReader(
		        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
		
		String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
		StringBuffer response = new StringBuffer();
		
		while ((inputLine = in.readLine()) != null) { 
			response.append(inputLine);
		}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
		in.close();
		System.out.println(response);
		JSONObject addplayers= new JSONObject(response.toString());
		ArrayList newplayer = new ArrayList();
		
		newplayer.add( addplayers.getString("name"));
		newplayer.add( addplayers.getJSONArray("location").getDouble(0));
		newplayer.add( addplayers.getJSONArray("location").getDouble(1));
		newplayer.add( addplayers.getJSONObject("info").getDouble("cash"));
		newplayer.add( addplayers.getJSONObject("info").getDouble("profit"));
		newplayer.add( addplayers.getJSONObject("info").getInt("sales"));
		newplayer.add( addplayers.getJSONObject("info").getJSONArray("drinksOffered").getJSONObject(0).getString("name"));
		newplayer.add( addplayers.getJSONObject("info").getJSONArray("drinksOffered").getJSONObject(0).getDouble("price"));
		newplayer.add( addplayers.getJSONObject("info").getJSONArray("drinksOffered").getJSONObject(0).getBoolean("hasAlcohol"));
		newplayer.add( addplayers.getJSONObject("info").getJSONArray("drinksOffered").getJSONObject(0).getBoolean("isCold"));
		
		
		
		System.out.println(newplayer);						/** Affiche le resultat en string de 'response'*/
			return newplayer;



	}
	
	/**
	 * Définitionn de la fonction Getmap()
	 * @return 
	 * @return une liste de string contenant le temps
	 * @throws Exception capture les exeptions qui peuvent apparaitre et envoie un message qui est directement pris de la classe mere
	 * int responseCode variable qui récupère le code retour émise par le serveur lors de la requête
	 */
	public ArrayList GetWeather() throws Exception {

			String url = "http://limonade-equipe7.herokuapp.com/metrology"	 /**"http://limonade-equipe7.herokuapp.com/GET/metrology"*/;    	 /** url utilisé plus loin pour les requêtes prend le sting url */
			URL obj = new URL(url);                  						 /** Déclaration d'une nouvelle instance de la classe importé URL */
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();/** */
			con.setRequestMethod("GET");									 /** Utilisation de l'option (Passe en 'mode' GET) */
			con.setRequestProperty("User-Agent", USER_AGENT);				 /** Ajoute un header à la requête */
			int responseCode = con.getResponseCode();						 /**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock dans une varibale*/
			
			System.out.println("\nSending 'GET' request to URL : " + url);	/** Affiche la requête envoyé  */
			System.out.println("Response Code : " + responseCode);			/**Affiche la réponse à la requête stocké dans la variable 'responseCode'*/
			
			
			BufferedReader in = new BufferedReader(
			        new InputStreamReader(con.getInputStream()));			/** Déclaration d'un nouvelle objet 'in' de type BuffereReader qui va contenir le flux de données entrant   */ 
			
			String inputLine;												/** Déclare un string pour stocker le conten lu du bufferReader */ 
			StringBuffer response = new StringBuffer();
			
			
			
			while ((inputLine = in.readLine()) != null) { 
				response.append(inputLine);
			}																/** Boucle qui écrit dans response tant que inputLine (qui contient in.readLine) n'est pas  NULL */ 						
			in.close();
			JSONObject entjson= new JSONObject(response.toString());
			ArrayList list = new ArrayList();
			list.add(entjson.getInt("timestamp"));
			list.add(entjson.getJSONArray("weather").getJSONObject(0).getInt("dfn"));
			list.add(entjson.getJSONArray("weather").getJSONObject(0).getString("weather"));
			list.add(entjson.getJSONArray("weather").getJSONObject(1).getInt("dfn"));
			list.add(entjson.getJSONArray("weather").getJSONObject(1).getString("weather"));
			
			System.out.println(list);
			
			return  list;
								
	
	
	
	
		}
	
	
	
	
	
	/**
	 * 
	 * @throws Exception capture les exeptions qui peuvent apparaitre et envoie un message qui est directement pris de la classe mere
	 * Déclaration de la fonction sendPost
	 */
	
		public void sendPost(String name,String recipe,int quantity) throws Exception {
			
			JSONObject sales= new JSONObject("{'player':"+name+",'item':"+recipe+",'quantity':"+quantity+"}"); /**Déclaration d'une nouvelle instance de la classe JSONObject */
			
			
					
			String url = "http://limonade-equipe7.herokuapp.com/sales";											/**Définiton de la nouvelle route  */
			URL obj = new URL(url);																				/** Déclaration  d'une nouvelle instance de la classe URL */
			HttpURLConnection con = (HttpURLConnection) obj.openConnection();									/**Déclaration d'une instance de la classe HttpURLConnection à qui on insére le cast de la fonction l'objet obj.openConnection() */
			con.setRequestMethod("POST");								 										/** Utilisation de l'option (Passe en 'mode' POST) */
			con.setRequestProperty("User-Agent", USER_AGENT);													/** Paramétre de la requête http (nav, safarie, mozilla...)  */
			con.setRequestProperty("Content-Type", "application/json");											/**Paramétrage du type de data  */
			
			
			con.setDoOutput(true);																				/**On utilise la fonction setDoOutput() de l'objet con avec le parametre true */
			DataOutputStream wr = new DataOutputStream(con.getOutputStream());
			wr.writeBytes(sales.toString());																	/**Envoie le contenue de sales stringifier */
			wr.flush();																							/**Nettoie le buffer  */
			wr.close();																							/**Ferme le link qui stream les datas reçu */

			int responseCode = con.getResponseCode();															/**Déclare un int et Récupère la reponse du Get envoyé par le serveur et la stock */ 
			System.out.println("\nSending 'POST' request to URL : " + url);										/**Affiche dans la console'\nSending 'POST' request to URL' puis le contenu de url */
			System.out.println("Post parameters : " + sales );													/**Affiche dans la console 'Post parameter' et le contenu de sales */
			System.out.println("Response Code : " + responseCode);												/**Affiche dans la console 'Response Code' plus le contenu de responseCode */ 
			

			
			con.disconnect();																					/**Met fin à la reqête http */

			
			

		}
	
}
	
	
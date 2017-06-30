package apiJavaProjetInte;
import java.util.Map;
import java.util.HashMap;

import apiJavaProjetInte.comunication;

public class main {

	public static void main(String[] args) throws Exception {			/** Main pour run et/ou tester les requêtes*/

		comunication http = new comunication();							/**Déclaration d'une nouvelle instance de la classe communication  */

		//System.out.println("Testing 1 - Send Http GET request");		/**Affiche l'intérieur des parenthèses sur la console */
	//	http.sendGet();													/**Utilisation de la fonction sendGet() de l'objet http */ 

	////	System.out.println("\nTesting 2 - Send Http POST request");		/**Affiche l'intérieur des parenthèses sur la console */
	///	http.sendPost();												/**Utilisation de la fonction sendPost() de l'objet http */ 

		

		System.out.println("\nTesting 2 - Send Http POST request");		/**Affiche l'intérieur des parenthèses sur la console */
		http.Getplayers();												/**Utilisation de la fonction sendPost() de l'objet http */ 
		/*Map<String,String> m = new HashMap<>();
		
		m.put("toti", "Le toti");
		m.put("toto", "Le toto");
		m.put("tota", "Le tota");
		m.put("tato", "Le tato");
		
		for(String s : m.keySet()){
			System.out.println(s);
		}*/
	}
	
}

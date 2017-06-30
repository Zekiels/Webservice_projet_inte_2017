/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;
import java.util.*;
import org.json.JSONObject;
import projet_inte.*;
/**
 *
 * @author imerir
 */
public class  main {
    
    
    public Map main() throws Exception {
        Communication com =new Communication();
         JSONObject composantCarte= new JSONObject();
         composantCarte = com.Getmap();
        
         
         
        int heure;
        String current_weather;
        String next_weather;
        JSONObject weather= new JSONObject();
        ArrayList<Joueur> joueur= new ArrayList<Joueur>();
        ArrayList<Client> client= new ArrayList<Client>();
        ArrayList<Recette> recette= new ArrayList<Recette>();
        ArrayList<MapItems> Items= new ArrayList<MapItems>();
        
       
        weather = com.GetWeather();
        heure= (weather.getInt("timestamp")%24);
        current_weather=(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));
        next_weather =(weather.getJSONArray("weather").getJSONObject(1).getString("weather"));
        Map carte;
                
       composantCarte =com.Getmap();
       for (int i = 0; i < composantCarte.getJSONObject("map").getJSONArray("ranking").length(); i++) {
            for(int j =0; j < composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).length();j++){
                  
               Items.add(new MapItems(composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("kind"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("owner"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("influence")));
                
               if(composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i))!=null){
                        recette.add(new Recette( composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("name")  ,  composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("price")  ) );
                 }}
            joueur.add(new Joueur(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i),composantCarte.getJSONObject("map").getJSONObject("playerInfo").getJSONObject(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getDouble("cash"),recette,Items));
       }
       
       carte = new Map(composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("longitudeSpan"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("latitudeSpan"),joueur);
        
        
        
        
      carte.NombreClient("");
      return carte;
        
      // for(int i =0;i<composantCarte.getJSONObject("map").getJSONArray("ranking").length();i++){
        //System.out.println( composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(0).getString("name"));
       
       //}
       }
    
    }
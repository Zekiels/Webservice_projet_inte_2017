/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

import java.util.ArrayList;
import java.util.Random;

/**
 *
 * @author Théo
 */
public class Map {
    private float longitude;
    private float lattitude;
    private float long_span;
    private float lat_span;
    private ArrayList<Joueur> joueur;
    private ArrayList<Client> client;
    private static Map INSTANCE = null;
    
    /**
     * Constructeur de la map
     * @param longitude
     * @param lattitude
     * @param long_span
     * @param lat_span
     * @param joueur 
     * @param client 
     */
    private Map(float longitude, float lattitude, float long_span, float lat_span, ArrayList<Joueur> joueur, ArrayList<Client> client) {
        this.longitude = longitude;
        this.lattitude = lattitude;
        this.long_span = long_span;
        this.lat_span = lat_span;
        this.joueur = joueur;
        this.client = client;
    }
    
    /**
     * Creer une instance de map
     * @param longitude
     * @param lattitude
     * @param long_span
     * @param lat_span
     * @param joueur
     * @param client
     * @return l'instance de la map
     */
    public static Map getInstance(float longitude, float lattitude, float long_span, float lat_span, ArrayList<Joueur> joueur, ArrayList<Client> client){
        if (INSTANCE == null){
            INSTANCE = new Map( longitude, lattitude, long_span, lat_span, joueur, client);
        }
        return INSTANCE;
    }
    
    /**
     * 
     * @return la longitude de la map 
     */
    public float getLongitude() {
        return longitude;
    }
    
    /**
     * Définit la longitude de la map
     * @param longitude 
     */
    public void setLongitude(float longitude) {
        this.longitude = longitude;
    }
    
    /**
     * 
     * @return la lattitude de la map
     */
    public float getLattitude() {
        return lattitude;
    }
    
    /**
     * Définit la lattitude de la map
     * @param lattitude 
     */
    public void setLattitude(float lattitude) {
        this.lattitude = lattitude;
    }
    
    /**
     * 
     * @return le span de la map
     */
    public float getLong_span() {
        return long_span;
    }
    
    /**
     * Définit le span de la map
     * @param long_span 
     */
    public void setLong_span(float long_span) {
        this.long_span = long_span;
    }
    
    /**
     * 
     * @return le span de la map
     */
    public float getLat_span() {
        return lat_span;
    }
    
    /**
     * Définit le span de la map
     * @param lat_span 
     */
    public void setLat_span(float lat_span) {
        this.lat_span = lat_span;
    }
    
    /**
     * 
     * @return les joueurs
     */
    public ArrayList<Joueur> getJoueur() {
        return joueur;
    }
    
    /**
     * Définit les joueurs
     * @param joueur 
     */
    public void setJoueur(ArrayList<Joueur> joueur) {
        this.joueur = joueur;
    }

    /**
     * 
     * @return les clients
     */
    public ArrayList<Client> getClient() {
        return client;
    }

    /**
     * Définit les clients
     * @param client 
     */
    public void setClient(ArrayList<Client> client) {
        this.client = client;
    }
    
    /**
     * Mise à jour de la taille de la map
     */
    public void tailleMap(){
        this.lat_span = this.joueur.size()*10;
        this.long_span = this.joueur.size()*10;
    }
    
    /**
     * Mise à jour du nombre de client
     */
    public void NombreClient(){
        /* les messures de la map */
        int min_long = (int) (this.longitude-this.long_span);
        int max_long = (int) (this.longitude+this.long_span);
        int min_lat = (int) (this.lattitude-this.lat_span);
        int max_lat = (int) (this.lattitude+this.lat_span);
        
        /* si il y a trop de client*/
        if (this.client.size() > this.joueur.size()*50){
            /* suppression des clients en trop */
            for(int i=this.client.size(); i>this.joueur.size()*50; i--){
               this.client.get(i).setLattitude(0);
               this.client.get(i).setLongitude(0);
               this.client.get(i).setJoueur(null);
               this.client.remove(i);
            }
           /* si il a pas assez de client */
        }else if (this.client.size() < this.joueur.size()*50){
            /* ajout de nouveau client */
            for(int i=0; this.client.size() < this.joueur.size()*50; i++){
               Random rand = new Random();
               float longi = rand.nextInt(max_long-min_long + 1)+min_long;
               float latti = rand.nextInt(max_lat-min_lat + 1)+min_lat;
               Client client = new Client(longi, latti, joueur);
               this.client.add(client);
            }
       }
    }
    
    /**
     * creation d'un joueur
     * @param nom
     * @param production
     * @param recette
     */
    public void createJoueur(String nom, ArrayList<Prod> production, ArrayList<Recette> recette){
        /* les messures de la map */
        int min_long = (int) (this.longitude-this.long_span);
        int max_long = (int) (this.longitude+this.long_span);
        int min_lat = (int) (this.lattitude-this.lat_span);
        int max_lat = (int) (this.lattitude+this.lat_span);
        
        /* Création du stand du joueur */
        Random rand = new Random();
        float longi = rand.nextInt(max_long-min_long + 1)+min_long;
        float latti = rand.nextInt(max_lat-min_lat + 1)+min_lat;
        Stand stand = new Stand(longi, latti, 5);
        ArrayList<Emplacement> emplacement = new ArrayList();
        emplacement.add(stand);
        
        /* création du joueur */
        Joueur player = new Joueur(nom, 100, production, recette, emplacement);
        this.joueur.add(player);
               
    }
    
    public void LancerVente(ArrayList<String> weather){
        int i=0;
        switch(weather.get(0)){
            case "thunderstrom":
                for(i=this.client.size(); i<this.client.size(); i++){
                    this.client.get(i).analyse();
                }
                break;
            case "rainny":
                for(i=(this.client.size()*85)/100; i<this.client.size(); i++){
                    this.client.get(i).analyse();
                }
                break;
            case "cloudy":
                for(i=(this.client.size()*70)/100; i<this.client.size(); i++){
                    this.client.get(i).analyse();
                }
                break;
            case "sunny":
                for(i = (this.client.size()*25)/100; i<this.client.size(); i++){
                    this.client.get(i).analyse();
                }
                break;
            case "heatwave":
                for(i=0; i<this.client.size(); i++){
                    this.client.get(i).analyse();
                }
                break;
        }
        
    }
   
}

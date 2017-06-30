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
    private double longitude ;
    private double latitude ;
    private double long_span;
    private double lat_span;
    private String current_weather;
    private String next_weather;

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
   public Map(double longitude, double latitude, double long_span, double lat_span, ArrayList<Joueur> joueur) {
        this.longitude = longitude;
        this.latitude = latitude;
        this.long_span = long_span;
        this.lat_span = lat_span;
        this.joueur = joueur;
        this.client =  new ArrayList();
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
    public static Map getInstance(double longitude, double latitude, double long_span, double lat_span, ArrayList<Joueur> joueur){
        if (INSTANCE == null){
            INSTANCE = new Map( longitude, latitude, long_span, lat_span, joueur);
        }
        return INSTANCE;
    }

    public String getCurrent_weather() {
        return current_weather;
    }

    public void setCurrent_weather(String current_weather) {
        this.current_weather = current_weather;
    }
    
    public void setNext_weather(String next_weather) {
        this.next_weather = next_weather;
    }

    public String getNext_weather() {
        return next_weather;
    }
    /**
     * 
     * @return la longitude de la map 
     */
    public double getLongitude() {
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
    public double getLattitude() {
        return latitude;
    }
    
    /**
     * Définit la lattitude de la map
     * @param lattitude 
     */
    public void setLattitude(double lattitude) {
        this.latitude = lattitude;
    }
    
    /**
     * 
     * @return le span de la map
     */
    public double getLong_span() {
        return long_span;
    }
    
    /**
     * Définit le span de la map
     * @param long_span 
     */
    public void setLong_span(double long_span) {
        this.long_span = long_span;
    }
    
    /**
     * 
     * @return le span de la map
     */
    public double getLat_span() {
        return lat_span;
    }
    
    /**
     * Définit le span de la map
     * @param lat_span 
     */
    public void setLat_span(double lat_span) {
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
        this.client=client;
    }
    
    /**
     * Mise à jour de la taille de la map
     */
    public void tailleMap(){
        //this.lat_span = this.joueur.size()*100;
        //this.long_span = this.joueur.size()*100;
    }
    
    /**
     * Mise à jour du nombre de client
     */
    
    public void CheckTime(int heure){
    if(heure==0){
    for(int i=0;i<this.client.size();i++){
        this.client.get(i).setAlready(true);
    }
    }
    
    }
    
    public void NombreClient(String weather){
        /* les messures de la map */
       int coefClient=100;
        switch(weather){
            case "thunderstrom":
                coefClient=20;
                break;
            case "rainny":
                coefClient=50;
                break;
            case "cloudy":
               coefClient=100;
                break;
            case "sunny":
                coefClient=150;
                
                break;
            case "heatwave":
                coefClient=200;
                
                break;
        }
        
        int min_long = 50;
        int max_long = 950;
        int min_lat = 50;
        int max_lat = 950;
        System.out.println(max_lat+""+min_lat);
        
        /* si il y a trop de client*/
        if (this.client.size() > this.joueur.size()*coefClient){
            /* suppression des clients en trop */
            for(int i=this.client.size(); i>this.joueur.size()*coefClient; i--){
               this.client.get(i).setLattitude(0);
               this.client.get(i).setLongitude(0);
               this.client.get(i).setJoueur(null);
               this.client.remove(i);
            }
           /* si il a pas assez de client */
        }else if (this.client.size() < this.joueur.size()*coefClient){
            /* ajout de nouveau client */
            for(int i=0; this.client.size() < this.joueur.size()*coefClient; i++){
               Random rand = new Random();
               double longi = Math.random()*1000;
               double latti = Math.random()*1000;
               
               for(int t=0; t < this.joueur.size();t++){
                 
                   if((longi!=this.joueur.get(t).getItems().get(0).getLongitude())&&(latti!=this.joueur.get(t).getItems().get(0).getLatitude())){
                       if((longi<980 && longi>20)&&(latti<980 && latti>20)){
                        Client client = new Client(longi, latti, joueur);
                         this.client.add(client);}}
               
                   }
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
        int min_long = (int) (this.longitude-this.long_span)+40;
        int max_long = (int) (this.longitude+this.long_span)-40;
        int min_lat = (int) (this.latitude-this.lat_span)-40;
        int max_lat = (int) (this.latitude+this.lat_span)+40;
        
        /* Création du stand du joueur */
        Random rand = new Random();
        float longi = rand.nextInt(max_long-min_long + 1)+min_long;
        float latti = rand.nextInt(max_lat-min_lat + 1)+min_lat;
        Stand stand = new Stand(longi, latti, 20);
        ArrayList<Emplacement> emplacement = new ArrayList();
        emplacement.add(stand);
        
        
               
    }
    public void mapload(double longitude, double latitude, double long_span, double lat_span, ArrayList<Joueur> joueur){
        this.longitude=longitude;
        this.latitude=latitude;
        this.long_span=long_span;
        this.lat_span=lat_span;
        this.joueur=joueur;
       
    
    
    
    
    
    }
    public void movement(){
    for(int i=0;i<this.client.size();i++){
        this.client.get(i).chooseCloser(this.joueur);
        
    }
    }
    
    public void LancerVente(String weather){
        int i=0;
        switch(weather){
            case "thunderstrom":
                for(i=this.client.size(); i<this.client.size(); i++){
                    this.client.get(i).buy();
                }
                break;
            case "rainny":
                for(i=(this.client.size()*85)/100; i<this.client.size(); i++){
                    this.client.get(i).buy();
                }
                break;
            case "cloudy":
                for(i=(this.client.size()*70)/100; i<this.client.size(); i++){
                    this.client.get(i).buy();
                }
                break;
            case "sunny":
                for(i = (this.client.size()*25)/100; i<this.client.size(); i++){
                    this.client.get(i).buy();
                }
                break;
            case "heatwave":
                for(i=0; i<this.client.size(); i++){
                    this.client.get(i).buy();
                }
                break;
        }
        
    }
   
}

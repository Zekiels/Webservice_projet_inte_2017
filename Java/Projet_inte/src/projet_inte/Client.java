/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

import java.util.ArrayList;

/**
 *
 * @author Théo
 */
public class Client {
    private float longitude;
    private float lattitude;
    private ArrayList<Joueur>  joueur;
    
    /**
     * Constructeur de Client
     * @param longitude
     * @param lattitude
     * @param joueur 
     */
    public Client(float longitude, float lattitude, ArrayList<Joueur> joueur) {
        this.longitude = longitude;
        this.lattitude = lattitude;
        this.joueur = joueur;
    }

    /**
     * 
     * @return la longitude du client
     */
    public float getLongitude() {
        return longitude;
    }
    
    /**
     * Définit la longitude d'un client
     * @param longitude 
     */
    public void setLongitude(float longitude) {
        this.longitude = longitude;
    }

    /**
     * 
     * @return la liste de joueur
     */
    public ArrayList<Joueur> getJoueur() {
        return joueur;
    }
    
    /**
     * Définit la liste de joueur 
     * @param joueur 
     */
    public void setJoueur(ArrayList<Joueur> joueur) {
        this.joueur = joueur;
    }
    
    
    
    /**
     * 
     * @return la lattitude d'un client
     */
    public float getLattitude() {
        return lattitude;
    }

    /**
     * Définit la lattitude d'un client
     * @param lattitude 
     */
    public void setLattitude(float lattitude) {
        this.lattitude = lattitude;
    }
    
    public void Target(ArrayList<Emplacement> emplacement){
        //si le client c'est que dans une seule zone d'influence
        if(emplacement.size() == 1){
            
            //retrouve le joueur à qui appartient cette emplacement et produit une vente 
            for(int i=0; i<this.joueur.size(); i++){
                for(int j=0; j<this.joueur.get(i).getEmplacement().size(); j++){
                    if (emplacement.get(0) == this.joueur.get(i).getEmplacement().get(j)){
                        this.joueur.get(i).CalculVente();
                    }
                }
            }
            
        //si le client est que dans plusieur zone d'influence
        }else if (emplacement.size()>1){
            double preDistance = Math.sqrt(Math.pow((emplacement.get(0).lattitude-this.lattitude), 2.0)+Math.pow((emplacement.get(0).longitude-this.longitude), 2.0));
            int target = 0;
            // Choisie l'emplacement vers lequel le client vas aller
            for(int i=1; i<emplacement.size(); i++){
                //calcul de la distance entre le client et un emplacement
                double distance = Math.sqrt(Math.pow((emplacement.get(i).lattitude-this.lattitude), 2.0)+Math.pow((emplacement.get(i).longitude-this.longitude), 2.0));
                if (distance<preDistance){
                    preDistance = distance;
                    target = i;
                    
                }else if (distance==preDistance){
                    //AMELIORATION CALCULER LA MOYENNE DES PRIX DE TOUTE LES BOISSONS PRODUITE
                    float prePrix = Float.POSITIVE_INFINITY;
                    float prix = 0;

                    //retrouve le joueur à qui appartient l'emplacement et récuppère le prix des limonades
                    for(int x=0; x<this.joueur.size(); x++){
                        for(int y=0; y<this.joueur.get(x).getEmplacement().size(); y++){
                            if (emplacement.get(target) == this.joueur.get(x).getEmplacement().get(y)){
                                prePrix = this.joueur.get(x).getProduction().get(0).prixVente;
                            }else if(emplacement.get(i) == this.joueur.get(x).getEmplacement().get(y)){
                                prix = this.joueur.get(x).getProduction().get(0).prixVente;
                            }
                        }
                    }

                    if(prix<prePrix){
                        preDistance = distance;
                        target = i;
                    }
                }
            }
            
            //retrouve le joueur à qui appartient cette emplacement et produit une vente 
            for(int i=0; i<this.joueur.size(); i++){
                for(int j=0; j<this.joueur.get(i).getEmplacement().size(); j++){
                    if (emplacement.get(target) == this.joueur.get(i).getEmplacement().get(j)){
                        this.joueur.get(i).CalculVente();
                    }
                }
            }
            
        //si le client n'est dans aucune zone d'influence
        }else if (emplacement.size()<=0){
            double preDistance = Math.sqrt(Math.pow((this.joueur.get(0).getEmplacement().get(0).lattitude-this.lattitude), 2.0)+Math.pow((this.joueur.get(0).getEmplacement().get(0).longitude-this.longitude), 2.0));
            int target = 0;
            for(int j=1; j<this.joueur.size(); j++){
                for(int i=0; i<this.joueur.get(j).getEmplacement().size(); i++){
                    //calcul de la distance entre le client et un emplacement
                    double distance = Math.sqrt(Math.pow((this.joueur.get(j).getEmplacement().get(i).lattitude-this.lattitude), 2.0)+Math.pow((this.joueur.get(j).getEmplacement().get(i).longitude-this.longitude), 2.0));
                    if (distance<preDistance){
                        preDistance = distance;
                        target = j;
                    }else if (distance==preDistance){
                        //AMELIORATION CALCULER LA MOYENNE DES PRIX DE TOUTE LES BOISSONS PRODUITE
                        /* récupère les prix de la limonade */
                        float prePrix = this.joueur.get(target).getProduction().get(0).prixVente;
                        float prix = this.joueur.get(j).getProduction().get(0).prixVente;

                        if(prix<prePrix){
                            preDistance = distance;
                            target = i;
                        }
                    }
                }
            }
            
            this.joueur.get(target).CalculVente();
        }
    }
    
    public void Move(){
        //TODO
        //déplacement du client jusqu'au stand
    }
    
    /* recherche tout les zones dans lesquelles ce trouve dans le client */
    public void analyse(){
        ArrayList<Emplacement> zone = new ArrayList();
        ArrayList<Emplacement> tab = new ArrayList();
        
        /* parcours de joueur */
        for(int i=0; i<this.joueur.size(); i++){
            tab = this.joueur.get(i).getEmplacement();
            /* parcours des emplacements des joueurs */
            for(int j=0; j<tab.size(); j++){
                /* si le client est dans la zone d'influence de l'emplacement */
                if (tab.get(j).lattitude + tab.get(j).influence > this.lattitude && tab.get(j).lattitude-tab.get(j).influence<this.lattitude){
                    if (tab.get(j).longitude+tab.get(j).influence>this.longitude && tab.get(j).longitude-tab.get(j).influence<this.longitude){
                        /* ajout de l'emplacement */
                        zone.add(tab.get(j));
                    }
                }        
            }
        }
        /* envoie des emplacements dans targets */
        Target(zone);
    }
    
}

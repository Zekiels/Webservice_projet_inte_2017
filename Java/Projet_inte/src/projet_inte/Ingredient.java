/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

import java.util.Random;

/**
 *
 * @author Théo
 */
public class Ingredient {
    private String nom;
    private float prix;
    
    /**
     * constructeur d'ingrédient
     * @param nom
     * @param prix 
     */
    public Ingredient(String nom, float prix) {
        this.nom = nom;
        this.prix = prix;
    }
    
    /**
     * retourne le nom de l'ingrédient  
     * @return 
     */
    public String getNom() {
        return nom;
    }
    
    /**
     * définit le nom de l'ingrédient
     * @param nom 
     */
    public void setNom(String nom) {
        this.nom = nom;
    }
    
    /**
     * 
     * @return le prix de l'ingrédient
     */
    public float getPrix() {
        return prix;
    }
     /**
      *  définit le prix de l'ingrédient
      * @param prix 
      */
    public void setPrix(float prix) {
        this.prix = prix;
    }
    
    /**
     * calcul la nouveau prix des ingrédients
     */
    public void fluctuation(){
        Random rand = new Random();
        float nombreAleatoire = rand.nextInt(100 + 1)-50;
        nombreAleatoire /= 10;
        nombreAleatoire = this.prix+(this.prix*nombreAleatoire)/100;
        
        /* tronquage à 2 nombres après la virgule*/
        nombreAleatoire *= 100;
        nombreAleatoire = (float) Math.floor(nombreAleatoire);
        this.prix =nombreAleatoire /= 100;
    }
}

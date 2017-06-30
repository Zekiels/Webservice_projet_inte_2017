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
public class Recette {
    private String nom;
    private double prix;
   
    
    /**
     * Constructeur
     * @param nom
     * @param cout
     * @param composition 
     */
    public Recette(String nom, double prix) {
        this.prix = prix;
        this.nom = nom;
       
    }
    
    /**
     * 
     * @return le prix de la recette
     */
    public double getPrix() {
        return prix;
    }

    /**
     * Définit le prix de la recette
     * @param prix 
     */
    public void setPrix(double prix) {
        this.prix = prix;
    }
    
    /**
     * 
     * @return le nom de la recette
     */
    public String getNom() {
        return nom;
    }
    
    /**
     * Définit le nom de la recette
     * @param nom 
     */
    public void setNom(String nom) {
        this.nom = nom;
    }
   
}

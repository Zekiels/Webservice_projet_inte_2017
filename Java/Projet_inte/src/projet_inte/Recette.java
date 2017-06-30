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
    private float cout;
    private float prix;
    private ArrayList<Ingredient> composition;
    
    /**
     * Constructeur
     * @param nom
     * @param cout
     * @param composition 
     */
    public Recette(String nom, float cout, float prix, ArrayList<Ingredient> composition) {
        this.prix = prix;
        this.nom = nom;
        this.cout = cout;
        this.composition = composition;
    }
    
    /**
     * 
     * @return le prix de la recette
     */
    public float getPrix() {
        return prix;
    }

    /**
     * Définit le prix de la recette
     * @param prix 
     */
    public void setPrix(float prix) {
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
    
    /**
     * 
     * @return le cout de la recette
     */
    public float getCout() {
        return cout;
    }

    /**
     * Définit le cout de la recette
     * @param cout 
     */
    public void setCout(float cout) {
        this.cout = cout;
    }

    /**
     * 
     * @return la composition
     */
    public ArrayList<Ingredient> getComposition() {
        return composition;
    }

    /**
     * Définit la composition
     * @param composition 
     */
    public void setComposition(ArrayList<Ingredient> composition) {
        this.composition = composition;
    }
    
    /**
     * Calcul le nouveau cout de la recette
     */
    public void CalculCout(){
        float newCout =0;
        for(int i = 0; this.composition.size()>i; i++ ){
            newCout += this.composition.get(i).getPrix();
        }
        this.cout = newCout;
    }
}

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
public class Joueur {
   private int quantity=0;
   
    private String nom;
    private double budget;
    protected ArrayList<MapItems> items;
    
    
    private ArrayList<Recette> recette;
    
    
    /**
     * Constructeur du joueur
     * @param nom
     * @param budget
     * @param production
     * @param recette 
     * @param emplacement 
     */
    public Joueur(String nom, double budget, ArrayList<Recette> recette, ArrayList<MapItems> items) {
        this.nom = nom;
        this.budget = budget;
        this.items =items;
        this.recette = recette;
       
    }  
    public void resetQuantity(int quantity){
    this.quantity=quantity;} 
    
    public void setQuantity(int quantity) {
   this.quantity = this.quantity+quantity;
    }

    public int getQuantity() {
        return quantity;
    }
    
    /**
     * 
     * @return le nom du joueur
     */
    public String getNom() {
        return nom;
    }
    
    /**
     * Définit le nom du joueur
     * @param nom 
     */
    public void setNom(String nom) {
        this.nom = nom;
    }
    
    /**
     * 
     * @return le budget du joueur 
     */
    public double getBudget() {
        return budget;
    }

    /**
     * Définit le buget du joueur
     * @param budget 
     */
    public void setBudget(float budget) {
        this.budget = budget;
    }

public ArrayList<MapItems> getItems(){

 return items;
}
    /**
     * 
     * @return Les recettes du joueur
     */
    public ArrayList<Recette> getRecette() {
        return recette;
    }

    /**
     * Définit les recettes du joueur 
     * @param recette 
     */
    public void setRecette(ArrayList<Recette> recette) {
        this.recette = recette;
    }

   
    
    
}

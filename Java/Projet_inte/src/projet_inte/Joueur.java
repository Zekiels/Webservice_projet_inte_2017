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
    
    private String nom;
    private float budget;
    private ArrayList<Prod> production;
    private ArrayList<Recette> recette;
    private ArrayList<Emplacement>  emplacement;
    
    /**
     * Constructeur du joueur
     * @param nom
     * @param budget
     * @param production
     * @param recette 
     * @param emplacement 
     */
    public Joueur(String nom, float budget, ArrayList<Prod> production, ArrayList<Recette> recette, ArrayList<Emplacement>  emplacement) {
        this.nom = nom;
        this.budget = budget;
        this.production = production;
        this.recette = recette;
        this.emplacement = emplacement;
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
    public float getBudget() {
        return budget;
    }

    /**
     * Définit le buget du joueur
     * @param budget 
     */
    public void setBudget(float budget) {
        this.budget = budget;
    }

    /**
     * 
     * @return La production du joueur
     */
    public ArrayList<Prod> getProduction() {
        return production;
    }

    /**
     * Définit la production du joueur
     * @param production 
     */
    public void setProduction(ArrayList<Prod> production) {
        this.production = production;
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

    /**
     * 
     * @return les emplacements du joueur
     */
    public ArrayList<Emplacement> getEmplacement() {
        return emplacement;
    }

    /**
     * Définit les emplacements du joueur
     * @param emplacement 
     */
    public void setEmplacement(ArrayList<Emplacement> emplacement) {
        this.emplacement = emplacement;
    }
    
    /**
     * calcul le cout de la production et met le budget à jour
     */
    public void CalculProd(){
        /* parcours les productions du joueur */
        for(int i=0; i<this.production.size(); i++){
            /* parcours des recettes du joueur */
            for(int j=0; j<this.recette.size(); j++){
               /* Si la prod et la recette ont le même nom de boisson on met à jour le budjet */
               if( this.production.get(i).recette == this.recette.get(j).getNom()){
                   this.budget -= this.production.get(i).quantite*this.recette.get(j).getCout();
               }
            }
        } 
    }
    
    /**
     * Vérifie si le stock n'est pas à 0
     * @return 1 si plus de stock et 0 si il en reste
     */
    public int stockProd(){
        int stock=0;
        /* Vérification du stock de boisson */
        for(int i=0; i<this.production.size(); i++){
            if (this.production.get(i).quantite == 0){
                stock++;
            }
        }
        
        /* Si le nombre de stock vide est égale au nombre de boisson prod */
        if(stock == this.production.size()){
            return 1;
        }else{
            return 0;
        }
    }
    
    /**
     * Produit une vente et met le budget à jour
     * @return 1 si aucune vente n'est possible 0 sinon
     */
    public int CalculVente(){
        boolean vente = false;
        if (stockProd() == 0){
            /* Tant qu'aucune vente n'as été faite */
            while(vente == false){
                /* vente d'une boisson aléatoire */
                Random rand = new Random();
                int nombreAleatoire = rand.nextInt(this.production.size());
                if (this.production.get(nombreAleatoire).quantite > 0){
                    this.production.get(nombreAleatoire).quantite -= 1;
                    this.budget += this.production.get(nombreAleatoire).prixVente;
                    vente = true;
                }
            }
            return 0;
        }else{
            return 1;
        }
    }
}

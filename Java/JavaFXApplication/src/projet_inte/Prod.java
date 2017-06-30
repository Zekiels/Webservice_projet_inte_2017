/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

/**
 *
 * @author Théo
 */
public class Prod {
    public String recette;
    public int quantite;
    public float prixVente;

    /**
     * 
     * @param recette
     * @param quantite
     * @param prixVente 
     */
    public Prod(String recette, int quantite, float prixVente) {
        this.recette = recette;
        this.quantite = quantite;
        this.prixVente = prixVente;
    }
    
    /**
     * 
     * 
     * @return 
     */
    public String getRecette() {
        return recette;
    }

    /**
     * 
     * @param recette 
     */
    public void setRecette(String recette) {
        this.recette = recette;
    }

    /**
     * 
     * @return 
     */
    public int getQuantite() {
        return quantite;
    }

    /**
     * 
     * @param quantité 
     */
    public void setQuantite(int quantite) {
        this.quantite = quantite;
    }

    /**
     * 
     * @return 
     */
    public float getPrixVente() {
        return prixVente;
    }

    /**
     * 
     * @param prixVente 
     */
    public void setPrixVente(float prixVente) {
        this.prixVente = prixVente;
    }
    
    
}

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
public abstract class Emplacement {
    protected float longitude;
    protected float lattitude;
    protected float influence;
    protected Joueur propietaire;
    
    /**
     * 
     * @return la longitude d'un emplacement 
     */
    public float getLongitude() {
        return longitude;
    }
    
    /**
     * Définit la longitude d'un emplacement
     * @param longitude 
     */
    public void setLongitude(float longitude) {
        this.longitude = longitude;
    }
    
    /**
     * 
     * @return la lattitude d'un emplacement
     */
    public float getLattitude() {
        return lattitude;
    }
    
    /**
     * Définit la lattitude d'un emplacement
     * @param lattitude 
     */
    public void setLattitude(float lattitude) {
        this.lattitude = lattitude;
    }
    
    /**
     * 
     * @return l'influence d'un emplacement
     */
    public float getInfluence() {
        return influence;
    }
    
    /**
     * Définit l'influence d'un emplacement
     * @param influence 
     */
    public void setInfluence(float influence) {
        this.influence = influence;
    }

    /**
     * 
     * @return le propriétaire de cette emplacement
     */
    public Joueur getPropietaire() {
        return propietaire;
    }

    /**
     * Définit le propriétaire de cette emplacement
     * @param propietaire 
     */
    public void setPropietaire(Joueur propietaire) {
        this.propietaire = propietaire;
    }
    
    /**
     * 
     */
    public void calculConflit(){
        
    }
    
    
}

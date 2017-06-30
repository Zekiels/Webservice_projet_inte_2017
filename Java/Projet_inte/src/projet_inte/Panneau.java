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
public class Panneau extends Emplacement {
    
    public Panneau(float longitude, float lattitude, float influence) { //A CHANGER
        this.longitude = longitude;
        this.lattitude = lattitude;
        this.influence = influence;
    }
    
    /**
     * 
     * @return la longitude d'un emplacement 
     */
    @Override
    public float getLongitude() {
        return longitude;
    }
    
    /**
     * Définit la longitude d'un emplacement
     * @param longitude 
     */
    @Override
    public void setLongitude(float longitude) {
        this.longitude = longitude;
    }
    
    /**
     * 
     * @return la lattitude d'un emplacement
     */
    @Override
    public float getLattitude() {
        return lattitude;
    }
    
    /**
     * Définit la lattitude d'un emplacement
     * @param lattitude 
     */
    @Override
    public void setLattitude(float lattitude) {
        this.lattitude = lattitude;
    }
    
    /**
     * 
     * @return l'influence d'un emplacement
     */
    @Override
    public float getInfluence() {
        return influence;
    }
    
    /**
     * Définit l'influence d'un emplacement
     * @param influence 
     */
    @Override
    public void setInfluence(float influence) {
        this.influence = influence;
    }
    
    /**
     * 
     */
    @Override
    public void calculConflit(){
        
    }
    
}

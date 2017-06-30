/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

/**
 *
 * @author imerir
 */
public class MapItems {
    
    protected String kind;
    protected String owner;
    protected double longitude;
    protected double latitude;
    protected double influence;
    
    
    public MapItems(String kind,String owner,double longitude,double latitude,double influence){
    
    this.kind=kind;
    this.owner=owner;
    this.longitude=longitude;
    this.latitude=latitude;
    this.influence=influence;
    }

    public String getKind() {
        return kind;
    }

    public String getOwner() {
        return owner;
    }

    public double getLongitude() {
        return longitude;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getInfluence() {
        return influence;
    }
    
    
    
    
}

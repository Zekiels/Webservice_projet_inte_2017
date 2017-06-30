/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package projet_inte;

import Graph.GraphSwing;
import java.util.ArrayList;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Application;

/**
 *
 * @author Théo
 */
public class Projet_inte {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        /*        
        *   SETUP 
        */
        
        /* ingrédient limonade */
        Ingredient cit = new Ingredient("citron", (float) 0.20);
        Ingredient suc = new Ingredient("sucre", (float) 0.20);
        Ingredient gla = new Ingredient("glace", (float) 0.02);
        Ingredient eau = new Ingredient("eau", (float) 0);
        
        /* Recette de la limonade */
        ArrayList<Ingredient> composition = new ArrayList();
        composition.add(cit);
        composition.add(suc);
        composition.add(gla);
        composition.add(eau);
        composition.add(eau);
        
        Recette limonade = new Recette("limonade", (float)0, (float)0, composition);
        
        /* Création de la prod */
        Prod prod = new Prod("limonade", 40, (float)1.50);
                
        /* Création de la map */
        ArrayList<Client> client = new ArrayList();
        ArrayList<Joueur> joueur = new ArrayList();
        
        Map carte = Map.getInstance(0, 0, 10, 10, joueur, client);
        
        ArrayList<Recette> recette = new ArrayList();
        recette.add(limonade);
        ArrayList<Prod> production = new ArrayList();
        production.add(prod);
        
        carte.createJoueur("player 1", production, recette);
        carte.tailleMap();
        carte.createJoueur("player 2", production, recette);
        carte.tailleMap();
        carte.NombreClient();
        
        Communication com = new Communication();
        
        /*
        *  JEU DE TEST
        */
        
        /* affichage taille map */
        System.out.println("Taille map :");
        System.out.println(carte.getLat_span());
        System.out.println(carte.getLong_span());
        System.out.println(carte.getLattitude());
        System.out.println(carte.getLongitude());
        System.out.println();
        
        ArrayList<Joueur> jou = carte.getJoueur();
        /* Affichage des positions des stands des joueurs */
        System.out.println("Affichage des positions des joueurs");
        for (int i=0; i<jou.size(); i++){
            System.out.println(jou.get(i).getEmplacement().get(0).lattitude);
            System.out.println(jou.get(i).getEmplacement().get(0).longitude);
        }
        System.out.println();
        
        limonade.CalculCout();
        
        
        /* Création de la prod */
        for (int i=0; i<jou.size(); i++){
            jou.get(i).CalculProd();
        }
        
        /* Affichage du budget */
        System.out.println("Affichage des budget: ");
        for (int i=0; i<jou.size(); i++){
            System.out.println(jou.get(i).getBudget());
        }
        System.out.println();
        
        /* Récupération de la météo et lancement des ventes */
        //ArrayList<String> weather = new ArrayList();
        //weather.add("sunny");
        try {
            carte.LancerVente(com.GetWeather());
        } catch (Exception ex) {
            Logger.getLogger(Projet_inte.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        /* Affichage du budget */
        System.out.println("Affichage des budget: ");
        for (int i=0; i<jou.size(); i++){
            System.out.println(jou.get(i).getBudget());
        }
        System.out.println();
        
        Application.launch(GraphSwing.class, args);
    }
    
}

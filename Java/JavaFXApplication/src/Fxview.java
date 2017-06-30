/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.awt.Image;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Text;

import javafx.stage.Stage;
import javax.swing.JPanel;
import org.json.JSONObject;
import projet_inte.*;

/**
 *
 * @author imerir
 */
public class Fxview extends Application {
         ArrayList <Circle>cercles =new ArrayList<Circle>();
        Communication com =new Communication();
        JSONObject composantCarte= new JSONObject();
        
        int heure;
         int current;
        JSONObject weather= new JSONObject();
         Map carte;
       
       public static void main(String[] args) {
        launch(args);
    }
    @Override
    public void start(Stage primaryStage) throws Exception {
        
                        weather = com.GetWeather();
                        composantCarte = com.Getmap();
                        System.out.println(weather);
                       
                        String current_weather;
                        String next_weather;
                        
                        ArrayList<Joueur> joueur= new ArrayList<Joueur>();
                        ArrayList<Recette> recette= new ArrayList<Recette>();
                        ArrayList<MapItems> Items= new ArrayList<MapItems>();
                        Map carte;

                        
                        
                      for (int i = 0; i < composantCarte.getJSONObject("map").getJSONArray("ranking").length(); i++) {
                            for(int j =0; j <composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).length();j++){

                               Items.add(new MapItems(composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("kind"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("owner"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("influence")));

                               //if(composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i))!=null){
                                        recette.add(new Recette( composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("name")  ,  composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("price")  ) );
                                 //}
                                         }
                            joueur.add(new Joueur(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i),composantCarte.getJSONObject("map").getJSONObject("playerInfo").getJSONObject(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getDouble("cash"),recette,Items));
                       }
                      
                       carte =new Map(composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("longitudeSpan"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("latitudeSpan"),joueur);
                      // System.out.println(weather.getInt("timestamp"));
                        carte.setCurrent_weather(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));
                        carte.setCurrent_weather(weather.getJSONArray("weather").getJSONObject(1).getString("weather"));
                       // System.out.println(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));
                        //System.out.println(weather.getJSONArray("weather").getJSONObject(1).getString("weather"));
                      carte.NombreClient(carte.getCurrent_weather());
        
        
                         heure=com.GetDay();
                         current=heure;

        Timer timer = new Timer();
        timer.schedule(new TimerTask() {

            @Override
            public void run() {
                
                Platform.runLater(() -> {
                    try {
                        Fxview view = new Fxview();
                        
                        //System.out.println(carte.getLat_span());
                         weather=com.GetWeather();
                        
                        
                        heure=com.GetDay();
                         System.out.println(com.GetDay());
                        // System.out.println(carte.getCurrent_weather());
                         if(heure!=current){
                             current=heure;
                        for(int i=0;i<carte.getJoueur().size();i++){
                             com.sendPost(carte.getJoueur().get(i).getNom() ,"limonade" ,carte.getJoueur().get(i).getQuantity());
                             System.out.println("ENVOIE DU SALES"+carte.getJoueur().get(i).getNom() +"limonade" +carte.getJoueur().get(i).getQuantity());
                             carte.getJoueur().get(i).resetQuantity(0);
                             for(int j=0;j< carte.getClient().size();j++){
                             if(carte.getClient().get(j).isAlready()==false){
                             carte.getClient().get(j).setAlready(true);
                             carte.getClient().clear();
                             
                             }
                             }
                         }
                         composantCarte = com.Getmap();
                          for (int i = 0; i < composantCarte.getJSONObject("map").getJSONArray("ranking").length(); i++) {
                            for(int j =0; j <composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).length();j++){

                               Items.add(new MapItems(composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("kind"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("owner"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getJSONObject("location").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("itemsByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("influence")));

                               //if(composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i))!=null){
                                        recette.add(new Recette( composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getString("name")  ,  composantCarte.getJSONObject("map").getJSONObject("drinksByPlayer").getJSONArray(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getJSONObject(j).getDouble("price")  ) );
                                 //}
                                         }
                            joueur.add(new Joueur(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i),composantCarte.getJSONObject("map").getJSONObject("playerInfo").getJSONObject(composantCarte.getJSONObject("map").getJSONArray("ranking").getString(i)).getDouble("cash"),recette,Items));
                       }
                      
                       carte.mapload(composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("longitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("center").getDouble("latitude"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("longitudeSpan"),composantCarte.getJSONObject("map").getJSONObject("region").getJSONObject("span").getDouble("latitudeSpan"),joueur);
                      // System.out.println(weather.getInt("timestamp"));
                        carte.setCurrent_weather(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));
                        carte.setCurrent_weather(weather.getJSONArray("weather").getJSONObject(1).getString("weather"));
                       // System.out.println(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));
                        //System.out.println(weather.getJSONArray("weather").getJSONObject(1).getString("weather"));
                      carte.NombreClient(carte.getCurrent_weather());
                             System.out.println(carte.getCurrent_weather());
                         
                         }

                         
                         
                          for(int i=0; i<carte.getJoueur().size();i++)
                        {for(int j=0;j<carte.getJoueur().get(i).getItems().size();j++){
                          Circle cercle = new Circle (carte.getJoueur().get(i).getItems().get(j).getLongitude(), carte.getJoueur().get(i).getItems().get(j).getLatitude(), 10);
                                cercle.setFill(Color.RED);
                                cercle.setStroke(Color.BLACK);
                                cercles.add(cercle);
                                    System.out.println(carte.getJoueur().get(i).getItems().get(j).getLongitude()+" "+ carte.getJoueur().get(i).getItems().get(j).getLatitude());
                        }
                        }
                         
                         
                         
                         
                         
                         
                                
                    
                        primaryStage.setTitle("Melordi");
                        Group root = new Group();
                        Scene scene = new Scene(root, 1000, 1500, Color.WHITE);
                         
                       
                        primaryStage.setScene(scene);
                        
                       /* Circle cercle = new Circle();
                        cercle.setCenterX(300);
                        cercle.setCenterY(200);
                        cercle.setRadius(100);
                        cercle.setFill(Color.YELLOW);
                        cercle.setStroke(Color.ORANGE);
                        cercle.setStrokeWidth(5);*/

                        Rectangle rectangle = new Rectangle();
                        rectangle.setX(0);
                        rectangle.setY(0);
                        rectangle.setWidth(1000);
                        rectangle.setHeight(200);
                        rectangle.setFill(Color.LIGHTBLUE);
                        rectangle.setStroke(Color.DARKGREEN);
                        rectangle.setStrokeWidth(5);
                        rectangle.setArcHeight(30);
                        rectangle.setArcWidth(30);
                        Text text1=new Text();
                        text1.setX(200);
                        text1.setY(100);
                        
                       text1.setText("Current Weather"+carte.getCurrent_weather()+"Tomorrow Weather"+carte.getNext_weather()+"it's"+weather.getInt("timestamp")%24+"H");
                     
                        root.getChildren().add(rectangle);//On ajoute le rectangle après le cercle
                        root.getChildren().add(text1);
                        for(int i=0;i<cercles.size();i++){
                        root.getChildren().add(cercles.get(i));
                        }
    

                        primaryStage.setScene(scene);
                       primaryStage.show();
                        cercles.clear();
/*
                         
                        StackPane root = new StackPane();

                        BorderPane temps =new BorderPane();
                   //     Canvas canvas =new Canvas(carte.getLong_span(),200);
                        Canvas canvasB = new Canvas(carte.getLong_span(),carte.getLat_span());

                        //System.out.println(carte.getLong_span()+""+carte.getLat_span());


                        GraphicsContext gb = canvasB.getGraphicsContext2D();
                       //  GraphicsContext time = canvas.getGraphicsContext2D();
                        gb.setFill(Color.RED);
                       for(int i=0; i<carte.getJoueur().size();i++)
                        {for(int j=0;j<carte.getJoueur().get(i).getItems().size();j++){
                         gb.fillRect(carte.getJoueur().get(i).getItems().get(j).getLongitude(), carte.getJoueur().get(i).getItems().get(j).getLatitude(), 10, 10);
                                    System.out.println(carte.getJoueur().get(i).getItems().get(j).getLongitude()+" "+ carte.getJoueur().get(i).getItems().get(j).getLatitude());
                        }
                        }
                       gb.setFill(Color.BLUE);
                       for(int i=0; i<carte.getClient().size();i++){
                         gb.fillRect(carte.getClient().get(i).getLongitude(),carte.getClient().get(i).getLatitude(), 5, 5);
                                    System.out.println(carte.getClient().get(i).getLongitude()+" "+carte.getClient().get(i).getLatitude());

                        }
                      // gb.fillRect(500, 500, 10, 10);




                      //  System.out.println(weather.getJSONArray("weather").getJSONObject(0).getString("weather"));

                        root.getChildren().addAll(canvasB);



                        primaryStage.setTitle("visuel");
                        primaryStage.setScene(new Scene(root));
                        primaryStage.show();*/
                       // carte.movement();
                    } catch (Exception ex) {
                        Logger.getLogger(Fxview.class.getName()).log(Level.SEVERE, null, ex);
                    }
                });
            }
        }, 0, 3000);
    }

    }

    /**
     * @param args the command line arguments
     */
 
    


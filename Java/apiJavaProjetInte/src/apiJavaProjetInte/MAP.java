package apiJavaProjetInte;
import apiJavaProjetInte.MapItem;
import apiJavaProjetInte.Region;
import apiJavaProjetInte.DrinkInfo;
import apiJavaProjetInte.PlayerInfo;
import java.util.HashMap;
import java.util.Map;

public class MAP {

		Region region;
		String[] ranking;
		Map<String,MapItem[]> itemsByPlayer;
		Map<String, PlayerInfo[]>playerInfo;
		Map<String,DrinkInfo[]>drinksByPlayer;
}

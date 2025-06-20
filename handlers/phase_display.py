from typing import Any, Optional
from utils.weapon_utils import categorize_weapons


class PhaseDisplayHandler:
    def __init__(self, logger):
        self.logger = logger
    
    def display_freezetime_info(self, player: Any, steamid: str, game_map: Any):
        """Display comprehensive information during freezetime phase."""
        self.logger.info("[ACTION] Entered 'freezetime' — prepping for next round.")
        
        self._display_match_stats(player)
        self._display_round_start_info(player)
        self._display_loadout(player)
        self._display_map_info(game_map)
    
    def _display_match_stats(self, player: Any):
        """Display player and match statistics."""
        match_stats = getattr(player, "match_stats", None)
        if match_stats is None:
            self.logger.warning("No match_stats found in payload.")
            return

        self.logger.info("[PLAYER]")
        self.logger.info(f"  NAME: {player.name}")
        self.logger.info(f"  TEAM: {player.team}")

        self.logger.info("[MATCH STATS]")
        self.logger.info(f"  Kills: {match_stats.kills or 0}")
        self.logger.info(f"  Assists: {match_stats.assists or 0}")
        self.logger.info(f"  Deaths: {match_stats.deaths or 0}")
        self.logger.info(f"  MVPs: {match_stats.mvps or 0}")
        self.logger.info(f"  Score: {match_stats.score or 0}")
    
    def _display_round_start_info(self, player: Any):
        """Display round start information like money and armor."""
        state = getattr(player, "state", None)
        if not state:
            self.logger.warning("No player state found.")
            return

        money = getattr(state, "money", None)
        armor = getattr(state, "armor", None)
        has_helmet = getattr(state, "helmet", None)

        self.logger.info("[ROUND START]")
        self.logger.info(f"  Money: ${money if money is not None else 'N/A'}")
        self.logger.info(f"  Armor: {armor if armor is not None else 'N/A'}")
        self.logger.info(f"  Helmet: {'Yes' if has_helmet else 'No' if has_helmet is not None else 'N/A'}")
    
    def _display_loadout(self, player: Any):
        """Display player weapon loadout."""
        weapons = getattr(player, "weapons", {})
        if not weapons:
            self.logger.warning("No weapon data available.")
            return

        weapon_categories = categorize_weapons(weapons)

        self.logger.info("[LOADOUT]")
        for category, weapon_list in weapon_categories.items():
            if weapon_list:
                category_display = category.title()
                if category == "others":
                    category_display = "Other"
                self.logger.info(f"  {category_display}: {', '.join(weapon_list)}")
    
    def _display_map_info(self, game_map: Any):
        """Display map and round information."""
        if not game_map:
            self.logger.warning("No map data found in payload.")
            return

        map_name = getattr(game_map, "name", "unknown")
        map_mode = getattr(game_map, "mode", "unknown")
        round_num = getattr(game_map, "round", "?")

        team_ct_score = getattr(game_map.team_ct, "score", 0)
        team_t_score = getattr(game_map.team_t, "score", 0)

        self.logger.info(f"[MAP INFO] Map: {map_name} | Mode: {map_mode}")
        self.logger.info(f"[MAP INFO] Round: {round_num}")
        self.logger.info(f"[SCORE] CT: {team_ct_score} | T: {team_t_score}")

        round_wins = getattr(game_map, "round_wins", {})
        if round_wins:
            self.logger.info("[ROUND HISTORY]")
            for rnd, result in sorted(round_wins.items(), key=lambda x: int(x[0])):
                self.logger.info(f"  Round {rnd}: {result}")


    def collect_freezetime_info(self, player: Any, game_map: Any) -> dict:
        """Collect structured freezetime data for LLM or analysis."""
        match_stats = getattr(player, "match_stats", {})
        state = getattr(player, "state", {})
        weapons = getattr(player, "weapons", {})
        weapon_categories = categorize_weapons(weapons)

        map_name = getattr(game_map, "name", "unknown")
        map_mode = getattr(game_map, "mode", "unknown")
        round_num = getattr(game_map, "round", "?")
        team_ct_score = getattr(game_map.team_ct, "score", 0)
        team_t_score = getattr(game_map.team_t, "score", 0)
        round_wins = getattr(game_map, "round_wins", {})

        return {
            "player_name": getattr(player, "name", "unknown"),
            "team": getattr(player, "team", "unknown"),
            "match_stats": {
                "kills": getattr(match_stats, "kills", 0),
                "assists": getattr(match_stats, "assists", 0),
                "deaths": getattr(match_stats, "deaths", 0),
                "mvps": getattr(match_stats, "mvps", 0),
                "score": getattr(match_stats, "score", 0)
            },
            "round_start": {
                "money": getattr(state, "money", 0),
                "armor": getattr(state, "armor", 0),
                "helmet": getattr(state, "helmet", False)
            },
            "loadout": weapon_categories,
            "map_info": {
                "map": map_name,
                "mode": map_mode,
                "round": round_num,
                "team_ct_score": team_ct_score,
                "team_t_score": team_t_score,
                "round_history": round_wins
            }
        }

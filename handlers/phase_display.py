from typing import Any, Optional
from event_tracker.logging_handler import GameEventLogger
from utils.weapon_utils import categorize_weapons


class PhaseDisplayHandler:
    def __init__(self, logger: GameEventLogger):
        self.logger = logger
    
    def display_freezetime_info(self, player: Any, steamid: str, game_map: Any):
        """Display comprehensive information during freezetime phase."""
        self.logger.log_phase_action("Entered 'freezetime' — prepping for next round.")
        
        self._display_match_stats(player)
        self._display_round_start_info(player)
        self._display_loadout(player)
        self._display_map_info(game_map)
    
    def _display_match_stats(self, player: Any):
        """Display player and match statistics."""
        match_stats = getattr(player, "match_stats", None)
        if match_stats is None:
            self.logger.log_warning("No match_stats found in payload.")
            return

        self.logger.log_info("[PLAYER]")
        self.logger.log_info(f"  NAME: {player.name}")
        self.logger.log_info(f"  TEAM: {player.team}")

        self.logger.log_info("[MATCH STATS]")
        self.logger.log_info(f"  Kills: {match_stats.kills or 0}")
        self.logger.log_info(f"  Assists: {match_stats.assists or 0}")
        self.logger.log_info(f"  Deaths: {match_stats.deaths or 0}")
        self.logger.log_info(f"  MVPs: {match_stats.mvps or 0}")
        self.logger.log_info(f"  Score: {match_stats.score or 0}")
    
    def _display_round_start_info(self, player: Any):
        """Display round start information like money and armor."""
        state = getattr(player, "state", None)
        if not state:
            self.logger.log_warning("No player state found.")
            return

        money = getattr(state, "money", None)
        armor = getattr(state, "armor", None)
        has_helmet = getattr(state, "helmet", None)

        self.logger.log_info("[ROUND START]")
        self.logger.log_info(f"  Money: ${money if money is not None else 'N/A'}")
        self.logger.log_info(f"  Armor: {armor if armor is not None else 'N/A'}")
        self.logger.log_info(f"  Helmet: {'Yes' if has_helmet else 'No' if has_helmet is not None else 'N/A'}")
    
    def _display_loadout(self, player: Any):
        """Display player weapon loadout."""
        weapons = getattr(player, "weapons", {})
        if not weapons:
            self.logger.log_warning("No weapon data available.")
            return

        weapon_categories = categorize_weapons(weapons)

        self.logger.log_info("[LOADOUT]")
        for category, weapon_list in weapon_categories.items():
            if weapon_list:
                category_display = category.title()
                if category == "others":
                    category_display = "Other"
                self.logger.log_info(f"  {category_display}: {', '.join(weapon_list)}")
    
    def _display_map_info(self, game_map: Any):
        """Display map and round information."""
        if not game_map:
            self.logger.log_warning("No map data found in payload.")
            return

        map_name = getattr(game_map, "name", "unknown")
        map_mode = getattr(game_map, "mode", "unknown")
        round_num = getattr(game_map, "round", "?")

        team_ct_score = getattr(game_map.team_ct, "score", 0)
        team_t_score = getattr(game_map.team_t, "score", 0)

        self.logger.log_info(f"[MAP INFO] Map: {map_name} | Mode: {map_mode}")
        self.logger.log_info(f"[MAP INFO] Round: {round_num}")
        self.logger.log_info(f"[SCORE] CT: {team_ct_score} | T: {team_t_score}")

        round_wins = getattr(game_map, "round_wins", {})
        if round_wins:
            self.logger.log_info("[ROUND HISTORY]")
            for rnd, result in sorted(round_wins.items(), key=lambda x: int(x[0])):
                self.logger.log_info(f"  Round {rnd}: {result}")
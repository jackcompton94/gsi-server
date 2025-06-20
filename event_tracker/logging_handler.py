import logging
from typing import Dict, Any, Optional

# Set up basic logging to console
logging.basicConfig(level=logging.INFO, format='%(message)s')


class GameEventLogger:
    def __init__(self, logger_name: str = "game_events"):
        self.logger = logging.getLogger(logger_name)
    
    def summarize_round(self, events: Optional[Dict[str, Any]]):
        """Log a summary of round events."""
        if not events:
            self.logger.warning("[ROUND SUMMARY] No round events found.")
            return

        self.logger.info("[ROUND SUMMARY]")
        self.logger.info(f"  Kills: {events.get('kills', 0)} ({events.get('hkills', 0)} headshots)")
        self.logger.info(f"  Player died: {events.get('player_died', False)}")
        self.logger.info(f"  Smoked: {events.get('smoked', 0)}")
        self.logger.info(f"  Flashed: {events.get('flashed', 0)}")

        kill_weapons = events.get("kill_weapons", {})
        headshot_weapons = events.get("headshot_weapons", {})

        if kill_weapons:
            self.logger.info("  Kill Weapons:")
            for weapon, count in kill_weapons.items():
                self.logger.info(f"    {weapon}: {count}")

        if headshot_weapons:
            self.logger.info("  Headshot Weapons:")
            for weapon, count in headshot_weapons.items():
                self.logger.info(f"    {weapon}: {count}")
    
    def log_player_death(self):
        """Log player death event."""
        self.logger.info("[LIVE EVENT] Player has died.")
    
    def log_new_kills(self, kill_count: int, weapon_name: str, weapon_type: str):
        """Log new kill events."""
        self.logger.info(f"[LIVE EVENT] Player scored {kill_count} new kill(s) with {weapon_name} ({weapon_type}).")
    
    def log_new_headshots(self, headshot_count: int, weapon_name: str, weapon_type: str):
        """Log new headshot events."""
        self.logger.info(f"[LIVE EVENT] {headshot_count} headshot kill(s) added with {weapon_name} ({weapon_type}).")
    
    def log_phase_change(self, previous_phase: str, current_phase: str):
        """Log phase transition."""
        self.logger.info(f"[PHASE] Phase changed: '{previous_phase}' → '{current_phase}'")
    
    def log_phase_action(self, message: str):
        """Log general phase action."""
        self.logger.info(f"[ACTION] {message}")
    
    def log_info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
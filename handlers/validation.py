from typing import Optional, Any
from event_tracker.logging_handler import GameEventLogger


class PayloadValidator:
    def __init__(self, target_steamid: str, logger: GameEventLogger):
        self.target_steamid = target_steamid
        self.logger = logger
    
    def validate_payload(self, payload: Any) -> Optional[Any]:
        """Validate payload and return player object if valid, None otherwise."""
        if not payload:
            self.logger.log_warning("Received empty payload; skipping phase check.")
            return None

        player = getattr(payload, 'player', None)
        if not player:
            self.logger.log_warning("Payload has no player data; skipping.")
            return None

        if payload.player.activity == 'menu':
            self.logger.log_info(f"[INFO] Player {player.name} in menu.")
            return None

        if payload.map.phase == 'warmup':
            self.logger.log_info("[INFO] Warm up")
            return None

        if player.steamid != self.target_steamid:
            self.logger.log_info(f"[INFO] Ignored payload for SteamID {player.steamid} (expected {self.target_steamid}).")
            return None

        return player
from typing import Dict, Any
from utils.logging_setup import logger
from utils.weapon_utils import get_active_weapon

class RoundEventTracker:
    def __init__(self):
        self.round_events: Dict[str, Dict[str, Any]] = {}

    def reset_player_events(self, steamid: str) -> Dict[str, Any]:
        events = {
            "player_died": False,
            "kills": 0,
            "hkills": 0,
            "kill_weapons": {},
            "headshot_weapons": {}
        }
        self.round_events[steamid] = events
        return events

    def get_player_events(self, steamid: str) -> Dict[str, Any]:
        if steamid not in self.round_events:
            return self.reset_player_events(steamid)
        return self.round_events[steamid]

    def update_player_death(self, steamid: str) -> bool:
        events = self.get_player_events(steamid)
        if not events["player_died"]:
            events["player_died"] = True
            return True
        return False

    def update_kills(self, steamid: str, new_kills: int, weapon_name: str) -> int:
        events = self.get_player_events(steamid)
        previous_kills = events["kills"]

        if new_kills > previous_kills:
            kill_diff = new_kills - previous_kills
            events["kills"] = new_kills
            events["kill_weapons"][weapon_name] = (
                    events["kill_weapons"].get(weapon_name, 0) + kill_diff
            )
            return kill_diff
        return 0

    def update_headshots(self, steamid: str, new_headshots: int, weapon_name: str) -> int:
        events = self.get_player_events(steamid)
        previous_headshots = events["hkills"]

        if new_headshots > previous_headshots:
            hs_diff = new_headshots - previous_headshots
            events["hkills"] = new_headshots
            events["headshot_weapons"][weapon_name] = (
                    events["headshot_weapons"].get(weapon_name, 0) + hs_diff
            )
            return hs_diff
        return 0

    def clear_player_events(self, steamid: str):
        if steamid in self.round_events:
            del self.round_events[steamid]

    def handle_live_tick(self, payload):
        player = payload.player
        state = player.state
        steamid = player.steamid

        if state.health == 0:
            if self.update_player_death(steamid):
                logger.info("[LIVE EVENT] Player has died.")

        kills = state.round_kills
        weapon_name, weapon_type = get_active_weapon(player.weapons)

        new_kills = self.update_kills(steamid, kills, weapon_name)
        if new_kills > 0:
            logger.info(f"[LIVE EVENT] Player scored {new_kills} new kill(s) with {weapon_name} ({weapon_type}).")

        headshots = state.round_killhs
        new_headshots = self.update_headshots(steamid, headshots, weapon_name)
        if new_headshots > 0:
            logger.info(f"[LIVE EVENT] {new_headshots} headshot kill(s) added with {weapon_name} ({weapon_type}).")

    def summarize_round(self, steamid: str):
        """Log a summary of the round for a given player."""
        events = self.get_player_events(steamid)
        if not events:
            logger.warning("[ROUND SUMMARY] No round events found.")

        logger.info("[ROUND SUMMARY]")
        logger.info(f"  Kills: {events.get('kills', 0)} ({events.get('hkills', 0)} headshots)")
        logger.info(f"  Player died: {events.get('player_died', False)}")

        kill_weapons = events.get("kill_weapons", {})
        headshot_weapons = events.get("headshot_weapons", {})

        if kill_weapons:
            logger.info("  Kill Weapons:")
            for weapon, count in kill_weapons.items():
                logger.info(f"    {weapon}: {count}")

        if headshot_weapons:
            logger.info("  Headshot Weapons:")
            for weapon, count in headshot_weapons.items():
                logger.info(f"    {weapon}: {count}")

    def collect_round_event_info(self, steamid: str):
        events = self.get_player_events(steamid)
        return {
            "kills": events.get("kills", 0),
            "headshots": events.get("hkills", 0),
            "player_died": events.get("player_died", False),
            "kill_weapons": events.get("kill_weapons", {}),
            "headshot_weapons": events.get("headshot_weapons", {})
        }
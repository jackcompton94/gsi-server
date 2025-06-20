from typing import Dict, Any


class RoundEventTracker:
    def __init__(self):
        self.round_events: Dict[str, Dict[str, Any]] = {}
    
    def reset_player_events(self, steamid: str) -> Dict[str, Any]:
        """Reset per-round stats for a player."""
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
        """Get current round events for a player."""
        if steamid not in self.round_events:
            return self.reset_player_events(steamid)
        return self.round_events[steamid]
    
    def update_player_death(self, steamid: str) -> bool:
        """Mark player as died. Returns True if this is the first death."""
        events = self.get_player_events(steamid)
        if not events["player_died"]:
            events["player_died"] = True
            return True
        return False
    
    def update_kills(self, steamid: str, new_kills: int, weapon_name: str) -> int:
        """Update kill count and weapon stats. Returns number of new kills."""
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
        """Update headshot count and weapon stats. Returns number of new headshots."""
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
        """Clear events for a specific player."""
        if steamid in self.round_events:
            del self.round_events[steamid]
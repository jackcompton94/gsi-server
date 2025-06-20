from typing import Tuple, Dict, List, Any


def get_active_weapon(weapons: Dict[str, Any]) -> Tuple[str, str]:
    """Return the currently active weapon's name and type."""
    for weapon in weapons.values():
        if weapon and weapon.state == "active":
            name = weapon.name or "unknown"
            wtype = weapon.type or "unknown"
            return name, wtype
    return "unknown", "unknown"


def categorize_weapons(weapons: Dict[str, Any]) -> Dict[str, List[str]]:
    """Categorize weapons by type into primary, secondary, grenades, and others."""
    primary, secondary, grenades, others = [], [], [], []
    
    for weapon in weapons.values():
        if not weapon or not weapon.name:
            continue
        
        wtype = weapon.type or "unknown"
        wname = weapon.name
        
        if wtype in ["rifle", "smg", "shotgun", "sniper"]:
            primary.append(wname)
        elif wtype == "pistol":
            secondary.append(wname)
        elif wtype == "grenade":
            grenades.append(wname)
        else:
            others.append(wname)
    
    return {
        "primary": primary,
        "secondary": secondary,
        "grenades": grenades,
        "others": others
    }
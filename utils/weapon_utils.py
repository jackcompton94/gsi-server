from typing import Tuple, Dict, List, Any


def get_active_weapon(weapons: Dict[str, Any]) -> Tuple[str, str]:
    """Return the currently active weapon's name and type."""
    for weapon in weapons.values():
        if weapon and weapon.state == "active":
            name = weapon.name or "unknown"
            wtype = weapon.type or "unknown"
            return name, wtype
    return "unknown", "unknown"


def get_weapon_names(weapons: Dict[str, Any]) -> List[str]:
    """Return a flat list of all weapon names."""
    weapon_names = []

    for weapon in weapons.values():
        if weapon and weapon.name:
            weapon_names.append(weapon.name)

    return weapon_names

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Provider:
    name: str
    appid: int
    version: int
    steamid: str
    timestamp: int


@dataclass
class Team:
    score: int


@dataclass
class Map:
    mode: str
    name: str
    phase: str
    round: int
    team_ct: Team
    team_t: Team
    num_matches_to_win_series: int
    round_wins: Dict[str, str]


@dataclass
class Round:
    phase: str
    win_team: Optional[str] = None


@dataclass
class State:
    health: int
    armor: int
    helmet: bool
    flashed: int
    smoked: int
    burning: int
    money: int
    round_kills: int
    round_killhs: int
    equip_value: int


@dataclass
class Weapon:
    name: str
    paintkit: str
    type: str
    state: str
    ammo_clip: Optional[int] = None
    ammo_clip_max: Optional[int] = None
    ammo_reserve: Optional[int] = None


@dataclass
class MatchStats:
    kills: int
    assists: int
    deaths: int
    mvps: int
    score: int


@dataclass
class Player:
    steamid: str
    name: str
    observer_slot: int
    team: str
    activity: str
    state: State
    weapons: Dict[str, Weapon]
    match_stats: MatchStats


@dataclass
class GSIPayload:
    provider: Provider
    map: Map
    round: Round
    player: Player

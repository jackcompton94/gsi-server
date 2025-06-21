from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Provider:
    name: Optional[str] = None
    appid: Optional[int] = None
    version: Optional[int] = None
    steamid: Optional[str] = None
    timestamp: Optional[int] = None


@dataclass
class Team:
    score: Optional[int] = None


@dataclass
class Map:
    mode: Optional[str] = None
    name: Optional[str] = None
    phase: Optional[str] = None
    round: Optional[int] = None
    team_ct: Optional[Team] = None
    team_t: Optional[Team] = None
    num_matches_to_win_series: Optional[int] = None
    round_wins: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class Round:
    phase: Optional[str] = None
    win_team: Optional[str] = None


@dataclass
class State:
    health: Optional[int] = None
    armor: Optional[int] = None
    helmet: Optional[bool] = None
    flashed: Optional[int] = None
    smoked: Optional[int] = None
    burning: Optional[int] = None
    money: Optional[int] = None
    round_kills: Optional[int] = None
    round_killhs: Optional[int] = None
    equip_value: Optional[int] = None


@dataclass
class Weapon:
    name: Optional[str] = None
    paintkit: Optional[str] = None
    type: Optional[str] = None
    state: Optional[str] = None
    ammo_clip: Optional[int] = None
    ammo_clip_max: Optional[int] = None
    ammo_reserve: Optional[int] = None


@dataclass
class MatchStats:
    kills: Optional[int] = None
    assists: Optional[int] = None
    deaths: Optional[int] = None
    mvps: Optional[int] = None
    score: Optional[int] = None


@dataclass
class Player:
    steamid: Optional[str] = None
    name: Optional[str] = None
    observer_slot: Optional[int] = None
    team: Optional[str] = None
    activity: Optional[str] = None
    state: Optional[State] = None
    weapons: Optional[Dict[str, Weapon]] = field(default_factory=dict)
    match_stats: Optional[MatchStats] = None


@dataclass
class GSIPayload:
    provider: Optional[Provider] = None
    map: Optional[Map] = None
    round: Optional[Round] = None
    player: Optional[Player] = None

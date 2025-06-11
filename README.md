# CS-AIGL (Counter-Strike AI Game Leader)

This repo holds the GSI Server code for the CS2 strategy provider CS-AIGL. 

## Context
A CS2 strategy provider that utilizes LLMs and ML to recommend the most optimal approach each round by analyzing trends 
in the outcomes of previous strategies, map choice, current side, both team’s economies, and active win-loss ratio in 
real-time.

## Documentation
[Counter-Strike: Global Offensive Game State Integration - Valve Developer Community](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration)

[Game State Integration: A Very Large and In-Depth Explanation](https://www.reddit.com/r/GlobalOffensive/comments/cjhcpy/game_state_integration_a_very_large_and_indepth/?sort=new)

## Example Payload
```bash
provider:
  name: Counter-Strike: Global Offensive
  appid: 730
  version: 14083
  steamid: 76561198065320026
  timestamp: 1749590290

map:
  mode: casual
  name: de_train
  phase: live
  round: 8
  team_ct:
    score: 3
    consecutive_round_losses: 1
    timeouts_remaining: 1
    matches_won_this_series: 0
  team_t:
    score: 5
    consecutive_round_losses: 1
    timeouts_remaining: 1
    matches_won_this_series: 0
  num_matches_to_win_series: 0
  round_wins:
    1: t_win_elimination
    2: t_win_elimination
    3: t_win_elimination
    4: t_win_elimination
    5: ct_win_elimination
    6: ct_win_defuse
    7: ct_win_time
    8: t_win_elimination

round:
  phase: over
  win_team: T

player:
  steamid: 76561198065320026
  name: jamarcus
  observer_slot: 5
  team: T
  activity: playing
  state:
    health: 100
    armor: 100
    helmet: True
    flashed: 0
    smoked: 0
    burning: 0
    money: 10000
    round_kills: 1
    round_killhs: 1
    equip_value: 3900
  weapons:
    weapon_0:
      name: weapon_knife_survival_bowie
      paintkit: aq_damascus_90
      type: Knife
      state: holstered
    weapon_1:
      name: weapon_glock
      paintkit: gs_glock_polymer
      type: Pistol
      ammo_clip: 20
      ammo_clip_max: 20
      ammo_reserve: 120
      state: holstered
    weapon_2:
      name: weapon_ak47
      paintkit: cu_ak47_asiimov
      type: Rifle
      ammo_clip: 27
      ammo_clip_max: 30
      ammo_reserve: 90
      state: active
  match_stats:
    kills: 15
    assists: 2
    deaths: 3
    mvps: 2
    score: 44
```
# GSI Server - Local Backend for CS AIGL

This is the local backend Game State Integration (GSI) server that receives real-time game data from Counter-Strike 2 via HTTP POST requests. The server processes and transforms the raw game state data before forwarding it to the separate CS AIGL AI Coach Service for tactical analysis and strategy recommendations.

## Architecture
- **Local GSI Server** (this repository): Receives POST requests from CS2, processes game state data
- **CS AIGL AI Coach Service** (separate service): Provides AI-powered tactical recommendations using OpenAI's GPT model

## Features
- **Real-time Game State Processing**: Receives and processes CS2 GSI data via HTTP POST
- **Interactive Terminal UI**: Modern tkinter-based dashboard with live logging and SteamID management
- **SteamID-based Player Tracking**: Validates and filters game data for specific Steam accounts
- **Round Event Tracking**: Comprehensive tracking of kills, deaths, headshots, and weapon usage
- **Death Analysis**: Captures active weapon and full loadout at time of death
- **Live Game Events**: Real-time logging of player actions, kills, and round events
- **Test Suite**: Automated testing with live snapshot replay functionality
- **Data Validation**: Robust payload validation with menu/warmup/gameover state handling

## New Components

### Terminal UI (`ui/log_terminal.py`)
- Splash screen with SteamID input
- Live dashboard with color-coded event logging
- Real-time typing animation for incoming events
- Modern dark theme with blue accent highlights

### Event Tracking (`event_tracker/round_events.py`)
- Per-player round statistics tracking
- Kill/headshot counters with weapon attribution
- Death state capture with weapon/loadout analysis
- Event persistence across game states

### Enhanced Validation (`handlers/validation.py`)
- SteamID-based filtering of game data
- Game state validation (menu, warmup, gameover handling)
- Improved error handling and logging

### Testing Framework (`tests/test.py`)
- Live snapshot testing with JSON replay
- UI testing with automated log feeding
- Network endpoint validation

## Installation & Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure CS2 GSI**:
   - Place the `gamestate_integration_aigl` config file in your CS2 cfg directory
   - Ensure the server URL matches your local setup (default: `http://localhost:8888`)

3. **Run the Server**:
   ```bash
   python main.py
   ```

4. **Enter SteamID**:
   - On first launch, enter your SteamID in the splash screen
   - The server will filter GSI data for your specific Steam account

## Usage

- **Terminal UI**: The application launches with a modern terminal interface
- **Live Events**: Real-time game events appear in the dashboard with color coding:
  - 🔴 **[ACTION]** - Critical game actions (red)
  - 🔵 **[STRATEGY]** - Strategic recommendations (blue) 
  - 🟢 **[INFO]** - General information (green)
- **Event Tracking**: Automatic tracking of kills, deaths, and weapon usage per round
- **Testing**: Use `tests/test.py` to replay game snapshots or test the UI

## Testing

Run the test suite to validate functionality:

```bash
# Test with live snapshots
python tests/test.py

# Test UI only
python -c "from tests.test import test_ui; test_ui()"
```

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
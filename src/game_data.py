def extract_game_data(json_data):

    # Player Data
    player_data = json_data.get('player', {})
    steamid = player_data.get('steamid')
    player_name = player_data.get('name')
    current_side = player_data.get('team')

    # Player State
    player_state = player_data.get('state', {})
    health = player_state.get('health')
    armor = player_state.get('armor')
    helmet = player_state.get('helmet')
    flashed = player_state.get('flashed')
    smoked = player_state.get('smoked')
    burning = player_state.get('burning')
    money = player_state.get('money')
    round_kills = player_state.get('round_kills')
    round_killsh = player_state.get('round_killsh')
    equip_value = player_state.get('equip_value')

    # Player Stats
    player_match_stats_data = player_data.get('match_stats', {})
    kills = player_match_stats_data.get('kills')
    assists = player_match_stats_data.get('assists')
    deaths = player_match_stats_data.get('deaths')
    mvps = player_match_stats_data.get('mvps')
    score = player_match_stats_data.get('score')

    # Player's Weapon Data
    weapons_data = player_data.get('weapons', {})
    weapons_info = []
    for weapon_key, weapon_info in weapons_data.items():
        weapon_name = weapon_info.get('name')
        paintkit = weapon_info.get('paintkit', 'default')
        weapon_type = weapon_info.get('type')
        ammo_clip = weapon_info.get('ammo_clip')
        ammo_clip_max = weapon_info.get('ammo_clip_max')
        ammo_reserve = weapon_info.get('ammo_reserve')
        state = weapon_info.get('state')

        # Store weapon data in a dictionary
        weapon_info_dict = {
            'weapon_name': weapon_name,
            'paintkit': paintkit,
            'type': weapon_type,
            'ammo_clip': ammo_clip,
            'ammo_clip_max': ammo_clip_max,
            'ammo_reserve': ammo_reserve,
            'state': state
        }
        weapons_info.append(weapon_info_dict)

    # Round Data
    round_data = json_data.get('round', {})
    round_phase = round_data.get('phase')
    bomb_status = round_data.get('bomb')
    round_win = round_data.get('win_team')

    # Map Data
    map_data = json_data.get('map', {})
    mode = map_data.get('mode')
    map_name = map_data.get('name')
    phase = map_data.get('phase')
    current_round = map_data.get('round')
    round_wins = map_data.get('round_wins')

    return {
        'steamid': steamid,
        'player_name': player_name,
        'current_side': current_side,
        'health': health,
        'armor': armor,
        'helmet': helmet,
        'flashed': flashed,
        'smoked': smoked,
        'burning': burning,
        'money': money,
        'round_kills': round_kills,
        'round_killsh': round_killsh,
        'equip_value': equip_value,
        'kills': kills,
        'assists': assists,
        'deaths': deaths,
        'mvps': mvps,
        'score': score,
        'weapons_info': weapons_info,
        'round_phase': round_phase,
        'bomb_status': bomb_status,
        'round_win': round_win,
        'mode': mode,
        'map_name': map_name,
        'phase': phase,
        'current_round': current_round,
        'round_wins': round_wins
    }

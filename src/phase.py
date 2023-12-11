from src.bot import ask_gpt

phases = {}


def handle_phase(game_data):
    # Get unique steamid for current user
    steamid = game_data['steamid']

    # Get current phase of the round
    current_phase = game_data['round_phase']

    if steamid in phases and phases[steamid] == current_phase:
        pass
    else:
        phases[steamid] = current_phase

        if current_phase == 'freezetime':
            return handle_freezetime(game_data)
        elif current_phase == 'live':
            return handle_live(game_data)
        elif current_phase == 'over':
            return handle_over(game_data)


def handle_freezetime(game_data):
    print(f"coaching {game_data['steamid']}")

    current_map = game_data['map_name']
    current_side = game_data['current_side']
    current_round = game_data['current_round']
    current_round += 1
    results = game_data['round_wins']
    money = game_data['money']
    total_kills = game_data['kills']
    total_deaths = game_data['deaths']

    return ask_gpt(current_map, current_side, current_round, results, money, total_kills, total_deaths)


def handle_over(game_data):
    return f"{game_data['round_win']} side wins | {game_data['steamid']} round kills: {game_data['round_kills']}"


def handle_live(game_data):
    print(f"{game_data['steamid']} round start")

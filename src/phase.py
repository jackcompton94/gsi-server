from src.bot import ask_gpt

phases = {}


def handle_phase(game_data):
    steamid = game_data['steamid']
    current_phase = game_data['round_phase']

    if steamid in phases and phases[steamid] == current_phase:
        pass
    else:
        phases[steamid] = current_phase

        if current_phase == 'freezetime':
            handle_freezetime(game_data)
        elif current_phase == 'live':
            handle_live()
        elif current_phase == 'over':
            handle_over(game_data)


def handle_freezetime(game_data):
    print("Getting strat from AIGL...")

    current_map = game_data['map_name']
    current_side = game_data['current_side']
    results = game_data['round_wins']
    money = game_data['money']
    total_kills = game_data['kills']
    total_deaths = game_data['deaths']

    print(ask_gpt(current_map, current_side, results, money, total_kills, total_deaths))


def handle_over(game_data):
    print(f"""Kills this Round: {game_data['round_kills']}
     {game_data['round_win']} side won""")


def handle_live():
    pass

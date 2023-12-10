from src.bot import ask_gpt

phases = {}


def handle_phase(game_data):
    # Get unique steamid for current user
    steamid = game_data['steamid']

    # Get current phase of the round
    current_phase = game_data['round_phase']

    # If the current user
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

    # TODO: Send response to UI with Web Socket
    print(ask_gpt(current_map, current_side, results, money, total_kills, total_deaths))


def handle_over(game_data):

    # TODO: Send response to UI with Web Socket
    print(f"""Kills this Round: {game_data['round_kills']}
     {game_data['round_win']} side won""")

    # TODO: Review if we need to handle a phases reset here


def handle_live():

    # TODO: Send 'live' state to UI with Web Socket
    pass

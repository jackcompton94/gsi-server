from src.bot import ask_gpt

phases = {}


def handle_phase(game_data, steamid):
    current_phase = game_data['round_phase']

    if steamid in phases and phases[steamid] == current_phase:
        # No action needed if the phase hasn't changed
        return None
    else:
        phases[steamid] = current_phase

        if current_phase == 'freezetime':
            # During freezetime, return the result of the ask_gpt function
            # return ask_gpt(game_data['map_name'], game_data['current_side'], game_data['current_round'], game_data['round_wins'], game_data['money'], game_data['kills'], game_data['deaths'])
            return f'freezetime'
        elif current_phase == 'live':
            return f'live'
        elif current_phase == 'over':
            return f'over'

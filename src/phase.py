def handle_phase(game_data):
    # If game is in `freezetime` ask AI for suggestion
    if game_data['round_phase'] == 'freezetime':
        print("Getting strat from AIGL...")

        # print(f"Map: {game_data['map_name']}")
        # print(f"Current Side: {game_data['current_side']}")
        # print(f"Past Results: {game_data['round_wins']}")
        # print(f"Current Money: {game_data['money']}")
        # print(f"Total Kills: {game_data['kills']}")
        # print(f"Total Deaths: {game_data['deaths']}")

    elif game_data['round_phase'] == 'over':
        print(f"""
        Kills this Round: {game_data['round_kills']}
        {game_data['round_win']} side won
        """)

    elif game_data['round_phase'] == 'live':
        pass

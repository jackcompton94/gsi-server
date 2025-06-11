phases = {}

def handle_phase_change(current_phase, steamid):

    if steamid in phases and phases[steamid] == current_phase:
        print(f'PHASE: {current_phase}')
    else:
        phases[steamid] = current_phase
        print(f'NEW PHASE: {current_phase}')

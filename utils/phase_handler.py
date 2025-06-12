phases = {}
STEAMID = "76561198065320026"

def handle_phase_change(payload):
    if not payload:
        print("[WARN] No payload received.")
        return

    player = payload.player
    round_info = payload.round

    # Filter for your own player only
    if player.steamid != STEAMID:
        print(f"[INFO] Ignored payload for SteamID {player.steamid} (expected {STEAMID}).")
        return

    current_phase = round_info.phase
    steamid = player.steamid

    previous_phase = phases.get(steamid)

    if previous_phase == current_phase:
        print(f"[DEBUG] Phase unchanged: {current_phase}")
        return

    # Log the phase transition
    if previous_phase:
        print(f"[PHASE] Transitioned from '{previous_phase}' to '{current_phase}'")
    else:
        print(f"[PHASE] Initial phase detected: '{current_phase}'")

    # Update to current phase
    phases[steamid] = current_phase

    # React to specific phase
    if current_phase == 'freezetime':
        print("[ACTION] Preparing round analysis (entered 'freezetime').")
        print(payload.player)
    elif current_phase == 'live':
        print("[ACTION] Round has started (entered 'live').")
    elif current_phase == 'over':
        print("[ACTION] Round has ended (entered 'over').")
    elif current_phase == 'gameover':
        print("[ACTION] Match has ended. Beginning final analysis (entered 'gameover').")
    else:
        print(f"[WARN] Unknown round phase encountered: '{current_phase}'")

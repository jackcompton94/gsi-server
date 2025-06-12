phases = {}
round_events = {}
STEAMID = "76561198065320026"  # SteamID of the player to track


def reset_round_events():
    """Reset per-round stats for a player."""
    return {
        "player_died": False,
        "kills": 0,
        "hkills": 0,
        # Add more tracked stats here as needed
        # TODO: Assists
        # TODO: Kills with Weapons
        # TODO: Deaths with nade/bomb in hand
        # TODO: Money made
        # TODO: were Helmet/Nades purchased
    }


def handle_live_tick(payload):
    """Track player events while the round is live."""
    player = payload.player
    state = player.state
    steamid = player.steamid

    # Initialize round tracking if not already set
    if steamid not in round_events:
        round_events[steamid] = reset_round_events()

    events = round_events[steamid]

    # Detect player death (first occurrence only)
    if state.health <= 0 and not events["player_died"]:
        events["player_died"] = True
        print("[LIVE EVENT] Player has died.")

    # Detect new kills this tick
    kills = state.round_kills
    if kills > events["kills"]:
        new_kills = kills - events["kills"]
        events["kills"] = kills
        print(f"[LIVE EVENT] Player scored {new_kills} new kill(s).")

    # Detect new headshot kills
    headshots = state.round_killhs
    if headshots > events["hkills"]:
        new_hs = headshots - events["hkills"]
        events["hkills"] = headshots
        print(f"[LIVE EVENT] {new_hs} headshot kill(s) added.")


def handle_phase_change(payload):
    """Handle transitions between round phases and summarize events."""
    if not payload:
        print("[WARN] Received empty payload; skipping phase check.")
        return

    player = payload.player
    round_info = payload.round
    current_phase = round_info.phase
    steamid = player.steamid
    previous_phase = phases.get(steamid)

    # Ignore players not being tracked
    if steamid != STEAMID:
        print(f"[INFO] Ignored payload for SteamID {steamid} (expected {STEAMID}).")
        return

    # Process live events on every tick during 'live'
    if current_phase == 'live':
        handle_live_tick(payload)

    # React only to phase changes
    if previous_phase != current_phase:
        if previous_phase:
            print(f"[PHASE] Phase changed: '{previous_phase}' → '{current_phase}'")

            # Summarize and reset after leaving 'live' phase
            if previous_phase == 'live':
                print(f"[ROUND SUMMARY] Final stats: {round_events.get(steamid)}")
        else:
            print(f"[PHASE] Initial phase detected: '{current_phase}'")

        phases[steamid] = current_phase

        # Log entry into new phase
        if current_phase == 'freezetime':
            print("[ACTION] Entered 'freezetime' — prepping for next round.")
            # TODO: Add previous round analysis logic
        elif current_phase == 'live':
            print("[ACTION] Entered 'live' — new round started.")
            round_events[steamid] = reset_round_events()
        elif current_phase == 'over':
            print("[ACTION] Entered 'over' — round officially ended.")
        elif current_phase == 'gameover':
            print("[ACTION] Entered 'gameover' — match is complete.")
            # TODO: Add full match analysis logic
        else:
            print(f"[WARN] Unrecognized round phase: '{current_phase}'")

phases = {}
round_events = {}
STEAMID = "76561198065320026"  # SteamID of the player to track


def reset_round_events():
    """Reset per-round stats for a player."""
    return {
        "player_died": False,
        "kills": 0,
        "hkills": 0,
        "smoked": 0,
        "flashed": 0,
        "kill_weapons": {},      # {"weapon_m4a1": 2, "weapon_usp_silencer": 1}
        "headshot_weapons": {}   # {"weapon_m4a1": 1}
    }


def summarize_round(events):
    print("[ROUND SUMMARY] Final stats:")

    print(f"  Kills: {events.get('kills', 0)} ({events.get('hkills', 0)} headshots)")
    print(f"  Player died: {events.get('player_died', False)}")
    print(f"  Smoked: {events.get('smoked', 0)}")
    print(f"  Flashed: {events.get('flashed', 0)}")

    kill_weapons = events.get("kill_weapons", {})
    headshot_weapons = events.get("headshot_weapons", {})

    if kill_weapons:
        print("  Kill Weapons:")
        for weapon, count in kill_weapons.items():
            print(f"    {weapon}: {count}")

    if headshot_weapons:
        print("  Headshot Weapons:")
        for weapon, count in headshot_weapons.items():
            print(f"    {weapon}: {count}")


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

        weapon_name, weapon_type = get_active_weapon(player.weapons)

        # Increment weapon kill counts in dictionary
        events["kill_weapons"][weapon_name] = events["kill_weapons"].get(weapon_name, 0) + new_kills

        print(f"[LIVE EVENT] Player scored {new_kills} new kill(s) with {weapon_name} ({weapon_type}).")


    # Detect new headshot kills
    headshots = state.round_killhs
    if headshots > events["hkills"]:
        new_hs = headshots - events["hkills"]
        events["hkills"] = headshots

        weapon_name, weapon_type = get_active_weapon(player.weapons)

        # Increment headshot weapon counts in dictionary
        events["headshot_weapons"][weapon_name] = events["headshot_weapons"].get(weapon_name, 0) + new_hs

        print(f"[LIVE EVENT] {new_hs} headshot kill(s) added with {weapon_name} ({weapon_type}).")


    smoked = state.smoked
    if smoked > events["smoked"]:
        events["smoked"] = smoked
        print(f"[LIVE EVENT] Player is smoked {smoked}.")

    flashed = state.flashed
    if flashed > events["flashed"]:
        events["flashed"] = flashed
        print(f"[LIVE EVENT] Player is flashed {flashed}.")


def get_active_weapon(weapons: dict):
    """Return the currently active weapon's name and type."""
    for weapon in weapons.values():
        if weapon and weapon.state == "active":
            name = weapon.name or "unknown"
            wtype = weapon.type or "unknown"
            return name, wtype
    return "unknown", "unknown"


def handle_phase_change(payload):
    """Handle transitions between round phases and summarize events."""
    if not payload:
        print("[WARN] Received empty payload; skipping phase check.")
        return

    if payload.map.phase == 'warmup':
        print(f'[INFO] Warm up')
        return

    if payload.map.phase == 'gameover':
        print("[ACTION] Entered 'gameover' — match is complete.")
        return
        # TODO: Add full match analysis logic

    player = payload.player
    steamid = player.steamid

    if player.activity == 'menu':
        print(f'[INFO] Player {player.name} - ({steamid}) in menu.')
        return

    if steamid != STEAMID:
        print(f"[INFO] Ignored payload for SteamID {steamid} (expected {STEAMID}).")
        return

    current_phase = payload.round.phase
    previous_phase = phases.get(steamid)

    # Continue processing ticks during 'live' and 'over' — kills can still occur until 'freezetime'
    if current_phase in ['live', 'over'] or previous_phase in ['live', 'over']:
        handle_live_tick(payload)


    # React only to phase changes
    if previous_phase != current_phase:
        if previous_phase:
            print(f"[PHASE] Phase changed: '{previous_phase}' → '{current_phase}'")

        phases[steamid] = current_phase

        # Log entry into new phase
        if current_phase == 'freezetime':
            print("[ACTION] Entered 'freezetime' — prepping for next round.")
            # TODO: Add previous round analysis logic
            summarize_round(round_events.get(steamid))
        elif current_phase == 'live':
            print("[ACTION] Entered 'live' — new round started.")
            round_events[steamid] = reset_round_events()
        elif current_phase == 'over':
            print("[ACTION] Entered 'over' — round officially ended.")
        else:
            print(f"[WARN] Unrecognized round phase: '{current_phase}'")

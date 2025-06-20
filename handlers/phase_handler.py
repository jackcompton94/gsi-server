from config import STEAMID
from event_tracker.round_events import RoundEventTracker
from event_tracker.logging_handler import GameEventLogger
from handlers.validation import PayloadValidator
from utils.weapon_utils import get_active_weapon
from handlers.phase_display import PhaseDisplayHandler

phases = {}
event_tracker = RoundEventTracker()
game_logger = GameEventLogger()
validator = PayloadValidator(STEAMID, game_logger)
phase_display = PhaseDisplayHandler(game_logger)


def handle_live_tick(payload):
    """Track player events while the round is live."""
    player = payload.player
    state = player.state
    steamid = player.steamid

    # Detect player death (first occurrence only)
    if state.health <= 0:
        if event_tracker.update_player_death(steamid):
            game_logger.log_player_death()

    # Detect new kills this tick
    kills = state.round_kills
    weapon_name, weapon_type = get_active_weapon(player.weapons)
    
    new_kills = event_tracker.update_kills(steamid, kills, weapon_name)
    if new_kills > 0:
        game_logger.log_new_kills(new_kills, weapon_name, weapon_type)

    # Detect new headshot kills
    headshots = state.round_killhs
    new_headshots = event_tracker.update_headshots(steamid, headshots, weapon_name)
    if new_headshots > 0:
        game_logger.log_new_headshots(new_headshots, weapon_name, weapon_type)


def handle_freezetime_phase(player, steamid, game_map):
    game_logger.summarize_round(event_tracker.get_player_events(steamid))
    phase_display.display_freezetime_info(player, steamid, game_map)


def handle_phase_change(payload):
    """Handle transitions between round phases and summarize events."""
    player = validator.validate_payload(payload)
    if not player:
        return

    steamid = player.steamid

    current_phase = payload.round.phase
    previous_phase = phases.get(steamid)

    if current_phase in ['live', 'over'] or previous_phase in ['live', 'over']:
        handle_live_tick(payload)

    if previous_phase != current_phase:
        handle_phase_transition(player, steamid, payload.map, current_phase, previous_phase)


def handle_phase_transition(player, steamid, game_map, current_phase, previous_phase):
    if previous_phase:
        game_logger.log_phase_change(previous_phase, current_phase)

    phases[steamid] = current_phase

    if current_phase == 'freezetime':
        handle_freezetime_phase(player, steamid, game_map)

    elif current_phase == 'live':
        game_logger.log_phase_action("Entered 'live' — new round started.")
        event_tracker.reset_player_events(steamid)

    elif current_phase == 'over':
        game_logger.log_phase_action("Entered 'over' — round officially ended.")

    else:
        game_logger.log_warning(f"Unrecognized round phase: '{current_phase}'")
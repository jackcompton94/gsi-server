from config import STEAMID
from event_tracker.round_events import RoundEventTracker
from utils.logging_setup import logger
from handlers.validation import PayloadValidator
from handlers.phase_display import PhaseDisplayHandler

phases = {}
event_tracker = RoundEventTracker()
validator = PayloadValidator(STEAMID, logger)
phase_display = PhaseDisplayHandler(logger)


def handle_freezetime_phase(player, steamid, game_map):

    round_event_data = event_tracker.collect_round_event_info(steamid)
    freezetime_data = phase_display.collect_freezetime_info(player, game_map)

    print(round_event_data)
    print(freezetime_data)

    # # LOGGING ONLY
    # event_tracker.summarize_round(steamid)
    # phase_display.display_freezetime_info(player, steamid, game_map)


def handle_phase_change(payload):
    """Handle transitions between round phases and summarize events."""
    player = validator.validate_payload(payload)
    if not player:
        return

    steamid = player.steamid

    current_phase = payload.round.phase
    previous_phase = phases.get(steamid)

    if current_phase in ['live', 'over'] or previous_phase in ['live', 'over']:
        event_tracker.handle_live_tick(payload)

    if previous_phase != current_phase:
        handle_phase_transition(player, steamid, payload.map, current_phase, previous_phase)


def handle_phase_transition(player, steamid, game_map, current_phase, previous_phase):
    if previous_phase:
        logger.info(f"[PHASE] Phase changed: '{previous_phase}' → '{current_phase}'")

    phases[steamid] = current_phase

    if current_phase == 'freezetime':
        handle_freezetime_phase(player, steamid, game_map)

    elif current_phase == 'live':
        logger.info("[ACTION] Entered 'live' — new round started.")
        event_tracker.reset_player_events(steamid)

    elif current_phase == 'over':
        logger.info("[ACTION] Entered 'over' — round officially ended.")

    else:
        logger.warning(f"Unrecognized round phase: '{current_phase}'")
import requests
import re
from config import STEAMID
from event_tracker.round_events import RoundEventTracker
from utils.logging_setup import logger
from handlers.validation import PayloadValidator
from handlers.phase_display import PhaseDisplayHandler
from ui.log_terminal import push_log

phases = {}
event_tracker = RoundEventTracker()
validator = PayloadValidator(STEAMID, logger)
phase_display = PhaseDisplayHandler(logger)
COACH_BACKEND_URL = "https://coach-backend-rho.vercel.app/api/get_strategy"

def strip_markdown(text):
    # Remove bold/italic formatting (**text**, *text*)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text


def handle_freezetime_phase(player, steamid, game_map):
    round_event_data = event_tracker.collect_round_event_info(steamid)
    freezetime_data = phase_display.collect_freezetime_info(player, game_map)

    context = {**freezetime_data, **round_event_data}
    logger.info("[CONTEXT]", context)

    try:
        response = requests.post(
            COACH_BACKEND_URL,
            json={"context": context},
            timeout=10
        )

        if response.ok:
            strategy = response.json().get("strategy")
            logger.info("[STRATEGY]", strategy)
            push_log(f"[STRATEGY] \n{strip_markdown(strategy)}")
        else:
            logger.error("[ERROR]", response.status_code, response.text)

    except requests.RequestException as e:
        logger.error(f"[EXCEPTION] Failed to get strategy: {e}")


def process_game_state(payload):
    """Processes an incoming GSI payload by validating the player,
    tracking round phase transitions, and invoking logic for live round events and strategic transitions.
    """
    player = validator.validate_payload(payload)
    if not player:
        return

    steamid = player.steamid

    current_phase = payload.round.phase
    previous_phase = phases.get(steamid)

    if current_phase in ['live', 'over'] or previous_phase in ['live', 'over']:
        event_tracker.handle_live_tick(payload)

    if previous_phase != current_phase:
        handle_phase_transition(player, steamid, payload.map, current_phase)


def handle_phase_transition(player, steamid, game_map, current_phase):
    phases[steamid] = current_phase

    if current_phase == 'freezetime':
        handle_freezetime_phase(player, steamid, game_map)

    elif current_phase == 'live':
        logger.info("[ACTION] New round started.")
        push_log("[ACTION] New round started.")
        event_tracker.reset_player_events(steamid)

    elif current_phase == 'over':
        logger.info("[ACTION] Round over.")
        push_log("[ACTION] Round over.")

    else:
        logger.warning(f"Unrecognized round phase: '{current_phase}'")
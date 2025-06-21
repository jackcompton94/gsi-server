import logging

# Set up basic logging to console
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Create a logger instance that can be imported anywhere
logger = logging.getLogger("game_events")
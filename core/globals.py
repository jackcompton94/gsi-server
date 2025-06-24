# globals.py
from handlers.validation import PayloadValidator
from utils.logging_setup import logger

validator = PayloadValidator(None, logger)

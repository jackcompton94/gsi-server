# core/logger_hooks.py
import queue

log_queue = queue.Queue()

def push_log(line):
    log_queue.put(line)

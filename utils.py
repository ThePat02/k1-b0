"""This module contains several utility functions for K1-B0"""

import datetime
import random
def print_line():
    """Prints a line of dashes"""
    line = "-" * 100
    print(line)

def botLog(msg):
    """Prints a message with a timestamp"""
    now = datetime.datetime.now()
    print(f"[{now.strftime('%H:%M:%S')}] {msg}")

def random_number(min, max):
    """Returns a random number between min and max"""
    return random.randint(min, max)
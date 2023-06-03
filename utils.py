"""This module contains several utility functions for K1-B0"""

import datetime

def print_line():
    """Prints a line of dashes"""
    line = "-" * 100
    print(line)

def botLog(msg):
    """Prints a message with a timestamp"""
    now = datetime.datetime.now()
    print(f"[{now.strftime('%H:%M:%S')}] {msg}")

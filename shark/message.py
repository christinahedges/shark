'''Messaging system. This is lifted directly out of PyKE'''

import sys
import time
import logging

def log(filename, message, verbose):
    """Write message to log file and shell."""
    if verbose:
        print(message)
    if filename:
        output = open(filename, 'a')
        output.write(message + '\n')
        output.close()

def err(filename, message, verbose):
    '''Throw an exception with a message'''
    log(filename, message, verbose)
    raise Exception(message)

def warn(filename, message, verbose):
    '''Warn the user'''
    log(filename, message, verbose)

def exit(message):
    """Write error message to shell and exit"""
    sys.exit(message)

def clock(filename, text, verbose):
    """write time to log file and shell"""
    if verbose:
        message = text + ': ' + time.asctime(time.localtime())
        log(filename, message, verbose)

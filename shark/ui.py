"""Implements the shark command-line tools.

more exciting tools coming soon
"""
import numpy as np
import os
import click
from . import PACKAGEDIR, __version__
from . import message as msg
from . import feature_finder as ff

DATA_DIR = '{}/data/'.format(PACKAGEDIR)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)

def shark(**kwargs):
    pass



@shark.command()
@click.option('-v', '--verbose', type=bool,
              default=True, metavar='<True/False>',
              help="Change verbosity")

def test(verbose):
    '''Tests the installation of shark'''
    if verbose:
        print("Testing shark installation.")
        print("Running shark version {}".format(__version__))

    #Test that all the required files are installed
    if not os.path.exists(DATA_DIR):
        msg.err('shark.log', '{} does not exist. Reinstall shark.'.format(DATA_DIR), verbose)
    
    return

if __name__ == '__main__':
    shark()

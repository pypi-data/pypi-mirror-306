import argparse
import os

from dotenv import load_dotenv

from synapse.plugins.utils import get_action


action = None


def run():
    global action
    parser = argparse.ArgumentParser(description='synapse plugin runner')

    # Add arguments
    parser.add_argument('action', help='action to run on this plugin')
    parser.add_argument('params', help='parameter of the action')
    parser.add_argument('--direct', help='run without using ray', action='store_true')
    parser.add_argument('--debug', help='run with debug mode', action='store_true')

    # Parse arguments
    args = parser.parse_args()

    # Access parsed arguments
    action = args.action
    params = args.params
    direct = args.direct
    debug = args.debug

    load_dotenv(os.path.join(os.getcwd(), '.env'))

    action = get_action(action, params, direct=direct, debug=debug)
    result = action.run_action()
    if debug:
        print(result)


__all__ = ['run']

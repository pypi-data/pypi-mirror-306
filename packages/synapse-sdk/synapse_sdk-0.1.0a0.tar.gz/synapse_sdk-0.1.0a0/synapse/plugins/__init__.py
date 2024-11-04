import argparse

from synapse.plugins.utils import get_action

action = None


def init():
    global action
    parser = argparse.ArgumentParser(description='synapse plugin runner')

    # Add arguments
    parser.add_argument('action', help='action to run on this plugin')
    parser.add_argument('params', help='parameter of the action')

    # Parse arguments
    args = parser.parse_args()

    # Access parsed arguments
    action = args.action
    params = args.params

    action = get_action(action, params)


def run():
    global action
    assert action is not None
    action.run()


__all__ = ['init', 'run']

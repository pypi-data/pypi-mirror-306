import json

from synapse.utils.file import get_dict_from_file
from synapse.utils.string import hash_text


def get_action(action, json_or_path):
    from synapse.plugins.categories import ACTIONS

    try:
        params = json.loads(json_or_path)
    except json.JSONDecodeError:
        params = get_dict_from_file(json_or_path)
    config = get_dict_from_file('config.yaml')
    category = config['category']
    return ACTIONS[category][action](params, config)


def get_available_actions(category):
    from synapse.plugins.categories import ACTIONS

    return list(ACTIONS[category].keys())


def get_plugin_checksum(plugin_id):
    return hash_text(plugin_id)

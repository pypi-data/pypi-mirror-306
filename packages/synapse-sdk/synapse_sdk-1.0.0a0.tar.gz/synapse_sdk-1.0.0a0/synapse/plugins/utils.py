import json

from synapse.plugins.categories.registry import _REGISTERED_ACTIONS, register_actions
from synapse.utils.file import get_dict_from_file
from synapse.utils.string import hash_text


def get_action(action, params_data, *args, **kwargs):
    if isinstance(params_data, str):
        try:
            params = json.loads(params_data)
        except json.JSONDecodeError:
            params = get_dict_from_file(params_data)
    else:
        params = params_data

    config_data = kwargs.pop('config', False)
    if config_data:
        if isinstance(config_data, str):
            config = get_dict_from_file(config_data)
        else:
            config = config_data
    else:
        config = get_dict_from_file('config.yaml')
    category = config['category']
    return get_action_class(category, action)(params, config, *args, **kwargs)


def get_action_class(category, action):
    register_actions()
    return _REGISTERED_ACTIONS[category][action]


def get_available_actions(category):
    register_actions()
    return list(_REGISTERED_ACTIONS[category].keys())


def get_plugin_checksum(plugin_id):
    return hash_text(plugin_id)

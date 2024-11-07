from synapse.plugins.categories.base import Action
from synapse.plugins.categories.decorators import register_action
from synapse.plugins.enums import RunMethod, PluginCategory


@register_action
class ValidationAction(Action):
    name = 'validation'
    category = PluginCategory.DATA_VALIDATION
    method = RunMethod.TASK

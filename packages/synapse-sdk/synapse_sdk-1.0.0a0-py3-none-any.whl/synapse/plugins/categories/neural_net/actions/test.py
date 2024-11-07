from synapse.plugins.categories.base import Action
from synapse.plugins.categories.decorators import register_action
from synapse.plugins.enums import RunMethod, PluginCategory


@register_action
class TestAction(Action):
    name = 'test'
    category = PluginCategory.NEURAL_NET
    method = RunMethod.TASK

from synapse.plugins.categories.base import Action
from synapse.plugins.categories.decorators import register_action
from synapse.plugins.enums import RunMethod, PluginCategory


@register_action
class PostAnnotationAction(Action):
    name = 'post_annotation'
    category = PluginCategory.POST_ANNOTATION
    method = RunMethod.TASK

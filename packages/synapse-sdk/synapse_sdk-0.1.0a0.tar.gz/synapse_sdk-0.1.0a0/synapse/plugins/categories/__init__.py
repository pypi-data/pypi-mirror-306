from synapse.plugins.categories.neural_net.actions.deployment import DeploymentAction
from synapse.plugins.categories.neural_net.actions.inference import InferenceAction
from synapse.plugins.categories.neural_net.actions.test import TestAction
from synapse.plugins.categories.neural_net.actions.train import TrainAction

ACTIONS = {
    'neural_net': {
        'deployment': DeploymentAction,
        'inference': InferenceAction,
        'train': TrainAction,
        'test': TestAction,
    },
}

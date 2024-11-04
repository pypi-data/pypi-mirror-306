from ray import serve

from synapse.plugins.categories.base import Action
from synapse.utils.module_loading import import_string


class DeploymentAction(Action):
    deployment = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deployment = self.get_deployment()

    def get_deployment(self):
        entrypoint = self.config['actions']['deployment']['entrypoint']
        deployment = import_string(entrypoint)
        return serve.deployment(ray_actor_options=self.get_actor_options())(deployment)

    def get_actor_options(self):
        return {'runtime_env': self.get_runtime_env()}

    def run(self):
        serve.delete(self.plugin_id)
        serve.run(self.deployment.bind(), name=self.plugin_id, route_prefix=f'/{self.plugin_checksum}')

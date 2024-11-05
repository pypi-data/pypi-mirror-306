import os
from functools import cached_property

from synapse.loggers import ConsoleLogger
from synapse.plugins.utils import get_plugin_checksum


class Action:
    params = None
    config = None
    client = None
    logger = None

    def __init__(self, params, config):
        self.params = params
        self.config = config

        # TODO logger 지정 방식 개선
        self.logger = ConsoleLogger()

    @cached_property
    def plugin_id(self):
        code = self.config['code']
        version = self.config['version']
        return f'{code}@{version}'

    @cached_property
    def plugin_checksum(self):
        return get_plugin_checksum(self.plugin_id)

    def get_plugin_url(self):
        base_url = os.getenv('SYNAPSE_PLUGIN_BASE_URL')
        return str(os.path.join(base_url, f'{self.plugin_checksum}.zip'))

    def get_runtime_env(self):
        return {'working_dir': self.get_plugin_url()}

    def run(self):
        raise NotImplementedError

    def set_progress(self, current, total, category=''):
        self.logger.set_progress(current, total, category)

    def log(self, action, data):
        self.logger.log(action, data)

    def log_event(self, message):
        self.logger.log('event', {'content': message})

    def end_log(self):
        self.log_event('Plugin run is complete.')

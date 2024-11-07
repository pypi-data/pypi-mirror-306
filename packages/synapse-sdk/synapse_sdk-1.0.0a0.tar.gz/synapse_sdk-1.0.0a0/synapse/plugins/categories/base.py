import inspect
import json
import os
from functools import cached_property
from pprint import pprint

import ray
import requests
from ray.dashboard.modules.job.sdk import JobSubmissionClient

from synapse.loggers import ConsoleLogger
from synapse.plugins.enums import RunMethod
from synapse.plugins.upload import upload_path, build_and_upload
from synapse.plugins.utils import get_plugin_checksum
from synapse.utils.module_loading import import_string


class Action:
    name = None
    category = None
    method = None
    params = None
    plugin_config = None
    config = None
    client = None
    logger = None
    debug = False

    default_envs = [
        'RAY_SERVE_ADDRESS',
        'SYNAPSE_PLUGIN_URL',
        'SYNAPSE_PLUGIN_PATH',
        'SYNAPSE_PLUGIN_BASE_URL',
        'SYNAPSE_PLUGIN_UPLOAD_S3_ENDPOINT_URL',
        'SYNAPSE_PLUGIN_UPLOAD_S3_BUCKET_NAME',
        'SYNAPSE_PLUGIN_UPLOAD_S3_ACCESS_KEY',
        'SYNAPSE_PLUGIN_UPLOAD_S3_SECRET_KEY',
        'SYNAPSE_PLUGIN_UPLOAD_S3_BASE_URL',
        'SYNAPSE_DEBUG_MODULES',
    ]

    def __init__(self, params, plugin_config, envs=None, job_id=None, direct=False, debug=False):
        self.params = params
        self.plugin_config = plugin_config
        self.config = plugin_config['actions'][self.name]
        self.job_id = job_id
        self.direct = direct
        self.debug = debug
        if envs:
            self.envs = {**envs, **self.get_default_envs()}
        else:
            self.envs = self.get_default_envs()

        # TODO logger 지정 방식 개선
        self.logger = ConsoleLogger()

    @cached_property
    def plugin_id(self):
        code = self.plugin_config['code']
        version = self.plugin_config['version']
        return f'{code}@{version}'

    @cached_property
    def plugin_checksum(self):
        return get_plugin_checksum(self.plugin_id)

    @cached_property
    def plugin_url(self):
        if self.debug:
            plugin_url = self.envs.get('SYNAPSE_PLUGIN_URL')
            if not plugin_url:
                plugin_url = upload_path(self.envs.get('SYNAPSE_PLUGIN_PATH', '.'), **self.get_kwargs_upload_path())
                self.envs['SYNAPSE_PLUGIN_URL'] = plugin_url
            return plugin_url
        base_url = self.envs['SYNAPSE_PLUGIN_BASE_URL']
        return str(os.path.join(base_url, f'{self.plugin_checksum}.zip'))

    @cached_property
    def entrypoint(self):
        return import_string(self.config['entrypoint'])

    def get_kwargs_upload_path(self):
        # TODO upload 관련 env 단일화 후 제거
        return {
            'endpoint_url': self.envs['SYNAPSE_PLUGIN_UPLOAD_S3_ENDPOINT_URL'],
            'bucket_name': self.envs['SYNAPSE_PLUGIN_UPLOAD_S3_BUCKET_NAME'],
            'access_key': self.envs['SYNAPSE_PLUGIN_UPLOAD_S3_ACCESS_KEY'],
            'secret_key': self.envs['SYNAPSE_PLUGIN_UPLOAD_S3_SECRET_KEY'],
            'base_url': self.envs['SYNAPSE_PLUGIN_UPLOAD_S3_BASE_URL'],
        }

    def get_default_envs(self):
        return {env: os.environ[env] for env in self.default_envs if env in os.environ}

    def get_debug_modules(self):
        debug_modules = []
        for module_path in self.envs.get('SYNAPSE_DEBUG_MODULES', '').split(','):
            if module_path.startswith('http'):
                module_url = module_path
            else:
                module_url = build_and_upload(module_path, **self.get_kwargs_upload_path())
            debug_modules.append(module_url)
        self.envs['SYNAPSE_DEBUG_MODULES'] = ','.join(debug_modules)
        return debug_modules

    def get_runtime_env(self):
        runtime_env = {
            'pip': ['-r ${RAY_RUNTIME_ENV_CREATE_WORKING_DIR}/requirements.txt'],
            'working_dir': self.plugin_url,
        }

        if self.debug:
            runtime_env['pip'] += self.get_debug_modules()

        runtime_env['env_vars'] = self.envs
        pprint(runtime_env)
        return runtime_env

    def run(self):
        return self.entrypoint(self, **self.params)

    def run_action(self):
        if self.direct:
            if self.method == RunMethod.RESTAPI:
                return self.run_by_restapi()
            else:
                return self.run()
        return getattr(self, f'run_by_{self.method.value}')()

    def run_by_task(self):
        @ray.remote(runtime_env=self.get_runtime_env())
        def run_task(category, action, *args, **kwargs):
            from synapse.plugins.utils import get_action_class

            action = get_action_class(category, action)(*args, **kwargs)
            return action.run_action()

        init_signature = inspect.signature(self.__class__.__init__)

        args = []
        kwargs = {}

        for param in init_signature.parameters.values():
            if param.name == 'self':
                continue
            if param.default == param.empty:
                args.append(getattr(self, param.name))
            else:
                kwargs[param.name] = getattr(self, param.name)

        kwargs['direct'] = True
        return ray.get(run_task.remote(self.category.value, self.name, *args, **kwargs))

    def run_by_job(self):
        entrypoint_args = [self.name, f'"{json.dumps(self.params)}"']
        if self.debug:
            entrypoint_args.append('--debug')

        client = JobSubmissionClient()
        return client.submit_job(
            submission_id=self.job_id,
            entrypoint=f'python main.py {" ".join(entrypoint_args)} --direct',
            runtime_env=self.get_runtime_env(),
        )

    def run_by_restapi(self):
        path = self.params.pop('path', '')
        method = self.params.pop('method')

        url = os.path.join(self.envs['RAY_SERVE_ADDRESS'], self.plugin_checksum, path)
        response = getattr(requests, method)(url, **self.params)
        # TODO ok response가 아닌 경우 대응하기
        return response.json()

    def set_progress(self, current, total, category=''):
        self.logger.set_progress(current, total, category)

    def log(self, action, data):
        self.logger.log(action, data)

    def log_event(self, message):
        self.logger.log('event', {'content': message})

    def end_log(self):
        self.log_event('Plugin run is complete.')

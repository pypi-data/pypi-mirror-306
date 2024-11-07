from enum import Enum


class RunMethod(Enum):
    JOB = 'job'
    TASK = 'task'
    RESTAPI = 'restapi'


class PluginCategory(Enum):
    NEURAL_NET = 'neural_net'
    EXPORT = 'export'
    IMPORT = 'import'
    POST_ANNOTATION = 'post_annotation'
    PRE_ANNOTATION = 'pre_annotation'
    DATA_VALIDATION = 'data_validation'

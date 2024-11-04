try:
    from constance import config as constance_config

    config = constance_config
except ImportError:
    config = None

__all__ = ['config']

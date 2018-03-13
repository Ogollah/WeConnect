# config.py
"""configurations"""


class Config(object):
    """
    Common configurations
    """

    SECRET_KEY = 'config-secret'

    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    SECRET_KEY = 'dev-secret-key'


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    SECRET_KEY = 'always-secret'
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

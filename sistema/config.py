class BaseConfig:
    TESTING = False


class DevelopmentConfig(BaseConfig):
    TESTING = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass
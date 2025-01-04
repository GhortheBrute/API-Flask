class Config:
    TESTING = False
    SECRET_KEY = "dev"
    # SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI=os_getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    JWT_SECRET_KEY = "super-secret"
    # JWT_SECRET_KEY = os.getenv("super-secret")


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    JWT_SECRET_KEY = "super-secret"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
    # SQLALCHEMY_DATABASE_URI=on_environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    JWT_SECRET_KEY = "test"

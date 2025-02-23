import os
from dotenv import load_dotenv

load_dotenv()


class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')

class Development(Config):
    DEBUG=True
    MYSQL_HOST=os.getenv('MYSQL_HOST')
    MYSQL_USER=os.getenv('MYSQL_USER')
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD')
    MYSQL_DB=os.getenv('MYSQL_DB')
    

class Production(Config):
    DEBUG=False
    MYSQL_HOST=os.getenv('MYSQL_HOST_CLEVER_CLOUD')
    MYSQL_USER=os.getenv('MYSQL_USER_CLEVER_CLOUD')
    MYSQL_PASSWORD=os.getenv('MYSQL_PASSWORD_CLEVER_CLOUD')
    MYSQL_DB=os.getenv('MYSQL_DB_CLEVER_CLOUD')


config={
    'development':Development,
    'production':Production
}


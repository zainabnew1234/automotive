class Config(object):
    MERCHANT_ID='bghrebe5634583rhw'

class ProductionConfig(Config):
    MERCHANT_ID='&^GYG4dyyrwrwefns'
    DATABASE_URI=''
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USERNAME='' 
    MAIL_PASSWORD=''
    MAIL_USE_SSL=True

class DevelopmentConfig(Config):
    MERCHANT_ID='hjewbhsrndw'
    DATABASE_URI=''

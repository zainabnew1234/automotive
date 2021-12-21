from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy  import SQLAlchemy
from flask_mail import Mail,Message
from flask_migrate import Migrate
import config



fins = Flask(__name__,instance_relative_config=True)
csrf = CSRFProtect(fins)
fins.config.from_pyfile("config.py")
fins.config.from_object(config.ProductionConfig)
mail=Mail(fins)
db = SQLAlchemy(fins)
migrate=Migrate(fins,db)


from bootcamp.allroutes  import user_route,admin_route
from bootcamp import models








from flask_sqlalchemy import SQLAlchemy
from SQLManager.BaseModel import BaseModel

sql_object = SQLAlchemy(model_class=BaseModel)

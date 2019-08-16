from flask_sqlalchemy import Model
import abc
from flask import session

class BaseModel(Model):

    id = None

    @classmethod
    @abc.abstractmethod
    def is_exist(cls, primary_key):
        # if there are multiple primary keys, then set the args to tuple or map
        ret = cls.query.get(primary_key)
        if ret is None:
            return False
        return True

    @classmethod
    def get_all_gen_list(cls):
        return cls.query.all()

    @classmethod
    @abc.abstractmethod
    def update_obj(cls, args_dict):
        if cls.id.name not in args_dict:
            print('id is none')
            return None
        obj = cls.get(args_dict[cls.id.name])
        if obj is not None:
            for k in cls.__table__.columns:
                if k.name in args_dict and args_dict[k.name] is not None:
                    setattr(obj, k.name, args_dict[k.name])

        print(cls.to_dict(obj))
        return obj

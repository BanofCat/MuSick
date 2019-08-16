from SQLManager import sql_object
import abc
from Exception.SqlException import DBException
import decimal
from datetime import datetime, date, time
from sqlalchemy.orm.dynamic import AppenderQuery
from flask_sqlalchemy import BaseQuery, DeclarativeMeta


class BaseObject(object):

    # logging.config.fileConfig(LOG_CONFIG_FILE)
    # logger = logging.getLogger(DB_LOGGER_NAME)
    # logger.setLevel(logging.INFO)

    def __init__(self):
        pass

    @classmethod
    def add(cls, db_obj, need_commit=True):
        print("in %s: add" % cls.__name__)
        if not isinstance(db_obj, sql_object.Model):
            print("add obj failed, %s is not a db model object" % db_obj)
            raise DBException
        sql_object.session.add(db_obj)
        if need_commit:
            sql_object.session.commit()

    @classmethod
    def delete(cls, db_obj, need_commit=False):
        print("in %s: delete" % __name__)
        if not isinstance(db_obj, cls):
            print("delete obj failed, %s is not a kind of %s db model object" % (db_obj, __name__))
            raise DBException
        is_exist = sql_object.session.query().get(db_obj)
        # is_exist = cls.is_exist(db_obj)
        if not is_exist:
            print("db has not this object, can not delete a not exist obj")
            raise DBException

        sql_object.session.delete(db_obj)
        if need_commit:
            sql_object.session.commit()
        return True

    @classmethod
    def commit(cls):
        # try:
        print("in %s: commit" % __name__)
        sql_object.session.commit()
        # except SQLAlchemyError as e:
        #     sql_object.session.rollback()
        #     # print('commit failed : %s' % (str(e)))
        #     print("in %s: commit end error" % __name__)
            # raise ObjectNotExist(str(e))

    @classmethod
    def to_dict(cls, o):
        print('%s: to_dict' % __name__)
        if isinstance(o, list):
            obj_list = []
            for item in o:
                if isinstance(item, sql_object.Model):
                    obj_list.append(BaseObject.to_dict(item))
                else:
                    print('can not recognize type: %s' % type(item))
            print("to_dict_list: ", obj_list)
            return obj_list
        elif isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            counter = 0
            # for field in [x for x in dir(o) if not x.startswith('_') and x != 'metadata']:
            for field in o.__table__.columns:
                data = getattr(o, field.name)
                counter += 1

                if isinstance(data, datetime):
                    fields[field.name] = data.strftime("%Y-%m-%d %H:%M:%S.%F")[:-3]
                elif isinstance(data, date):
                    fields[field.name] = data.strftime("%Y-%m-%d")
                elif isinstance(data, time):
                    fields[field.name] = data.strftime("%H:%M:%S")
                elif isinstance(data, decimal.Decimal):
                    fields[field.name] = float(data)
                elif isinstance(data, int):
                    fields[field.name] = data
                elif isinstance(data, BaseQuery):
                    pass
                elif isinstance(data, AppenderQuery):
                    pass
                elif isinstance(data, type):
                    pass
                elif isinstance(data, sql_object.Model):
                    pass
                elif isinstance(data, str):
                    fields[field.name] = data
                else:
                    fields[field.name] = BaseObject.to_dict(data)
            print("to_dict: ", fields)
            return fields
        return None



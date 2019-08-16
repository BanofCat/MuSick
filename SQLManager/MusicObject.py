# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.BaseObject import BaseObject


class MusicObject(sql_object.Model, BaseObject):

    __tablename__ = 'MusicObject'

    id = sql_object.Column(sql_object.String(32), primary_key=True)

    name = sql_object.Column(sql_object.String(128), unique=False, nullable=False)

    singer = sql_object.Column(sql_object.String(128), nullable=True, unique=False)


    def __init__(self, id, use_type, producer):
        BaseObject.__init__(self)
        self._set_data(id, use_type, producer)

    def _set_data(self, id, use_type, producer):
        self.id = id
        self.use_type = use_type
        self.producer = producer

    @classmethod
    def to_obj(cls, args_dict):
        for k in MusicObject.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_cam = MusicObject(args_dict[MusicObject.id.name],
                              args_dict[MusicObject.use_type.name],
                              args_dict[MusicObject.producer.name])
        return new_cam




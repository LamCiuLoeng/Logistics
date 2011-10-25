# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import json, traceback
import sqlalchemy.types as types
from sqlalchemy.types import MutableType

__all__ = ['JSONColumn', ]


class JSONColumn(MutableType, types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        if value is None: return None
        return json.dumps(value, ensure_ascii = False)

    def process_result_value(self, value, dialect):
        try:
            return json.loads(str(value))
        except:
            traceback.print_exc()
            return None

    def compare_values(self, x, y): # x new value, y come from copy value

        return x == y

    def is_mutable(self): return True

    def copy_value(self, value):
        if value:
            return []
        return value

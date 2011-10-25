# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sys2do.model import DeclarativeBase
from auth import SysMixin


__all__ = ['DataDictionary', 'SystemLog', 'UploadFile']

#===============================================================================
# data table for system common function
#===============================================================================

class DataDictionary(DeclarativeBase):
    __tablename__ = 'system_data_dictionary'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))
    value = Column(Unicode(1000))


class SystemLog(DeclarativeBase, SysMixin):
    __tablename__ = 'system_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    type = Column(Unicode(100))
    remark = Column(Unicode(5000))


class UploadFile(DeclarativeBase, SysMixin):
    __tablename__ = 'system_upload_file'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))
    path = Column(Unicode(1000))
    url = Column(Unicode(1000))
    size = Column(Integer, default = None)
    type = Column(Unicode(20))
    remark = Column(Unicode(5000))

#===============================================================================
# 
#===============================================================================


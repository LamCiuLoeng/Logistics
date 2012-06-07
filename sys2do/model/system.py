# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import os
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer, Text
from sys2do.model import DeclarativeBase
from auth import SysMixin
from sys2do.setting import UPLOAD_FOLDER_PREFIX


__all__ = ['DataDictionary', 'SystemLog', 'UploadFile']

#===============================================================================
# data table for system common function
#===============================================================================

class DataDictionary(DeclarativeBase):
    __tablename__ = 'system_data_dictionary'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    value = Column(Text)


class SystemLog(DeclarativeBase, SysMixin):
    __tablename__ = 'system_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    type = Column(Text)
    remark = Column(Text)


class UploadFile(DeclarativeBase, SysMixin):
    __tablename__ = 'system_upload_file'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    path = Column(Text)
    url = Column(Text)
    size = Column(Integer, default = None)
    type = Column(Text)
    remark = Column(Text)

    @property
    def real_path(self):
        return os.path.join(UPLOAD_FOLDER_PREFIX, self.path)



#===============================================================================
# 
#===============================================================================


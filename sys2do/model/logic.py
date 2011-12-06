# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from master import *

ORDER_CANCELLED = -1
ORDER_NEW = 0
RECEIVED_GOODS = 1
IN_STORE = 2
OUT_STORE = 3
LOADED_GOODS = 4
IN_TRAVEL = 5
ORDER_COMPLETE = 9





class OrderHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))
    source_company = Column(Unicode(1000))

    target_company = Column(Unicode(1000))

    status = Column(Integer, default = 0)

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
                'source_company' : self.source_company,
                'target_company' : self.target_company,
                }



class DeliverHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))

    status = Column(Integer, default = 0)

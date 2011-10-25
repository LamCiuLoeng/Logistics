# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession

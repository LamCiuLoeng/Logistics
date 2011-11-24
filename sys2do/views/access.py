# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-23
#  @author: cl.lam
#  Description:
###########################################
'''
from base import createHandler, Handler
from sys2do.model import User, Group, Permission

__all__ = ['userHandler', 'groupHandler', 'permissionHandler']


userHandler = createHandler(User, name_for_url = 'userHandler')
groupHandler = createHandler(Group, name_for_url = 'groupHandler')
permissionHandler = createHandler(Permission, 'permissionHandler')

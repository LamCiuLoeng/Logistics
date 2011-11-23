# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-23
#  @author: cl.lam
#  Description:
###########################################
'''
from base import Handler
from sys2do.model import User, Group, Permission

__all__ = ['userHandler', 'groupHandler', 'permissionHandler']


userHandler = Handler(User, 'userHandler')
groupHandler = Handler(Group, 'groupHandler')
permissionHandler = Handler(Permission, 'permissionHandler',)

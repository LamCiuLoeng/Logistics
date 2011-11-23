# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import session

__all__ = ["get_permission", "get_all_permissions", "get_any_permissions",
           "in_group", "in_all_groups", "in_any_groups", ]

def get_permission(p):
    return p in session['user_profile']['permissions']

def get_all_permissions(psList):
    return all(map(lambda p: p in session['user_profile']['permissions'], psList))

def get_any_permissions(psList):
    return any(map(lambda p: p in session['user_profile']['permissions'], psList))


def in_group(g):
    return g in session['user_profile']['groups']

def in_all_groups(rsList):
    return all(map(lambda r: r in session['user_profile']['groups'], rsList))


def in_any_groups(rsList):
    return any(map(lambda r: r in session['user_profile']['groups'], rsList))

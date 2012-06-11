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
    if 'user_profile' not in session or p not in session['user_profile']['permissions']:
        return False
    else:
        return True


def get_all_permissions(psList):
    return all(map(lambda p: get_permission(p), psList))



def get_any_permissions(psList):
    return any(map(lambda p: get_permission(p), psList))


def in_group(g):
    if 'user_profile' not in session or g not in session['user_profile']['groups']:
        return False
    else:
        return True


def in_all_groups(rsList):
    return all(map(lambda r: in_group(r), rsList))


def in_any_groups(rsList):
    return any(map(lambda r: in_group(r), rsList))

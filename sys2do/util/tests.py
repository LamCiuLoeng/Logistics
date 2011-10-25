# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import session

__all__ = ["in_all_permissions", "in_any_permissions", "in_all_roles", "in_any_roles"]

def in_all_permissions(psList):
    return all(map(lambda p: p in session['user_profile']['permissions'], psList))


def in_any_permissions(psList):
    return any(map(lambda p: p in session['user_profile']['permissions'], psList))


def in_all_roles(rsList):
    return all(map(lambda r: r in session['user_profile']['roles'], rsList))


def in_any_roles(rsList):
    return any(map(lambda r: r in session['user_profile']['roles'], rsList))

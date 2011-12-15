# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-12
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
import random

__all__ = ['genSystemNo', 'getDeliverNo', ]

def genSystemNo():
    return 'DD%s%s' % (dt.now().strftime('%Y%m%d%H%M%S'), random.randint(0, 999))


def getDeliverNo():
    return 'DL%s%s' % (dt.now().strftime('%Y%m%d%H%M%S'), random.randint(0, 999))

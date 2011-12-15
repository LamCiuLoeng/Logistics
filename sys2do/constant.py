# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-6
#  @author: cl.lam
#  Description:
###########################################
'''

from flaskext.babel import _



MESSAGE_INFO = "INFO"
MESSAGE_ERROR = "ERROR"


#alert messages
MSG_NO_SUCH_ACTION = _('No such action!')
MSG_SAVE_SUCC = _('Save the record successfully!')
MSG_UPDATE_SUCC = _('Update the record successfully!')
MSG_DELETE_SUCC = _('Delete the record successfully!')
MSG_SERVER_ERROR = _('The service is not available temporarily,please try it later or contact the administrator.')
MSG_NO_ID_SUPPLIED = _('No ID supply for this record!')
MSG_RECORD_NOT_EXIST = _('The record does not exist!')
MSG_RECORD_ALREADY_EXIST = _('The record already exist!')


#order status
ORDER_CANCELLED = (-1, _('Cancelled'))
ORDER_NEW = (0, _('New'))
RECEIVED_GOODS = (1, _('Goods Received'))
IN_STORE = (2, _('In Store'))
OUT_STORE = (3, _('Out Store'))
LOADED_GOODS = (4, _('Goods Loaded'))
IN_TRAVEL = (5, _('In Travel'))
GOODS_ARRIVED = (6, _('Goods Arrived'))
GOODS_SIGNED = (7, _('Goods Signed'))

STATUS_LIST = [
               ORDER_CANCELLED, ORDER_NEW, RECEIVED_GOODS, IN_STORE, OUT_STORE, LOADED_GOODS, IN_TRAVEL,
               GOODS_ARRIVED, GOODS_SIGNED
               ]



#button label
BTN_SAVE = _('Save')
BTN_RESET = _('Reset')
BTN_CANCEL = _('Cancel')
BTN_RETURN = _('Return')

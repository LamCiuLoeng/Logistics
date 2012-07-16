# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-6
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from flaskext.babel import _



MESSAGE_INFO = "INFO"
MESSAGE_ERROR = "ERROR"


class T(object):
    def __init__(self, msg): self.msg = msg
    def __str__(self): return _(self.msg)
    def __unicode__(self): return _(self.msg)
    def __repr__(self): return _(self.msg)


#alert messages
MSG_NO_SUCH_ACTION = T('No such action!')
MSG_SAVE_SUCC = T('Save the record successfully!')
MSG_UPDATE_SUCC = T('Update the record successfully!')
MSG_DELETE_SUCC = T('Delete the record successfully!')
MSG_SERVER_ERROR = T('The service is not available temporarily,please try it later or contact the administrator.')
MSG_NO_ID_SUPPLIED = T('No ID supply for this record!')
MSG_RECORD_NOT_EXIST = T('The record does not exist!')
MSG_RECORD_ALREADY_EXIST = T('The record already exist!')
MSG_NO_FILE_UPLOADED = T('No file upload!')
MSG_INVALID_FILE_TO_UPLOAD = T('Invalid file to upload!')
MSG_USER_NOT_EXIST = T('This user does not exist!')
MSG_WRONG_PASSWORD = T('The password is wrong!')
MSG_CONFIRM_DELETE = T('Are your sure to delete this record ?')




LOG_CREATE_ORDER = T('Create Order.')
LOG_SEND_RECEIVER = T('Already send receiver to fetch the goods.')
LOG_GOODS_IN_WAREHOUSE = T('Goods have been gotten into warehouse.')
LOG_GOODS_SORTED = T('Goods have been sorted')
LOG_GOODS_SENT_OUT = T('Goods have been sent out.')
LOG_GOODS_IN_TRAVEL = T('Goods is in travel.')
LOG_GOODS_ARRIVAL = T('Goods have arrived.')
LOG_GOODS_SIGNED = T('Goods have been signed.')
LOG_GOODS_PICKUPED = T('Goods have been pickuped.')

#order status
ORDER_CANCELLED = (-1, T('Cancelled'))
ORDER_NEW = (0, T('New'))
ORDER_CONFIRMED = (1, T('Confirmed'))
ASSIGN_RECEIVER = (10, T('Assign Receiver'))
FETCH_GOODS = (11, T('Fetch Goods'))
IN_WAREHOUSE = (20, T('In Warehouse'))
SORTING = (30, T('Sorting'))
OUT_WAREHOUSE = (40, T('Out Warehouse'))
SEND_OUT = (50, T('Sent Out'))
IN_TRAVEL = (60, T('In Travel'))
GOODS_ARRIVED = (70, T('Goods Arrived'))
GOODS_SIGNED = (90, T('Goods Signed'))
GOODS_PICKUP = (95, T('Goods Pickuped'))


STATUS_LIST = [
               ORDER_CANCELLED, ORDER_NEW, ORDER_CONFIRMED, ASSIGN_RECEIVER, IN_WAREHOUSE, SORTING, OUT_WAREHOUSE, SEND_OUT, IN_TRAVEL,
               GOODS_ARRIVED, GOODS_SIGNED, GOODS_PICKUP
               ]



#button label
BTN_SAVE = T('Save')
BTN_INPUT = T('Input')
BTN_REVISE = T('Revise')
BTN_DELETE = T('Delete')
BTN_SUBMIT = T('Submit')
BTN_RESET = T('Reset')
BTN_CANCEL = T('Cancel')
BTN_RETURN = T('Return')


SYSTEM_NOW = lambda : dt.now()

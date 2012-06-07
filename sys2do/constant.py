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
MSG_NO_FILE_UPLOADED = _('No file upload!')
MSG_INVALID_FILE_TO_UPLOAD = _('Invalid file to upload!')

#order status
ORDER_CANCELLED = (-1, _('Cancelled'))
ORDER_NEW = (0, _('New'))
ASSIGN_PICKER = (10, _('Assign Picker'))
IN_WAREHOUSE = (20, _('In Warehouse'))
SORTING = (30, _('Sorting'))
#OUT_WAREHOUSE = (40, _('Out Warehouse'))
SEND_OUT = (50, _('Sent Out'))
IN_TRAVEL = (60, _('In Travel'))
GOODS_ARRIVED = (70, _('Goods Arrived'))
GOODS_SIGNED = (90, _('Goods Signed'))

STATUS_LIST = [
               ORDER_CANCELLED, ORDER_NEW, ASSIGN_PICKER, IN_WAREHOUSE, SORTING, IN_TRAVEL,
               GOODS_ARRIVED, GOODS_SIGNED
               ]



#button label
BTN_SAVE = _('Save')
BTN_SUBMIT = _('Submit')
BTN_RESET = _('Reset')
BTN_CANCEL = _('Cancel')
BTN_RETURN = _('Return')

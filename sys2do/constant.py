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

SYSTEM_DATE_FORMAT = "%Y-%m-%d"
SYSTEM_TIME_FORMAT = "%H:%M"
SYSTEM_DATETIME_FORMAT = "%Y-%m-%d %H:%M"

MESSAGE_INFO = "INFO"
MESSAGE_ERROR = "ERROR"


class T(object):
    def __init__(self, msg): self.msg = msg
    def __str__(self): return _(self.msg)
    def __unicode__(self): return _(self.msg)
    def __repr__(self): return _(self.msg)


#alert messages
MSG_NO_SUCH_ACTION = u'没有该操作！'
MSG_SAVE_SUCC = u'成功保存记录！'
MSG_UPDATE_SUCC = u'成功更新记录！'
MSG_DELETE_SUCC = u'成功删除记录！'
MSG_SERVER_ERROR = u'该服务暂时不可用，请稍后再试，或者联系系统管理员！'
MSG_NO_ID_SUPPLIED = u'没有提供记录的ID！'
MSG_RECORD_NOT_EXIST = u'该记录不存在！'
MSG_RECORD_ALREADY_EXIST = u'该记录已经存在！'
MSG_NO_FILE_UPLOADED = u'没有文件上传！'
MSG_INVALID_FILE_TO_UPLOAD = u'上传非法文件！'
MSG_USER_NOT_EXIST = u'该用户不存在！'
MSG_WRONG_PASSWORD = u'密码错误!'
MSG_CONFIRM_DELETE = u'你确认删除该记录吗？'




LOG_CREATE_ORDER = u'新建订单。'
LOG_SEND_RECEIVER = u'已派遣收件人取货。'
LOG_GOODS_IN_WAREHOUSE = u'货物已入仓。'
LOG_GOODS_SORTED = u'货物已分拣'
LOG_GOODS_SENT_OUT = u'货物已发出。'
LOG_GOODS_IN_TRAVEL = u'货物在运输途中。'
LOG_GOODS_ARRIVAL = u'货物已到达目的地。'
LOG_GOODS_SIGNED = u'货物已签收。'
LOG_GOODS_PICKUPED = u'货物已提货。'

#order status
ORDER_CANCELLED = (-1, u'已取消')
ORDER_NEW = (0, u'新建')
ORDER_CONFIRMED = (1, u'已确认')
ASSIGN_RECEIVER = (10, u'已指派收件人')
FETCH_GOODS = (11, u'在收件')
IN_WAREHOUSE = (20, u'已入仓')
SORTING = (30, u'已分拣')
OUT_WAREHOUSE = (40, u'已出仓')
SEND_OUT = (50, u'已发货')
IN_TRAVEL = (60, u'在途')
GOODS_ARRIVED = (70, u'货物已到达')
GOODS_SIGNED = (90, u'货物已签收')
GOODS_PICKUP = (95, u'货物已提货')


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

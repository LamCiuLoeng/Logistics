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
from sqlalchemy.orm.query import aliased



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


# alert messages
MSG_NO_SUCH_ACTION = u'没有该操作！'
MSG_SAVE_SUCC = u'成功保存记录！'
MSG_UPDATE_SUCC = u'成功更新记录！'
MSG_DELETE_SUCC = u'成功删除记录！'
MSG_SERVER_ERROR = u'该服务暂时不可用，请稍后再试，或者联系系统管理员！'
MSG_FORBIDDEN_ACCESS = u'禁止访问！'
MSG_NO_ID_SUPPLIED = u'没有提供记录的ID！'
MSG_RECORD_NOT_EXIST = u'该记录不存在！'
MSG_RECORD_ALREADY_EXIST = u'该记录已经存在！'
MSG_NO_FILE_UPLOADED = u'没有文件上传！'
MSG_INVALID_FILE_TO_UPLOAD = u'上传非法文件！'
MSG_USER_NOT_EXIST = u'该用户不存在！'
MSG_WRONG_PASSWORD = u'密码错误!'
MSG_CONFIRM_DELETE = u'你确认删除该记录吗？'
MSG_ORDER_NOT_FIT_FOR_DELIVER = u'所选择的订单中有状态不能创建送货单的记录，请注意订单状态再重新创建！'
MSG_ATLEAST_ONE_ORDER_TO_CREATE_DELIVER = u'请选择至少一条记录以创建送货单！'
MSG_ATLEAST_ONE_ORDER_TO_EXPORT = u'请先选择订单然后再导出！'
MSG_LEAVE_WITHOUT_SAVING = u'确认不保存而离开这个页面吗？'



LOG_CREATE_ORDER = u'新建订单。'
LOG_SEND_RECEIVER = u'已派遣收件人取货。'
LOG_GOODS_IN_WAREHOUSE = u'货物已入仓。'
LOG_GOODS_SORTED = u'货物已分拣'
LOG_GOODS_SENT_OUT = u'货物已发出。'
LOG_GOODS_IN_TRAVEL = u'货物在运输途中。'
LOG_GOODS_ARRIVAL = u'货物已到达目的地。'
LOG_GOODS_SIGNED = u'货物已签收。'
LOG_GOODS_PICKUPED = u'货物已提货。'

# order status
ORDER_DRAFT = (-2, u'草稿')
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
               ORDER_DRAFT, ORDER_CANCELLED, ORDER_NEW, ORDER_CONFIRMED, ASSIGN_RECEIVER, IN_WAREHOUSE, SORTING, OUT_WAREHOUSE, SEND_OUT, IN_TRAVEL,
               GOODS_ARRIVED, GOODS_SIGNED, GOODS_PICKUP
               ]



# validate status
ORDER_NOT_MAKE_APPROVAL = (0, u'未审核')
ORDER_APPROVED = (1, u'审核通过')
ORDER_DISAPPROVED = (2, u'审核不通过')


APPROVAL_STATUS_LIST = [ORDER_NOT_MAKE_APPROVAL, ORDER_APPROVED, ORDER_DISAPPROVED]


# paid status
ORDER_NOT_PAID = (0, u'客户未付款')
ORDER_PAID = (1, u'客户已付款')
ORDER_PAID_STATUS_LIST = [ORDER_NOT_PAID, ORDER_PAID]


DELIVER_NOT_PAID = (0, u'未付款予承运商')
DELIVER_PAID = (1, u'已付款予承运商')
DELIVER_PAID_STATUS_LIST = [DELIVER_NOT_PAID, DELIVER_PAID ]

ORDER_NOT_RETURN_NOTE = (0, u'客户未返回单')
ORDER_RETURN_NOTE = (1, u'客户已返回单')
ORDER_RETURN_STATUS_LIST = [ORDER_NOT_RETURN_NOTE, ORDER_RETURN_NOTE ]




# button label
BTN_SAVE = T('Save')
BTN_INPUT = T('Input')
BTN_REVISE = T('Revise')
BTN_DELETE = T('Delete')
BTN_SUBMIT = T('Submit')
BTN_RESET = T('Reset')
BTN_CANCEL = T('Cancel')
BTN_RETURN = T('Return')


SYSTEM_NOW = lambda : dt.now()


def _getMaster(v):
    from sys2do.util.common import getMasterAll
    return getMasterAll(v)

MASTER_ALL = _getMaster


def _getRelatedCity(cid):
    from sys2do.util.common import getRelatedCity
    return getRelatedCity(cid)


RELATED_CITY = _getRelatedCity

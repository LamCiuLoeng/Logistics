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
from sys2do.model import DBSession
from sys2do.model.logic import DeliverDetail, DeliverHeader
from sqlalchemy.sql.functions import sum
from sqlalchemy.sql.expression import and_
from sys2do.model.master import Barcode

__all__ = ['getDeliverNo', ]



def getDeliverNo():
    return 'DL%s%s' % (dt.now().strftime('%Y%m%d%H%M%S'), random.randint(0, 999))



#def updateDeliverHeaderStatus(id, status):
#    dheader = DBSession.query(DeliverHeader).get(id)
#    dheader.status = status
#
#    will_affected_order_details = []
#    will_affected_order_headers = []
#
#    actual_affected_order_details = []
#    actual_affected_order_headers = []
#
#    for ddetail in dheader.details :
#        ddetail.status = status
#        if ddetail.order_detail not in will_affected_order_details : will_affected_order_details.append(ddetail.order_detail)
#
#    for odetail in will_affected_order_details:
#        total_deliver_qty = DBSession.query(sum(DeliverDetail.deliver_qty)).filter(and_(DeliverDetail.active == 0,
#                                                                                        DeliverDetail.order_detail_id == odetail.id,
#                                                                                        DeliverDetail.status >= status)).scalar()
#        if total_deliver_qty >= odetail.order_qty:
#            odetail.status = status
#            actual_affected_order_details.append(odetail)
#            if odetail.header not in will_affected_order_headers : will_affected_order_headers.append(odetail.header)
#
#    for oheader in will_affected_order_headers:
#        if all(map(lambda v : v.status >= status, oheader.details)) :
#            oheader.status = status
#            actual_affected_order_headers.append(oheader)
#
#
#    return (actual_affected_order_headers, actual_affected_order_details)
#
#
#
#
#
#def updateDeliverDetailsStatus(id, status):
#    ddetail = DBSession.query(DeliverDetail).get(id)
#    ddetail.status = status
#
#    #if all the detail of the header's status is the same ,update the header's status
#    if all(map(lambda d : d.status >= status, ddetail.header.details)) : ddetail.header.status = status
#
#    total_deliver_qty = DBSession.query(sum(DeliverDetail.deliver_qty))\
#        .filter(and_(DeliverDetail.order_detail_id == ddetail.order_detail_id, DeliverDetail.status >= status)).scalar()
#
#    affected_order_headers = None
#    #if all the deliver qty more than the order qty, meaning that all the order detail need to change the status
#    if total_deliver_qty >= ddetail.order_detail.order_qty :
#        ddetail.order_detail.status = status
#        affected_order_headers = ddetail.order_detail.header
#
#    if affected_order_headers:
#        if all(map(lambda d : d.status >= status, affected_order_headers.details)) : affected_order_headers.status = status



# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from master import *

ORDER_CANCELLED = -1
ORDER_NEW = 0
RECEIVED_GOODS = 1
IN_STORE = 2
OUT_STORE = 3
LOADED_GOODS = 4
IN_TRAVEL = 5
ORDER_COMPLETE = 9



class CommonMixin(object):
    remark = Column(Unicode(50000))
    attachments = Column(Unicode(10000))



class OrderHeader(DeclarativeBase, SysMixin, CommonMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))
#    order_time = Column(DateTime, default = dt.now)
    order_type = Column(Unicode(50))
    payment_id = Column(Integer, ForeignKey('master_payment.id'))
    payment = relation(Payment)

    #for source
    source_company = Column(Unicode(1000))
    source_company_address = Column(Unicode(5000))
    source_contact_person = Column(Unicode(100))
    source_contact_phone = Column(Unicode(100))
    source_address = Column(Unicode(5000))
    arrive_source_time = Column(Unicode(50))
    order_maker = Column(Unicode(100))
    saler = Column(Unicode(100))

    #for target
    target_company = Column(Unicode(1000))
    target_company_address = Column(Unicode(5000))
    target_contact_person = Column(Unicode(100))
    target_contact_phone = Column(Unicode(100))
    target_address = Column(Unicode(5000))

    #for cars
    cars_send_out_time = Column(Unicode(100))
    cars_sender = Column(Unicode(100))
    cars_no = Column(Unicode(100))
    cars_driver = Column(Unicode(100))
    cars_arrive_time = Column(Unicode(100))
    cars_remark = Column(Unicode(1000))

    goods_weight = Column(Float, default = 0)
    goods_weight_unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    goods_weight_unit = relation(ItemUnit, primaryjoin = goods_weight_unit_id == ItemUnit.id, lazy = False)
    goods_size = Column(Float, default = 0)
    goods_size_unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    goods_size_unit = relation(ItemUnit, primaryjoin = goods_size_unit_id == ItemUnit.id, lazy = False)

    cost = Column(Float, default = 0)
    status = Column(Integer, default = 0)


    def populate(self):
        values = {}
        fields = ['id', 'no', 'order_type', 'payment_id', 'source_company', 'source_company_address', 'source_contact_person',
                  'source_contact_phone', 'source_address', 'arrive_source_time', 'order_maker', 'saler',
                  'target_company', 'target_company_address', 'target_contact_person', 'target_contact_phone', 'target_address',
                  'goods_weight', 'goods_weight_unit_id', 'goods_size', 'goods_size_unit_id', 'remark', ]
        for f in fields : values[f] = getattr(self, f)
        return values

class OrderDetail(DeclarativeBase, SysMixin, CommonMixin):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader)
    line_no = Column(Integer, default = 0)

    item_id = Column(Integer, ForeignKey('master_item.id'))
    item = relation(Item)
    unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    unit = relation(ItemUnit)
    qty = Column(Integer, default = 0)

    status = Column(Integer, default = 0)



class ShipmentHeader(DeclarativeBase, SysMixin, CommonMixin):
    __tablename__ = 'shipment_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))
    leave_time = Column(DateTime)
    arrive_time = Column(DateTime)
    vendor_id = Column(Integer, ForeignKey('master_vendor.id'))
    vendor = relation(Vendor)
    payment_id = Column(Integer, ForeignKey('master_payment.id'))
    payment = relation(Payment)

    status = Column(Integer, default = 0)



class ShipmentDetail(DeclarativeBase, SysMixin, CommonMixin):
    __tablename__ = 'shipment_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('shipment_header.id'))
    header = relation(ShipmentHeader)
    line_no = Column(Integer, default = 0)

    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    order_detail = relation(OrderDetail)

    logistics_unit_id = Column(Integer, ForeignKey('master_logistics_unit.id'))
    logistics_unit = relation(LogisticsUnit)

    qty = Column(Float, default = 0)

    leave_time = Column(DateTime)
    arrive_time = Column(DateTime)
    receiver = Column(Unicode(1000))



class ShipmentLog(DeclarativeBase, SysMixin, CommonMixin):
    __tablename__ = 'shipment_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('shipment_header.id'))
    header = relation(ShipmentHeader)

    category_id = Column(Integer, ForeignKey('master_shipment_log_category.id'))
    category = relation(ShipmentLogCategory)


#class Transportation(DeclarativeBase, SysMixin):
#    __tablename__ = 'transportation'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#
#    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
#    order_detail = relation(OrderDetail)
#
#    logistics_unit_id = Column(Integer, ForeignKey('master_logistics_unit.id'))
#    logistics_unit = relation(LogisticsUnit)
#
#    status = Column(Integer, default = 0)
#    remark = Column(Unicode(10000))
#
#
#
#class TransportationLog(DeclarativeBase, SysMixin):
#    __tablename__ = 'transportation_log'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    transportation_id = Column(Integer, ForeignKey('transportation.id'))
#    transportation = relation(Transportation)
#    remark = Column(Unicode(10000))

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
from sys2do.model.master import Customer, Vendor, Item, ItemUnit








class OrderHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))

    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("orders", order_by = id), primaryjoin = "and_(Customer.id == OrderHeader.customer_id, OrderHeader.active == 0)")

    customer_address = Column(Unicode(5000))

    vendor_id = Column(Integer, ForeignKey('master_vendor.id'))
    vendor = relation(Vendor, backref = backref("orders", order_by = id), primaryjoin = "and_(Vendor.id == OrderHeader.vendor_id, OrderHeader.active == 0)")
    vendor_address = Column(Unicode(5000))

    expect_time = Column(DateTime)

    status = Column(Integer, default = 0)


    def __str__(self): return self.no

    def __repr__(self): return self.no

    def __unicode__(self): return self.no

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
                'customer' : self.customer,
                'vendor' : self.vendor,
                'status' : self.status,
                }



class OrderDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("details", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderDetail.header_id, OrderDetail.active == 0)")

    item_id = Column(Integer, ForeignKey('master_item.id'))
    item = relation(Item, backref = backref("details", order_by = id), primaryjoin = "and_(Item.id == OrderDetail.item_id, OrderDetail.active == 0)")

    qty = Column(Integer, default = 0)

    item_unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    item_unit = relation(ItemUnit, backref = backref("details", order_by = id), primaryjoin = "and_(ItemUnit.id == OrderDetail.item_unit_id, OrderDetail.active == 0)")

    status = Column(Integer, default = 0)



class DeliverHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))

    status = Column(Integer, default = 0)



    def get_related_orders(self):
        orders = []
        for d in self.details:
            if d.order_detail.header not in orders : orders.append(d.order_detail.header)
        return orders




class DeliverDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)

    header_id = Column(Integer, ForeignKey('deliver_header.id'))
    header = relation(DeliverHeader, backref = backref("details", order_by = id), primaryjoin = "and_(DeliverHeader.id == DeliverDetail.header_id, DeliverDetail.active == 0)")

    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    order_detail = relation(OrderDetail, backref = backref("deliver_details", order_by = id), primaryjoin = "and_(OrderDetail.id == DeliverDetail.order_detail_id, DeliverDetail.active == 0)")










class OrderLog(DeclarativeBase, SysMixin):
    __tablename__ = 'order_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    order_id = Column(Integer, ForeignKey('order_header.id'))
    order = relation(OrderHeader, backref = backref("logs", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderLog.order_id, OrderLog.active == 0)")
    remark = Column(Unicode(5000))

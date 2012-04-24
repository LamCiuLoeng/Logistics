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
from sqlalchemy.types import Unicode, Integer, DateTime, Float, Date
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from sys2do.model.master import Customer, Supplier, Item, ItemUnit, ShipmentType, \
    WeightUnit








class OrderHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))

    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("orders", order_by = id), primaryjoin = "and_(Customer.id == OrderHeader.customer_id, OrderHeader.active == 0)")

    source_address = Column(Unicode(5000))
    source_contact = Column(Unicode(100))
    source_tel = Column(Unicode(100))

    remark = Column(Unicode(10000))
    status = Column(Integer, default = 0)


    def __str__(self): return self.no

    def __repr__(self): return self.no

    def __unicode__(self): return self.no

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
                'customer' : self.customer,
                'source_address' : self.source_address,
                'source_contact' : self.source_contact,
                'source_tel' : self.source_tel,
                'remark' : self.remark,
                'status' : self.status,
                }

    def update_status(self, status):
        self.status = status
        for d in self.details : d.status = status



class OrderDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("details", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderDetail.header_id, OrderDetail.active == 0)")

#    item_id = Column(Integer, ForeignKey('master_item.id'))
#    item = relation(Item, backref = backref("details", order_by = id), primaryjoin = "and_(Item.id == OrderDetail.item_id, OrderDetail.active == 0)")


    line_no = Column(Integer, default = 1)
    item = Column(Unicode(1000))
    order_qty = Column(Float, default = 0) #client order qty
    delivered_qty = Column(Integer)
    unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    unit = relation(ItemUnit)

    weight = Column(Float, default = 0)
    weight_unit_id = Column(Integer, ForeignKey('master_weight_unit.id'))
    weight_unit = relation(WeightUnit)

    shipment_type_id = Column(Integer, ForeignKey('master_shipment_type.id'))
    shipment_type = relation(ShipmentType)
#    shipment_instruction = Column(Unicode(5000))

    destination_address = Column(Unicode(5000))
    destination_contact = Column(Unicode(100))
    destination_tel = Column(Unicode(100))

    expect_time = Column(Date, default = None)
    remark = Column(Unicode(10000))
    status = Column(Integer, default = 0)



class DeliverHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))

    destination_address = Column(Unicode(5000))
    supplier_id = Column(Integer, ForeignKey('master_supplier.id'))
    supplier = relation(Supplier)

    supplier_contact = Column(Unicode(100))
    supplier_tel = Column(Unicode(100))

    expect_time = Column(Date, default = None)
    remark = Column(Unicode(10000))
    status = Column(Integer, default = 0)



    def get_related_orders(self):
        orders = []
        for d in self.details:
            if d.order_detail.header not in orders : orders.append(d.order_detail.header)
        return orders

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
                'destination_address' : self.destination_address,
                'supplier_id' : self.supplier_id,
                'supplier' : self.supplier,
                'supplier_contact' : self.supplier_contact,
                'supplier_tel' : self.supplier_tel,
                'expect_time' : self.expect_time,
                'remark' : self.remark,
                'status' : self.status,
                }


class DeliverDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)

    header_id = Column(Integer, ForeignKey('deliver_header.id'))
    header = relation(DeliverHeader, backref = backref("details", order_by = id), primaryjoin = "and_(DeliverHeader.id == DeliverDetail.header_id, DeliverDetail.active == 0)")
    line_no = Column(Integer, default = 1)

    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    order_detail = relation(OrderDetail, backref = backref("deliver_details", order_by = id), primaryjoin = "and_(OrderDetail.id == DeliverDetail.order_detail_id, DeliverDetail.active == 0)")
    order_detail_line_no = Column(Integer)

    deliver_qty = Column(Integer)

    remark = Column(Unicode(10000))
    status = Column(Integer, default = 0)





class OrderLog(DeclarativeBase, SysMixin):
    __tablename__ = 'order_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    order_header_id = Column(Integer, ForeignKey('order_header.id'))
    order_header = relation(OrderHeader, backref = backref("logs", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderLog.order_header_id, OrderLog.active == 0)")

    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    order_detail = relation(OrderDetail, backref = backref("logs", order_by = id), primaryjoin = "and_(OrderDetail.id == OrderLog.order_detail_id, OrderLog.active == 0)")
    remark = Column(Unicode(5000))

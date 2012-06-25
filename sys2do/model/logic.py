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
from sqlalchemy.types import Unicode, Integer, DateTime, Float, Date, Text
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from sys2do.model.master import Customer, Supplier, ItemUnit, ShipmentType, \
    WeightUnit, InventoryLocation
from sys2do.model.auth import CRUDMixin
from sys2do.model.system import UploadFile
from sqlalchemy.sql.expression import and_








class OrderHeader(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Text)

    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("orders", order_by = id), primaryjoin = "and_(Customer.id == OrderHeader.customer_id, OrderHeader.active == 0)")


#    source_province_id = Column(Integer, ForeignKey('master_province.id'))
#    source_provice = relation(Province)
#    source_city_id = Column(Integer, ForeignKey('master_city.id'))
#    source_city = relation(City)
#    source_district_id = Column(Integer, ForeignKey('master_district.id'))
#    source_district = relation(District)

    source_address = Column(Text)
    source_contact = Column(Text)
    source_tel = Column(Text)
    source_mobile = Column(Text)

    picker = Column(Text)
    picker_contact = Column(Text)
    picker_remark = Column(Text)

    in_warehouse_remark = Column(Text)

    remark = Column(Text)
    barcode_id = Column(Integer, ForeignKey('system_upload_file.id'))
    barcode = relation(UploadFile)
    amount = Column(Float, default = 0)
    status = Column(Integer, default = 0)

    def __str__(self): return self.no

    def __repr__(self): return self.no

    def __unicode__(self): return self.no

    def populate(self):

#        address = " ".join(filter(lambda v: v or '', [self.source_provice, self.source_city, self.source_district, self.source_address]))

        return {
                'id' : self.id,
                'no' : self.no,
                'customer' : self.customer,
#                'source_provice' : self.source_provice,
#                'source_city' : self.source_city,
#                'source_district' : self.source_district,
                'source_address' : self.source_address,
                'source_contact' : self.source_contact,
                'source_tel' : self.source_tel,
                'picker' : self.picker,
                'picker_contact' : self.picker_contact,
                'picker_remark' : self.picker_remark,
                'in_warehouse_remark' : self.in_warehouse_remark,
                'remark' : self.remark,
                'status' : self.status,
                'barcode' : self.barcode,
                'amount' : self.amount,
#                'destination_full_address' : self.destination_full_address,
                }

    def update_status(self, status):
        self.status = status
        for d in self.details :
            if d.status < self.status : d.status = status

    def get_logs(self):
        return DBSession.query(TransferLog).filter(and_(
                                                TransferLog.active == 0,
                                                TransferLog.type == 0,
                                                TransferLog.refer_id == self.id
                                                )).order_by(TransferLog.id)


#    @property
#    def destination_full_address(self):
#        return "".join(filter(lambda v:v, [self.source_provice, self.source_city, self.source_address]))


class OrderDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("details", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderDetail.header_id, OrderDetail.active == 0)")

#    item_id = Column(Integer, ForeignKey('master_item.id'))
#    item = relation(Item, backref = backref("details", order_by = id), primaryjoin = "and_(Item.id == OrderDetail.item_id, OrderDetail.active == 0)")


    line_no = Column(Integer, default = 1)
    no = Column(Text)
    item = Column(Text)
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

#    destination_province_id = Column(Integer, ForeignKey('master_province.id'))
#    destination_provice = relation(Province)
#    destination_city_id = Column(Integer, ForeignKey('master_city.id'))
#    destination_city = relation(City)
#    destination_district_id = Column(Integer, ForeignKey('master_district.id'))
#    destination_district = relation(District)
    destination_address = Column(Text)
    destination_contact = Column(Text)
    destination_tel = Column(Text)
    destination_mobile = Column(Text)

    expect_time = Column(Date, default = None)
    actual_time = Column(Date, default = None)

#    charge_type = 
    barcode_id = Column(Integer, ForeignKey('system_upload_file.id'))
    barcode = relation(UploadFile)
    charge = Column(Float, default = 0)
    inventory_location_id = Column(Integer, ForeignKey('master_inventory_location.id'))
    inventory_location = relation(InventoryLocation, backref = backref("items", order_by = id))
    remark = Column(Text)
    status = Column(Integer, default = 0)


    def update_status(self, status):
        self.status = status
        self.header.status = min([d.status for d in self.header.details])

#    @property
#    def destination_full_address(self):
#        return "".join(filter(lambda v:v, [self.destination_provice, self.destination_city, self.destination_address]))




class DeliverHeader(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'deliver_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Text)

#    destination_province_id = Column(Integer, ForeignKey('master_province.id'))
#    destination_provice = relation(Province)
#    destination_city_id = Column(Integer, ForeignKey('master_city.id'))
#    destination_city = relation(City)
    destination_address = Column(Text)
    supplier_id = Column(Integer, ForeignKey('master_supplier.id'))
    supplier = relation(Supplier)

    supplier_contact = Column(Text)
    supplier_tel = Column(Text)

    need_transfer = Column(Text)

    send_out_remark = Column(Text)
    arrived_remark = Column(Text)

    expect_time = Column(Date, default = None)
    actual_time = Column(Date, default = None)

    amount = Column(Float, default = 0)

    remark = Column(Text)
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
                'create_time' : self.create_time,
                'create_by' : self.create_by,
                'update_time' : self.update_time,
                'update_by' : self.update_by,
                }

    def update_status(self, status):
        self.status = status
        for d in self.details :
            if d.status < self.status : d.status = status


    def get_logs(self):
        return DBSession.query(TransferLog).filter(and_(
                                                TransferLog.active == 0,
                                                TransferLog.type == 1,
                                                TransferLog.refer_id == self.id
                                                )).order_by(TransferLog.id)

#    @property
#    def destination_full_address(self):
#        return "".join(filter(lambda v:v, [self.destination_provice, self.destination_city, self.destination_address]))


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

    remark = Column(Text)
    cost = Column(Float, default = 0)
    status = Column(Integer, default = 0)


    def update_status(self, status):
        self.status = status
        self.header.status = min([d.status for d in self.header.details])


#class OrderLog(DeclarativeBase, SysMixin):
#    __tablename__ = 'order_log'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    order_header_id = Column(Integer, ForeignKey('order_header.id'))
#    order_header = relation(OrderHeader, backref = backref("logs", order_by = id), primaryjoin = "and_(OrderHeader.id == OrderLog.order_header_id, OrderLog.active == 0)")
#
#    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
#    order_detail = relation(OrderDetail, backref = backref("logs", order_by = id), primaryjoin = "and_(OrderDetail.id == OrderLog.order_detail_id, OrderLog.active == 0)")
#    remark = Column(Text)
#
#
#class DeliverLog(DeclarativeBase, SysMixin):
#    __tablename__ = 'deliver_log'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    deliver_header_id = Column(Integer, ForeignKey('deliver_header.id'))
#    deliver_header = relation(DeliverHeader, backref = backref("logs", order_by = id), primaryjoin = "and_(DeliverHeader.id == DeliverLog.deliver_header_id, DeliverLog.active == 0)")
#
#    remark = Column(Text)



class TransferLog(DeclarativeBase, SysMixin):
    __tablename__ = 'transfer_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    refer_id = Column(Integer)
    transfer_date = Column(Text)
    type = Column(Integer, default = 0) # 0 is order ,1 is deliver
    remark = Column(Text)

# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import traceback
from datetime import datetime as dt
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float, Date, Text
from sqlalchemy.orm import relation, backref, synonym
from sqlalchemy.sql.expression import and_
from flask import session


from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from sys2do.model.master import Customer, Supplier, ItemUnit, ShipmentType, \
    WeightUnit, InventoryLocation, Payment, PickupType, PackType, CustomerTarget, \
    Receiver, Item, Note, Province, City, CustomerSource
from sys2do.model.auth import CRUDMixin, User
from sys2do.model.system import UploadFile, SystemLog
from sys2do.util.common import _error




class OrderHeader(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)

    no = Column(Text, doc = u'系统编号')
    ref_no = Column(Text, doc = u'单号')

    note_id = Column(Integer, ForeignKey('master_note.id'), doc = u'票据前缀')
    note = relation(Note, backref = backref("orders", order_by = id), primaryjoin = "and_(Note.id == OrderHeader.note_id, OrderHeader.active == 0)")
    note_no = Column(Text, doc = u'票据号码')
    customer_id = Column(Integer, ForeignKey('master_customer.id'), doc = u'客户')
    customer = relation(Customer, backref = backref("orders", order_by = id), primaryjoin = "and_(Customer.id == OrderHeader.customer_id, OrderHeader.active == 0)")

    source_province_id = Column(Integer, ForeignKey('master_province.id'), doc = u'始发站(省)')
    source_province = relation(Province, backref = backref("source_orders", order_by = id), primaryjoin = "and_(Province.id == OrderHeader.source_province_id, OrderHeader.active == 0)")
    source_city_id = Column(Integer, ForeignKey('master_city.id'), doc = u'始发站(市)')
    source_city = relation(City, backref = backref("source_orders", order_by = id), primaryjoin = "and_(City.id == OrderHeader.source_city_id, OrderHeader.active == 0)")

    source_company_id = Column(Integer, ForeignKey('master_customer_source.id'), doc = u'发货公司')
    source_company = relation(CustomerSource)
    source_address = Column(Text, doc = u'发货地址')
    source_contact = Column(Text, doc = u'发货人')
    source_tel = Column(Text, doc = u'发货人电话')
    source_mobile = Column(Text, doc = u'发货人手机')
    source_sms = Column(Integer, default = 0, doc = u'发货人短信通知') # 0 is no sms, 1 is send sms when the order status changed

    payment_id = Column(Integer, ForeignKey('master_payment.id'), doc = u'付款方式')
    payment = relation(Payment)

    qty = Column(Float, default = None, doc = u'数量') #client order qty
    unit_id = Column(Integer, ForeignKey('master_item_unit.id'), doc = u'')
    unit = relation(ItemUnit)

    weight = Column(Float, default = None, doc = u'重量')
    weight_unit_id = Column(Integer, ForeignKey('master_weight_unit.id'), doc = u'')
    weight_unit = relation(WeightUnit)

    vol = Column(Float, default = None, doc = u'体积')

    shipment_type_id = Column(Integer, ForeignKey('master_shipment_type.id'), doc = u'')
    shipment_type = relation(ShipmentType)

    pickup_type_id = Column(Integer, ForeignKey('master_pickup_type.id'), doc = u'提货方式')
    pickup_type = relation(PickupType)

    pack_type_id = Column(Integer, ForeignKey('master_pack_type.id'), doc = u'包装方式')
    pack_type = relation(PackType)


    destination_province_id = Column(Integer, ForeignKey('master_province.id'), doc = u'目的站(省)')
    destination_province = relation(Province, backref = backref("destination_orders", order_by = id), primaryjoin = "and_(Province.id == OrderHeader.destination_province_id, OrderHeader.active == 0)")
    destination_city_id = Column(Integer, ForeignKey('master_city.id'), doc = u'目的站(市)')
    destination_city = relation(City, backref = backref("destination_orders", order_by = id), primaryjoin = "and_(City.id == OrderHeader.destination_city_id, OrderHeader.active == 0)")

    destination_company_id = Column(Integer, ForeignKey('master_customer_target.id'), doc = u'收货公司')
    destination_company = relation(CustomerTarget)
    destination_address = Column(Text, doc = u'收货地址')
    destination_contact = Column(Text, doc = u'收货人')
    destination_tel = Column(Text, doc = u'收货人电话')
    destination_mobile = Column(Text, doc = u'收货人手机')
    destination_sms = Column(Integer, default = 0, doc = u'收货人短信通知') # 0 is no sms, 1 is send sms when the order arrive


    order_time = Column(Text, doc = u'下单时间')
    estimate_time = Column(Text, doc = u'估计到达')
    expect_time = Column(Text, doc = u'到达预期')
    actual_time = Column(Text, doc = u'实际到达')

    qty_ratio = Column(Float, default = None, doc = u'件数费率')
    weight_ratio = Column(Float, default = None, doc = u'重量费率')
    vol_ratio = Column(Float, default = None, doc = u'体积费率')

    insurance_charge = Column(Float, default = 0, doc = u'保险费用')
    sendout_charge = Column(Float, default = 0, doc = u'送货费用')
    receive_charge = Column(Float, default = 0, doc = u'上门接货费用')
    package_charge = Column(Float, default = 0, doc = u'包装费用')
    load_charge = Column(Float, default = 0, doc = u'装货费用')
    unload_charge = Column(Float, default = 0, doc = u'卸货费用')
    proxy_charge = Column(Float, default = 0, doc = u'代理费用')
    actual_proxy_charge = Column(Float, default = 0, doc = u'已退回扣')
    other_charge = Column(Float, default = 0, doc = u'其它费用')
    amount = Column(Float, default = 0, doc = u'金额(元)')
    cost = Column(Float, default = 0, doc = u'')

    receiver_contact_id = Column(Integer, ForeignKey('master_receiver.id'), doc = u'')
    receiver_contact = relation(Receiver, backref = backref("orders", order_by = id), primaryjoin = "and_(Receiver.id == OrderHeader.receiver_contact_id, OrderHeader.active == 0)")
#    receiver_contact = Column(Text)
    receiver_tel = Column(Text, doc = u'')
    receiver_mobile = Column(Text, doc = u'')
    receiver_remark = Column(Text, doc = u'')


    signed_contact = Column(Text, doc = u'')
    signed_tel = Column(Text, doc = u'')
    signed_time = Column(Text, doc = u'')
    signed_remark = Column(Text, doc = u'')

    barcode_id = Column(Integer, ForeignKey('system_upload_file.id'), doc = u'')
    barcode = relation(UploadFile)

    inventory_location_id = Column(Integer, ForeignKey('master_inventory_location.id'), doc = u'')
    inventory_location = relation(InventoryLocation, backref = backref("items", order_by = id))

    approve = Column(Integer, default = 0, doc = u'') # 0 is undone ,1 is approved ,2 is disapprove
    paid = Column(Integer, default = 0, doc = u'') # 0 is not paid, 1 is paid
    supplier_paid = Column(Integer, default = 0, doc = u'') # 0 is not paid to supplier, 1 is paid to supplier
    is_exception = Column(Integer, default = 0, doc = u'') # 0 is normal ,1 is exception
    is_less_qty = Column(Integer, default = 0, doc = u'') # 0 is normal ,1 is less than the order qty
    is_return_note = Column(Integer, default = 0, doc = u'') # 0 is not return note ,1 is return note
    is_discount_return = Column(Integer, default = 0, doc = u'') # 0 is not discount ,1 is discount
    discount_return_time = Column(Text, doc = u'退款时间')
    discount_return_person_id = Column(Integer, ForeignKey('system_user.id'), doc = u'退款人员')
    discount_return_person = relation(User)
    discount_return_remark = Column(Text, doc = u'退款备注')

    remark = Column(Text, doc = u'')

    deliver_header_ref = Column(Integer, default = None, doc = u'')
    deliver_header_no = Column(Text, doc = u'')
    status = Column(Integer, default = 0, doc = u'')


    def __str__(self): return self.no
    def __repr__(self): return self.no
    def __unicode__(self): return self.no

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
                'customer' : self.customer,
#                'source_province' : self.source_province,
#                'source_city' : self.source_city,
#                'source_district' : self.source_district,
                'source_address' : self.source_address,
                'source_contact' : self.source_contact,
                'source_tel' : self.source_tel,
#                'picker' : self.picker,
#                'picker_contact' : self.picker_contact,
#                'picker_remark' : self.picker_remark,
#                'in_warehouse_remark' : self.in_warehouse_remark,
                'remark' : self.remark,
                'status' : self.status,
                'barcode' : self.barcode,
                'amount' : self.amount,
#                'destination_full_address' : self.destination_full_address,
                }

    def update_status(self, status):
        self.status = status


    def get_logs(self):
        return DBSession.query(TransferLog).filter(and_(
                                                TransferLog.active == 0,
                                                TransferLog.type == 0,
                                                TransferLog.refer_id == self.id
                                                )).order_by(TransferLog.transfer_date)


    def get_deliver_header(self):
        try:
            deliver = DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == self.id)).one()
            return deliver.header
        except:
            return None


    @property
    def deliver_header(self):
        try:
            return DBSession.query(DeliverHeader).get(self.deliver_header_ref)
        except:
            return None


    def insert_system_logs(self, comare_result):
        try:
            _remark = [u"[%s]'%s' 修改为 '%s'" % (name, ov, nv) for (name, ov, nv) in comare_result['update']]
            DBSession.add(SystemLog(
                                    type = self.__class__.__name__,
                                    ref_id = self.id,
                                    remark = u"%s 修改该记录。%s" % (session['user_profile']['name'], ";".join(_remark))
                                    ))
            DBSession.commit()
        except:
            DBSession.rollback()
            _error(traceback.print_exc())


class ItemDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_item_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("item_details", order_by = id), primaryjoin = "and_(OrderHeader.id == ItemDetail.header_id, ItemDetail.active == 0)")

    item_id = Column(Integer, ForeignKey('master_item.id'))
    item = relation(Item, backref = backref("order_details", order_by = id), primaryjoin = "and_(Item.id == ItemDetail.item_id, ItemDetail.active == 0)")

#    item = Column(Text)
    qty = Column(Float, default = None) #client order qty
    vol = Column(Float, default = None)
    weight = Column(Float, default = None)
    remark = Column(Text)



class WarehouseDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_warehouse_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("warehouse_details", order_by = id), primaryjoin = "and_(OrderHeader.id == WarehouseDetail.header_id, WarehouseDetail.active == 0)")

    action_type = Column(Text)
    action_time = Column(Text)
#    location_id = Column(Integer, ForeignKey('master_inventory_location.id'))
#    location = relation(InventoryLocation)
    remark = Column(Text)




#class TransitDetail(DeclarativeBase, SysMixin):
#    __tablename__ = 'order_transit_detail'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    header_id = Column(Integer, ForeignKey('order_header.id'))
#    header = relation(OrderHeader, backref = backref("transit_details", order_by = id), primaryjoin = "and_(OrderHeader.id == TransitDetail.header_id, TransitDetail.active == 0)")
#
#    action_time = Column(Text)
#    action_location = Column(Text)
#    remark = Column(Text)





class PickupDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_pickup_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader, backref = backref("pickup_details", order_by = id), primaryjoin = "and_(OrderHeader.id == PickupDetail.header_id, PickupDetail.active == 0)")

    action_time = Column(Text)
    contact = Column(Text)
    tel = Column(Text)
    qty = Column(Float, default = 0)
    remark = Column(Text)





class DeliverHeader(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'deliver_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Text, doc = u'系统编号')
    ref_no = Column(Text, doc = u'送货单号码')
    destination_province_id = Column(Integer, ForeignKey('master_province.id'), doc = u'目的地')
    destination_province = relation(Province)
    destination_city_id = Column(Integer, ForeignKey('master_city.id'), doc = u'目的地')
    destination_city = relation(City)
    destination_address = Column(Text, doc = u'收货地址')
    destination_contact = Column(Text, doc = u'收货人')
    destination_tel = Column(Text, doc = u'收货人电话')
    destination_mobile = Column(Text, doc = u'收货人手机')

    supplier_id = Column(Integer, ForeignKey('master_supplier.id'), doc = u'第三方承运商')
    supplier = relation(Supplier)

    supplier_contact = Column(Text, doc = u'承运商联系人')
    supplier_tel = Column(Text, doc = u'承运商电话')

    order_time = Column(Text, doc = u'下单时间')
    sendout_time = Column(Text, doc = u'发货时间')
    expect_time = Column(Text, doc = u'到达预期')
    actual_time = Column(Text, doc = u'实际到达')

    insurance_charge = Column(Float, default = 0, doc = u'保险费用')
    sendout_charge = Column(Float, default = 0, doc = u'送货费用')
    receive_charge = Column(Float, default = 0, doc = u'上门接货费用')
    package_charge = Column(Float, default = 0, doc = u'包装费用')
    other_charge = Column(Float, default = 0, doc = u'其它费用')
    load_charge = Column(Float, default = 0, doc = u'装货费用')
    unload_charge = Column(Float, default = 0, doc = u'卸货费用')
    proxy_charge = Column(Float, default = 0, doc = u'代理费用')
    carriage_charge = Column(Float, default = 0, doc = u'运费')
    amount = Column(Float, default = 0, doc = u'总费用')

    qty = Column(Float, default = None, doc = u'数量')
    weight = Column(Float, default = None, doc = u'重量')
    vol = Column(Float, default = None, doc = u'体积')

    supplier_paid = Column(Integer, default = 0, doc = u'') # 0 is not paid to supplier, 1 is paid to supplier
    payment_id = Column(Integer, ForeignKey('master_payment.id'), doc = u'付款方式')
    payment = relation(Payment)

    pickup_type_id = Column(Integer, ForeignKey('master_pickup_type.id'), doc = u'提货方式')
    pickup_type = relation(PickupType)

    remark = Column(Text, doc = u'备注')
    _status = Column('status', Integer, default = 0)



    def get_related_orders(self):
        orders = []
        for d in self.details:
            if d.order_detail.header not in orders : orders.append(d.order_detail.header)
        return orders

    def populate(self):
        return {
                'id' : self.id,
                'no' : self.no,
#                'destination_address' : self.destination_address,
                'destination_province' : self.destination_province,
                'destination_city' : self.destination_city,
                'supplier_id' : self.supplier_id,
                'supplier' : self.supplier,
                'supplier_contact' : self.supplier_contact,
                'supplier_tel' : self.supplier_tel,
                'expect_time' : self.expect_time,
                'insurance_charge' : self.insurance_charge ,
                'sendout_charge' : self.sendout_charge ,
                'receive_charge' : self.receive_charge ,
                'package_charge' : self.package_charge ,
                'other_charge' : self.other_charge ,
                'proxy_charge' : self.proxy_charge,
                'amount' : self.amount,
                'supplier_paid' : self.supplier_paid,
                'payment_id' : self.payment_id,
                'payment' : self.payment,
                'remark' : self.remark,
                'status' : self.status,
                'create_time' : self.create_time,
                'create_by' : self.create_by,
                'update_time' : self.update_time,
                'update_by' : self.update_by,
                }


    def _get_status(self): return self._status

    def _set_status(self, status):
        self._status = status
        for d in self.details :
            if d.status < self.status : d.status = status

    status = synonym('_status', descriptor = property(_get_status, _set_status))


    def get_logs(self):
        return DBSession.query(TransferLog).filter(and_(
                                                TransferLog.active == 0,
                                                TransferLog.type == 1,
                                                TransferLog.refer_id == self.id
                                                )).order_by(TransferLog.id)


    def insert_system_logs(self, comare_result):
        try:
            _remark = [u"[%s]'%s' 修改为 '%s'" % (name, ov, nv) for (name, ov, nv) in comare_result['update']]
            DBSession.add(SystemLog(
                                    type = self.__class__.__name__,
                                    ref_id = self.id,
                                    remark = u"%s 修改该记录。%s" % (session['user_profile']['name'], ";".join(_remark))
                                    ))
            DBSession.commit()
        except:
            DBSession.rollback()
            _error(traceback.print_exc())

#    @property
#    def destination_full_address(self):
#        return "".join(filter(lambda v:v, [self.destination_province, self.destination_city, self.destination_address]))


class DeliverDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'deliver_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)

    header_id = Column(Integer, ForeignKey('deliver_header.id'))
    header = relation(DeliverHeader, backref = backref("details", order_by = id), primaryjoin = "and_(DeliverHeader.id == DeliverDetail.header_id, DeliverDetail.active == 0)")
    line_no = Column(Integer, default = 1)

    order_header_id = Column(Integer, ForeignKey('order_header.id'))
    order_header = relation(OrderHeader)

    qty = Column(Float, default = None, doc = u'数量')
    weight = Column(Float, default = None, doc = u'重量')
    vol = Column(Float, default = None, doc = u'体积')

    insurance_charge = Column(Float, default = 0, doc = u'保险费用')
    sendout_charge = Column(Float, default = 0, doc = u'送货费用')
    receive_charge = Column(Float, default = 0, doc = u'上门接货费用')
    package_charge = Column(Float, default = 0, doc = u'包装费用')
    other_charge = Column(Float, default = 0, doc = u'其它费用')
    load_charge = Column(Float, default = 0, doc = u'装货费用')
    unload_charge = Column(Float, default = 0, doc = u'卸货费用')
    proxy_charge = Column(Float, default = 0, doc = u'代理费用')
    carriage_charge = Column(Float, default = 0, doc = u'运费')
    amount = Column(Float, default = 0, doc = u'单笔总费用')

    remark = Column(Text, doc = u'备注')

    supplier_paid = Column(Integer, default = 0) # 0 is not paid to supplier, 1 is paid to supplier
    _status = Column('status', Integer, default = 0)


    def _get_status(self): return self._status

    def _set_status(self, status):
        self._status = status
        self.order_header.status = status


    status = synonym('_status', descriptor = property(_get_status, _set_status))


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

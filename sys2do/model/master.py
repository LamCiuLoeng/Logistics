# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-25
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin

#__all__ = ['']



class Payment(DeclarativeBase, SysMixin):
    __tablename__ = 'master_payment'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))



class ItemUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    type = Column(Unicode(100))
    remark = Column(Unicode(10000))



class Item(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    item_no = Column(Unicode(100))
    name = Column(Unicode(1000))
#    unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
#    unit = relation(ItemUnit)
    remark = Column(Unicode(10000))



class Warehouse(DeclarativeBase, SysMixin):
    __tablename__ = 'master_warehouse'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    address = Column(Unicode(10000))
    remark = Column(Unicode(10000))




class WarehouseItem(DeclarativeBase, SysMixin):
    __tablename__ = 'warehouse_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    warehouse_id = Column(Integer, ForeignKey('master_warehouse.id'))
    warehouse = relation(Warehouse)

    item_id = Column(Integer, ForeignKey('master_item.id'))
    item = relation(Item)

    max_qty = Column(Float, default = 0)
    min_qty = Column(Float, default = 0)
    current_qty = Column(Float, default = 0)
    future_qty = Column(Float, default = 0)
    remark = Column(Unicode(10000))



class Vendor(DeclarativeBase, SysMixin):
    __tablename__ = 'master_vendor'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Unicode(1000))
    contact_person = Column(Unicode(100))
    contact_phone = Column(Unicode(100))
    contact_address = Column(Unicode(5000))
    remark = Column(Unicode(10000))



class LogisticsUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_logistics_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Unicode(1000))
    vendor_id = Column(Integer, ForeignKey('master_vendor.id'))
    vendor = relation(Vendor)

    contact_person = Column(Unicode(100))
    contact_phone = Column(Unicode(100))
    contact_address = Column(Unicode(5000))

    qty = Column(Float, default = 0)
    capability = Column(Float, default = 0)
    remark = Column(Unicode(10000))



class ShipmentLogCategory(DeclarativeBase, SysMixin):
    __tablename__ = 'master_shipment_log_category'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))

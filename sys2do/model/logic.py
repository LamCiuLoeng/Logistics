# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin


class ItemUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))



class Item(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    item_no = Column(Unicode(100))
    name = Column(Unicode(1000))
    unit_id = Column(Integer, ForeignKey('master_item_unit.id'))
    unit = relation(ItemUnit)
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

    max_qty = Column(Integer, default = 0)
    min_qty = Column(Integer, default = 0)
    current_qty = Column(Integer, default = 0)
    future_qty = Column(Integer, default = 0)
    remark = Column(Unicode(10000))




class LogisticsUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_logistics_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Unicode(1000))
    qty = Column(Integer, default = 0)
    capability = Column(Integer, default = 0)
    remark = Column(Unicode(10000))





class OrderHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'order_header'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Unicode(100))
    cost = Column(Float, default = 0)
    status = Column(Integer, default = 0)
    remark = Column(Unicode(10000))



class OrderDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement = True, primary_key = True)
    header_id = Column(Integer, ForeignKey('order_header.id'))
    header = relation(OrderHeader)
    status = Column(Integer, default = 0)
    remark = Column(Unicode(10000))



class Transportation(DeclarativeBase, SysMixin):
    __tablename__ = 'transportation'

    id = Column(Integer, autoincrement = True, primary_key = True)

    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    order_detail = relation(OrderDetail)

    logistics_unit_id = Column(Integer, ForeignKey('master_logistics_unit.id'))
    logistics_unit = relation(LogisticsUnit)

    status = Column(Integer, default = 0)
    remark = Column(Unicode(10000))



class TransportationLog(DeclarativeBase, SysMixin):
    __tablename__ = 'transportation_log'

    id = Column(Integer, autoincrement = True, primary_key = True)
    transportation_id = Column(Integer, ForeignKey('transportation.id'))
    transportation = relation(Transportation)
    remark = Column(Unicode(10000))

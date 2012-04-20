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
from sqlalchemy.sql.expression import and_



#__all__ = ['']


class ShipmentType(DeclarativeBase, SysMixin):
    __tablename__ = 'master_shipment_type'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name


class Province(DeclarativeBase, SysMixin):
    __tablename__ = 'master_province'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))
    is_direct = Column(Integer, default = 0)
    remark = Column(Unicode(10000))

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name




class City(DeclarativeBase, SysMixin):
    __tablename__ = 'master_city'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))
    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province, backref = backref("cities", order_by = id), primaryjoin = "and_(Province.id == City.province_id, City.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name




class District(DeclarativeBase, SysMixin):
    __tablename__ = 'master_district'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100))
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City, backref = backref("districts", order_by = id), primaryjoin = "and_(City.id == District.city_id, District.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class CustomerProfile(DeclarativeBase, SysMixin):
    __tablename__ = 'master_customer_profile'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class Customer(DeclarativeBase, SysMixin):
    __tablename__ = 'master_customer'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Unicode(1000))
    address = Column(Unicode(5000))
    phone = Column(Unicode(100))
    contact_person = Column(Unicode(100))
    remark = Column(Unicode(10000))

    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
    prifile = relation(CustomerProfile, backref = backref("customers", order_by = id), primaryjoin = "and_(CustomerProfile.id == Customer.profile_id, Customer.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class Supplier(DeclarativeBase, SysMixin):
    __tablename__ = 'master_supplier'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Unicode(1000))
    address = Column(Unicode(5000))
    phone = Column(Unicode(100))
    contact_person = Column(Unicode(100))
    remark = Column(Unicode(10000))

    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
    prifile = relation(CustomerProfile, backref = backref("suppliers", order_by = id), primaryjoin = "and_(CustomerProfile.id == Supplier.profile_id, Supplier.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class Item(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))

    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
    prifile = relation(CustomerProfile, backref = backref("items", order_by = id), primaryjoin = "and_(CustomerProfile.id == Item.profile_id, Item.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class ItemUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000)) #cn
    english_name = Column(Unicode(1000)) #en
    tradition_name = Column(Unicode(1000)) #zh
    remark = Column(Unicode(10000))

#    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
#    prifile = relation(CustomerProfile, backref = backref("itemunits", order_by = id), primaryjoin = "and_(CustomerProfile.id == ItemUnit.profile_id, ItemUnit.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name


class WeightUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_weight_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000)) #cn
    english_name = Column(Unicode(1000)) #en
    tradition_name = Column(Unicode(1000)) #zh
    remark = Column(Unicode(10000))

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class Warehouse(DeclarativeBase, SysMixin):
    __tablename__ = 'master_warehouse'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    manager = Column(Unicode(1000))
    address = Column(Unicode(10000))
    remark = Column(Unicode(10000))

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name


    @property
    def items(self):
        return DBSession.query(WarehouseItem).filter(and_(WarehouseItem.active == 0, WarehouseItem.warehouse_id == self.id))


class WarehouseItem(DeclarativeBase, SysMixin):
    __tablename__ = 'master_warehouse_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    item_id = Column(Integer, ForeignKey('master_item.id'))
    item = relation(Item)
    warehouse_id = Column(Integer, ForeignKey('master_warehouse.id'))
    warehouse = relation(Warehouse)
    qty = Column(Integer, default = 0)
    order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    remark = Column(Unicode(10000))


    @property
    def order_detail(self):
        from sys2do.model.logic import OrderDetail
        return DBSession.query(OrderDetail).get(self.order_detail_id)


class Payment(DeclarativeBase, SysMixin):
    __tablename__ = 'master_payment'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(1000))
    remark = Column(Unicode(10000))




#===============================================================================
# 
#===============================================================================

'''

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


'''

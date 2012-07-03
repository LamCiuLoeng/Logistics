# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-25
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float, Text
from sqlalchemy.orm import relation, backref
from sys2do.model import DeclarativeBase, metadata, DBSession
from auth import SysMixin
from sqlalchemy.sql.expression import and_
from sys2do.model.auth import CRUDMixin, Group



#__all__ = ['']


class ShipmentType(DeclarativeBase, SysMixin):
    __tablename__ = 'master_shipment_type'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name



class Ratio(DeclarativeBase, SysMixin):
    __tablename__ = 'master_ratio'

    id = Column(Integer, autoincrement = True, primary_key = True)

    type = Column(Text)
    value = Column(Float, default = 0)

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name


#class Province(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_province'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text)
#    is_direct = Column(Integer, default = 0)
#    remark = Column(Text)
#
#    def __str__(self): return self.name
#    def __repr__(self): return self.name
#    def __unicode__(self): return self.name
#
#
#
#
#
#
#class City(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_city'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text)
#    province_id = Column(Integer, ForeignKey('master_province.id'))
#    province = relation(Province, backref = backref("cities", order_by = id), primaryjoin = "and_(Province.id == City.province_id, City.active == 0)")
#
#    def __str__(self): return self.name
#    def __repr__(self): return self.name
#    def __unicode__(self): return self.name
#
#
#
#
#
#
#class District(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_district'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text)
#    city_id = Column(Integer, ForeignKey('master_city.id'))
#    city = relation(City, backref = backref("districts", order_by = id), primaryjoin = "and_(City.id == District.city_id, District.active == 0)")
#
#    def __str__(self): return self.name
#
#    def __repr__(self): return self.name
#
#    def __unicode__(self): return self.name





class Customer(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_customer'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Text)
#    province_id = Column(Integer, ForeignKey('master_province.id'))
#    provice = relation(Province)
#    city_id = Column(Integer, ForeignKey('master_city.id'))
#    city = relation(City)
#    district_id = Column(Integer, ForeignKey('master_district.id'))
#    district = relation(District)
    address = Column(Text)
    phone = Column(Text)
    contact_person = Column(Text)
    remark = Column(Text)


    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    def populate(self):
        params = {}
        for k in ['id', 'name',
#                  'province_id', 'city_id', 'district_id',
                  'address', 'phone', 'contact_person', 'remark']:
            params[k] = getattr(self, k)
        return params

    @classmethod
    def saveAsNew(clz, v):
        return None

    def saveAsUpdate(self, v):
        return None





class CustomerProfile(DeclarativeBase, SysMixin):
    __tablename__ = 'master_customer_profile'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    remark = Column(Text)

    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("customer_profile", order_by = id))
    group_id = Column(Integer, ForeignKey('system_group.id'))
    group = relation(Group, backref = backref("customer_profile", order_by = id))

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name




class Supplier(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_supplier'

    id = Column(Integer, autoincrement = True, primary_key = True)

    name = Column(Text)
#    province_id = Column(Integer, ForeignKey('master_province.id'))
#    provice = relation(Province)
#    city_id = Column(Integer, ForeignKey('master_city.id'))
#    city = relation(City)
#    district_id = Column(Integer, ForeignKey('master_district.id'))
#    district = relation(District)
    address = Column(Text)
    phone = Column(Text)
    contact_person = Column(Text)
    remark = Column(Text)

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    def populate(self):
        params = {}
        for k in ['id', 'name',
#                  'province_id', 'city_id', 'district_id',
                  'address', 'phone', 'contact_person', 'remark']:
            params[k] = getattr(self, k)
        return params


class SupplierProfile(DeclarativeBase, SysMixin):
    __tablename__ = 'master_supplier_profile'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    remark = Column(Text)

    supplier_id = Column(Integer, ForeignKey('master_supplier.id'))
    supplier = relation(Supplier, backref = backref("supplier_profile", order_by = id))
    group_id = Column(Integer, ForeignKey('system_group.id'))
    group = relation(Group, backref = backref("supplier_profile", order_by = id))

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name



#class Item(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_item'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text)
#    remark = Column(Text)
#
#    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
#    prifile = relation(CustomerProfile, backref = backref("items", order_by = id), primaryjoin = "and_(CustomerProfile.id == Item.profile_id, Item.active == 0)")
#
#    def __str__(self): return self.name
#
#    def __repr__(self): return self.name
#
#    def __unicode__(self): return self.name



class ItemUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_item_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text) #cn
    english_name = Column(Text) #en
    tradition_name = Column(Text) #zh
    remark = Column(Text)

#    profile_id = Column(Integer, ForeignKey('master_customer_profile.id'))
#    prifile = relation(CustomerProfile, backref = backref("itemunits", order_by = id), primaryjoin = "and_(CustomerProfile.id == ItemUnit.profile_id, ItemUnit.active == 0)")

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name


class WeightUnit(DeclarativeBase, SysMixin):
    __tablename__ = 'master_weight_unit'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text) #cn
    english_name = Column(Text) #en
    tradition_name = Column(Text) #zh
    remark = Column(Text)

    def __str__(self): return self.name

    def __repr__(self): return self.name

    def __unicode__(self): return self.name



class InventoryLocation(DeclarativeBase, SysMixin):
    __tablename__ = 'master_inventory_location'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    manager = Column(Text)
    address = Column(Text)
    remark = Column(Text)
    full_path = Column(Text)
    full_path_ids = Column(Text)
    parent_id = Column(Integer, default = None)

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

#
#
#    @property
#    def items(self):
#        return DBSession.query(WarehouseItem).filter(and_(WarehouseItem.active == 0, WarehouseItem.warehouse_id == self.id))

class InventoryItem(DeclarativeBase, SysMixin):
    __tablename__ = 'master_Inventory_item'

    id = Column(Integer, autoincrement = True, primary_key = True)

    item = Column(Text)
    location_id = Column(Integer, ForeignKey('master_inventory_location.id'))
    location = relation(InventoryLocation)
    qty = Column(Integer, default = 0)
    refer_order_header = Column(Text)
#    refer_order_detail_id = Column(Integer, ForeignKey('order_detail.id'))
    remark = Column(Text)


#    @property
#    def order_detail(self):
#        from sys2do.model.logic import OrderDetail
#        return DBSession.query(OrderDetail).get(self.refer_order_detail_id)


class Payment(DeclarativeBase, SysMixin):
    __tablename__ = 'master_payment'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    remark = Column(Text)


    def __str__(self): return self.name
    def __unicode__(self): return self.name
    def __repr__(self): return self.name



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

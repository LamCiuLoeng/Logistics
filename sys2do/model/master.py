# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-25
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Unicode, Integer, DateTime, Float, Text
from sqlalchemy.orm import relation, backref, synonym
from sys2do.model import DeclarativeBase, metadata, DBSession
from sqlalchemy.sql.expression import and_

from auth import SysMixin
from sys2do.model.auth import CRUDMixin, Group, User
from sys2do.util.common import _gl, _gp, _info
from sys2do.constant import SYSTEM_DATETIME_FORMAT
from sys2do.model.system import UploadFile
from sys2do.util.barcode_helper import generate_barcode_file


#__all__ = ['']

class Payment(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_payment'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, doc = u'名称')
    remark = Column(Text, doc = u'备注')


    def __str__(self): return self.name
    def __unicode__(self): return self.name
    def __repr__(self): return self.name


    @classmethod
    def _get_fields(clz):
        return ['name', 'remark']


class ShipmentType(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_shipment_type'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, doc = u'名称')
    remark = Column(Text, doc = u'备注')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    @classmethod
    def _get_fields(clz):
        return ['name', 'remark']


class PickupType(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_pickup_type'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, doc = u'名称')
    remark = Column(Text, doc = u'备注')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    @classmethod
    def _get_fields(clz):
        return ['name', 'remark']


class PackType(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_pack_type'

    __fields = ['name', 'remark']

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, doc = u'名称')
    remark = Column(Text, doc = u'备注')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    @classmethod
    def _get_fields(clz):
        return ['name', 'remark']



class Ratio(DeclarativeBase, SysMixin):
    __tablename__ = 'master_ratio'

    id = Column(Integer, autoincrement = True, primary_key = True)

    type = Column(Text)
    value = Column(Float, default = 0)

    def __str__(self): return self.type
    def __repr__(self): return self.type
    def __unicode__(self): return self.type




class Receiver(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_receiver'

    id = Column(Integer, autoincrement = True, primary_key = True)

    code = Column(Text, doc = u'车牌号')
    name = Column(Text, doc = u'收件人')
    tel = Column(Text, doc = u'电话')
    mobile = Column(Text, doc = u'手机')
    remark = Column(Text, doc = u'备注')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    @classmethod
    def _get_fields(clz):
        return ['code', 'name', 'tel', 'mobile', 'remark']

    def populate(self):
        return {
                'id' : self.id,
                'code' : self.code,
                'name' : self.name,
                'tel' : self.tel,
                'mobile' : self.mobile,
                }

class Diqu(DeclarativeBase, SysMixin):
    __tablename__ = 'master_diqu'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    code = Column(Text)
    parent_id = Column(Integer, default = None)
    full_path = Column(Text)

    @property
    def parent(self):
        try:
            return DBSession.query(Diqu).filter(Diqu.id == self.parent_id).one()
        except:
            return None

    @property
    def children(self):
        return DBSession.query(Diqu).filter(Diqu.parent_id == self.id).all()





class Province(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_province'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    code = Column(Text)
    shixiao = Column(Integer, default = 0)
    qty_ratio = Column(Float, default = 0, doc = u'数量费率')
    weight_ratio = Column(Float, default = 0, doc = u'重量费率')
    vol_ratio = Column(Float, default = 0, doc = u'体积费率')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name


    def children(self):
        return DBSession.query(City).filter(and_(City.parent_code == self.code, City.active == 0)).order_by(City.name).all()

    @classmethod
    def _get_fields(clz):
        return ['name', 'code']


class City(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_city'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text)
    code = Column(Text)
    parent_code = Column(Text)
    shixiao = Column(Integer, default = 0)
    qty_ratio = Column(Float, default = 0, doc = u'数量费率')
    weight_ratio = Column(Float, default = 0, doc = u'重量费率')
    vol_ratio = Column(Float, default = 0, doc = u'体积费率')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    def parent(self):  return DBSession.query(Province).filter(Province.code == self.parent_code).one()
#    def children(self): return DBSession.query(District).filter(and_(District.parent_code == self.code)).all()

    @classmethod
    def _get_fields(clz):
        return ['name', 'code', 'parent_code']

#class District(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_district'
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    name = Column(Text)
#    code = Column(Text)
#    parent_code = Column(Text)
#
#
#    def __str__(self): return self.name
#    def __repr__(self): return self.name
#    def __unicode__(self): return self.name
#    def parent(self):  return DBSession.query(City).filter(City.code == self.parent_code).one()


class Note(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_note'

    id = Column(Integer, autoincrement = True, primary_key = True)
    code = Column(Text, doc = u'票据编号')
    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province)
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City)
    name = Column(Text, doc = u'票据前缀')
    apply_person_id = Column(Integer, ForeignKey('system_user.id'), doc = u'领用人')
    apply_person = relation(User, primaryjoin = "and_(User.id == Note.apply_person_id, Note.active == 0)")
    apply_time = Column(Text, doc = u'申请时间')
    operator_id = Column(Integer, ForeignKey('system_user.id'), doc = u'操作者')
    operator = relation(User, primaryjoin = "and_(User.id == Note.operator_id, Note.active == 0)")
    begin_no = Column(Text, doc = u'开始编号')
    end_no = Column(Text, doc = u'结束编号')
    current_no = Column(Text)
    status = Column(Integer, default = 0) # 0 is still using, 1 is full used 
    remark = Column(Text, doc = u'备注')

#    _range = Column('range', Text)

    def __str__(self): return '%s(%s)' % (self.name, self.code)
    def __repr__(self): return '%s(%s)' % (self.name, self.code)
    def __unicode__(self): return '%s(%s)' % (self.name, self.code)

    @classmethod
    def _get_fields(clz):
        return ['name', 'code', 'province_id', 'city_id', 'begin_no', 'end_no', 'current_no',
                'apply_time', 'apply_person_id', 'operator_id', 'remark']

#    def _get_range(self):
#        if not self._range : return []
#        return map(lambda v: v.split("~"), self._range.split("|"))
#
#    def _set_range(self, ranges):
#        if not ranges: self._range = None
#        self._range = ("|").join([("~").join(r) for r in ranges])
#
#    range = synonym('_range', descriptor = property(_get_range, _set_range))


    def populate(self):
        result = {
                  'id' : self.id,
                  }
        for f in ['name', 'code', 'province_id', 'city_id', 'begin_no', 'end_no', 'current_no',
                  'apply_time', 'apply_person_id', 'operator_id', 'status', 'remark']:
            result[f] = unicode(getattr(self, f) or '')
        return result


    @classmethod
    def saveAsNew(clz, v):
        params = {}
        for f in ['name', 'code', 'province_id', 'city_id', 'begin_no', 'end_no',
                  'apply_time', 'apply_person_id', 'operator_id', 'remark']:
            params[f] = v.get(f, None) or None

        obj = clz(**params)
        DBSession.add(obj)
        return obj


    def saveAsUpdate(self, v):
        for f in ['name', 'code', 'province_id', 'city_id', 'begin_no', 'end_no', 'current_no',
                  'apply_time', 'apply_person_id', 'operator_id', 'remark', 'status']:
            setattr(self, f, v.get(f, None) or None)
        return self







class Customer(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_customer'

    id = Column(Integer, autoincrement = True, primary_key = True)
    no = Column(Text)
    name = Column(Text, doc = u'客户名称')
    display_name = Column(Text)
    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province)
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City)

    address = Column(Text, doc = u'地址')
    contact_person = Column(Text, doc = u'联系人')
    mobile = Column(Text, doc = u'手机')
    phone = Column(Text, doc = u'电话')
    email = Column(Text, doc = u'电子邮箱')

    note_id = Column(Integer, ForeignKey('master_note.id'), doc = u'票据前缀')
    note = relation(Note)

    remark = Column(Text, doc = u'备注')


    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    def populate(self):
        params = {}
        for k in ['id', 'name', 'no', 'province_id', 'city_id', 'address', 'phone',
                  'mobile', 'contact_person', 'email' , 'note_id', 'remark']:
            params[k] = getattr(self, k)

        params['create_time'] = self.create_time.strftime(SYSTEM_DATETIME_FORMAT)
        params['create_by'] = unicode(self.create_by) if self.create_by else ''
        return params


    @classmethod
    def _get_fields(clz):
        return ['name', 'no', 'province_id', 'city_id', 'address', 'phone', 'mobile', 'email', 'contact_person', 'remark', 'payment_id']





class CustomerSource(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_customer_source'


    id = Column(Integer, autoincrement = True, primary_key = True)
    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("sources", order_by = id), primaryjoin = "and_(Customer.id == CustomerSource.customer_id, CustomerSource.active == 0)")
    name = Column(Text)

    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province)
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City)
    remark = Column(Text)
    payment_id = Column(Integer, ForeignKey('master_payment.id'))
    payment = relation(Payment)


    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    def populate(self):
        params = {}
        for k in ['id', 'name', 'customer_id', 'province_id', 'city_id', 'payment_id']:
            params[k] = getattr(self, k)
        return params


    def contacts(self):
        return DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0 ,
                                                     CustomerContact.customer_id == self.customer_id,
                                                     CustomerContact.refer_id == self.id,
                                                     CustomerContact.type == 'S',
                                                     )).order_by(CustomerContact.name)

    def default_contact(self):
        try:
            return DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0 ,
                                                     CustomerContact.customer_id == self.customer_id,
                                                     CustomerContact.refer_id == self.id,
                                                     CustomerContact.type == 'S',
                                                     CustomerContact.is_default == 1
                                                     )).one()
        except:
            return None




class CustomerDiquRatio(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_customer_ditu_ratio'

    id = Column(Integer, autoincrement = True, primary_key = True)
    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer)
    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province)
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City)
    qty_ratio = Column(Float, default = 0, doc = u'数量费率')
    weight_ratio = Column(Float, default = 0, doc = u'重量费率')
    vol_ratio = Column(Float, default = 0, doc = u'体积费率')
    remark = Column(Text)


class CustomerTarget(DeclarativeBase, SysMixin):
    __tablename__ = 'master_customer_target'

    id = Column(Integer, autoincrement = True, primary_key = True)
    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("targets", order_by = id), primaryjoin = "and_(Customer.id == CustomerTarget.customer_id, CustomerTarget.active == 0)")
    name = Column(Text)
    province_id = Column(Integer, ForeignKey('master_province.id'))
    province = relation(Province)
    city_id = Column(Integer, ForeignKey('master_city.id'))
    city = relation(City)
    remark = Column(Text)

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name


    def populate(self):
        params = {}
        for k in ['id', 'name', 'customer_id', 'province_id', 'city_id',
#                  'address', 
                  ]:
            params[k] = getattr(self, k)
        return params


    def contacts(self):
        return DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0 ,
                                                     CustomerContact.customer_id == self.customer_id,
                                                     CustomerContact.refer_id == self.id,
                                                     CustomerContact.type == 'T',
                                                     )).order_by(CustomerContact.name)

    def default_contact(self):
        try:
            return DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0 ,
                                                     CustomerContact.customer_id == self.customer_id,
                                                     CustomerContact.refer_id == self.id,
                                                     CustomerContact.type == 'T',
                                                     CustomerContact.is_default == 1
                                                     )).one()
        except:
            return None



#class CustomerTargetContact(DeclarativeBase, SysMixin):
#    __tablename__ = 'master_customer_target_contact'
#
#    id = Column(Integer, autoincrement = True, primary_key = True)
#    customer_target_id = Column(Integer, ForeignKey('master_customer_target.id'))
#    customer_target = relation(CustomerTarget, backref = backref("contacts", order_by = id), primaryjoin = "and_(CustomerTarget.id == CustomerTargetContact.customer_target_id, CustomerTargetContact.active == 0)")
#    name = Column(Text)
#    address = Column(Text)
#    mobile = Column(Text)
#    phone = Column(Text)
#    email = Column(Text)
#    remark = Column(Text)
#    is_default = Column(Integer, default = 0) # 1 is default , 0 is normal 
#
#    def __str__(self): return self.name
#    def __repr__(self): return self.name
#    def __unicode__(self): return self.name
#
#
#    def populate(self):
#        params = {}
#        for k in ['id', 'name', 'phone', 'email', 'mobile', 'address']:
#            params[k] = getattr(self, k)
#        return params





class CustomerContact(DeclarativeBase, SysMixin):
    __tablename__ = 'master_customer_contact'

    id = Column(Integer, autoincrement = True, primary_key = True)
    customer_id = Column(Integer, ForeignKey('master_customer.id'))
    customer = relation(Customer, backref = backref("contacts", order_by = id), primaryjoin = "and_(Customer.id == CustomerContact.customer_id, CustomerContact.active == 0)")
    type = Column(Text, default = None) # S is source contact , T is target contact
    refer_id = Column(Integer, default = None)
    name = Column(Text)
    address = Column(Text)
    mobile = Column(Text)
    phone = Column(Text)
    email = Column(Text)
    remark = Column(Text)
    is_default = Column(Integer, default = 0) # 1 is default , 0 is normal 

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name


    def populate(self):
        params = {}
        for k in ['id', 'customer_id', 'type', 'refer_id', 'name', 'phone', 'email', 'mobile', 'address', 'is_default']:
            params[k] = getattr(self, k)
        return params






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
    no = Column(Text, doc = u'承运商编号')
    name = Column(Text, doc = u'承运商名称')
    display_name = Column(Text)
#    province_id = Column(Integer, ForeignKey('master_province.id'))
#    provice = relation(Province)
#    city_id = Column(Integer, ForeignKey('master_city.id'))
#    city = relation(City)
#    district_id = Column(Integer, ForeignKey('master_district.id'))
#    district = relation(District)
    address = Column(Text, doc = u'地址编号')
    phone = Column(Text, doc = u'电话')
    mobile = Column(Text, doc = u'手提电话')
    email = Column(Text, doc = u'邮件')
    contact_person = Column(Text, doc = u'联系人')
    remark = Column(Text, doc = u'备注')
    payment_id = Column(Integer, ForeignKey('master_payment.id'), doc = u'付款方式')
    payment = relation(Payment)

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



class Item(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_item'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, doc = u'货物名称')
    remark = Column(Text , doc = u'备注')

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

    @classmethod
    def _get_fields(clz):
        return ['name', 'remark']


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
    parent_id = Column(Integer, ForeignKey('master_inventory_location.id'))
    parent = relation('InventoryLocation', backref = backref("children", remote_side = id))

    def __str__(self): return self.name
    def __repr__(self): return self.name
    def __unicode__(self): return self.name

#
#
#    @property
#    def items(self):
#        return DBSession.query(WarehouseItem).filter(and_(WarehouseItem.active == 0, WarehouseItem.warehouse_id == self.id))

class InventoryItem(DeclarativeBase, SysMixin):
    __tablename__ = 'master_inventory_item'

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






class Barcode(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'master_barcode'

    id = Column(Integer, autoincrement = True, primary_key = True)
    value = Column(Text)
    ref_no = Column(Text)
    status = Column(Integer, default = 0)  #0 is used ,1 is reserved ,2 is cancelled 
    img_id = Column(Integer, ForeignKey('system_upload_file.id'))
    img = relation(UploadFile)

    def __str__(self): return self.value
    def __repr__(self): return self.value
    def __unicode__(self): return self.value


    @classmethod
    def getOrCreate(clz, value, ref_no, status = 0):
        if value: # get the existing
            try:
                b = DBSession.query(clz).filter(clz.value == value).one()
                return b
            except:
                pass
        #create
        b = clz(value = value, ref_no = ref_no, status = status)
        DBSession.add(b)
        DBSession.flush()
        b.value = '%s%06d' % (dt.now().strftime('%y%m%d'), (b.id % 1000000))
        b.img = generate_barcode_file(b.value)
        return b


    @classmethod
    def check(clz, value):
        try:
            b = DBSession.query(clz).filter(clz.value == value).one()
            return (0, b.status) #barcode exist
        except:
            return (1, None) # barcode not exist

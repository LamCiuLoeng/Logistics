# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import traceback
from sys2do.model import metadata, engine, DBSession, Permission, Group, User
#import sys2do.model.logic as logic
import sys
from sys2do.model.master import CustomerProfile, Customer, \
    ItemUnit, InventoryLocation, WeightUnit, ShipmentType, Payment, Province, Supplier, \
    ChargeType
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    try:
        print "create tables"
        metadata.drop_all(engine)
        metadata.create_all(engine)

        print "insert default value"
        #add the default value here

        uAdmin = User(name = 'admin', email = 'admin@test.com', password = 'admin', first_name = 'Admin', last_name = 'Test')
        uCustomer = User(name = 'customer', email = 'customer@test.com', password = '123', first_name = 'Customer', last_name = 'Test')
        uOfficer = User(name = 'officer', email = 'officer@test.com', password = '123', first_name = 'Officer', last_name = 'Test')
        uSupplier = User(name = 'supplier', email = 'supplier@test.com', password = '123', first_name = 'Supplier', last_name = 'Test')
        uWarehouse = User(name = 'warehouse', email = 'warehouse@test.com', password = '123', first_name = 'Warehouse', last_name = 'Test')

        pCreateUser = Permission(name = 'CREATE_USER')
        pUpdateUser = Permission(name = 'UPDATE_USER')
        pDeleteUser = Permission(name = 'DELETE_USER')
        pSearchUser = Permission(name = 'SEARCH_USER')
        pCreateOrder = Permission(name = 'CREATE_ORDER')
        pUpdateOrder = Permission(name = 'UPDATE_ORDER')
        pDeleteOrder = Permission(name = 'DELETE_ORDER')
        pSearchOrder = Permission(name = 'SEARCH_ORDER')
        pManageOrder = Permission(name = 'MANAGE_ORDER')
        pSearchAllOrder = Permission(name = 'SEARCH_ALL_ORDER')
        pCreateDeliver = Permission(name = 'CREATE_DELIVER')
        pUpdateDeliver = Permission(name = 'UPDATE_DELIVER')
        pDeleteDeliver = Permission(name = 'DELETE_DELIVER')
        pSearchDeliver = Permission(name = 'SEARCH_DELIVER')
        pManageDeliver = Permission(name = 'MANAGE_DELIVER')
        pSearchAllDeliver = Permission(name = 'SEARCH_ALL_ELIVER')
        pCreateCustomer = Permission(name = 'CREATE_CUSTOMER')
        pUpdateCustomer = Permission(name = 'UPDATE_CUSTOMER')
        pDeleteCustomer = Permission(name = 'DELETE_CUSTOMER')
        pSearchCustomer = Permission(name = 'SEARCH_CUSTOMER')
        pCreateSupplier = Permission(name = 'CREATE_SUPPLIER')
        pUpdateSupplier = Permission(name = 'UPDATE_SUPPLIER')
        pDeleteSupplier = Permission(name = 'DELETE_SUPPLIER')
        pSearchSupplier = Permission(name = 'SEARCH_SUPPLIER')
        pCreateWarehouse = Permission(name = 'CREATE_WAREHOUSE')
        pUpdateWarehouse = Permission(name = 'UPDATE_WAREHOUSE')
        pDeleteWarehouse = Permission(name = 'DELETE_WAREHOUSE')
        pSearchWarehouse = Permission(name = 'SEARCH_WAREHOUSE')
        pCreateDriver = Permission(name = 'CREATE_DRIVER')
        pUpdateDriver = Permission(name = 'UPDATE_DRIVER')
        pDeleteDriver = Permission(name = 'DELETE_DRIVER')
        pSearchDriver = Permission(name = 'SEARCH_DRIVER')

        gAdmin = Group(name = 'ADMIN', display_name = 'Administrator', type = 0)
        gAdmin.permissions = [pCreateUser, pUpdateUser, pDeleteUser, pSearchUser,
                              pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                              pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                              pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                              pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                              pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                              pCreateDriver, pUpdateDriver, pDeleteDriver, pSearchDriver]
        gAdmin.users = [uAdmin, ]
        gCustomer = Group(name = 'CUSTOMER', display_name = 'Customer', type = 0)
        gCustomer.permissions = [pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, ]
        gCustomer.users = [uCustomer, ]
        gOfficer = Group(name = 'OFFICER', display_name = 'Officer', type = 0)
        gOfficer.permissions = [pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder,
                                pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                                ]
        gOfficer.users = [uOfficer]
        gSupplier = Group(name = 'SUPPLIER', display_name = 'Supplier', type = 0)
        gSupplier.permissions = [pUpdateDeliver, pSearchDeliver ]
        gSupplier.users = [uSupplier]
        gWarehouse = Group(name = 'WAREHOUSE', display_name = 'Warehouse', type = 0)
        gWarehouse.permissions = [pUpdateOrder, pSearchOrder, pSearchAllOrder,
                                  pUpdateDeliver, pSearchDeliver, pSearchAllDeliver, ]
        gWarehouse.users = [uWarehouse]


        DBSession.add_all([
                            uAdmin, uCustomer, uOfficer, uSupplier, uWarehouse,
                            pCreateUser, pUpdateUser, pDeleteUser, pSearchUser,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                            pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                            pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                            pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                            pCreateDriver, pUpdateDriver, pDeleteDriver, pSearchDriver,
                            gAdmin, gCustomer, gOfficer, gSupplier, gWarehouse,
                            ])

        for n, en, tn in [(u'米', u'meter', u'米'), (u'分米', u'dm', u'分米'), (u'厘米', u'cm', u'釐米'), (u'吨', u'ton', u'噸'), (u'千克', u'kg', u'千克'), (u'克', u'g', u'克'),
                     (u'箱', u'box', u'箱'), (u'瓶', u'bottle', u'瓶'), (u'只', u'pic', u'只'), (u'打', u'dozen', u'打'), ]:
            DBSession.add(ItemUnit(name = n, english_name = en, tradition_name = tn))


        for n, en, tn in [(u'吨', u'ton', u'噸'), (u'千克', u'kg', u'千克'), (u'克', u'g', u'克'), ]:
            DBSession.add(WeightUnit(name = n, english_name = en, tradition_name = tn))

        location1 = InventoryLocation(name = u"深圳仓库", address = u"仓库地址 1", manager = "MANAGER 1", full_path = u"深圳仓库")
        location2 = InventoryLocation(name = u"东莞仓库", address = u"仓库地址 2", manager = "MANAGER 2", full_path = u"东莞仓库")
        DBSession.add(location1)
        DBSession.add(location2)

        DBSession.flush()
        location1.full_path_ids = location1.id
        location2.full_path_ids = location2.id

        DBSession.add(ShipmentType(name = u"陆运"))
        DBSession.add(ShipmentType(name = u"水运"))
        DBSession.add(ShipmentType(name = u"空运"))
        DBSession.add(Payment(name = u"月结"))
        DBSession.add(ChargeType(name = u"按件",))
        DBSession.add(ChargeType(name = u"按体积",))
        DBSession.add(ChargeType(name = u"按重量",))


        DBSession.add(Customer(name = u"客户一", address = u"广东省深圳市福田区", phone = "0755-25311000", contact_person = u"李先生"))
        DBSession.add(Customer(name = u"客户二", address = u"广东省深圳市罗湖区", phone = "0755-25141000", contact_person = u"陈小姐"))
        DBSession.add(Customer(name = u"客户三", address = u"广东省深圳市南山区", phone = "0755-25340000", contact_person = u"张先生"))
        DBSession.add(Customer(name = u"客户四", address = u"广东省深圳市龙岗区", phone = "0755-25361422", contact_person = u"王先生"))

        DBSession.add(Supplier(name = u"承运商一", address = u"广东省珠海市斗门区", phone = "0756-25361422", contact_person = u"林先生"))
        DBSession.add(Supplier(name = u"承运商二", address = u"广东省珠海市金湾区", phone = "0756-25361422", contact_person = u"邓先生"))
        DBSession.add(Supplier(name = u"承运商三", address = u"广东省珠海市拱北区", phone = "0756-25361422", contact_person = u"黄先生"))

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()

if __name__ == '__main__':
    init()

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
    ItemUnit, InventoryLocation, WeightUnit, ShipmentType, Payment, Supplier, \
    ChargeType, SupplierProfile
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    try:
        print "create tables"
        metadata.drop_all(engine,checkfirst=True)
        
        metadata.create_all(engine)

        print "insert default value"
        #add the default value here

        uAdmin = User(name = 'admin', email = 'admin@sfhlwl.com', password = 'admin', first_name = 'Admin', last_name = '')
        uKinlong = User(name = u'kinlong', email = 'customer@test.com', password = '123', first_name = u'坚朗', last_name = '')
        uWeiqian = User(name = u'weiqian', email = 'customer@test.com', password = '123', first_name = u'味千', last_name = '')
        uKefu1 = User(name = u'kefu1', email = 'kefu1@sfhlwl.com', password = '123', first_name = u'客服1', last_name = '')
        uKefu2 = User(name = u'kefu2', email = 'kefu2@sfhlwl.com', password = '123', first_name = u'客服2', last_name = '')
        uSupplier = User(name = 'supplier', email = 'supplier@test.com', password = '123', first_name = 'Supplier', last_name = 'Test')
        uWarehouse = User(name = 'warehouse', email = 'warehouse@sfhlwl.com', password = '123', first_name = 'Warehouse', last_name = 'Test')
        
        

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
        gCustomer.users = [uKinlong,uWeiqian ]
        gKinlongGroup = Group(name = 'KINLONG_GROUP', display_name = 'KINLONG GROUP', type = 1)
        gKinlongGroup.users = [uKinlong,]
        gWeiqianGroup = Group(name = 'WEIQIAN_GROUP', display_name = 'WEIQIAN GROUP', type = 1)
        gWeiqianGroup.users = [uWeiqian]
        gOfficer = Group(name = 'OFFICER', display_name = 'Officer', type = 0)
        gOfficer.permissions = [pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder,
                                pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                                ]
        gOfficer.users = [uKefu1,uKefu2]
        gSupplier = Group(name = 'SUPPLIER', display_name = 'Supplier', type = 0)
        gSupplier.permissions = [pUpdateDeliver, pSearchDeliver ]
        gSupplier.users = [uSupplier]
        
        gSupplier1 = Group(name = 'SUPPLIER_1', display_name = 'Supplier1', type = 1)
        gSupplier1.users = [uSupplier]
        gWarehouse = Group(name = 'WAREHOUSE', display_name = 'Warehouse', type = 0)
        gWarehouse.permissions = [pUpdateOrder, pSearchOrder, pSearchAllOrder,
                                  pUpdateDeliver, pSearchDeliver, pSearchAllDeliver, ]
        gWarehouse.users = [uWarehouse]


        DBSession.add_all([
                            uAdmin, uKefu1,uKefu2, uSupplier, uWarehouse,
                            pCreateUser, pUpdateUser, pDeleteUser, pSearchUser,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                            pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                            pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                            pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                            pCreateDriver, pUpdateDriver, pDeleteDriver, pSearchDriver,
                            gAdmin, gCustomer, gOfficer, gSupplier, gWarehouse,
                            gKinlongGroup,gWeiqianGroup,
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
#        DBSession.add(ShipmentType(name = u"水运"))
#        DBSession.add(ShipmentType(name = u"空运"))
        DBSession.add(Payment(name = u"月结"))
        
        
        DBSession.add(ChargeType(name = u"按件",))
        DBSession.add(ChargeType(name = u"按体积",))
        DBSession.add(ChargeType(name = u"按重量",))


        kinlong = Customer(name = u"广东坚朗五金制品股份有限公司", address = u"广东省东莞市塘厦镇大坪村工业区卢地坑路3号", phone = "0769-82166666", contact_person = None)
        kinlong_profile = CustomerProfile(name="KINLONG_PROFILE",customer = kinlong, group = gKinlongGroup)
        
        weiqian = Customer(name = u"味千（中国）控股有限公司", address = u"广东省深圳市福田区金田路3037号金中环商务大厦主楼23号", phone = "0755-8280 5333", contact_person = None)
        weiqian_profile = CustomerProfile(name="WEIQIAN_PROFILE",customer = weiqian, group = gWeiqianGroup)

        
        supplier1 = Supplier(name = u"承运商一", address = u"广东省珠海市斗门区", phone = "0756-25361422", contact_person = u"林先生")
        supplier1_profile = SupplierProfile(name="SUPPLIER1_PROFILE",supplier=supplier1,group=gSupplier1)


        DBSession.add_all([kinlong,kinlong_profile,weiqian,weiqian_profile,supplier1,supplier1_profile])

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()

if __name__ == '__main__':
    init()

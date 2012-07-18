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
    SupplierProfile, Ratio, PickupType, PackType, Diqu, CustomerTarget, Receiver
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    try:
        print "create tables"
        metadata.drop_all(engine, checkfirst = True)

        metadata.create_all(engine)

        print "insert default value"
        #add the default value here

        uAdmin = User(name = 'admin', email = 'admin@sfhlwl.com', password = 'admin')
        uKinlong = User(name = u'kinlong', email = 'customer@test.com', password = '123')
        uWeiqian = User(name = u'weiqian', email = 'customer@test.com', password = '123')
        uKefu1 = User(name = u'kefu1', email = 'kefu1@sfhlwl.com', password = '123')
        uKefu2 = User(name = u'kefu2', email = 'kefu2@sfhlwl.com', password = '123')
        uSupplier = User(name = 'supplier', email = 'supplier@test.com', password = '123')
        uWarehouse = User(name = 'warehouse', email = 'warehouse@sfhlwl.com', password = '123')



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
        gCustomer.users = [uKinlong, uWeiqian ]
        gKinlongGroup = Group(name = 'KINLONG_GROUP', display_name = 'KINLONG GROUP', type = 1)
        gKinlongGroup.users = [uKinlong, ]
        gWeiqianGroup = Group(name = 'WEIQIAN_GROUP', display_name = 'WEIQIAN GROUP', type = 1)
        gWeiqianGroup.users = [uWeiqian]
        gOfficer = Group(name = 'OFFICER', display_name = 'Officer', type = 0)
        gOfficer.permissions = [pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder,
                                pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                                ]
        gOfficer.users = [uKefu1, uKefu2]
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
                            uAdmin, uKefu1, uKefu2, uSupplier, uWarehouse,
                            pCreateUser, pUpdateUser, pDeleteUser, pSearchUser,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                            pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                            pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                            pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                            pCreateDriver, pUpdateDriver, pDeleteDriver, pSearchDriver,
                            gAdmin, gCustomer, gOfficer, gSupplier, gWarehouse,
                            gKinlongGroup, gWeiqianGroup,
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

        payment1 = Payment(name = u"月付")
        payment2 = Payment(name = u"到付")
        payment3 = Payment(name = u"现付")
        DBSession.add_all([payment1, payment2, payment3])

        DBSession.add(Ratio(type = "QTY", value = 10))
        DBSession.add(Ratio(type = "VOL", value = 0.33))
        DBSession.add(Ratio(type = "WEIGHT", value = 0.5))

        DBSession.add(PickupType(name = u"自提"))
        DBSession.add(PickupType(name = u"送货"))
        DBSession.add(PickupType(name = u"司机直送"))
        DBSession.add(PickupType(name = u"送货上门"))
        DBSession.add(PickupType(name = u"送货上楼"))

        DBSession.add(PackType(name = u"纸箱"))
        DBSession.add(PackType(name = u"袋装"))
        DBSession.add(PackType(name = u"桶装"))
        DBSession.add(PackType(name = u"林架"))

        kinlong = Customer(name = u"广东坚朗五金制品股份有限公司", address = u"广东省东莞市塘厦镇大坪村工业区卢地坑路3号", phone = "0769-82166666", contact_person = u'陈先生', mobile = '12800138999', payment = payment1)
        kinlong_profile = CustomerProfile(name = "KINLONG_PROFILE", customer = kinlong, group = gKinlongGroup)

        kinlong_target1 = CustomerTarget(customer = kinlong, name = u'收货公司一', address = u'福建省福州市', contact_person = u'李先生', mobile = u'13880138111', phone = u'123456')
        kinlong_target2 = CustomerTarget(customer = kinlong, name = u'收货公司二', address = u'广东省深圳市', contact_person = u'张小姐', mobile = u'13800138222', phone = u'456789')
        kinlong_target3 = CustomerTarget(customer = kinlong, name = u'收货公司三', address = u'湖南省长沙市', contact_person = u'林先生', mobile = u'13800138333', phone = u'369852')

        weiqian = Customer(name = u"味千（中国）控股有限公司", address = u"广东省深圳市福田区金田路3037号金中环商务大厦主楼23号", phone = "0755-8280 5333", contact_person = u'胡先生', mobile = '12800138999', payment = payment1)
        weiqian_profile = CustomerProfile(name = "WEIQIAN_PROFILE", customer = weiqian, group = gWeiqianGroup)

        weiqian_target1 = CustomerTarget(customer = weiqian, name = u'味千收货公司一', address = u'福建省福清市', contact_person = u'张先生', mobile = u'1388013111', phone = u'123456')
        weiqian_target2 = CustomerTarget(customer = weiqian, name = u'味千收货公司二', address = u'广东省珠海市', contact_person = u'郭先生', mobile = u'1388013111', phone = u'123456')
        weiqian_target3 = CustomerTarget(customer = weiqian, name = u'味千收货公司三', address = u'湖北省武汉市', contact_person = u'赵先生', mobile = u'1388013111', phone = u'123456')

        supplier1 = Supplier(name = u"承运商一", address = u"广东省珠海市斗门区", phone = "0756-25361422", contact_person = u"林先生")
        supplier1_profile = SupplierProfile(name = "SUPPLIER1_PROFILE", supplier = supplier1, group = gSupplier1)


        DBSession.add_all([kinlong, kinlong_profile, kinlong_target1, kinlong_target2, kinlong_target3,
                           weiqian, weiqian_profile, weiqian_target1, weiqian_target2, weiqian_target3,
                           supplier1, supplier1_profile])


        receiver1 = Receiver(code = 'C001', name = '李司机', tel = '0755-12345671', mobile = '13800138111',)
        receiver2 = Receiver(code = 'C002', name = '张司机', tel = '0755-12345672', mobile = '13800138222',)
        receiver3 = Receiver(code = 'C003', name = '黄司机', tel = '0755-12345673', mobile = '13800138333',)
        receiver4 = Receiver(code = 'C004', name = '王司机', tel = '0755-12345674', mobile = '13800138444',)
        DBSession.add_all([receiver1, receiver2, receiver3, receiver4])
        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()



if __name__ == '__main__':
    init()

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
    SupplierProfile, Ratio, PickupType, PackType, Diqu, CustomerTarget, Receiver, \
    Item, CustomerTargetContact, Note
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
        uFin1 = User(name = u'fin1', email = 'fin1@sfhlwl.com', password = '123')
        uSupplier = User(name = 'supplier', email = 'supplier@test.com', password = '123')
        uWarehouse = User(name = 'warehouse', email = 'warehouse@sfhlwl.com', password = '123')


        pAdminManage = Permission(name = 'AMIN_MANAGE')
        pCreateUser = Permission(name = 'CREATE_USER')
        pUpdateUser = Permission(name = 'UPDATE_USER')
        pDeleteUser = Permission(name = 'DELETE_USER')
        pSearchUser = Permission(name = 'SEARCH_USER')
        pManageUser = Permission(name = 'MANAGE_USER')
        pCreateGroup = Permission(name = 'CREATE_GROUP')
        pUpdateGroup = Permission(name = 'UPDATE_GROUP')
        pDeleteGroup = Permission(name = 'DELETE_GROUP')
        pSearchGroup = Permission(name = 'SEARCH_GROUP')
        pManageGroup = Permission(name = 'MANAGE_GROUP')
        pCreatePermission = Permission(name = 'CREATE_PERMISSION')
        pUpdatePermission = Permission(name = 'UPDATE_PERMISSION')
        pDeletePermission = Permission(name = 'DELETE_PERMISSION')
        pSearchPermission = Permission(name = 'SEARCH_PERMISSION')
        pManagePermission = Permission(name = 'MANAGE_PERMISSION')
        pCreateMaster = Permission(name = 'CREATE_MASTER')
        pUpdateMaster = Permission(name = 'UPDATE_MASTER')
        pDeleteMaster = Permission(name = 'DELETE_MASTER')
        pSearchMaster = Permission(name = 'SEARCH_MASTER')
        pManageMaster = Permission(name = 'MANAGE_MASTER')
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

        pManageFin = Permission(name = 'MANAGE_FIN')
        pFinSearch = Permission(name = 'FIN_SEARCH')
        pFinApprove = Permission(name = 'FIN_APPROVE')
        pFinPaid = Permission(name = 'FIN_PAID')
        pFinSupplierPaid = Permission(name = 'FIN_SUPPLIER_PAID')


        gAdmin = Group(name = u'管理员组', display_name = u'管理员组', type = 0)
        gAdmin.permissions = [pAdminManage, pCreateUser, pUpdateUser, pDeleteUser, pSearchUser, pManageUser,
                              pCreateGroup, pUpdateGroup, pDeleteGroup, pSearchGroup, pManageGroup,
                              pCreatePermission, pUpdatePermission, pDeletePermission, pSearchPermission, pManagePermission,
                              pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                              pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                              pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                              pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                              pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                              pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                              pManageFin, pFinSearch, pFinApprove, pFinPaid, pFinSupplierPaid
                              ]
        gAdmin.users = [uAdmin, ]
        gCustomer = Group(name = u'客户组', display_name = u'客户组', type = 0)
        gCustomer.permissions = [pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, ]
        gCustomer.users = [uKinlong, uWeiqian ]
        gKinlongGroup = Group(name = 'KINLONG_GROUP', display_name = 'KINLONG GROUP', type = 1)
        gKinlongGroup.users = [uKinlong, ]
        gWeiqianGroup = Group(name = 'WEIQIAN_GROUP', display_name = 'WEIQIAN GROUP', type = 1)
        gWeiqianGroup.users = [uWeiqian]
        gOfficer = Group(name = u'客服组', display_name = u'客服组', type = 0)
        gOfficer.permissions = [
                                pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                                pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                                pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                                ]
        gOfficer.users = [uKefu1, uKefu2]

        gFin = Group(name = u'财务组', display_name = u'财务组', type = 0)
        gFin.permissions = [
                            pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                            pManageFin, pFinSearch, pFinApprove, pFinPaid, pFinSupplierPaid
                            ]
        gFin.users = [uFin1, ]

        gSupplier = Group(name = u'承运商组', display_name = u'承运商组', type = 0)
        gSupplier.permissions = [pUpdateDeliver, pSearchDeliver ]
        gSupplier.users = [uSupplier]

        gSupplier1 = Group(name = 'SUPPLIER_1', display_name = 'Supplier1', type = 1)
        gSupplier1.users = [uSupplier]
        gWarehouse = Group(name = u'仓库组', display_name = u'仓库组', type = 0)
        gWarehouse.permissions = [pUpdateOrder, pSearchOrder, pSearchAllOrder,
                                  pUpdateDeliver, pSearchDeliver, pSearchAllDeliver, ]
        gWarehouse.users = [uWarehouse]


        DBSession.add_all([
                            uAdmin, uKefu1, uKefu2, uSupplier, uWarehouse,
                            pCreateUser, pUpdateUser, pDeleteUser, pSearchUser, pManageUser,
                            pCreateGroup, pUpdateGroup, pDeleteGroup, pSearchGroup, pManageGroup,
                            pCreatePermission, pUpdatePermission, pDeletePermission, pSearchPermission, pManagePermission,
                            pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                            pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                            pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                            pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
                            gAdmin, gCustomer, gOfficer, gSupplier, gWarehouse,
                            gKinlongGroup, gWeiqianGroup,
                            ])

        for n, en, tn in [(u'米', u'meter', u'米'), (u'分米', u'dm', u'分米'), (u'厘米', u'cm', u'釐米'), (u'吨', u'ton', u'噸'), (u'千克', u'kg', u'千克'), (u'克', u'g', u'克'),
                     (u'箱', u'box', u'箱'), (u'瓶', u'bottle', u'瓶'), (u'只', u'pic', u'只'), (u'打', u'dozen', u'打'), ]:
            DBSession.add(ItemUnit(name = n, english_name = en, tradition_name = tn))


        for n, en, tn in [(u'吨', u'ton', u'噸'), (u'千克', u'kg', u'千克'), (u'克', u'g', u'克'), ]:
            DBSession.add(WeightUnit(name = n, english_name = en, tradition_name = tn))

#        location1 = InventoryLocation(name = u"深圳仓库", address = u"仓库地址 1", manager = "李先生", full_path = u"深圳仓库")
#        location1_A = InventoryLocation(name = u"A区", address = u"仓库地址 1", manager = "李先生", full_path = u"A区", parent = location1)
#        location1_B = InventoryLocation(name = u"B区", address = u"仓库地址 1", manager = "李先生", full_path = u"B区", parent = location1)
#        location1_C = InventoryLocation(name = u"C区", address = u"仓库地址 1", manager = "李先生", full_path = u"C区", parent = location1)
#        location2 = InventoryLocation(name = u"东莞仓库", address = u"仓库地址 2", manager = "林先生", full_path = u"东莞仓库")
#        location2_A = InventoryLocation(name = u"A区", address = u"仓库地址 2", manager = "林先生", full_path = u"A区", parent = location2)
#        location2_B = InventoryLocation(name = u"B区", address = u"仓库地址 2", manager = "林先生", full_path = u"B区", parent = location2)
#        location2_C = InventoryLocation(name = u"C区", address = u"仓库地址 2", manager = "林先生", full_path = u"C区", parent = location2)
#
#        DBSession.add_all([location1, location1_A, location1_B, location1_C,
#                           location2, location2_A, location2_B, location2_C,
#                           ])
#        location1.full_path_ids = location1.id
#        location2.full_path_ids = location2.id

        DBSession.flush()

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

        DBSession.add(Item(name = u"五金"))
        DBSession.add(Item(name = u"食品"))
        DBSession.add(Item(name = u"器材"))
        DBSession.add(Item(name = u"木料"))
        DBSession.add(Item(name = u"器具"))
        DBSession.add(Item(name = u"家具"))


        kinlong = Customer(name = u"广东坚朗五金制品股份有限公司", display_name = u'坚朗', address = u"广东省东莞市塘厦镇大坪村工业区卢地坑路3号", phone = "0769-82166666", contact_person = u'陈先生', mobile = '12800138999', payment = payment1)
        kinlong_profile = CustomerProfile(name = "KINLONG_PROFILE", customer = kinlong, group = gKinlongGroup)

        kinlong_target1 = CustomerTarget(customer = kinlong, name = u'收货公司一')
        kinlong_target1_c1 = CustomerTargetContact(customer_target = kinlong_target1, name = u'李一', mobile = u'13880138111', phone = u'1234561', address = u'福建省福州市AA区', is_default = 1)
        kinlong_target1_c2 = CustomerTargetContact(customer_target = kinlong_target1, name = u'张一', mobile = u'13880138112', phone = u'1234562', address = u'福建省福州市BB区',)
        kinlong_target1_c3 = CustomerTargetContact(customer_target = kinlong_target1, name = u'王一', mobile = u'13880138113', phone = u'1234563', address = u'福建省福州市CC区',)

        kinlong_target2 = CustomerTarget(customer = kinlong, name = u'收货公司二')
        kinlong_target2_c1 = CustomerTargetContact(customer_target = kinlong_target2, name = u'樊一', mobile = u'13800138221', phone = u'4578251', address = u'广东省深圳市AA区', is_default = 1)
        kinlong_target2_c2 = CustomerTargetContact(customer_target = kinlong_target2, name = u'林一', mobile = u'13800138222', phone = u'4578252', address = u'广东省深圳市BB区')
        kinlong_target2_c3 = CustomerTargetContact(customer_target = kinlong_target2, name = u'余一', mobile = u'13800138223', phone = u'4578253', address = u'广东省深圳市CC区')

        kinlong_target3 = CustomerTarget(customer = kinlong, name = u'收货公司三')
        kinlong_target3_c1 = CustomerTargetContact(customer_target = kinlong_target3, name = u'樊一', mobile = u'13800138331', phone = u'14587541', address = u'湖南省长沙市AA区', is_default = 1)
        kinlong_target3_c2 = CustomerTargetContact(customer_target = kinlong_target3, name = u'林一', mobile = u'13800138332', phone = u'14587542', address = u'湖南省长沙市BB区')
        kinlong_target3_c3 = CustomerTargetContact(customer_target = kinlong_target3, name = u'余一', mobile = u'13800138333', phone = u'14587543', address = u'湖南省长沙市CC区')

        weiqian = Customer(name = u"味千（中国）控股有限公司", display_name = u'味千', address = u"广东省深圳市福田区金田路3037号金中环商务大厦主楼23号", phone = "0755-8280 5333", contact_person = u'胡先生', mobile = '12800138999', payment = payment1)
        weiqian_profile = CustomerProfile(name = "WEIQIAN_PROFILE", customer = weiqian, group = gWeiqianGroup)

        weiqian_target1 = CustomerTarget(customer = weiqian, name = u'味千收货公司一')
        weiqian_target1_c1 = CustomerTargetContact(customer_target = weiqian_target1 , name = u'张二', mobile = u'1388013111', phone = u'123456', address = u'福建省福清市AA区', is_default = 1)
        weiqian_target1_c2 = CustomerTargetContact(customer_target = weiqian_target1 , name = u'李二', mobile = u'1388013111', phone = u'123456', address = u'福建省福清市BB区')

        weiqian_target2 = CustomerTarget(customer = weiqian, name = u'味千收货公司二')
        weiqian_target2_c1 = CustomerTargetContact(customer_target = weiqian_target2 , name = u'林二', mobile = u'1388013111', phone = u'123456', address = u'广东省珠海市AA区', is_default = 1)
        weiqian_target2_c2 = CustomerTargetContact(customer_target = weiqian_target2 , name = u'五二', mobile = u'1388013111', phone = u'123456', address = u'广东省珠海市BB区')

        weiqian_target3 = CustomerTarget(customer = weiqian, name = u'味千收货公司三')
        weiqian_target2_c1 = CustomerTargetContact(customer_target = weiqian_target3 , name = u'林三', mobile = u'1388013111', phone = u'123456', address = u'湖北省武汉市AA区', is_default = 1)
        weiqian_target2_c2 = CustomerTargetContact(customer_target = weiqian_target3 , name = u'五三', mobile = u'1388013111', phone = u'123456', address = u'湖北省武汉市BB区')

        supplier1 = Supplier(name = u"承运商一", display_name = u'承运商一', address = u"广东省珠海市吉大区", phone = "0756-25361422", contact_person = u"林先生")
        supplier1_profile = SupplierProfile(name = "SUPPLIER1_PROFILE", supplier = supplier1, group = gSupplier1)


        DBSession.add_all([kinlong, kinlong_profile,
                           kinlong_target1, kinlong_target1_c1, kinlong_target1_c2, kinlong_target1_c3,
                           kinlong_target2, kinlong_target2_c1, kinlong_target2_c2, kinlong_target2_c3,
                           kinlong_target3, kinlong_target3_c1, kinlong_target3_c2, kinlong_target3_c3,
                           weiqian, weiqian_profile,
                           weiqian_target1, weiqian_target1_c1, weiqian_target1_c2,
                           weiqian_target2, weiqian_target2_c1, weiqian_target2_c2,
                           weiqian_target3, weiqian_target2_c1, weiqian_target2_c2,
                           supplier1, supplier1_profile])


        receiver1 = Receiver(code = 'C001', name = '李司机', tel = '0755-12345671', mobile = '13800138111',)
        receiver2 = Receiver(code = 'C002', name = '张司机', tel = '0755-12345672', mobile = '13800138222',)
        receiver3 = Receiver(code = 'C003', name = '黄司机', tel = '0755-12345673', mobile = '13800138333',)
        receiver4 = Receiver(code = 'C004', name = '王司机', tel = '0755-12345674', mobile = '13800138444',)
        DBSession.add_all([receiver1, receiver2, receiver3, receiver4])


        DBSession.add_all([
                           Note(name = u'坚朗', range = [('1001', '2000'), ('3001', '4000')]),
                           Note(name = u'味千', range = [('2001', '3000'), ('4001', '5000')]),
                           ])


        print 'insert diqu'
        province_f = open('sys2do/sql/master_province.sql')
        province_sql = "".join(province_f.readlines())
        province_f.close()

        city_f = open('sys2do/sql/master_city.sql')
        city_sql = "".join(city_f.readlines())
        city_f.close()

        conn = DBSession.connection()
        conn.execute(province_sql)
        conn.execute(city_sql)

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()



if __name__ == '__main__':
    init()
#    insert_diqu()

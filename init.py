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
#        uKinlong = User(name = u'kinlong', email = 'customer@test.com', password = '123')
#        uWeiqian = User(name = u'weiqian', email = 'customer@test.com', password = '123')
        uKefua = User(name = u'kefu1', email = 'kefu1@sfhlwl.com', password = '123')
        uWha = User(name = u'wh1', email = 'kefu1@sfhlwl.com', password = '123')
        uFina = User(name = u'fin1', email = 'kefu1@sfhlwl.com', password = '123')
        uUser1 = User(name = u'罗凌云', email = 'kefu1@sfhlwl.com', password = '123')
        uUser2 = User(name = u'陈龙', email = 'kefu1@sfhlwl.com', password = '123')
#        uUser3 = User(name = u'邓二', email = 'kefu1@sfhlwl.com', password = '123')
        uUser4 = User(name = u'刘坤', email = 'kefu1@sfhlwl.com', password = '123')
        uUser5 = User(name = u'何灿明', email = 'kefu1@sfhlwl.com', password = '123')
#        uUser6 = User(name = u'黄燕琴', email = 'kefu1@sfhlwl.com', password = '123')
        uUser7 = User(name = u'吴丽玲', email = 'kefu1@sfhlwl.com', password = '123')
        uUser8 = User(name = u'徐腾芳', email = 'kefu1@sfhlwl.com', password = '123')
        uUser9 = User(name = u'黄霄莹', email = 'kefu1@sfhlwl.com', password = '123')
        uUser10 = User(name = u'林凤', email = 'kefu1@sfhlwl.com', password = '123')
#        uUser11 = User(name = u'吴秋梅', email = 'kefu1@sfhlwl.com', password = '123')
        uUser12 = User(name = u'林秀贤', email = 'kefu1@sfhlwl.com', password = '123')
        uUser13 = User(name = u'曾德莲', email = 'kefu1@sfhlwl.com', password = '123')
        uUser14 = User(name = u'李时坚', email = 'kefu1@sfhlwl.com', password = '123')

        uUser15 = User(name = u'深福合力', email = 'kefu1@sfhlwl.com', password = '123')


        pAdminManage = Permission(name = 'AMIN_MANAGE', desc = u'进入管理员控制台')
        pCreateUser = Permission(name = 'CREATE_USER', desc = u'创建新用户')
        pUpdateUser = Permission(name = 'UPDATE_USER', desc = u'更新用户信息')
        pDeleteUser = Permission(name = 'DELETE_USER', desc = u'删除用户')
        pSearchUser = Permission(name = 'SEARCH_USER', desc = u'查询用户')
        pManageUser = Permission(name = 'MANAGE_USER', desc = u'管理所有用户')
        pCreateGroup = Permission(name = 'CREATE_GROUP', desc = u'删除组')
        pUpdateGroup = Permission(name = 'UPDATE_GROUP', desc = u'更新组信息')
        pDeleteGroup = Permission(name = 'DELETE_GROUP', desc = u'删除组')
        pSearchGroup = Permission(name = 'SEARCH_GROUP', desc = u'查询所在组')
        pManageGroup = Permission(name = 'MANAGE_GROUP', desc = u'管理所有组')
        pCreatePermission = Permission(name = 'CREATE_PERMISSION', desc = u'创建新权限')
        pUpdatePermission = Permission(name = 'UPDATE_PERMISSION', desc = u'更新权限')
        pDeletePermission = Permission(name = 'DELETE_PERMISSION', desc = u'删除权限')
        pSearchPermission = Permission(name = 'SEARCH_PERMISSION', desc = u'查询所在权限')
        pManagePermission = Permission(name = 'MANAGE_PERMISSION', desc = u'管理所在权限')
        pCreateMaster = Permission(name = 'CREATE_MASTER', desc = u'创建新的系统设置')
        pUpdateMaster = Permission(name = 'UPDATE_MASTER', desc = u'更新现有的系统设置')
        pDeleteMaster = Permission(name = 'DELETE_MASTER', desc = u'删除系统设置')
        pSearchMaster = Permission(name = 'SEARCH_MASTER', desc = u'查询所有的系统设置')
        pManageMaster = Permission(name = 'MANAGE_MASTER', desc = u'进入系统设置控制台')
        pCreateOrder = Permission(name = 'CREATE_ORDER', desc = u'创建新的订单')
        pUpdateOrder = Permission(name = 'UPDATE_ORDER', desc = u'更新订单信息')
        pDeleteOrder = Permission(name = 'DELETE_ORDER', desc = u'删除订单')
        pSearchOrder = Permission(name = 'SEARCH_ORDER', desc = u'查询订单')
        pManageOrder = Permission(name = 'MANAGE_ORDER', desc = u'管理所有的订单')
        pSearchAllOrder = Permission(name = 'SEARCH_ALL_ORDER', desc = u'查询所有的订单')
        pCreateDeliver = Permission(name = 'CREATE_DELIVER', desc = u'创建新的送货单')
        pUpdateDeliver = Permission(name = 'UPDATE_DELIVER', desc = u'更新送货单信息')
        pDeleteDeliver = Permission(name = 'DELETE_DELIVER', desc = u'删除送货单信息')
        pSearchDeliver = Permission(name = 'SEARCH_DELIVER', desc = u'查询所在的送货单')
        pManageDeliver = Permission(name = 'MANAGE_DELIVER', desc = u'进入送货单管理控制台')
        pSearchAllDeliver = Permission(name = 'SEARCH_ALL_ELIVER', desc = u'查询所有的送货单')
        pCreateCustomer = Permission(name = 'CREATE_CUSTOMER', desc = u'创建新的客户')
        pUpdateCustomer = Permission(name = 'UPDATE_CUSTOMER', desc = u'更新客户信息')
        pDeleteCustomer = Permission(name = 'DELETE_CUSTOMER', desc = u'删除客户')
        pSearchCustomer = Permission(name = 'SEARCH_CUSTOMER', desc = u'查询所有的客户')
        pCreateSupplier = Permission(name = 'CREATE_SUPPLIER', desc = u'创建新的承运商')
        pUpdateSupplier = Permission(name = 'UPDATE_SUPPLIER', desc = u'更新承运商信息')
        pDeleteSupplier = Permission(name = 'DELETE_SUPPLIER', desc = u'删除承运商信息')
        pSearchSupplier = Permission(name = 'SEARCH_SUPPLIER', desc = u'查询所有的承运商信息')
        pCreateWarehouse = Permission(name = 'CREATE_WAREHOUSE', desc = u'创建新的仓存地点')
        pUpdateWarehouse = Permission(name = 'UPDATE_WAREHOUSE', desc = u'更新仓存地点信息')
        pDeleteWarehouse = Permission(name = 'DELETE_WAREHOUSE', desc = u'删除仓存地点')
        pSearchWarehouse = Permission(name = 'SEARCH_WAREHOUSE', desc = u'查询所有仓存地点')
        pManageFin = Permission(name = 'MANAGE_FIN', desc = u'进入财务管理控制台')
        pFinSearch = Permission(name = 'FIN_SEARCH', desc = u'查询订单信息')
        pFinApprove = Permission(name = 'FIN_APPROVE', desc = u'审核通过订单信息')
        pFinPaid = Permission(name = 'FIN_PAID', desc = u'确认客户是否已付款')
        pFinSupplierPaid = Permission(name = 'FIN_SUPPLIER_PAID', desc = u'确认是否已付款予承运商')



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

        gKinlongGroup = Group(name = 'KINLONG_GROUP', display_name = 'KINLONG GROUP', type = 1)

        gWeiqianGroup = Group(name = 'WEIQIAN_GROUP', display_name = 'WEIQIAN GROUP', type = 1)

        gOfficer = Group(name = u'客服组', display_name = u'客服组', type = 0)
        gOfficer.permissions = [
                                pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                                pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                                pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                                ]
        gOfficer.users = [uKefua, uUser7, uUser9, uUser10, uUser13 ]

        gFin = Group(name = u'财务组', display_name = u'财务组', type = 0)
        gFin.permissions = [
                            pCreateMaster, pUpdateMaster, pDeleteMaster, pSearchMaster, pManageMaster,
                            pCreateOrder, pUpdateOrder, pDeleteOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                            pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pManageDeliver, pSearchAllDeliver,
                            pManageFin, pFinSearch, pFinApprove, pFinPaid, pFinSupplierPaid
                            ]
        gFin.users = [uFina, uUser1, uUser2, uUser4, uUser5, uUser12, uUser15]

        gSupplier = Group(name = u'承运商组', display_name = u'承运商组', type = 0)
        gSupplier.permissions = [pUpdateDeliver, pSearchDeliver ]
#        gSupplier.users = [uSupplier]

        gSupplier1 = Group(name = 'SUPPLIER_1', display_name = 'Supplier1', type = 1)
#        gSupplier1.users = [uSupplier]
        gWarehouse = Group(name = u'仓库组', display_name = u'仓库组', type = 0)
        gWarehouse.permissions = [pUpdateOrder, pSearchOrder, pSearchAllOrder, pManageOrder,
                                  pCreateDeliver, pUpdateDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver ]
        gWarehouse.users = [uWha, uUser8, uUser14]


        DBSession.add_all([
                            uAdmin, uKefua, uFina, uWha,
#                            uKefu2, uSupplier, uWarehouse,
                            uUser1, uUser2, uUser4, uUser5, uUser7, uUser8, uUser9, uUser10, uUser12, uUser13, uUser14, uUser15,
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


        kinlong = Customer(name = u"广东坚朗五金制品股份有限公司", display_name = u'坚朗', province_id = 19, city_id = 304, address = u"塘厦镇大坪村工业区卢地坑路3号", phone = "0769-82166666", contact_person = u'陈先生', mobile = '12800138999', payment = payment1)
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

        weiqian = Customer(name = u"味千（中国）控股有限公司", display_name = u'味千', province_id = 19, city_id = 290, address = u"金田路3037号金中环商务大厦主楼23号", phone = "0755-8280 5333", contact_person = u'胡先生', mobile = '12800138999', payment = payment1)
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

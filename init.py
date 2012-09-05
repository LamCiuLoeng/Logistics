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
    Item, CustomerContact, Note, CustomerSource, City
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
                              pCreateDeliver, pUpdateDeliver, pDeleteDeliver, pSearchDeliver, pSearchAllDeliver, pManageDeliver,
                              pCreateCustomer, pUpdateCustomer, pDeleteCustomer, pSearchCustomer,
                              pCreateSupplier, pUpdateSupplier, pDeleteSupplier, pSearchSupplier,
                              pCreateWarehouse, pUpdateWarehouse, pDeleteWarehouse, pSearchWarehouse,
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


        receiver1 = Receiver(code = u'粤BIP092', name = u'黄司机', tel = None, mobile = '15976884544',)
        receiver2 = Receiver(code = u'粤BQ4225', name = '叶司机', tel = None, mobile = '13682553458',)
        receiver3 = Receiver(code = u'粤BJU706', name = u'张司机', tel = None, mobile = '15813808186',)
        receiver4 = Receiver(code = u'粤BJX667', name = u'李司机', tel = None, mobile = '13590435287',)
        receiver5 = Receiver(code = u'粤BPY286', name = u'杨司机', tel = None, mobile = '13554881765',)
        receiver6 = Receiver(code = u'粤BVQ582', name = u'杨司机', tel = None, mobile = '13724255912',)
        receiver7 = Receiver(code = u'粤B2X846', name = u'巍司机', tel = None, mobile = '13410189026',)

        DBSession.add_all([receiver1, receiver2, receiver3, receiver4, receiver5, receiver6, receiver7])

        note1 = Note(code = '0001191-1', name = u'坚朗', province_id = 19, city_id = 290, apply_person_id = 1, apply_time = '2012-08-23',
                     begin_no = '1188000', end_no = '1188599', remark = u'坚朗专用二本')

        note2 = Note(code = '1001191-1', name = u'味千', province_id = 19, city_id = 290, apply_person_id = 1, apply_time = '2012-08-23',
                     begin_no = '2188000', end_no = '2188599', remark = u'味千专用一本')

        DBSession.add_all([
                           note1,
                           ])



        kinlong = Customer(name = u"广东坚朗五金制品股份有限公司", display_name = u'坚朗', province_id = 19, city_id = 304,
                           address = u"塘厦镇大坪村工业区卢地坑路3号", phone = "0769-82166666", contact_person = u'陈先生',
                           mobile = '12800138999', note = note1)

        kinlong_source1 = CustomerSource(customer = kinlong, name = u"坚朗一厂", province_id = 19, city_id = 304, payment = payment1)  #东莞
        kinlong_source2 = CustomerSource(customer = kinlong, name = u"坚朗二厂", province_id = 19, city_id = 304, payment = payment1)  #东莞
        kinlong_source3 = CustomerSource(customer = kinlong, name = u"坚朗三厂", province_id = 19, city_id = 304, payment = payment1)  #东莞


        DBSession.add_all([
                           kinlong, kinlong_source1, kinlong_source2, kinlong_source3,
                           ])

        DBSession.flush()


        kinlong_source1_c1 = CustomerContact(customer = kinlong, type = 'S', refer_id = kinlong_source1.id, name = u'李小明', mobile = u'13880138111', phone = u'1234561', address = u'厚街', is_default = 1)
        kinlong_source1_c2 = CustomerContact(customer = kinlong, type = 'S', refer_id = kinlong_source1.id, name = u'张三', mobile = u'13880138112', phone = u'1234562', address = u'长安',)

        kinlong_source2_c1 = CustomerContact(customer = kinlong, type = 'S', refer_id = kinlong_source2.id, name = u'王二', mobile = u'13880138113', phone = u'1234563', address = u'常平',)
        kinlong_source2_c2 = CustomerContact(customer = kinlong, type = 'S', refer_id = kinlong_source2.id, name = u'王小川', mobile = u'13880138114', phone = u'1234563', address = u'虎门',)

        kinlong_source3_c2 = CustomerContact(customer = kinlong, type = 'S', refer_id = kinlong_source3.id, name = u'钟远', mobile = u'13880138116', phone = u'1234563', address = u'大岭山',)

        DBSession.add_all([
                           kinlong_source1_c1, kinlong_source1_c2, kinlong_source2_c1, kinlong_source2_c2, kinlong_source3_c2,
                           ])

        #import the kinlong target contact
        import_kinlong_target(kinlong)
        #import the supplier
        import_supplier(payment1)


        weiqian = Customer(name = u"味千(中国)控投有限公司", display_name = u'味千', province_id = 19, city_id = 290,
                           address = u"福田区金田路3037号金中环商务大厦主楼23号", phone = "0755-8280 5333", contact_person = None,
                           mobile = None, note = note2)

        weiqian_source1 = CustomerSource(customer = weiqian, name = u"味千一厂", province_id = 19, city_id = 290, payment = payment1)

        DBSession.add_all([
                           weiqian, weiqian_source1
                           ])

        DBSession.flush()

        weiqian_source1_c1 = CustomerContact(customer = weiqian, type = 'S', refer_id = weiqian_source1.id, name = u'陆先生', mobile = u'13880138111', phone = u'1234561', address = u'福田', is_default = 1)
        DBSession.add_all([
                           weiqian_source1_c1,
                           ])

        import_weiqian_targets(weiqian)

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()





def import_kinlong_target(kinlong):
    print "insert kinlong target"
    d = open('kinlong_contact.txt')
    for line in d:
        location, name, mobile = line.strip().split("|")
        location = unicode(location)
        try:
            c = DBSession.query(City).filter(City.name.op('like')('%%%s%%' % location[:2])).one()
            t = CustomerTarget(customer = kinlong, name = location, province_id = c.parent().id, city_id = c.id)
            DBSession.add(t)
            DBSession.flush()
            contact = CustomerContact(customer = kinlong, type = 'T', refer_id = t.id, name = name, mobile = mobile, phone = None, address = None)
            DBSession.add(contact)
        except:
            pass
    d.close()

    hangkou = CustomerTarget(customer = kinlong, name = u'汉口办(公共)', province_id = 17, city_id = 261)
    DBSession.flush()
    hangkou_c = CustomerContact(customer = kinlong, type = 'T', refer_id = hangkou.id, name = u'张明洋', mobile = '13407191121', phone = None, address = u'汉口')
    wuchang = CustomerTarget(customer = kinlong, name = u'武昌办公共、商用建筑销售部', province_id = 17, city_id = 261)
    shanghai = CustomerTarget(customer = kinlong, name = u'上海住宅开发部', province_id = 9, city_id = None)
    DBSession.flush()
    shanghai_c = CustomerContact(customer = kinlong, type = 'T', refer_id = shanghai.id, name = u'李金虎', mobile = '13774413112', phone = None, address = None)
    fuqing = CustomerTarget(customer = kinlong, name = u'福清销售点', province_id = 13, city_id = 207)
    DBSession.flush()
    fuqing_c = CustomerContact(customer = kinlong, type = 'T', refer_id = fuqing.id, name = u'陈文峰', mobile = '18259122060', phone = None, address = u'福清')
    huadu = CustomerTarget(customer = kinlong, name = u'花都办', province_id = 19, city_id = 288)
    DBSession.flush()
    huadu_c = CustomerContact(customer = kinlong, type = 'T', refer_id = huadu.id, name = u'彭双林', mobile = '13060809011', phone = None, address = u'花都')
    changshu = CustomerTarget(customer = kinlong, name = u'常熟办', province_id = 10, city_id = 170)
    DBSession.flush()
    changshu_c = CustomerContact(customer = kinlong, type = 'T', refer_id = changshu.id, name = u'梅陈赓', mobile = '15951100335', phone = None, address = u'常熟')
    kunshang = CustomerTarget(customer = kinlong, name = u'昆山销售点', province_id = 10, city_id = 170)
    DBSession.flush()
    kunshang_c = CustomerContact(customer = kinlong, type = 'T', refer_id = kunshang.id, name = u'肖杰', mobile = '13616218299', phone = None, address = u'昆山')
    wujiang = CustomerTarget(customer = kinlong, name = u'吴江销售点', province_id = 10, city_id = 170)
    DBSession.flush()
    wujiang_c = CustomerContact(customer = kinlong, type = 'T', refer_id = wujiang.id, name = u'向武将', mobile = '13862105593', phone = None, address = u'吴江')
    zjg = CustomerTarget(customer = kinlong, name = u'张家港销售点', province_id = 10, city_id = 170)
    DBSession.flush()
    zjg_c = CustomerContact(customer = kinlong, type = 'T', refer_id = zjg.id, name = u'胡伟', mobile = '15850181896', phone = None, address = u'张家港')
    yx = CustomerTarget(customer = kinlong, name = u'宜兴办', province_id = 10, city_id = 167)
    DBSession.flush()
    yx_c = CustomerContact(customer = kinlong, type = 'T', refer_id = yx.id, name = u'王伟', mobile = '13347926039', phone = None, address = u'宜兴')
    cx = CustomerTarget(customer = kinlong, name = u'慈溪销售点', province_id = 11, city_id = 180)
    DBSession.flush()
    cx_c = CustomerContact(customer = kinlong, type = 'T', refer_id = cx.id, name = u'刘晓', mobile = '13566087866', phone = None, address = u'慈溪')
    zj = CustomerTarget(customer = kinlong, name = u'诸暨销售点', province_id = 11, city_id = 184)
    DBSession.flush()
    zj_c = CustomerContact(customer = kinlong, type = 'T', refer_id = zj.id, name = u'叶坦', mobile = '13575559619', phone = None, address = u'诸暨')
    cn = CustomerTarget(customer = kinlong, name = u'苍南销售点', province_id = 11, city_id = 181)
    DBSession.flush()
    cn_c = CustomerContact(customer = kinlong, type = 'T', refer_id = cn.id, name = u'李志坚', mobile = '13646536682', phone = None, address = u'苍南')
    wl = CustomerTarget(customer = kinlong, name = u'温岭销售点', province_id = 11, city_id = 188)
    DBSession.flush()
    wl_c = CustomerContact(customer = kinlong, type = 'T', refer_id = wl.id, name = u'彭学江', mobile = '13957677975', phone = None, address = u'温岭')
    yw = CustomerTarget(customer = kinlong, name = u'义乌销售点', province_id = 11, city_id = 185)
    DBSession.flush()
    yw_c = CustomerContact(customer = kinlong, type = 'T', refer_id = yw.id, name = u'贡健', mobile = '15057840176', phone = None, address = u'义乌')


    DBSession.add_all([
                       hangkou, hangkou_c, wuchang, shanghai, shanghai_c, fuqing, fuqing_c, huadu, huadu_c, changshu, changshu_c, kunshang, kunshang_c,
                       wujiang, wujiang_c, zjg, zjg_c, yx, yx_c, cx, cx_c, zj, zj_c, cn, cn_c, wl, wl_c, yw, yw_c,
                       ])



def import_weiqian_targets(weiqian):
    print 'import weiqian targets'
    t1 = CustomerTarget(customer = weiqian, name = u'深圳市味来道贸易有限公司Ａ', province_id = 19, city_id = 290)
    DBSession.flush()
    t1_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t1.id, name = u'邓梦成', mobile = '13410716458', phone = '0755-89538779,83742178', address = u'南山区沙河西路深宝路交界处白沙物流旁（深圳市粮食集团曙光冷库）', remark = u'深圳代理商')

    t2 = CustomerTarget(customer = weiqian, name = u'广州白云沪苏贸易经营部', province_id = 19, city_id = 290)
    DBSession.flush()
    t2_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t2.id, name = u'吴煌龙', mobile = '13798313454', phone = '0755-28273934', address = u'布吉莲花路莲山庄五村内围42号', remark = u'深圳代理商')

    t3 = CustomerTarget(customer = weiqian, name = u'香港港丰控股有限公司', province_id = 33, city_id = None)
    DBSession.flush()
    t3_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t3.id, name = u'刘德基', mobile = None, phone = '0085292678917,0085225167033', email = 'newtongroupholdings@gmail.com', address = u'新界将军澳工业村 骏光街9号（惠康超市）- 牛奶公司冷藏货收货区', remark = u'香港代理商')

    t4 = CustomerTarget(customer = weiqian, name = u'深圳市味来道贸易有限公司Ｂ', province_id = 19, city_id = 290)
    DBSession.flush()
    t4_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t4.id, name = u'邓梦成', mobile = None, phone = '0755-89538779,83472178', email = None, address = u'龙岗区坪山镇坑梓工业园沃尔玛中心配送仓', remark = u'深圳代理商')

    t5 = CustomerTarget(customer = weiqian, name = u'深圳市农批华兴经营部', province_id = 19, city_id = 290)
    DBSession.flush()
    t5_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t5.id, name = u'邓老板', mobile = '13823636826', phone = None, email = None, address = u'龙岗区布路布吉警署后松园新村', remark = u'深圳代理商')

    t6 = CustomerTarget(customer = weiqian, name = u'深圳市金满源贸易有限公司', province_id = 19, city_id = 290)
    DBSession.flush()
    t6_c1 = CustomerContact(customer = weiqian, type = 'T', refer_id = t6.id, name = u'罗发财', mobile = '18926455915', phone = None, email = None, address = u'布吉镇坂田街道岗头风门坳村亚洲工业园15号', remark = u'深圳代理商')
    t6_c2 = CustomerContact(customer = weiqian, type = 'T', refer_id = t6.id, name = u'王进云', mobile = '13423967408', phone = '0755-29001027', email = 'wembnc118@163.com', address = u'布吉镇坂田街道岗头风门坳村亚洲工业园15号', remark = u'深圳代理商')

    t7 = CustomerTarget(customer = weiqian, name = u'成都永盛食品有限责任公司', province_id = 23, city_id = 326)
    DBSession.flush()
    t7_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t7.id, name = u'蒋志英', mobile = '18980019806', phone = '028-85354318', email = '410137392@qq.com', address = u'锦江区琉璃场径天中路上东家园77路公交车总站', remark = u'成都代理商')

    t8 = CustomerTarget(customer = weiqian, name = u'湘潭市兴盛贸易有限公司', province_id = 18, city_id = 27)
    DBSession.flush()
    t8_c1 = CustomerContact(customer = weiqian, type = 'T', refer_id = t8.id, name = u'谭冰艳', mobile = '18608489007', phone = None, email = None, address = u'雨湖区草塘路61号', remark = u'湘潭代现商')
    t8_c2 = CustomerContact(customer = weiqian, type = 'T', refer_id = t8.id, name = u'周卫星', mobile = '13317425511', phone = '0731-55578399', email = None, address = u'雨湖区草塘路61号', remark = u'湘潭代现商')


    t9 = CustomerTarget(customer = weiqian, name = u'惠州市三林贸易有限公司', province_id = 19, city_id = 298)
    DBSession.flush()
    t9_c1 = CustomerContact(customer = weiqian, type = 'T', refer_id = t9.id, name = u'张君', mobile = None, phone = '0752-2695370', email = None, address = u'惠城区镇隆镇皇后村委斜对面', remark = u'惠州代理商')
    t9_c2 = CustomerContact(customer = weiqian, type = 'T', refer_id = t9.id, name = u'徐三林', mobile = '18688335596', phone = '0752-2695370', email = 'hzssl2008@163.com', address = u'惠城区镇隆镇皇后村委斜对面', remark = u'惠州代理商')

    t10 = CustomerTarget(customer = weiqian, name = u'佛山顺德区瑞驰贸易有限公司', province_id = 19, city_id = 293)
    DBSession.flush()
    t10_c1 = CustomerContact(customer = weiqian, type = 'T', refer_id = t10.id, name = u'梁友鸿', mobile = '13702622982', phone = '0757-2229201', email = None, address = u'顺德区大良大门小湾村为民街8号', remark = u'顺德代理商')
    t10_c2 = CustomerContact(customer = weiqian, type = 'T', refer_id = t10.id, name = u'温风涛', mobile = None, phone = None, email = None, address = u'顺德区大良大门小湾村为民街8号', remark = u'顺德代理商')

    t11 = CustomerTarget(customer = weiqian, name = u'东莞市良云贸易有限公司', province_id = 19, city_id = 304)
    DBSession.flush()
    t11_c1 = CustomerContact(customer = weiqian, type = 'T', refer_id = t11.id, name = u'钟丽情', mobile = '13431268281', phone = '0769-22467285', email = None, address = u'南城区白马翠园街西二环巷8号', remark = u'东莞代理商')
    t11_c2 = CustomerContact(customer = weiqian, type = 'T', refer_id = t11.id, name = u'朱小毛', mobile = '13728275577', phone = '0769-76922467285', email = '729518726@qq.com', address = u'南城区白马翠园街西二环巷8号', remark = u'东莞代理商')

    t12 = CustomerTarget(customer = weiqian, name = u'厦门恒顺联商贸有限公司', province_id = 19, city_id = 288)
    DBSession.flush()
    t12_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t12.id, name = u'朱蔚', mobile = '18927843611', phone = None, email = '653009253@qq.com', address = u'白云区沙太北路大源南路自编33号', remark = u'广州代理商')

    t13 = CustomerTarget(customer = weiqian, name = u'广州市领隆贸易有限公司', province_id = 19, city_id = 288)
    DBSession.flush()
    t13_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t13.id, name = u'曹领', mobile = '15989152636', phone = '020-84265759', email = '653009253@qq.com', address = u'广州市白云区沙太北路大源南路自编33号', remark = u'广州代理商')

    t14 = CustomerTarget(customer = weiqian, name = u'广州沃奥贸易有限公司', province_id = 19, city_id = 288)
    DBSession.flush()
    t14_c = CustomerContact(customer = weiqian, type = 'T', refer_id = t14.id, name = u'林奇峰', mobile = '15989152636', phone = '020-81795981', email = None, address = u'白云区增槎路东旺市场南二排42档', remark = u'广州代理商')

    DBSession.add_all([
                       t1, t1_c, t2, t2_c, t3, t3_c, t4, t4_c, t5, t5_c, t6, t6_c1, t6_c2, t7, t7_c, t8, t8_c1, t8_c2, t9, t9_c1, t9_c2, t10, t10_c1, t10_c2,
                       t11, t11_c1, t11_c2, t12, t12_c, t13, t13_c, t14, t14_c
                       ])



def import_supplier(payment1):
    print "insert supplier"
    DBSession.add_all([
               Supplier(name = u'中深翔', display_name = u'中深翔', address = u'布吉丹竹头金鹏物流园A区A栋18-20号', mobile = '13600432849', contact_person = u'全总', remark = u'上海', payment = payment1),
               Supplier(name = u'深中联', display_name = u'深中联', address = u'布吉丹竹头金鹏物流园A栋5-6号', mobile = '13392826777,18902480211', contact_person = u'王总，丁小姐', remark = u'温州、台州、温岭、临海、黄岩', payment = payment1),
               Supplier(name = u'旺平达', display_name = u'旺平达', address = u'龙华明治大道华通源物流中心B2栋263-266号', mobile = '15099917300', contact_person = u'李飞章', remark = u'苏州、无锡、昆山、张家港、宜兴、常熟、太仓、吴江', payment = payment1),
               Supplier(name = u'顺福', display_name = u'顺福', address = u'丹竹头白泥坑宇达物流园3栋301-318号', phone = '89575677', mobile = '13316895558', contact_person = u'陈老板', remark = u'徐州、南通、淮安、盐城、连云港、启东', payment = payment1),
               Supplier(name = u'鑫金叶', display_name = u'鑫金叶', address = u'布吉李朗东西干道南岭大龙山物流园G栋1-3号', mobile = '13906667228', contact_person = u'金经理        ', remark = u'温州苍南', payment = payment1),
               Supplier(name = u'华发', display_name = u'华发', address = u'金鹏物流园B区9栋7-12号', mobile = '15999677737', contact_person = u' 陈老板', remark = u'南京、常州、扬州、泰州、镇江、靖江', payment = payment1),
               Supplier(name = u'京鹏', display_name = u'京鹏', address = u'华通源物流中心C4栋138-152号', mobile = '13066815788,13066815788', contact_person = u'老板娘           傅总', remark = u'杭州、上虞、湖州、德清、临安、丽水、桐乡、长兴、云南省', payment = payment1),
               Supplier(name = u'凯林瑞', display_name = u'凯林瑞', address = u'龙岗区丹竹头金鹏物流园B区D栋41-42号', phone = '0755-82432843', mobile = '', contact_person = u'杨总', remark = u'浙江嘉兴', payment = payment1),
               Supplier(name = u'海联', display_name = u'海联', address = u'华通源物流中心', mobile = '18688838882', contact_person = u'李老板', remark = u'宁波、义乌、绍兴、衢州、诸暨、金华、慈溪、余姚、舟山、奉化', payment = payment1),
               Supplier(name = u'荣晖', display_name = u'荣晖', address = u'金鹏A区B栋15-18号,40-42号', mobile = '13631528080', contact_person = u'胡总', remark = u'南昌、赣州、新余、吉安、九江、萍乡、宜春、鹰潭', payment = payment1),
               Supplier(name = u'深湘', display_name = u'深湘', address = u'长城货代市场83档', mobile = '13902485137', contact_person = u'丘总', remark = u'长沙、常德、衡阳、株洲、湘阴、岳阳、怀化、湘潭', payment = payment1),
               Supplier(name = u'澳跃', display_name = u'澳跃', address = u'金鹏', mobile = '13902311565', contact_person = u'肖总', remark = u'武汉、黄冈、黄石、荆州、咸宁、孝感、襄樊、恩施、十堰、襄阳', payment = payment1),
               Supplier(name = u'金鹏行', display_name = u'金鹏行', address = u'', mobile = '18926534999', contact_person = u'俞总', remark = u'合肥、淮南、黄山、桐城、芜湖、宣城、安庆、铜陵、涡阳、滁州、怀远', payment = payment1),
               Supplier(name = u'京鹏', display_name = u'京鹏', address = u'华通源物流中心C4栋138-152号', mobile = '13066815788', contact_person = u'傅小姐', remark = u'昆明、大理、曲靖、景洪', payment = payment1),
               Supplier(name = u'鑫辉', display_name = u'鑫辉', address = u'布吉丹平路闽鹏程货运市场11栋1-4号', mobile = '13925234059', contact_person = u'刘先生', remark = u'龙岩、三明', payment = payment1),
               Supplier(name = u'广运物流', display_name = u'广运物流', address = u'龙岗丹竹头闽鹏程货运市场5栋29-30号', mobile = '18923724600', contact_person = u'徐先生', remark = u'顺德', payment = payment1),
               Supplier(name = u'金华航', display_name = u'金华航', address = u'华通源物流园', phone = '0755-23022756', mobile = '', contact_person = u'刘先生', remark = u'中山', payment = payment1),
               Supplier(name = u'速速达', display_name = u'速速达', address = u'龙岗区布吉上李朗方鑫路22号速速达物流', phone = None, mobile = '13392831936', contact_person = u'王晓刚', remark = u'南宁、桂林、柳州、钦州', payment = payment1),
               Supplier(name = u'盛丰', display_name = u'盛丰', address = u'龙岗区南湾街道吉厦社区早禾坑工业区15号A栋', phone = None, mobile = '13798363667', contact_person = u'周总', remark = u'泉州、福州、莆田、福清', payment = payment1),
               Supplier(name = u'美泰', display_name = u'美泰', address = u'龙岗布吉大龙山物流园F栋10号美泰物流', phone = None, mobile = '18926795962', contact_person = u'毛主管', remark = u'广州', payment = payment1),
               Supplier(name = u'凯利', display_name = u'凯利', address = u'布吉单竹头金鹏物流园B区E栋1-5号 ', phone = '61217611,61217600', mobile = '', contact_person = u'熊小姐', remark = u'三亚、海口、琼海、万宁', payment = payment1),
               Supplier(name = u'骏兴顺', display_name = u'骏兴顺', address = u'龙华民治大道华通源物流中心C1栋58-60号', phone = None, mobile = '15914055308', contact_person = u'曾经理', remark = u'贵阳、金沙、安顺', payment = payment1),
               Supplier(name = u'澳跃', display_name = u'澳跃', address = u'金鹏A区栋13-15号', phone = None, mobile = '18923411132', contact_person = u'李峰', remark = u'漳州', payment = payment1),
               Supplier(name = u'勤威', display_name = u'勤威', address = u'金鹏B区C栋33号', phone = None, mobile = '13728866595', contact_person = u'石总', remark = u'厦门', payment = payment1),
               ])
    DBSession.commit()




if __name__ == '__main__':
    init()

#    import_kinlong_target(None)

#    insert_diqu()

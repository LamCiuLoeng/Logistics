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
from sys2do.model.master import CustomerProfile, Customer, Item, Vendor, \
    ItemUnit, Warehouse
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    try:
        print "create tables"
        metadata.drop_all(engine)
        metadata.create_all(engine)

        print "insert default value"
        #add the default value here

        DBSession.add(User(name = 'admin', email = 'admin@test.com', password = 'admin', first_name = 'Admin', last_name = 'Test'))
        DBSession.add(User(name = 'customer', email = 'customer@test.com', password = 'customer', first_name = 'Customer', last_name = 'Test'))

#        sqlfile = file('AllCityData.sql')
#        for index, sql in enumerate(sqlfile):
#            if sql and not sql.startswith('--'):
#                engine.execute(sql)
#                print '------', index
#        sqlfile.close()

        #add test customer
        pfTest = CustomerProfile(name = 'PF_TEST')
        c1 = Customer(name = 'CUSTOMER COMPANY 1', address = 'CUSTOMER ADDRESS 1', phone = '12134567' , contact_person = 'CUSTOMER PERSON 1', prifile = pfTest)
        c2 = Customer(name = 'CUSTOMER COMPANY 2', address = 'CUSTOMER ADDRESS 2', phone = '12134567' , contact_person = 'CUSTOMER PERSON 2', prifile = pfTest)
        v1 = Vendor(name = 'VENDOR 1', address = 'VENDOR ADDRESS 1', phone = '1122334455', contact_person = 'VENDOR PERSON 1', prifile = pfTest)
        v2 = Vendor(name = 'VENDOR 2', address = 'VENDOR ADDRESS 2', phone = '1122334455', contact_person = 'VENDOR PERSON 2', prifile = pfTest)
        item1 = Item(name = 'ITEM 1', prifile = pfTest)
        item2 = Item(name = 'ITEM 2', prifile = pfTest)
        item3 = Item(name = 'ITEM 3', prifile = pfTest)

        DBSession.add_all([pfTest, c1, c2, v1, v2, item1, item2, item3])
        for unit in [u'米', u'分米', u'厘米', u'吨', u'千克', u'克', u'箱', u'瓶', u'支', u'打', ]:
            DBSession.add(ItemUnit(name = unit, prifile = pfTest))

        DBSession.add(Warehouse(name = "WAREHOUSE 1", address = "Address 1", manager = "MANAGER 1"))
        DBSession.add(Warehouse(name = "WAREHOUSE 2", address = "Address 2", manager = "MANAGER 2"))

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()

if __name__ == '__main__':
    init()

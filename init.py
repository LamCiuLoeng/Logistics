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
reload(sys)
sys.setdefaultencoding('utf8')

def init():
    try:
        print "create tables"
        metadata.drop_all(engine)
        metadata.create_all(engine)

        print "insert default value"
        #add the default value here

        DBSession.add(User(name = 'admin', email = 'admin@text.com', password = 'admin', first_name = 'Admin', last_name = 'Test'))

        DBSession.commit()
        print "finish init!"
    except:
        traceback.print_exc()
        DBSession.rollback()

if __name__ == '__main__':
    init()

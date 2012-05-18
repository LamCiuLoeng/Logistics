# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2012-5-8
#  @author: CL.Lam
#  Description:
###########################################
'''
import traceback
#import sys2do.model.logic as logic
import sys
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Unicode, Text, Date
import datetime

reload(sys)
sys.setdefaultencoding('utf8')


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URI = "mysql://root:admin@192.168.21.157/sfhl"

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo = False)
maker = sessionmaker(autoflush = True, autocommit = False)
DBSession = scoped_session(maker)
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
DBSession.configure(bind = engine)


class OrderInfo(DeclarativeBase):
    __tablename__ = 'ecgol_order_info'

    id = Column(Integer, autoincrement = True, primary_key = True)
    create_time_old = Column(Unicode(20))
    create_time = Column(Date)
    no = Column(Unicode(100))
    target = Column(Unicode(1000))
    receiver = Column(Unicode(100))
    qty = Column(Unicode(10))
    weight = Column(Unicode(10))
    pickup_tel = Column(Unicode(100))
    region = Column(Unicode(10))
    transfter = Column(Unicode(10))
    pickup_no = Column(Unicode(100))
    sendout_time_old = Column(Unicode(20))
    sendout_time = Column(Date)
    first_trace = Column(Unicode(100))
    second_trace = Column(Unicode(100))
    require_arrival_old = Column(Unicode(20))
    require_arrival = Column(Date)
    actual_arrival_old = Column(Unicode(20))
    actual_arrival = Column(Date)
    kpi = Column(Unicode(100))
    notify_day_qty = Column(Unicode(100))
    first_pickup = Column(Unicode(100))
    second_pickup = Column(Unicode(100))
    third_pickup = Column(Unicode(100))
    left_pickup = Column(Unicode(100))
    left_price = Column(Unicode(100))
    left_charge = Column(Unicode(100))
    remark = Column(Text)
    exception = Column(Text)
    overdue = Column(Unicode(10))
    signed = Column(Unicode(10))
    signed_contact = Column(Unicode(100))
    signed_time = Column(Unicode(100))




def create_tables():
    print "create tables begin"
    metadata.drop_all(engine)
    metadata.create_all(engine)
    DBSession.commit()
    print "create tables end"


def adjust_date():
    _a = lambda v: datetime.date(1899, 12, 30) + datetime.timedelta(days = int(v))

    for row in DBSession.query(OrderInfo):
        row.no = row.no.replace('坚朗', '')
        if row.create_time_old : row.create_time = _a(row.create_time_old)
        if row.sendout_time_old :row.sendout_time = _a(row.sendout_time_old)
        if row.require_arrival_old : row.require_arrival = _a(row.require_arrival_old)
        if row.actual_arrival_old : row.actual_arrival = _a(row.actual_arrival_old)
    DBSession.commit()
    print "adjust finished"

if __name__ == "__main__":
    args = filter(lambda v : v != __file__, sys.argv)
    if "h" in args:
        print "h -- help"
        print "c -- create table"
        print "a -- adjust"
    elif "c" in args:
        create_tables()
    elif "a" in args:
        adjust_date()
    else:
        print "No methos"


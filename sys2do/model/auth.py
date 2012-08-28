# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''

import traceback
from datetime import datetime as dt, date
import os
import sys
from sqlalchemy.sql.expression import desc, and_
from sys2do.constant import SYSTEM_DATETIME_FORMAT, SYSTEM_DATE_FORMAT
from sqlalchemy.ext.declarative import declared_attr




try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')



from flask import session
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Date, Text
from sqlalchemy.orm import relation, synonym, backref
from sys2do.model import DeclarativeBase, metadata, DBSession

__all__ = ['User', 'Group', 'Permission', 'SysMixin', 'CRUDMixin', ]

def getUserID():
    try:
        return session['user_profile']['id']
    except:
        return None


class SysMixin(object):
    create_time = Column(DateTime, default = dt.now)
    create_by_id = Column(Integer, default = getUserID)
    update_time = Column(DateTime, default = dt.now, onupdate = dt.now)
    update_by_id = Column(Integer, default = getUserID, onupdate = getUserID)
    _attachment = Column('attachment', Text)
    active = Column(Integer, default = 0) # 0 is active ,1 is inactive


    @property
    def create_by(self):
        try:
            return DBSession.query(User).get(self.create_by_id)
        except:
            return None

    @property
    def update_by(self):
        try:
            return DBSession.query(User).get(self.update_by_id)
        except:
            return None


    def compare(self, old_obj, new_obj):
        old_keys = old_obj.keys()
        new_keys = new_obj.keys()
        result = {
                  "new" : [],
                  "update" : [],
                  "delete" : [],
                  }

        for key in list(set(old_keys).intersection(set(new_keys))):
            old_val = old_obj[key][0]
            new_val = new_obj[key][0]

            if old_val != new_val:
                result['update'].append((old_obj[key][1], old_obj[key][0], new_obj[key][0]))

        for key in list(set(old_obj).difference(set(new_obj))):
            result['delete'].append((old_obj[key][1], old_obj[key][0], None))

        for key in list(set(new_obj).difference(set(old_obj))):
            result['new'].append((old_obj[key][1], None, new_obj[key][0]))
        return result


    def insert_system_logs(self, comare_result):
        from sys2do.model.system import SystemLog
        from sys2do.util.common import _error
        try:
            _remark = [u"[%s]'%s' 修改为 '%s'" % (name, ov, nv) for (name, ov, nv) in comare_result['update']]
            DBSession.add(SystemLog(
                                    type = self.__class__.__name__,
                                    ref_id = self.id,
                                    remark = u"%s 修改该记录。%s" % (session['user_profile']['name'], ";".join(_remark))
                                    ))
            DBSession.commit()
        except:
            DBSession.rollback()
            _error(traceback.print_exc())


    @property
    def system_logs(self):
        from sys2do.model.system import SystemLog
        return DBSession.query(SystemLog).filter(and_(SystemLog.type == self.__class__.__name__, SystemLog.ref_id == self.id)).order_by(desc(SystemLog.create_time))



    def serialize(self, fields = []):
        from sys2do.util.common import _info
        result = {}
        m = self.__mapper__.columns

        for cname in fields:
            if cname not in m.keys(): continue
            colClz = m[cname]
            if isinstance(colClz, Column):
                v = getattr(self, cname)

                if v is None: v = u'' #the value is None
                elif m[cname].foreign_keys : #it's a foreign key
                    tmp_name = cname.replace("_id", '')
                    try:
                        v = unicode(getattr(self, tmp_name))
                    except:
                        _info(traceback.print_exc())
                        v = u''
                elif isinstance(v, dt) : v = dt.strftime(SYSTEM_DATETIME_FORMAT)
                elif isinstance(v, date) : v = dt.strftime(SYSTEM_DATE_FORMAT)
                elif isinstance(v, (int, float)) : v = u'%s' % v
                else: v = unicode(v)

                result[cname] = (v, colClz.doc or cname)
        _info(result)
        return result


    def _get_attachment(self):
        try:
            from sys2do.model.system import UploadFile
            return DBSession.query(UploadFile).filter(and_(UploadFile.active == 0, UploadFile.id.in_(self._attachment.split("|")))).order_by(UploadFile.id)
        except:
            return []


    def _set_attachment(self, v):
        ids = None
        if v :
            if type(v) == list:
                ids = "|".join(map(unicode, v))
            elif isinstance(v, basestring):
                ids = v
        self._attachment = ids


    @declared_attr
    def attachment(self):
        return synonym('_attachment', descriptor = property(self._get_attachment, self._set_attachment))



class CRUDMixin(object):

#    __fields = []

    @classmethod
    def get(clz, id):
        try:
            return DBSession.query(clz).get(id)
        except:
            return None

    @classmethod
    def all(clz, order_by = "name"):
        return DBSession.query(clz).filter(clz.active == 0).order_by(getattr(clz, order_by)).all()

    @classmethod
    def _get_fields(clz):
        return []

    def populate(self):
        result = {
                  'id' : self.id
                  }
        for f in self._get_fields():
            result[f] = unicode(getattr(self, f) or '')
        return result


    @classmethod
    def saveAsNew(clz, v):
        params = {}
        for f in clz._get_fields():
            params[f] = v.get(f, None) or None
        obj = clz(**params)
        DBSession.add(obj)
        return obj


    def saveAsUpdate(self, v):
        for f in self._get_fields():
            setattr(self, f, v.get(f, None) or None)
        return self





#{ Association tables


# This is the association table for the many-to-many relationship between
# groups and permissions. This is required by repoze.what.
group_permission_table = Table('system_group_permission', metadata,
    Column('group_id', Integer, ForeignKey('system_group.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    Column('permission_id', Integer, ForeignKey('system_permission.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True)
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships. It's required by repoze.what.
user_group_table = Table('system_user_group', metadata,
    Column('user_id', Integer, ForeignKey('system_user.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    Column('group_id', Integer, ForeignKey('system_group.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True)
)


#{ The auth* model itself


class Group(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'system_group'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    display_name = Column(Text)
    desc = Column(Text)
    type = Column(Integer, default = 1) #0 is for system use, 1 is for normal use
    users = relation('User', secondary = user_group_table, backref = 'groups')

    def __repr__(self): return self.display_name or self.name

    def __str__(self): return self.display_name or self.name

    def __unicode__(self): return self.display_name or self.name


    def populate(self):
        return {
                "id" : self.id,
                "name" :self.name,
                "display_name" : self.display_name,
                "desc" : self.desc,
                "type" : self.type,
                }


    @classmethod
    def saveAsNew(clz, v):
        params = {
                  "name" : v.get("name", None) or None,
                  "desc" : v.get("desc", None) or None,
                  "display_name" : v.get("display_name", None) or None
                  }
        group = clz(**params)
        DBSession.add(group)
        return group


    def saveAsUpdate(self, v):
        self.name = v.get("name", None) or None
        self.desc = v.get("desc", None) or None
        self.display_name = v.get("display_name", None) or None
        return self

# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class User(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'system_user'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    email = Column(Text)
    _password = Column('password', Text)
    phone = Column(Text)
    mobile = Column(Text)
    image_url = Column(Text)
    last_login = Column(DateTime, default = dt.now)

    def __repr__(self): return self.name
    def __str__(self): return self.name
    def __unicode__(self): return self.name


    @property
    def permissions(self):
        """Return a set of strings for the permissions granted."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter(cls.email_address == email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter(cls.name == username).first()
#
#    def validate_password(self, password):
#        return self.password == password


    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        # Make sure the hashed password is an UTF-8 object at the end of the
        # process because SQLAlchemy _wants_ a unicode object for Unicode
        # columns
        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self._password = hashed_password

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor = property(_get_password, _set_password))

    #}

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()


    @classmethod
    def identify(cls, value):
        return DBSession.query(cls).filter(cls.user_name.match(value)).one()

    def populate(self):
        return {
                'id' : self.id,
                'name' : self.name,
                'password' : self.password,
                'email' : self.email,
                'image_url' : self.image_url,
                'phone' : self.phone,
#                'birthday' : self.birthday,
                }


    @classmethod
    def saveAsNew(clz, v):
        params = {}
        for f in ['name', 'password', 'email', 'image_url', 'phone', 'mobile', ]:
            params[f] = v.get(f, None) or None
        one = clz(**params)
        DBSession.add(one)
        return one

    def saveAsUpdate(self, v):
        for f in ['name', 'password', 'email', 'image_url', 'phone', 'mobile']:
            setattr(self, f, v.get(f, None) or None)
        return self


    @property
    def customer_profile(self):
        from sys2do.model.master import CustomerProfile
        return DBSession.query(CustomerProfile).get(self.customer_profile_id)


class Permission(DeclarativeBase, SysMixin, CRUDMixin):
    __tablename__ = 'system_permission'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Text, unique = True, nullable = False)
    desc = Column(Text)
    groups = relation(Group, secondary = group_permission_table, backref = 'permissions')

    def __repr__(self): return self.name

    def __str__(self): return self.name

    def __unicode__(self): return self.name


    def populate(self):
        return {"id" : self.id , "name" : self.name, 'desc' : self.desc}

    @classmethod
    def saveAsNew(clz, v):
        params = {
                  'name' : v.get('name', None) or None,
                  'desc' : v.get('desc', None) or None,
                  }
        one = clz(**params)
        DBSession.add(one)
        return one

    def saveAsUpdate(self, v):
        self.name = v.get("name", None) or None
        self.desc = v.get("desc", None) or None
        return self

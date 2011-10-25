# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''

from datetime import datetime as dt
import sys
try:
    from hashlib import sha1
except ImportError:
    sys.exit('ImportError: No module named hashlib\n'
             'If you are on python2.4 this library is not part of python. '
             'Please install it. Example: easy_install hashlib')

from flask import session
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Date
from sqlalchemy.orm import relation
from sys2do.model import DeclarativeBase, metadata, DBSession

__all__ = ['User', 'Group', 'Permission', 'SysMixin']

def getUserID():
    return session['user_profile']['id']


class SysMixin(object):
    create_time = Column(DateTime, default = dt.now)
    create_by_id = Column(Integer, default = getUserID)
    update_time = Column(DateTime, default = dt.now, onupdate = dt.now)
    update_by_id = Column(Integer, default = getUserID, onupdate = getUserID)
    active = Column(Integer, default = 0) # 0 is active ,1 is inactive

    @property
    def create_by(self):
        return DBSession.query(User).get(self.create_by_id)

    @property
    def update_by(self):
        return DBSession.query(User).get(self.update_by_id)


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


class Group(DeclarativeBase, SysMixin):
    __tablename__ = 'system_group'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100), unique = True, nullable = False)
    display_name = Column(Unicode(100))
    desc = Column(Unicode(1000))
    users = relation('User', secondary = user_group_table, backref = 'groups')

    def __repr__(self):
        return self.display_name or self.name

    def __unicode__(self):
        return self.display_name or self.name


# The 'info' argument we're passing to the email_address and password columns
# contain metadata that Rum (http://python-rum.org/) can use generate an
# admin interface for your models.
class User(DeclarativeBase, SysMixin):
    __tablename__ = 'system_user'

    id = Column(Integer, autoincrement = True, primary_key = True)
    email = Column(Unicode(100), unique = True, nullable = False)
    password = Column(Unicode(50))
    first_name = Column(Unicode(50))
    last_name = Column(Unicode(50))
    phone = Column(Unicode(50))
    birthday = Column(Date, default = None)
    image_url = Column(Unicode(100))

    def __repr__(self): return "%s %s" % (self.first_name, self.last_name)

    def __unicode__(self): return "%s %s" % (self.first_name, self.last_name)

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
        return DBSession.query(cls).filter(cls.user_name == username).first()

    def validate_password(self, password):
        return self.password == password

    @classmethod
    def identify(cls, value):
        return DBSession.query(cls).filter(cls.user_name.match(value)).one()

    def populate(self):
        return {
                'id' : self.id,
                'email' : self.email,
                'first_name' : self.first_name,
                'last_name' : self.last_name,
                'image_url' : self.image_url,
                'phone' : self.phone,
                'name' : unicode(self)
                }


class Permission(DeclarativeBase, SysMixin):
    __tablename__ = 'system_permission'

    id = Column(Integer, autoincrement = True, primary_key = True)
    name = Column(Unicode(100), unique = True, nullable = False)
    desc = Column(Unicode(1000))
    groups = relation(Group, secondary = group_permission_table, backref = 'permissions')

    def __repr__(self): return self.name

    def __unicode__(self): return self.name

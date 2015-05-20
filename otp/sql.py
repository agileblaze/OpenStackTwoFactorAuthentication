import base64
from datetime import datetime, timedelta
import hashlib
import hmac
import struct
import time
import uuid

from oslo_log import log
from oslo_config import cfg

from keystone import exception
from keystone.common import sql as keystone_sql
from keystone.identity.backends.sql import User
import sqlalchemy as sql
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func


from keystone.auth.plugins.otp import utils
from keystone.auth.plugins.otp import config

LOG = log.getLogger(__name__)
CONF = cfg.CONF

engine = create_engine(CONF.otp_options.connection)
session = sessionmaker(bind = engine)()

Column = sql.Column
String = sql.String
ForeignKey = sql.ForeignKey
DateTime = sql.DateTime
Boolean = sql.Boolean
Integer = sql.Integer

#"""
#Created the Tables



class UserOneTimePassword(keystone_sql.ModelBase):
    __tablename__  = 'user_otp'
    
    id = Column(String(64), primary_key = True)
    user_id = Column(String(64), ForeignKey(User.id))
    phone_number = Column(String(15), nullable = False)
    secret = Column(String(64), nullable = False)
    enabled = Column(Boolean, nullable = False)
    
    def __init__(self, user_id, phone_number, enabled = True):
        self.user_id = user_id
        self.phone_number = phone_number
        self.enabled = enabled
        self.id = UserOneTimePassword.generate_unique_pk()
        self.secret = UserOneTimePassword.generate_unique_secret()

    def __repr__(self):
        return "<UserOneTimePassword('%s', '%s', '%s')>" % (self.user_id, self.phone_number, self.secret)
    
    @classmethod    
    def generate_unique_pk(cls):
        return generate_unique_value(cls, "id")
        
    @classmethod    
    def generate_unique_secret(cls):
        return generate_unique_value(cls, "secret")
        
    
class OneTimePasswordFailures(keystone_sql.ModelBase):
    __tablename__  = 'otp_failures'
    
    id = Column(String(64), primary_key = True)
    user_id = Column(String(64), ForeignKey(User.id))
    successive_failures = Column(Integer, nullable = False)
    last_failure_timestamp = Column(DateTime)
    
    def __init__(self, user_id, successive_failures):
        self.id  = OneTimePasswordFailures.generate_unique_pk()
        self.user_id = user_id
        self.successive_failures = successive_failures
        self.last_failure_timestamp = utils.get_current_mysql_gmtime()
        
    def __repr__(self):
        return "<OneTimePasswordFailures('%s', '%d', '%s')>" % (self.user_id, self.successive_failures, self.last_failure_timestamp)
    
    @classmethod    
    def generate_unique_pk(cls):
        return generate_unique_value(cls, "id")
    
def get_otp_auth_status(user_id):
    """Get the status of the one-time password authentication for a user
    
    Returns the object of OneTimePasswordFailures for the user. If there is no entry
    for the user returns None, means no one-time password failure is recorded for the
    user
    """
    try:
        time_now  = datetime.fromtimestamp(utils.get_current_unix_time())

        count = session.query(OneTimePasswordFailures).filter(
            and_(OneTimePasswordFailures.user_id == user_id,
                 OneTimePasswordFailures.last_failure_timestamp > time_now - timedelta(hours=24) )).count()
        
        last_failure_timestamp = session.query(func.max(OneTimePasswordFailures.last_failure_timestamp)).filter(
            OneTimePasswordFailures.user_id == user_id).one()
        
        return {'count':int(count) , 'last_failure_timestamp':last_failure_timestamp[0]}
        #return session.query(OneTimePasswordFailures).filter(OneTimePasswordFailures.user_id == user_id).one()
    except Exception as no_failure_info_exists:
        LOG.info(no_failure_info_exists.message)
        return None

def generate_secrete_for_allusers():
    """Generate saves phone number and secret for each user in the 'user' table
    
    This is interactive and asks for phone numbers for each user
    """
    for row in session.query(User.id, User.name).all():
        phone_no = raw_input('What is the phone number of user %s ? : ' %(row.name))
        add_phone_number(row.id, phone_no)
    
def add_phone_number(user_id, phone_number):
    user_otp_info = UserOneTimePassword(user_id, phone_number)
    session.add(user_otp_info)
    session.commit()
    
def get_secret(user_id):
    """Get secret stored for a user for the generation of one-time password
    
    """
    print user_id
    row = session.query(UserOneTimePassword.secret).filter(UserOneTimePassword.user_id == user_id).one()
    return row.secret

def generate_unique_value(model_class, attribute = 'id'):
    """Returns a unique value for an attribute of a table
    
    This is used to generate unique id for tables, and also used to generate unique secret for
    each user
    """
    new_value = utils.generate_uuid4_string()
    try:
        session.query(model_class).filter(getattr(model_class, attribute, 'id') == new_value).one()
        return generate_unique_value(model_class, attribute)
    except AttributeError as attribute_not_found:
        raise AttributeError
    except Exception as value_not_exists:
        return new_value



def update_otp_auth_status(user_id, success = True):
    """Used to update the authentication status for a user
    
    After performing the one-time password authentication depends on
    whether it was success or failure we need to clear or update/add
    failure status information to the backend
    
    :param user_id: id of the user trying to autheticate
    :param success: whether the authenication succeeded
    """
    if not success:
        try:
            #failure_status = session.query(OneTimePasswordFailures).filter(OneTimePasswordFailures.user_id == user_id).one()
            #update one time password failure data into database
            #failure_status.successive_failures = failure_status.successive_failures + 1
            #failure_status.last_failure_timestamp = utils.get_current_mysql_gmtime()
            #session.add(failure_status)
            #session.commit()
            
            LOG.info("failure data pushed")
            
            new_failure_info = OneTimePasswordFailures(user_id, 1)
            session.add(new_failure_info)
            session.commit()
             
        except AttributeError as attribute_missing:
            LOG.exception(attribute_missing.message)
        except Exception as no_user_info:
            LOG.exception(no_user_info.message)
            
            #add one time password failure data into database
            #new_failure_info = OneTimePasswordFailures(user_id, 1)
            #session.add(new_failure_info)
            #session.commit()
    else:
        try:
            LOG.info("failure data deleted")
            #failure_status = session.query(OneTimePasswordFailures).filter(OneTimePasswordFailures.user_id == user_id).one()
            session.query(OneTimePasswordFailures).filter(OneTimePasswordFailures.user_id == user_id).delete()
            #session.delete(failure_status)
            session.commit()
        except AttributeError as attribute_missing:
            LOG.exception(attribute_missing.message)
        except Exception as no_user_info:
            LOG.exception(no_user_info.message)
            
            
def authenticate( user_id, one_time_password):
    """Authenticate the one-time password received for the user
    
    """
    utils.validate_totp(get_secret(user_id), one_time_password)            
 
def generate_otp_for_user(user_id):
    """Generate one-time password for a user.
    
    """
    secret = get_secret(user_id)
    return utils.generate_totp(secret)

def get_phone_number(user_id):
    """Returns the phone number of a user
    
    Used to send the one-time password to the user
    """
    row = session.query(UserOneTimePassword.phone_number).filter(UserOneTimePassword.user_id == user_id).one()
    return row.phone_number
#"""    


#generate_secrete_for_allusers()

"""
#Drop the tables

tables = ['user_otp', 'otp_failures', 'users', ]

meta = sql.MetaData()
meta.bind = engine


for t in tables:
    table = sql.Table(t, meta, autoload=True)
    table.drop(engine, checkfirst=True)
"""

    
    
if __name__ == '__main__':
    try:
        keystone_sql.ModelBase.metadata.create_all(engine)
        generate_secrete_for_allusers()
    except Exception as exception_db_create:
        print "Exception in creating db"
        print exception_db_create.message
        LOG.warning(exception_db_create.message)



    





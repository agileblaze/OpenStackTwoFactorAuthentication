# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import datetime
import json
import operator
import uuid

from keystoneclient.common import cms
import mock
from oslo_utils import timeutils
import six
from testtools import testcase
from oslo_config import cfg

from sqlalchemy.orm import sessionmaker


from keystone.auth import controllers as auth_controllers
from keystone.common import dependency
from keystone import auth
from keystone import resource

from keystone.tests import unit as tests
from keystone.tests.unit.ksfixtures import database
from keystone.tests.unit import test_v3
from keystone.tests.unit import test_v3_auth
from keystone.tests.unit import default_fixtures

from keystone.auth.plugins.otp import utils
from keystone.auth.plugins.otp import config
from keystone.auth.plugins.otp import sql


from testtools import TestCase

from webtest import TestApp
from webtest import AppError


app = TestApp('http://*:35357')
test_user_id = 'd5072ef18e844852810150a217a3d496'

class TestOtpAuthInfo(TestCase):
    """ This test class uses the ruuning keystone WSGI application in the local system
    
    It uses live running system, not using any virtual environments
   
    Before running this tests you have to do the following
   
    1. Create a user "admin" with domain "default"
    
    In this test file change the attribute  "test_user_id" to the id of the user
    
    
    """
    
    def setUp(self):
        super(TestOtpAuthInfo, self).setUp()

    def build_authentication_request(self, user_id=None,
                                     username=None, user_domain_id=None,
                                     user_domain_name=None, password=None,
                                     password_otp=None,
                                     one_time_password = None, **kwargs):
        """Build auth dictionary.

        It will create an auth dictionary based on all the arguments
        that it receives.
        """
        auth_data = {}
        auth_data['identity'] = {'methods': []}

        if password:
            auth_data['identity']['methods'].append('password')
            auth_data['identity']['password'] = self.build_password_auth(
                user_id, username, user_domain_id, user_domain_name, password)
        
        if password_otp:
            auth_data['identity']['methods'].append('password_otp')
            auth_data['identity']['password_otp'] = self.build_password_auth(
                user_id, username, user_domain_id, user_domain_name, password_otp)
            
        if one_time_password:
            auth_data['identity']['methods'].append('otp')
            auth_data['identity']['otp'] = self.build_password_auth(
                user_id, username, user_domain_id, user_domain_name, one_time_password)

        if kwargs:
            auth_data['scope'] = self.build_auth_scope(**kwargs)
        return {'auth': auth_data}
    
    
    def test_valid_otp(self):
      
        print "Running correct OTP Test \n"

        otp = utils.generate_totp(sql.get_secret(test_user_id))
        auth_data = self.build_authentication_request(
            username='admin',
            user_domain_id='default',
            password='password',
            one_time_password=str(otp))
        
        auth_data = json.dumps(auth_data)
        return self.new_post(url = '/v3/auth/tokens', body=auth_data, expected_status=201)
    
    def test_invalid_otp(self):
      
        print "Running invalid OTP Test \n"
        
        otp = utils.generate_totp(sql.get_secret(test_user_id))
        otp = otp - 1
        
        auth_data = self.build_authentication_request(
            username='admin',
            user_domain_id='default',
            password='password',
            one_time_password=str(otp))
        
        auth_data = json.dumps(auth_data)
        return self.new_post(url = '/v3/auth/tokens', body=auth_data, expected_status=201)
    
    def test_expired_otp(self):
        
        print "Running expired OTP Test \n"
      
        otp = utils.generate_totp(sql.get_secret(test_user_id), position = 3)
        
        auth_data = self.build_authentication_request(
            username='admin',
            user_domain_id='default',
            password='password',
            one_time_password=str(otp))
        
        auth_data = json.dumps(auth_data)
        
        return self.new_post('/v3/auth/tokens', body=auth_data, expected_status=401)
     
    def test_blocked_user(self):
      
        print "Running blocked user Test \n"
      
        auth_data = self.build_authentication_request(
            username='admin',
            user_domain_id='default',
            password_otp='password')
        
        auth_data = json.dumps(auth_data)
        
        return self.new_post('/v3/auth/tokens', body=auth_data, expected_status=401)
         
         
    def test_send_sms(self):
      
        print "Running send SMS Test \n"
      
        auth_data = self.build_authentication_request(
            username='admin',
            user_domain_id='default',
            password_otp='password')
        
        auth_data = json.dumps(auth_data)
        return self.new_post('/v3/auth/tokens', body=auth_data, expected_status=201)

    
    def new_post(self, url=None, body=None, expected_status=None):
      try:
         response = app.post(url, body, content_type='application/json')
         print response
      except AppError as e:
         print e.message
      
      
    def build_password_auth(self, user_id=None, username=None,
                            user_domain_id=None, user_domain_name=None,
                            password=None):
        password_data = {'user': {}}
        if user_id:
            password_data['user']['id'] = user_id
        else:
            password_data['user']['name'] = username
            if user_domain_id or user_domain_name:
                password_data['user']['domain'] = {}
                if user_domain_id:
                    password_data['user']['domain']['id'] = user_domain_id
                else:
                    password_data['user']['domain']['name'] = user_domain_name
        password_data['user']['password'] = password
        return password_data
    
        
        
        
        
        
        
        

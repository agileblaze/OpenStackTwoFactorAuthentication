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

from keystone import auth
from keystone.tests.unit import test_v3
from keystone.tests.unit import test_v3_auth
from keystone.tests.unit import default_fixtures

from keystone.auth.plugins.otp import utils
from keystone.auth.plugins.otp import config
from keystone.auth.plugins.otp import sql


from  oslo_config import cfg

CONF = cfg.CONF


class TestOtpAuthInfo(test_v3.RestfulTestCase):
    
    def setUp(self):
    
        #super(TestOtpAuthInfo, self).setUp()
    #    auth.controllers.load_auth_methods()
    #    #self.load_fixtures(default_fixtures)
    #    sql.add_phone_number(self.user_id, CONF.otp_options.twilio_from_phone)
        

      
       

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
                user_id, username, user_domain_id, user_domain_name, password)
            
        if one_time_password:
            auth_data['identity']['methods'].append('otp')
            auth_data['identity']['otp'] = self.build_password_auth(
                user_id, username, user_domain_id, user_domain_name, password)

        if kwargs:
            auth_data['scope'] = self.build_auth_scope(**kwargs)
        return {'auth': auth_data}
    
    
    def test_valid_otp(self):
        otp = utils.generate_totp(sql.get_secret(self.user['id']))
        
        auth_data = self.build_authentication_request(
            username=self.user['name'],
            user_domain_id=self.domain_id,
            password=self.user['password'],
            one_time_password=otp)
        
        return self.post('/auth/tokens', body=auth_data, expected_status=201)
    
    def test_invalid_otp(self):
        otp = utils.generate_totp(sql.get_secret(self.user_id))
        otp = otp - 1
        
        auth_data = self.build_authentication_request(
            username=self.user['name'],
            user_domain_id=self.domain_id,
            password=self.user['password'],
            one_time_password=otp)
        
        return self.post('/auth/tokens', body=auth_data, expected_status=401)
    
    def test_expired_otp(self):
        otp = utils.generate_totp(sql.get_secret(self.user_id), positions_behind = 3)
        
        auth_data = self.build_authentication_request(
            username=self.user['name'],
            user_domain_id=self.domain_id,
            password=self.user['password'],
            one_time_password=otp)
        
        return self.post('/auth/tokens', body=auth_data, expected_status=401)
    
    def test_blocked_user(self):
        otp = utils.generate_totp(sql.get_secret(self.user_id))
        
        auth_data = self.build_authentication_request(
            username=self.user['name'],
            user_domain_id=self.domain_id,
            password_otp=self.user['password'])
        
        return self.post('/auth/tokens', body=auth_data, expected_status=401)
        
        
    def test_send_sms(self):
        otp = utils.generate_totp(sql.get_secret(self.user_id))
        
        auth_data = self.build_authentication_request(
            username=self.user['name'],
            user_domain_id=self.domain_id,
            password_otp=self.user['password'])
        
        return self.post('/auth/tokens', body=auth_data, expected_status=201)
        
        
        
    
        
        
        
        
        
        
        

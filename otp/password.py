# Copyright 2013 OpenStack Foundation
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

import calendar
import time

from oslo_log import log

from keystone.auth.plugins.core import UserAuthInfo
from keystone.common import dependency
from keystone import auth
from keystone import exception
from keystone.i18n import _

from keystone.auth.plugins.otp import exceptions
from keystone.auth.plugins.otp import sql
from keystone.auth.plugins.otp import twilio_api


METHOD_NAME = 'password_otp'

LOG = log.getLogger(__name__)

class UserOtpAuthInfo(object):
    @staticmethod
    def create(user_id):
        otp_auth_info = UserOtpAuthInfo(user_id)
        return otp_auth_info

    def __init__(self, user_id):
        self.user_id = user_id
        
    def validate(self):
        failures  = sql.get_otp_auth_status(self.user_id)
        
        LOG.info("failures : " + str(failures))
        
        if failures:
            if failures['count'] > 2:
                time_blocked_from = failures['last_failure_timestamp']
                blocked_from_epoch = calendar.timegm(time.strptime(str(time_blocked_from), '%Y-%m-%d %H:%M:%S'))
                blocked_period_seonds = self.epoch_time_difference(time.time(), blocked_from_epoch)
                if self.is_account_blocked(blocked_period_seonds):
                    blocked_period = self.seconds_to_hrs_mins_secs(86400 - blocked_period_seonds)
                    error_message = "Your accound is blocked for 24 hours, wait %d hours %d minutes %d seconds to get the account reactivated" % (blocked_period[0], blocked_period[1], blocked_period[2])
                    raise exceptions.Blocked(error_message)
            
    def epoch_time_difference(self, later_time, former_time):
        return later_time - former_time
    
    def seconds_to_hrs_mins_secs(self, seconds):
        minutes , seconds  = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return hours, minutes, seconds
    
    def is_account_blocked(self,blocked_period_seconds):
        if blocked_period_seconds >= 86400 :
            return False
        else:
            return True
        

@dependency.requires('identity_api')
class Password(auth.AuthMethodHandler):

    method = METHOD_NAME

    def authenticate(self, context, auth_payload, user_context):
        """Try to authenticate against the identity backend."""
        user_info = UserAuthInfo.create(auth_payload, self.method)
        otp_auth_info = UserOtpAuthInfo(user_info.user_id)

        try:
            self.identity_api.authenticate(
                context,
                user_id=user_info.user_id,
                password=user_info.password)
            
            otp_auth_info.validate()
            twilio_api.send_otp(user_info.user_id)
            
        except AssertionError:
            msg = _('Invalid username or password')
            raise exception.Unauthorized(msg)
        except exceptions.Blocked as user_blocked_exception:
            raise exception.Unauthorized(user_blocked_exception.message)

        if 'user_id' not in user_context:
            user_context['user_id'] = user_info.user_id

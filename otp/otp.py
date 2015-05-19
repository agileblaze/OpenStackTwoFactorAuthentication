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


from keystone.auth.plugins.password import UserAuthInfo
from keystone.common import dependency
from keystone import auth
from keystone import exception
from keystone.openstack.common.gettextutils import _
from keystone.openstack.common import log

import utils
import sql
import twilio_api

METHOD_NAME = 'otp'

LOG = log.getLogger(__name__)


@dependency.requires('identity_api')
class Otp(auth.AuthMethodHandler):

    method = METHOD_NAME

    def authenticate(self, context, auth_payload, user_context):
        """Try to authenticate against the identity backend."""
        user_info = UserAuthInfo.create(auth_payload)
        try:
            sql.authenticate(user_info.user_id, user_info.password)
            sql.update_otp_auth_status(user_info.user_id, True)
        except AssertionError:
            # authentication failed because of invalid username or one time password
            sql.update_otp_auth_status(user_info.user_id, False)
            msg = _('Invalid one time password')
            raise exception.Unauthorized(msg)
            
        if 'user_id' not in user_context:
            user_context['user_id'] = user_info.user_id
            
        


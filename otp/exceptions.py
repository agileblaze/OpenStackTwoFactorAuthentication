from keystone.exception import SecurityError
from keystone.openstack.common.gettextutils import _

class Blocked(SecurityError):
    message_format = _("Your account is blocked for 24 hrs.")
    code = 401
    title = 'Unauthorized'
    
    def _get_message(self):
        return self.message

    

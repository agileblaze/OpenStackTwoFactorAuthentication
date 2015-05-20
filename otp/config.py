from oslo_config import cfg
from oslo_config import types
from oslo_log import log

LOG = log.getLogger(__name__)

otp_options = cfg.OptGroup(name = "otp_options",
                             title= "Options for One time password")
    
one_time_password_opts =[ 
    cfg.IntOpt('time_step', default = 30,
               help = 'The time-step used for the OTP generation and validation.'),
    
    cfg.IntOpt('time_step_window_back', default = 2,
               help = 'The number of time-step windows preceedig the current to consider'
                      'when performing validation of OTP. Usually used to take network'
                      'delay into account, and prevent the situation of expiration of OTP codes'
                      'because of network delay which cause the OTP to get delivered only on next'
                      'time-step window.'),
    
    cfg.StrOpt('connection', default = 'mysql://keystone:root@controller/keystone',
               help = 'The connection string to keystone database'),
    
    cfg.StrOpt('twilio_account_sid', default = 'TWILIO_ACCOUNT_SID',
               help = 'Account Sid for Twilio API'),
    
    cfg.StrOpt('twilio_auth_token', default = 'TWILIO_AUTH_TOKEN',
               help = 'Auth Token for Twilio API'),
    
    cfg.StrOpt('twilio_from_phone', default = 'PHONE_NO',
               help = 'SMS enabled from phone number in the twilio account'),

]



'''
class ConfigOpts(object):
    config_file_opt =  cfg.MultiStrOpt('config-file', default = '/etc/keystone/keystone.otp.conf')

    def __init__(self,conf):
        self.conf = conf
        self.conf.register_group(otp_options)
        self.conf.register_opts(one_time_password_opts, otp_options)
        self.conf.register_cli_opt(self.config_file_opt)
        
'''        




CONF = cfg.CONF
CONF.register_group(otp_options)
CONF.register_opts(one_time_password_opts, otp_options)

#if __name__ == '__main__': 
#CONF(default_config_files=['/etc/keystone/keystone.otp.conf',])
#LOG.info(CONF.otp_options.time_step)




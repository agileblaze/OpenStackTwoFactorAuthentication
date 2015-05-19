from oslo_config import cfg
from oslo_config import types


otp_options = cfg.OptGroup(name = "otp_options",
                             title= "Options for One time password")
    
one_time_password_opts =[ 
    cfg.IntOpt('time_step', default = 120,
               help = 'The time-step used for the OTP generation and validation.'),
    
    cfg.IntOpt('time_step_window_back', default = 2,
               help = 'The number of time-step windows preceedig the current to consider \
                      when performing validation of OTP. Usually used to take network \
                      delay into account, and prevent the situation of expiration of OTP codes\
                      because of network delay which cause the OTP to get delivered only on next \
                      time-step window.'),
    
    cfg.StrOpt('connection', default = 'mysql://keystone:root@localhost/keystone',
               help = 'The connection string to keystone database'),

]

CONF = cfg.CONF
CONF.register_group(otp_options)
CONF.register_opts(one_time_password_opts, otp_options)

if __name__ == '__main__': 
    CONF(default_config_files=['otp.conf'])



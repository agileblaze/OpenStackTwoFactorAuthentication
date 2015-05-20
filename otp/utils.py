import config
import hashlib
import hmac
import os
import struct
import time
import uuid

from oslo_log import log
from oslo_config import cfg 

"""Functions for generating and validaing OTP

The method used for one-time password generation is RFC6238-TOTP.
For more information on RFC6238 please visit
https://tools.ietf.org/html/rfc6238
"""
#CONF = config.ConfigOpts(cfg)
#CONF(sys.argv[1:])


CONF = cfg.CONF

LOG = log.getLogger(__name__)

def _get_time_step():
    """Gets the time-step for the TOTP
    """
    return CONF.otp_options.time_step
    
def _get_max_time_step_window():
    """Number of time-step windows considered backwards for OTP validation
    
    A one-time password could be received on the next time-step window
    rather the same time-step window in which it generated. So at the time
    of validation we could check the validity of the token by considering
    time-step windows which preceeds the current one
    
    If the OTP is valid for any of the considered time-step window we take
    the OTP as a valid one.
    
    The number of time-step windows need to consider can be set in the
    configuration file.
    """
    
    return CONF.otp_options.time_step_window_back

    
def generate_totp(secret, position = 0):
    """Generate the TOTP using secret
    
    :param secret: the secret of the user
    
    :returns totp: the one-time password
    """
    
    #code to generate otp based on unix time
    unix_time_synced = get_time_step_window(position)
    hmac_digest = hmac.new(bytes([unix_time_synced]), secret, digestmod = hashlib.sha256)
    
    totp = struct.unpack("16i",bytearray(hmac_digest.hexdigest()))[15]% 1000000
    
    while len(str(totp)) < 6:
        totp = totp * 10
    #return otp
    return  totp
    
    
def get_time_step_window(position = 0):
    """Returns the starting unix-time of the step-time window
    
    This function can be used to get the begining unix-time for the
    time-step window which comes before the current time-step window
    
    Position 0 means the current time-step window
    
    :param position: position of the time-step window before the
                     current time-step window
    """

    sync_time = get_current_unix_time() - _get_time_step() * position
    return  sync_time - (sync_time % _get_time_step())
    

def get_current_unix_time():
    """Returns the current unix time
    """
    
    return int(time.time())

def validate_totp(secret, totp):
    """Validates the one-time password using the secret
    
    For each time-step window specified for validation this function
    will generate an TOTP and will compare with the received TOTP
    if a match found for any of the generated TOTP the function
    treat that OTP as a valid one
    
    If the validation fails for all the generated TOTPs the function
    generates Exception
    
    :param secret: the secret of the user from whom the OTP is received
    :param otp: one-time password received from the user
    
    :returns None: if the validation is okay
    
    :raises AssertionError: if the validation fails
    """
    try:
        
        for position in range(0, _get_max_time_step_window()):
            
            otp_for_validation = generate_totp(secret, position)
            LOG.info(str(totp) +" "+str(otp_for_validation))
            if otp_for_validation == int(totp) :
                return None
        raise AssertionError
    except Exception as e:
        LOG.warning(e.message)
        raise AssertionError

def generate_secret():
    
    return os.urandom(24)

def generate_uuid4_string():
    """Generate a UUID string
    """
    
    return uuid.uuid4().get_hex()

def get_current_mysql_gmtime():
    """Generate the current time in MYSQL time format
    """
    
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(get_current_unix_time()))



    
    
    
    
        
        
     
        
    
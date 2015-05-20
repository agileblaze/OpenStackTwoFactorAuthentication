from oslo_log import log

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

from keystone.auth.plugins.otp import config
from  keystone.auth.plugins.otp import sql
from keystone.auth.plugins.otp import utils

CONF = config.CONF


account_sid = CONF.otp_options.twilio_account_sid
auth_token  = CONF.otp_options.twilio_auth_token
sms_enabled_phone = CONF.otp_options.twilio_from_phone

LOG = log.getLogger(__name__)


def send_sms(one_time_password, to_mobile_number):
    """The one-time password is send to the phone number
    """
    
    try:
        client = TwilioRestClient(account_sid, auth_token)
        msg_body = "Dear customer, use OTP "+str(one_time_password)+" to use login to your OpenStack account" 
        message = client.messages.create(body=msg_body,
             to=to_mobile_number,    
             from_=sms_enabled_phone)
    except TwilioRestException as unable_to_send_otp:
        LOG.warning("unable to send otp message")

        
        
def send_otp(user_id):
    """The one-time password is generated and is sent to the user 
    """
    send_sms( utils.generate_totp(sql.get_secret(user_id)), sql.get_phone_number(user_id))
    
    





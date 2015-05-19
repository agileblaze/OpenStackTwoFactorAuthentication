import logging

from twilio.rest import TwilioRestClient
from twilio import TwilioRestException

import sql
import utils

 
account_sid = "AC42e84817250a5e9443789619e52ab101"
auth_token  = "5205e1db9bfa9858fb40c058124d99b3"
sms_enabled_phone = "+12677331230"


def send_sms(one_time_password, to_mobile_number):
    try:
        
        client = TwilioRestClient(account_sid, auth_token)
        msg_body = "Dear customer, use OTP "+str(one_time_password)+" to use login to your OpenStack account" 
        message = client.messages.create(body=msg_body,
            to=to_mobile_number,    
            from_=sms_enabled_phone) 
        print message.sid
    except TwilioRestException as unable_to_send_otp:
        print "unable_to_send_otp.message"
        
        
def send_otp(user_id):
    """The one-time password is generated and is sent to the user 
    
    """
    send_sms( utils.generate_totp(sql.get_secret(user_id)), sql.get_phone_number(user_id))
    
    





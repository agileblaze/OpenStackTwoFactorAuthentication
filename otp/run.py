import utils
import sql
import time
import calendar
import twilio_api


#print keystoneopt.generate_otp_for_user("8b2ed80d-01f0-4140-a399-89f2c1215afd");

#sql.generate_secrete_for_allusers()

#print sql.UserOneTimePassword.generate_unique_pk()
#print sql.UserOneTimePassword.generate_unique_secret()

#print sql.get_otp_auth_status('31c7d8ef81e54e45a9a84725652f386f').last_failure_timestamp

#print time.strptime(sql.get_otp_auth_status('31c7d8ef81e54e45a9a84725652f386f').last_failure_timestamp, '%Y-%m-%d %H:%M:%S')

#print str(sql.get_otp_auth_status('31c7d8ef81e54e45a9a84725652f386f').last_failure_timestamp)

totp = sql.generate_otp_for_user('31c7d8ef81e54e45a9a84725652f386f')

print totp

secret = sql.get_secret('31c7d8ef81e54e45a9a84725652f386f')

print sql.authenticate('31c7d8ef81e54e45a9a84725652f386f', totp)

#print time.strptime(str(sql.get_otp_auth_status('31c7d8ef81e54e45a9a84725652f386f').last_failure_timestamp), '%Y-%m-%d %H:%M:%S')


#print UserOneTimePassword.__table__
#print UserOneTimePassword.__mapper__


#keystone_sql.ModelBase.metadata.create_all(engine)


#twilio_api.send_sms(896583, "+919846875857")

#twilio_api.send_otp('df62fa9e0c41484f86eb3a8dfa1a37e3')
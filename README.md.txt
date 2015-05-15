The purpose of this project is to develop a two factor authentication feature that integrates  Twilio with OpenStack Keystone and Horizon.    
1. Using OpenStack Keystone v3  create a OTP authentication plugin that will send the  OTP value over SMS using the Twilio service.   

2. If authentication fails to the plugin more than 3 times then you need to lockout the user for 24  hours where authentication will always fail  during the lockout period.     

3. Using OpenStack Horizon implement a second Django template that will be displayed  after the user has  entered in their username/password.  The view for template will retrieve the  phone number for the user  with the username/password from Keystone, generate the OTP  value, and make two RPC calls:  
	first to Keystone to set the OTP value, and 
	second to Twilio  to message the SMS token using the  phone number.  
Once the user enters the OTP value  into the second template and submits the  form make an RPC call to Keystone and will  include 2 methods: one for password and  another for OTP.   Upon successful authentication  grant access to the portal.  Upon failure display an invalid  credentials error  message. 
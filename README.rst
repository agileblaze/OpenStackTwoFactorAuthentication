=============================
Horizon (OpenStack Dashboard) with Two Factor Authentication
=============================

Horizon is a Django-based project aimed at providing a complete OpenStack
Dashboard along with an extensible framework for building new dashboards
from reusable components. The ``Two Factor Authentication`` provides:

 * Password Authentication
 * OTP Authentication

Password Authentication
=============

Password Authenttication is the default authentication provided by Horizon. Here, user credentials like Username and Password are verified.
If credentials are verified then using OpenStack Keystone v3 OTP authentication plugin will send the OTP value over SMS using the Twilio service.
This OTP is sent to users stored contact number using Twilio API Service. User then gets redirected to the OTP Validation page  

OTP Validation
=============

Once the user enters the OTP value into the second template and submits the form Horizon will make an RPC call to Keystone and will include 2 methods: one for password and another for OTP.Upon successful authentication Horizon will grant access to the portal. Upon failure you will display an invalid credentials error message. If authentication fails to the plugin more than 3 times then keystonewill lockout the user for 24 hours where authentication will always fail during the lockout period.	  


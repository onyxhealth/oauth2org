# oauth2org - An OAuth2 Provider (Server) and FHIR Proxy with "Batteries Included"

The OAuth2org project is a "batteries included", reusable OAuth2 Server and FHIR Proxy. It is written in Django 2/3  and Python 3. It uses the Django OAuth Toolkit as its base.

Here is some of what you can do:

* Build B2C and B2B APIs.
* User Authorization Portal - A customizable member/user authorization screen where they agree to share x,y,z with with appliaction ABC Wizbang.  
* A proxy for other APIs via OAuth2.
* A proxy FHIR sever for HAPI, SmileCDR, Microsoft/Azure FHIR, or tother FHIR Server.
* A Developer Portal - Register and manage applications (OAuth2 Clients)
* An OpenID Connect Relying Party: Connect this service to an upstream OpendID Connect Provider or other account system. OAuth2org has built in support for VerifyMyIdentity, Okta, and Google.
* Connect a Health Infortmation Exchange(HIE). Built in support for InterSystems is pre-installed.
* Ingest HL7 v2/ ADT Messages and automatically create APIs.
* Build MongoDB-based APIs, without writing any code, using the pre-installed Djmongo plugin app.  
* Build whatever you want! You can build virtually any RESTful API or app
on top of this base project. Use Django REST Framework or write your own from scatch.

Project History
---------------

This tool is based off of work done on behalf of the
Office of the National Coordinator for Health Information
Technology (HHS ONC) and the  Centers for Medicare and Medicaid
Services (HHS CMS). It is a "hard fork" of the CMS Blue Button 2.0 API,
but shares much of the underlying code.  This version was designed for designed for re-use by  EHRs, insurance companies, states, HIEs, etc.)


Installation
------------

This project is based on Python 3.6 and Django 2.2.18. 

Download the project:


    git clone https://github.com/TransparentHealth/oauth2org.git
   

Install supporting libraries. (Consider using virtualenv for your python setup).


    cd oauth2org
    pip install -r requirements.txt

Depending on your local environment you made need some supporting libraries
for the above command to run cleanly. For example you need a 
compiler and python-dev.

Setup some local environment variables. 


    export ALLOWED_HOSTS="*"
    export EC2PARAMSTORE_4_ENVIRONMENT_VARIABLES=".ENV" 
    
The `EC2PARAMSTORE_4_ENVIRONMENT_VARIABLES`  setting says to look for envvars in a file called `.env`. If this string is `EC2_PARAMSTORE`,
the anything in `.env` will be overridden with parameters in an AWS EC2 Parameter store.
There are a number of variables that can be set based on your
specific environment and setup.  This is how you can brand the project to your needs.
See the `settings.py` and for a full list.  Below are some basic variable you may want to set.


    export AWS_ACCESS_KEY_ID="YOUR_KEY_ID"
    export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"
    export DJANGO_SUPERUSER_USERNAME="youruser"
    export DJANGO_SUPERUSER_PASSWORD="yourpassword"
    export DJANGO_SUPERUSER_EMAIL="super@example.com"
    export DJANGO_SUPERUSER_FIRST_NAME="Super"
    export DJANGO_SUPERUSER_LAST_NAME="User"
    export ALLOWED_HOSTS="*"


Just add the above to a `.env` and then do a 'source .env' to make the changes take effect.
See https://docs.djangoproject.com/en/2.2/topics/settings/ for all the details about Django settings.


Create the database of your choice.  (Default is SqLite). Override the setting in your env to create/point to  the DB you desire.:


    python manage.py migrate


Create a superuser (Optional)


    python manage.py create_super_user_from_envars


Create default Groups.  This will create the groups `ApplicationDeveloper` and `DynamicClientRegistrationProtocol`.


    python manage.py create_default_groups

(Please note that in order for users to register apps (i.e. clients) in the web interface, they first need 
added to the `ApplicationDeveloper` group. This may be accomplished in the admin or programatically.  

    
Create the sampe `TestApp` application, so the test Client application  will work as expected.)


    python manage.py create_test_application


Applications can also be registered via OAuth2 Dynamic client registration protocol.  
The script `oauth2org_app_register.py`. is a command line utility which calles the registration endpoint.
Your user needs to be in the `DynamicClientRegistrationProtocol` group in order to use this feature. 
Do this in the admin.

You man also use the management command (via `manage.py` ) called `register_oauth2_client`.


Upstream OIDC Connection
------------------------

Out of the box this service uses an external OIDC IdP for login.  It is preconfigured for VerifyMyIdentity
but this can be changed.

Be sure to register this application in the OIDC Server and then set the values in your `.env`.
For example your `.env` file may contain the following lines:


     export SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_KEY="oauth2org-1kjdfkdjfasasas"
     export SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_SECRET="oauth2org-dsjkfj87234ndsh89r3b434y8dTWocG"
     export SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_OIDC_ENDPOINT="http://verifymyidentity:8000"

You may also use other upsteam identity providers such as Ping,Okta, SAML, etc.  See Python Social Auth documentation.

If you are a developer running `oauth2org` server and the `vmi` OpenID Connect server locally on the same machine for development,
we recommend setting up hostnames locally for each server host. 
In your  `/etc/hosts` file, you might add lines like the following:


    127.0.0.1       oauth2org
    127.0.0.1       verifymyidentity


The convention is to run `vmi` on port `8000` and `oauth2org` on `8001`. Any 3rd party apps on `8002`, etc.......
To start this server on port `8001` issue the following command.


     python manage.py runserver 8001


.....then point your browser to http://oauth2org:8001 or http://localhost:8001


Advanced Connectivity Topics
============================


Connecting to a Backend FHIR service via the `fhirproxy` app.
------------------------------------

The following settings illustrate how you can connect to an existing FHIR backend service (such as Microsoft Azure)
using OAuth2 client credentials grant type.


     export DEFAULT_FHIR_SERVER="https://example.azurehealthcareapis.com/"
     export DEFAULT_FHIR_URL_PREFIX="/fhir/R4"
     export BACKEND_FHIR_CLIENT_ID="xxxxxxxxxxxx-0000-11111-222222222222"
     export BACKEND_FHIR_CLIENT_SECRET="8347843ndnisd723nj23423cjbndu89er3i4jn3890d823r3r"
     export BACKEND_FHIR_RESOURCE="https://example.azurehealthcareapis.com"
     export BACKEND_FHIR_TOKEN_ENDPOINT="https://login.microsoftonline.com/ee75491b-f5a0-4a95-a1a0-a05eb719943c/oauth2/token"


Connecting to InterSystems  Health Information Exchange (HIE)
-------------------------------------------------------------
This OAuth2 Provider can connect to an InterSystems-based backend. The `hie` app gets a CCDA(XML) document,
converts it to FHIR (JSON), and then serve it as a consumer-facing API via OAuth2.  If your organization is
interested in using this feature, please contact us.



Deploy with Docker
------------------
Docker is supported. These instructions will configure a postgreSQL docker instance on 
port **5432**.

Run docker with:

     docker-compose -f .development/docker-compose.yml up
     
If you make changes to requirements.txt to add libraries re-run 
docker-compose with the --build option.

If you're working with a fresh db image the migrations have 
to be run.

Associated Projects
===================

[VerifyMyIdentity - vmi](https://github.com/videntity/vmi)
Out of the box, `oauth2org` comes configured to act as a relying party to VerifyMyIdentity (a.k.a. `vmi`).


`vmi` is an open source, standards-based, OpenID Connect Identity Provider (IdP) with rich and extensible claim support. Some of the claims/fields supported by `vmi` that yuou may care about include `ial`, `aal`, `vot`  `vtm`,  `amr`, `sex`, `gender` `date_of_birth`, `document`, and `verified_claims`, `person_to_person`.  `vmi` has an extensible authorization framework. `vmi` may connect to an upstream identity provider such as Ping, Okta, or Google. It may also connect to a direcotry (e.g. LDAP/ActiveDirectory) or for account information such as username and password validation. `vmi` may also be used in a stand alone mode.  

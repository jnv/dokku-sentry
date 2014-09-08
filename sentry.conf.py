
# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *
import dj_database_url
import os.path
import urlparse
import os

CONF_ROOT = os.path.dirname(__file__)
DATABASES = {'default': dj_database_url.config()}


############
## SENTRY ##
############

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = os.environ.get('SECRET_KEY')

# Should Sentry allow users to create new accounts?
# Defaults to True (can register).
registration = os.environ.get('SENTRY_ALLOW_REGISTRATION', 'True')
SENTRY_ALLOW_REGISTRATION = (registration == 'True')

# Should Sentry make all data publicly accessible?
# This should only be used if you’re installing Sentry behind your company’s firewall.
# Defaults to False
SENTRY_PUBLIC = 'SENTRY_PUBLIC' in os.environ

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings

###########
## CACHE ##
###########

# You'll need to install the required dependencies for Memcached:
#   pip install python-memcached
#
# CACHES = {
#     'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [os.environ['MEMCACHE_SERVERS']],
#     }
# }

###########
## Queue ##
###########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

# You can enable queueing of jobs by turning off the always eager setting:
# CELERY_ALWAYS_EAGER = False
# BROKER_URL = 'redis://localhost:6379'

####################
## Update Buffers ##
####################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

# You'll need to install the required dependencies for Redis buffers:
#   pip install redis hiredis nydus
#
redis_url = urlparse.urlparse(os.environ.get('REDIS_URL'))
SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': redis_url.hostname,
            'port': redis_url.port,
        }
    }
}

################
## Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = os.environ.get('SENTRY_URL_PREFIX', '')  # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# and X-Forwarded-Host headers, and uncomment the following settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = int(os.environ.get('PORT', 9000))
SENTRY_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    'limit_request_line': 0,  # required for raven-js
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

#################
## Mail Server ##
#################

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = 465
EMAIL_USE_TLS = True

# The email address to send on behalf of
SERVER_EMAIL = ''

###########
## etc. ##
###########

# Social Auth
# -----------
SOCIAL_AUTH_CREATE_USERS = 'SOCIAL_AUTH_CREATE_USERS' in os.environ
# Twitter
# -------
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
# Facebook
# --------
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_API_SECRET = os.environ.get('FACEBOOK_API_SECRET')
# Google
# ------
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH2_CLIENT_SECRET')
# GitHub
# ------
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_API_SECRET = os.environ.get('GITHUB_API_SECRET')
GITHUB_EXTENDED_PERMISSIONS = ['repo']
# Bitbucket
# ---------
BITBUCKET_CONSUMER_KEY = os.environ.get('BITBUCKET_CONSUMER_KEY')
BITBUCKET_CONSUMER_SECRET = os.environ.get('BITBUCKET_CONSUMER_SECRET')

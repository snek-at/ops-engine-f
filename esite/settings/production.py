"""
Django production settings for esite project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/

This development settings are unsuitable for production, see
https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/
"""

from .base import *


#> Allowed hosts
# Accept all hostnames, since we don't know in advance
# which hostname will be used for any given Docker instance.
# IMPORTANT: Set this to a real hostname when using this in production!
# See https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []
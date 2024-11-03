#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#
from __future__ import unicode_literals
from django.conf import settings

# These credentials can be generated and retrieved from your Replyify account where the `OAuth2 Application` was created/managed
REPLYIFY_CLIENT_ID = getattr(settings, 'REPLYIFY_CLIENT_ID', None)
REPLYIFY_CLIENT_SECRET = getattr(settings, 'REPLYIFY_CLIENT_SECRET', None)
# This is the path to your oauth callback view: i.e. https://youapplication.com/replyify/callback
# This path must be set in your `OAuth2 Application Settings` in Replyify and must match
REPLYIFY_REDIRECT_URI = getattr(settings, 'REPLYIFY_REDIRECT_URI', None)

REPLYIFY_AUTH_URL = getattr(settings, 'REPLYIFY_AUTH_URL', 'https://app.replyify.com/oauth2/authorize')
REPLYIFY_TOKEN_URL = getattr(settings, 'REPLYIFY_TOKEN_URL', 'https://app.replyify.com/oauth2/token')

REPLYIFY_USER_ID_FIELD = getattr(settings, 'REPLYIFY_USER_ID_FIELD', 'id')  # Foreign Key used by your application for referencing users in your db
REPLYIFY_DENIED_REDIRECT = getattr(settings, 'REPLYIFY_DENIED_REDIRECT', '/')  # Fallback path for denied access

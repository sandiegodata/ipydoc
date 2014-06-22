"""Social Auth authentication Pipeline functions.

Copyright (c) 2014 San Diego Regional Data Library. This file is licensed under the terms of the
Revised BSD License, included in this distribution as LICENSE.txt
"""

import logging

from uuid import uuid4

from social_auth.utils import setting, module_member
from social_auth.models import UserSocialAuth

logger = logging.getLogger('any')
logger.setLevel(logging.DEBUG)


def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):

    """Create user. Depends on get_username pipeline."""

    if user:
        return {'user': user}
    if not username:
        return None

    # Avoid hitting field max length
    email = details.get('email')
    original_email = None

    # There seems to be something odd about the Github orgs backend; we're getting dicts here instead of strings.
    if isinstance(email, dict):
        email = email.get('email', None)

    if email and UserSocialAuth.email_max_length() < len(email):
        original_email = email
        email = ''


    return {
        'user': UserSocialAuth.create_user(username=username, email=email),
        'original_email': original_email,
        'is_new': True
    }


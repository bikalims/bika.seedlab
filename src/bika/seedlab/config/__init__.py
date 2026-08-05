# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory

from bika.seedlab.interfaces import IBikaSeedlabLayer
from bika.lims.api import get_request

PROFILE_ID = "profile-bika.seedlab:default"
PROJECTNAME = "bika.seedlab"

logger = logging.getLogger(PROJECTNAME)
_ = MessageFactory(PROJECTNAME)


def is_installed():
    """Returns whether the product is installed or not"""
    request = get_request()
    return IBikaSeedlabLayer.providedBy(request)


def check_installed(default_return):
    """Decorator to prevent the function to be called if product not installed

    :param default_return: value to return if not installed
    """
    def is_installed_decorator(func):
        def wrapper(*args, **kwargs):
            if not is_installed():
                return default_return
            return func(*args, **kwargs)
        return wrapper
    return is_installed_decorator

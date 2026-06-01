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

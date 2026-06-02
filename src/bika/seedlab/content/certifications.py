# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from bika.seedlab.interfaces import ICertifications
from senaite.core.interfaces import IHideActionsMenu


class ICertificationsSchema(model.Schema):
    """Schema interface
    """


@implementer(ICertifications, ICertificationsSchema, IHideActionsMenu)
class Certifications(Container):
    """A folder/container for Certifications
    """

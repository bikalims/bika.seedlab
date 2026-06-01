# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from bika.seedlab.interfaces import IGrades
from senaite.core.interfaces import IHideActionsMenu


class IGradesSchema(model.Schema):
    """Schema interface
    """


@implementer(IGrades, IGradesSchema, IHideActionsMenu)
class Grades(Container):
    """A folder/container for material types
    """

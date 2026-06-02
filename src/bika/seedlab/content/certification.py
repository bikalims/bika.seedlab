# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer

from bika.lims import api
from bika.lims.interfaces import IDeactivable
from bika.seedlab.interfaces import ICertification
from senaite.core.catalog import SETUP_CATALOG


class ICertificationSchema(model.Schema):
    """ Marker interface and Dexterity Python Schema for Certification
    """


@implementer(ICertification, ICertificationSchema, IDeactivable)
class Certification(Item):
    """
    """
    _catalogs = [SETUP_CATALOG]

    security = ClassSecurityInfo()

    @security.private
    def accessor(self, fieldname):
        """Return the field accessor for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        return schema[fieldname].get

    @security.private
    def mutator(self, fieldname):
        """Return the field mutator for the fieldname"""
        schema = api.get_schema(self)
        if fieldname not in schema:
            return None
        result = schema[fieldname].set
        self.reindexObject()
        return result

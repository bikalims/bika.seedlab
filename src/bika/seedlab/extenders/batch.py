# -*- coding: utf-8 -*-

from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.interface import implements
from zope.component import adapts

from bika.seedlab.config import is_installed
from bika.seedlab.interfaces import IBikaSeedlabLayer
from bika.lims.interfaces import IBatch


class BatchSchemaModifier(object):
    adapts(IBatch)
    implements(ISchemaModifier)
    layer = IBikaSeedlabLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema["ClientBatchID"].widget.label = "Crop Number"

        return schema

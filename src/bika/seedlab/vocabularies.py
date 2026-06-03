# -*- coding: utf-8 -*-

from Products.Archetypes.public import DisplayList
from bika.seedlab.config import _

SAMPLE_DIRECTION = DisplayList((
    ('', _('None')),
    ('inbound', _('Inbound')),
    ('outbound', _('Outbound')),
))

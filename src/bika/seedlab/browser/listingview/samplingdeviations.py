# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.seedlab.config import _
from bika.seedlab.config import is_installed
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter
from senaite.core.i18n import translate


class SamplingDeviationListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

        self.title = translate(_(
            "listing_cultivars_title",
            default="Seed Types")
        )

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item
        return item

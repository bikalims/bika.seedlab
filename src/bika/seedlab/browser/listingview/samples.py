# -*- coding: utf-8 -*-

from zope.component import adapts
from zope.interface import implements

from bika.lims import api
from bika.lims.utils import get_link
from bika.seedlab.config import is_installed
from bika.seedlab.config import _
from bika.seedlab.vocabularies import SAMPLE_DIRECTION
from senaite.app.listing.interfaces import IListingView
from senaite.app.listing.interfaces import IListingViewAdapter


class SamplesListingViewAdapter(object):
    adapts(IListingView)
    implements(IListingViewAdapter)

    def __init__(self, listing, context):
        self.listing = listing
        self.context = context

    def before_render(self):
        if not is_installed():
            return

        certification = [("Certification", {"toggle": False, "title": _("Certification")})]
        self.listing.columns.update(certification)
        grade = [
            ("Grade", {"toggle": False, "title": _("Grade")})
        ]
        self.listing.columns.update(grade)
        lot = [("Lot", {"toggle": False, "title": _("Lot")})]
        self.listing.columns.update(lot)
        tonnage = [
            ("Tonnage", {"toggle": False, "title": _("Tonnage")})
        ]
        self.listing.columns.update(tonnage)
        packsize = [
            ("PackSize", {"toggle": False, "title": _("Pack Size")})
        ]
        self.listing.columns.update(packsize)
        direction = [
            ("Direction", {"toggle": False, "title": _("Direction")})
        ]
        self.listing.columns.update(direction)
        self.listing.columns["Vintage"]["title"] = "Production Year"
        self.listing.columns["Cultivar"]["title"] = "Variety"
        for i in range(len(self.listing.review_states)):
            self.listing.review_states[i]["columns"].append("Certification")
            self.listing.review_states[i]["columns"].append("Grade")
            self.listing.review_states[i]["columns"].append("Lot")
            self.listing.review_states[i]["columns"].append("Tonnage")
            self.listing.review_states[i]["columns"].append("PackSize")
            self.listing.review_states[i]["columns"].append("Direction")

    def folder_item(self, obj, item, index):
        if not is_installed():
            return item

        full_object = api.get_object(obj)

        # Certification
        certification_field = full_object.Schema().getField("Certification")
        if certification_field:
            certification = certification_field.get(full_object)
        if certification:
            container_title = certification.Title()
            container_url = certification.absolute_url()
            container_link = get_link(container_url, container_title)
            item["Certification"] = container_title
            item["replace"]["Certification"] = container_link

        # Grade
        grade_field = full_object.Schema().getField("Grade")
        if grade_field:
            grade = grade_field.get(full_object)
        if grade:
            spec_title = grade.Title()
            spec_url = grade.absolute_url()
            spec_link = get_link(spec_url, spec_title)
            item["Grade"] = spec_title
            item["replace"]["Grade"] = spec_link

        # Lot
        lot_field = full_object.Schema().getField("Lot")
        if lot_field:
            lot = lot_field.get(full_object)
        if lot:
            item["replace"]["Lot"] = lot

        # Tonnage
        tonnage_field = full_object.Schema().getField("Tonnage")
        if tonnage_field:
            tonnage = tonnage_field.get(full_object)
        if tonnage:
            item["replace"]["Tonnage"] = tonnage

        # PackSize
        packsize_field = full_object.Schema().getField("PackSize")
        if packsize_field:
            packsize = packsize_field.get(full_object)
        if packsize:
            item["replace"]["PackSize"] = packsize

        # Direction
        direction_field = full_object.Schema().getField("Direction")
        if direction_field:
            direction = direction_field.get(full_object)
        if direction:
            item["replace"]["Direction"] = SAMPLE_DIRECTION.getValue(direction)

        return item

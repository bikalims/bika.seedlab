# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import StringWidget
from Products.CMFCore.permissions import View
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from zope.interface import implements
from zope.component import adapts
from zope.interface import implementer

from bika.seedlab.config import _
from bika.seedlab.config import is_installed
from bika.seedlab.extenders.fields import ExtStringField
from bika.seedlab.extenders.fields import ExtUIDReferenceField
from bika.seedlab.interfaces import IBikaSeedlabLayer
from bika.seedlab.vocabularies import SAMPLE_DIRECTION

from bika.lims import FieldEditContact
from bika.lims import SETUP_CATALOG
from bika.lims.browser.widgets.selectionwidget import SelectionWidget
from bika.lims.interfaces import IAnalysisRequest
from senaite.core.browser.widgets.referencewidget import ReferenceWidget

certification_field = ExtUIDReferenceField(
    "Certification",
    required=False,
    allowed_types=("Certification",),
    relationship="AnalysisRequestCertification",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Certification"),
        description=_("Select the certification"),
        render_own_label=True,
        size=20,
        catalog_name=SETUP_CATALOG,
        base_query={"sort_on": "sortable_title", "is_active": True},
        showOn=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
        ui_item="title",
        colModel=[
            dict(columnName="UID", hidden=True),
            dict(columnName="title", width="60", label=_("Title")),
        ],
    ),
)

grade_field = ExtUIDReferenceField(
    "Grade",
    required=False,
    allowed_types=("Grade",),
    relationship="AnalysisRequestGrade",
    format="select",
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=ReferenceWidget(
        label=_(u"Grade"),
        description=_("Select the grade"),
        render_own_label=True,
        size=20,
        catalog_name=SETUP_CATALOG,
        base_query={"sort_on": "sortable_title", "is_active": True},
        showOn=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
        ui_item="title",
        colModel=[
            dict(columnName="UID", hidden=True),
            dict(columnName="title", width="60", label=_("Title")),
        ],
    ),
)

lot_field = ExtStringField(
    "Lot",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=StringWidget(
        label=_(u"Lot"),
        description=_("Lot"),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)

tonnage_field = ExtStringField(
    "Tonnage",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=StringWidget(
        label=_(u"Tonnage"),
        description=_("Lot"),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)

pack_size_field = ExtStringField(
    "PackSize",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    widget=StringWidget(
        label=_(u"Pack Size"),
        description=_("Pack Size"),
        render_own_label=True,
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)

direction_field = ExtStringField(
    "Direction",
    required=False,
    mode="rw",
    read_permission=View,
    write_permission=FieldEditContact,
    vocabulary=SAMPLE_DIRECTION,
    widget=SelectionWidget(
        label=_("Direction"),
        description=_("Select the direction"),
        format="select",
        visible={
            "add": "edit",
            "header_table": "visible",
            "secondary": "disabled",
            "verified": "view",
            "published": "view",
        },
    ),
)


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    layer = IBikaSeedlabLayer

    fields = [
        grade_field,
        lot_field,
        tonnage_field,
        pack_size_field,
        certification_field,
        direction_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields


class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)
    layer = IBikaSeedlabLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """
        """
        if is_installed():
            schema["SampleType"].widget.label = _(
                "label_sample_sampletype", default="Kind")
            schema["SampleType"].widget.description = _(
                "description_sample_sampletype",
                default="Select the kind of this sample")
            schema["ClientSampleID"].widget.label = _("Inspectorate Number")
            schema["ClientReference"].widget.label = _("Stock Number")
            schema["SamplingDeviation"].widget.label = _(
                "label_sample_samplingdeviation", default="Seed Type")
            schema["SamplingDeviation"].widget.description = _(
                "description_sample_samplingdeviation",
                default="Seed Type between the sample and how it was sampled")

        return schema

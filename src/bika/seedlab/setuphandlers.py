# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer

from bika.lims import api
from bika.seedlab.config import PROFILE_ID
from bika.seedlab.config import _
from bika.seedlab.config import logger
from senaite.core.content.samplepoint import ISamplePointSchema
from senaite.core.setuphandlers import add_dexterity_items
from senaite.core.content.sampletype import ISampleTypeSchema


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'bika.seedlab:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    logger.info("BIKA.SEEDLAB post install handler [BEGIN]")
    profile_id = PROFILE_ID
    context = context._getImportContext(profile_id)
    portal = context.getSite()
    setup(portal)
    add_dexterity_setup_items(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup(portal):
    # Batches
    senaite_setup = api.get_senaite_setup()

    # pt
    pt = api.get_tool("portal_types", context=portal)

    # Sample Types
    senaite_setup.sampletypes.setTitle("Kinds")
    fti = pt.get("SampleType")
    fti.title = _("Kind")

    ISampleTypeSchema["prefix"].title = u"Kind Prefix"

    # Sample Points
    sp_schema = ISamplePointSchema
    sample_type_filed = sp_schema["sample_types"]
    sample_type_filed.title = _("Kinds")

    # Vintages
    senaite_setup.vintages.setTitle("Production Years")
    fti = pt.get("Vintage")
    fti.title = _("Production Year")
    fti.description = _("Production Year")

    # Cultivars
    senaite_setup.cultivars.setTitle("Varieties")
    fti = pt.get("Cultivar")
    fti.title = _("Variety")
    fti.description = _("Variety")

    # Sampling Deviations
    senaite_setup.samplingdeviations.setTitle("Seed Types")
    fti = pt.get("SamplingDeviation")
    fti.title = _("Seed Type")
    fti.description = _("Seed Type between the sample and how it was sampled")

    logger.info("BIKA.SEEDLAB setup [DONE]")


def add_dexterity_setup_items(portal):
    """Adds the Dexterity Container in the Setup Folder

    N.B.: We do this in code, because adding this as Generic Setup Profile in
          `profiles/default/structure` flushes the contents on every import.
    """
    # Tuples of ID, Title, FTI
    items = [
        ("grades", "Grades", "Grades"),
    ]
    setup = api.get_setup()
    add_dexterity_items(setup, items)

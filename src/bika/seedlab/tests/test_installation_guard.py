# -*- coding: utf-8 -*-
"""Sample Add must respect site installation even with a stale layer."""
import unittest

from bika.seedlab import config
from bika.seedlab.extenders.analysisrequest import AnalysisRequestSchemaExtender
from bika.seedlab.extenders.analysisrequest import AnalysisRequestSchemaModifier
from bika.seedlab.extenders.batch import BatchSchemaModifier
from bika.lims.content.batch import Batch
from Products.Archetypes.public import Schema, StringField, StringWidget


def shared_field_schema(base):
    """Match schemaextender's shallow copy, which reuses field objects."""
    schema = base.__class__()
    schema._names = list(base._names)
    schema._fields = base._fields.copy()
    schema._props = base._props.copy()
    schema._layers = base._layers.copy()
    return schema


class TestInstallationGuard(unittest.TestCase):

    def setUp(self):
        self.originals = (config.get_request, config.get_tool,
                          config.IBikaSeedlabLayer)
        self.has_layer = True
        self.installed = False
        self.installer = self
        config.get_request = lambda: object()
        config.get_tool = lambda name, default=None: self.installer
        config.IBikaSeedlabLayer = self

    def tearDown(self):
        (config.get_request, config.get_tool,
         config.IBikaSeedlabLayer) = self.originals

    def providedBy(self, request):
        return self.has_layer

    def isProductInstalled(self, name):
        self.assertEqual(name, "bika.seedlab")
        return self.installed

    def test_stale_layer_does_not_enable_sample_fields(self):
        self.assertFalse(config.is_installed())
        self.assertEqual(AnalysisRequestSchemaExtender(None).getFields(), [])

    def test_installed_site_has_sample_fields(self):
        self.installed = True
        self.assertTrue(config.is_installed())
        extender = AnalysisRequestSchemaExtender(None)
        self.assertEqual(extender.getFields(), extender.fields)

    def test_missing_layer_disables_installed_product(self):
        self.installed = True
        self.has_layer = False
        self.assertFalse(config.is_installed())

    def test_missing_installer_disables_product(self):
        self.installer = None
        self.assertFalse(config.is_installed())

    def test_stale_layer_does_not_change_batch_add_label(self):
        schema = Batch.schema.copy()
        original_label = schema["ClientBatchID"].widget.label
        result = BatchSchemaModifier(None).fiddle(schema)
        self.assertIs(result, schema)
        self.assertEqual(schema["ClientBatchID"].widget.label, original_label)

    def test_installed_site_has_crop_number_label(self):
        self.installed = True
        schema = Batch.schema.copy()
        BatchSchemaModifier(None).fiddle(schema)
        self.assertEqual(schema["ClientBatchID"].widget.label, "Crop Number")

    def test_batch_label_does_not_leak_between_sites(self):
        base = Batch.schema.copy()
        original_label = base["ClientBatchID"].widget.label
        installed_schema = shared_field_schema(base)
        self.installed = True
        BatchSchemaModifier(None).fiddle(installed_schema)
        self.assertEqual(installed_schema["ClientBatchID"].widget.label,
                         "Crop Number")
        self.assertEqual(base["ClientBatchID"].widget.label, original_label)
        self.installed = False
        uninstalled_schema = shared_field_schema(base)
        BatchSchemaModifier(None).fiddle(uninstalled_schema)
        self.assertEqual(uninstalled_schema["ClientBatchID"].widget.label,
                         original_label)

    def test_sample_labels_do_not_leak_between_sites(self):
        names = ("SampleType", "ClientSampleID", "ClientReference",
                 "SamplingDeviation", "Vintage", "Cultivar")
        base = Schema([StringField(name, widget=StringWidget(
            label=name, description="Original description")) for name in names])
        installed_schema = shared_field_schema(base)
        self.installed = True
        AnalysisRequestSchemaModifier(None).fiddle(installed_schema)
        self.assertEqual(installed_schema["ClientSampleID"].widget.label,
                         "Inspectorate Number")
        self.installed = False
        uninstalled_schema = shared_field_schema(base)
        AnalysisRequestSchemaModifier(None).fiddle(uninstalled_schema)
        for name in names:
            self.assertEqual(base[name].widget.label, name)
            self.assertEqual(uninstalled_schema[name].widget.label, name)
            self.assertEqual(base[name].widget.description,
                             "Original description")

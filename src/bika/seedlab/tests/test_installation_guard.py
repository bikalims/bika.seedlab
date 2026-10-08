# -*- coding: utf-8 -*-
"""Sample Add must respect site installation even with a stale layer."""
import unittest

from bika.seedlab import config
from bika.seedlab.extenders.analysisrequest import AnalysisRequestSchemaExtender
from bika.seedlab.extenders.batch import BatchSchemaModifier
from bika.lims.content.batch import Batch


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

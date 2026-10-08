# -*- coding: utf-8 -*-
"""Sample Add must respect site installation even with a stale layer."""
import unittest

from bika.seedlab import config
from bika.seedlab.extenders.analysisrequest import AnalysisRequestSchemaExtender


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

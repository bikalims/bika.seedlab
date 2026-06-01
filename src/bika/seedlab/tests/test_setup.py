# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from bika.seedlab.testing import BIKA_SEEDLAB_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that bika.seedlab is properly installed."""

    layer = BIKA_SEEDLAB_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if bika.seedlab is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'bika.seedlab'))

    def test_browserlayer(self):
        """Test that IBikaSeedlabLayer is registered."""
        from bika.seedlab.interfaces import (
            IBikaSeedlabLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IBikaSeedlabLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = BIKA_SEEDLAB_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['bika.seedlab'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if bika.seedlab is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'bika.seedlab'))

    def test_browserlayer_removed(self):
        """Test that IBikaSeedlabLayer is removed."""
        from bika.seedlab.interfaces import \
            IBikaSeedlabLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IBikaSeedlabLayer,
            utils.registered_layers())

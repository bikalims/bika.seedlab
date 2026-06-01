# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import bika.seedlab


class BikaSeedlabLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=bika.seedlab)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bika.seedlab:default')


BIKA_SEEDLAB_FIXTURE = BikaSeedlabLayer()


BIKA_SEEDLAB_INTEGRATION_TESTING = IntegrationTesting(
    bases=(BIKA_SEEDLAB_FIXTURE,),
    name='BikaSeedlabLayer:IntegrationTesting',
)


BIKA_SEEDLAB_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(BIKA_SEEDLAB_FIXTURE,),
    name='BikaSeedlabLayer:FunctionalTesting',
)


BIKA_SEEDLAB_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        BIKA_SEEDLAB_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='BikaSeedlabLayer:AcceptanceTesting',
)

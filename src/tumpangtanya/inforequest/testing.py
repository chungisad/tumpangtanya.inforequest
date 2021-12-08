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

import tumpangtanya.inforequest


class TumpangtanyaInforequestLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=tumpangtanya.inforequest)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tumpangtanya.inforequest:default')


TUMPANGTANYA_INFOREQUEST_FIXTURE = TumpangtanyaInforequestLayer()


TUMPANGTANYA_INFOREQUEST_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TUMPANGTANYA_INFOREQUEST_FIXTURE,),
    name='TumpangtanyaInforequestLayer:IntegrationTesting',
)


TUMPANGTANYA_INFOREQUEST_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TUMPANGTANYA_INFOREQUEST_FIXTURE,),
    name='TumpangtanyaInforequestLayer:FunctionalTesting',
)


TUMPANGTANYA_INFOREQUEST_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TUMPANGTANYA_INFOREQUEST_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='TumpangtanyaInforequestLayer:AcceptanceTesting',
)

# -*- coding: utf-8 -*-
from tumpangtanya.inforequest.content.info_request import IInfoRequest  # NOQA E501
from tumpangtanya.inforequest.testing import TUMPANGTANYA_INFOREQUEST_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class InfoRequestIntegrationTest(unittest.TestCase):

    layer = TUMPANGTANYA_INFOREQUEST_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_info_request_schema(self):
        fti = queryUtility(IDexterityFTI, name='Info Request')
        schema = fti.lookupSchema()
        self.assertEqual(IInfoRequest, schema)

    def test_ct_info_request_fti(self):
        fti = queryUtility(IDexterityFTI, name='Info Request')
        self.assertTrue(fti)

    def test_ct_info_request_factory(self):
        fti = queryUtility(IDexterityFTI, name='Info Request')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IInfoRequest.providedBy(obj),
            u'IInfoRequest not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_info_request_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Info Request',
            id='info_request',
        )

        self.assertTrue(
            IInfoRequest.providedBy(obj),
            u'IInfoRequest not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('info_request', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('info_request', parent.objectIds())

    def test_ct_info_request_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Info Request')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_info_request_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Info Request')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'info_request_id',
            title='Info Request container',
        )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )

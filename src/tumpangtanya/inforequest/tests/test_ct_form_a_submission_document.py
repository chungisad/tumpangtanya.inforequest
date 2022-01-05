# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from tumpangtanya.inforequest.content.form_a_submission_document import (
    IFormASubmissionDocument  # NOQA E501,
)
from tumpangtanya.inforequest.testing import (
    TUMPANGTANYA_INFOREQUEST_INTEGRATION_TESTING  # noqa,
)
from zope.component import createObject, queryUtility

import unittest


class FormASubmissionDocumentIntegrationTest(unittest.TestCase):

    layer = TUMPANGTANYA_INFOREQUEST_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            'Info Request',
            self.portal,
            'parent_container',
            title='Parent container',
        )
        self.parent = self.portal[parent_id]

    def test_ct_form_a_submission_document_schema(self):
        fti = queryUtility(IDexterityFTI, name='Form A Submission Document')
        schema = fti.lookupSchema()
        self.assertEqual(IFormASubmissionDocument, schema)

    def test_ct_form_a_submission_document_fti(self):
        fti = queryUtility(IDexterityFTI, name='Form A Submission Document')
        self.assertTrue(fti)

    def test_ct_form_a_submission_document_factory(self):
        fti = queryUtility(IDexterityFTI, name='Form A Submission Document')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IFormASubmissionDocument.providedBy(obj),
            u'IFormASubmissionDocument not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_form_a_submission_document_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.parent,
            type='Form A Submission Document',
            id='form_a_submission_document',
        )

        self.assertTrue(
            IFormASubmissionDocument.providedBy(obj),
            u'IFormASubmissionDocument not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('form_a_submission_document', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('form_a_submission_document', parent.objectIds())

    def test_ct_form_a_submission_document_globally_not_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Form A Submission Document')
        self.assertFalse(
            fti.global_allow,
            u'{0} is globally addable!'.format(fti.id)
        )

    def test_ct_form_a_submission_document_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Form A Submission Document')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'form_a_submission_document_id',
            title='Form A Submission Document container',
        )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )

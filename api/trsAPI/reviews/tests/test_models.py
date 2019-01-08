from django import test
from django.db import transaction

from rest_framework.authtoken.models import Token

from trsAPI.reviews import factories as reviews_factories


__author__ = 'smirnov.ev'


class UserModelTestCase(test.TestCase):
    def setUp(self):
        self.obj_model = reviews_factories.UserFactory._meta.model
        self.object = reviews_factories.UserFactory.create()

    def tearDown(self):
        self.object.delete()
        self.assertEqual(self.obj_model.objects.count(), 0)

    @transaction.atomic()
    def test_create_token_method(self):
        """ Testing reviews.signals create_auth_token signal """
        _token = Token.objects.get(user=self.object)
        self.assertIsNotNone(_token.pk)

        self.object.save()
        _token = Token.objects.get(user=self.object)
        self.assertIsNotNone(_token.pk)

        _token.delete()


class CompanyModelTestCase(test.TestCase):
    def setUp(self):
        self.obj_model = reviews_factories.CompanyFactory._meta.model
        self.object = reviews_factories.CompanyFactory.create()

    def tearDown(self):
        self.object.delete()
        self.assertEqual(self.obj_model.objects.count(), 0)

    def test_str_method(self):
        """ Testing reviews.Company model __str__ method """
        self.assertEqual(
            '{}'.format(self.object),
            '{} {}'.format(self.object.pk, self.object.name)
        )


class ReviewModelTestCase(test.TestCase):
    def setUp(self):
        self.obj_model = reviews_factories.ReviewFactory._meta.model
        self.user = reviews_factories.UserFactory.create()
        self.company = reviews_factories.CompanyFactory.create()
        self.object = reviews_factories.ReviewFactory.create(
            user=self.user, company=self.company)

    def tearDown(self):
        self.object.delete()
        self.assertEqual(self.obj_model.objects.count(), 1)
        self.obj_model.objects.filter(pk=self.object.pk).delete()
        self.assertEqual(self.obj_model.objects.count(), 0)
        self.user.delete()
        self.company.delete()

    @transaction.atomic()
    def test_delete_method(self):
        """ Testing reviews.Review model delete method """
        self.assertEqual(self.obj_model.objects.count(), 1)
        self.object.delete()
        self.assertEqual(self.obj_model.objects.count(), 1)

    def test_has_read_permission_method(self):
        """ Testing reviews.Review model has_read_permission method """
        class DummyRequest(object):
            user = self.user

        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_read_permission(_request))

    def test_has_object_read_permission_method(self):
        """ Testing reviews.Review model has_object_read_permission method """
        class DummyRequest(object):
            user = self.user

        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_object_read_permission(_request))

    def test_has_write_permission_method(self):
        """ Testing reviews.Review model has_write_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_write_permission(_request))

    def test_has_object_write_permission_method(self):
        """ Testing reviews.Review model has_object_write_permission method """
        class DummyRequest(object):
            user = self.user
            session = {
                'accident_hash': '123'
            }
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_object_write_permission(_request))

    def test_has_object_update_permission_method(self):
        """ Testing reviews.Review model has_object_update_permission method """
        class DummyRequest(object):
            user = self.user
            session = {
                'accident_hash': '123'
            }
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_object_update_permission(_request))

    def test_has_create_permission_method(self):
        """ Testing reviews.Review model has_create_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_create_permission(_request))

    def test_has_destroy_permission_method(self):
        """ Testing reviews.Review model has_destroy_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_destroy_permission(_request))

    def test_has_object_destroy_permission_method(self):
        """ Testing reviews.Review model has_object_destroy_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_object_destroy_permission(_request))

    def test_has_remove_permission_method(self):
        """ Testing reviews.Review model has_remove_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_remove_permission(_request))

    def test_has_object_remove_permission_method(self):
        """ Testing reviews.Review model has_object_remove_permission method """
        class DummyRequest(object):
            user = self.user
        _request = DummyRequest()
        self.assertTrue(_request.user.is_authenticated)
        self.assertTrue(self.object.has_object_remove_permission(_request))

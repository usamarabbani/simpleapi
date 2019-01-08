import json

from django import test

from django.db import transaction
from django.test import Client
from django.urls import reverse

from rest_framework.test import APIClient

from trsAPI.reviews import factories as reviews_factories

__author__ = 'smirnov.ev'


class APIBaseTestCase(test.TestCase):
    """ Base class for API with creating a default user with password 12345 """

    def setUp(self):
        self.client = Client()
        self.apiclient = APIClient()
        self.user = reviews_factories.UserFactory.create(is_active=True)
        self.user_password = '12345'
        with transaction.atomic():
            self.user.set_password(self.user_password)
            self.user.save()

    def tearDown(self):
        self.user.delete()


class UserViewSetTestCase(APIBaseTestCase):

    def setUp(self):
        super(UserViewSetTestCase, self).setUp()
        self.obj_model = reviews_factories.UserFactory._meta.model
        self.object = reviews_factories.UserFactory.create()

    def tearDown(self):
        self.object.delete()
        super(UserViewSetTestCase, self).tearDown()

    @transaction.atomic()
    def test_api_list_view(self):
        """ Testing reviews.api.UserViewSet list view """
        url = reverse('user-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 403)

        # authorization
        res = self.apiclient.login(password='12345', username=self.user)
        self.assertTrue(res)

        url = reverse('user-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(len(data), 2)
        _obj = data[0]
        self.assertEqual(_obj['id'], self.user.pk)
        _obj = data[1]
        self.assertEqual(_obj['id'], self.object.pk)

        self.apiclient.logout()


class CompanyViewSetTestCase(APIBaseTestCase):

    def setUp(self):
        super(CompanyViewSetTestCase, self).setUp()
        self.obj_model = reviews_factories.CompanyFactory._meta.model
        self.object = reviews_factories.CompanyFactory.create()

    def tearDown(self):
        self.object.delete()
        super(CompanyViewSetTestCase, self).tearDown()

    @transaction.atomic()
    def test_api_list_view(self):
        """ Testing reviews.api.CompanyViewSet list view """
        url = reverse('company-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 403)

        # authorization
        res = self.apiclient.login(password='12345', username=self.user)
        self.assertTrue(res)

        url = reverse('company-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(len(data), 1)
        _obj = data[0]
        self.assertEqual(_obj['id'], self.object.pk)

        self.apiclient.logout()


class ReviewViewSetTestCase(APIBaseTestCase):

    def setUp(self):
        super(ReviewViewSetTestCase, self).setUp()
        self.obj_model = reviews_factories.ReviewFactory._meta.model
        self.company = reviews_factories.CompanyFactory.create()
        self.object = reviews_factories.ReviewFactory.create(
            user=self.user, company=self.company)
        self.user2 = reviews_factories.UserFactory.create()
        self.object2 = reviews_factories.ReviewFactory.create(
            user=self.user2, company=self.company)

    def tearDown(self):
        self.obj_model.objects.filter(pk=self.object.pk).delete()
        self.obj_model.objects.filter(pk=self.object2.pk).delete()
        self.company.delete()
        self.user2.delete()
        super(ReviewViewSetTestCase, self).tearDown()

    @transaction.atomic()
    def test_api_list_view(self):
        """ Testing reviews.api.ReviewViewSet list view """
        url = reverse('review-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 403)

        # authorization
        res = self.apiclient.login(password='12345', username=self.user)
        self.assertTrue(res)

        url = reverse('review-list')
        res = self.apiclient.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(len(data), 1)
        _obj = data[0]
        self.assertEqual(_obj['id'], self.object.pk)

        self.apiclient.logout()

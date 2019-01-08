from django import test

from trsAPI.reviews import factories as reviews_factories
from trsAPI.reviews.serializers import ReviewSerializer

__author__ = 'smirnov.ev'


class ReviewSerializerTestCase(test.TestCase):

    def setUp(self):
        self.obj_model = reviews_factories.ReviewFactory._meta.model
        self.user = reviews_factories.UserFactory.create(is_active=True)
        self.company = reviews_factories.CompanyFactory.create()
        self.object = reviews_factories.ReviewFactory.create(
            user=self.user, company=self.company)
        self.serializer_class = ReviewSerializer

    def tearDown(self):
        self.obj_model.objects.filter(pk=self.object.pk).delete()
        self.company.delete()
        self.user.delete()
        self.assertEqual(self.obj_model.objects.count(), 0)

    def test_validate_user_id_method(self):
        """ Testing reviews.ReviewSerializer serializer validate_user_id method """
        class DummyRequest(object):
            user = self.user
            META = dict(
                REMOTE_ADDR='8.8.8.8'
            )
        serializer = self.serializer_class(context={'request': DummyRequest})
        self.assertEqual(serializer.validate_user_id(13), self.user)

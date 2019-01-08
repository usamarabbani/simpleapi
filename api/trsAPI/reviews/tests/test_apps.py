from django.apps import apps
from django import test

from trsAPI.reviews.apps import ReviewsConfig

__author__ = 'smirnov.ev'


class ReviewsConfigConfigTest(test.TestCase):
    def test_apps(self):
        self.assertEqual(ReviewsConfig.name, 'reviews')
        self.assertEqual(apps.get_app_config('reviews').name, 'trsAPI.reviews')

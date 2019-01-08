import factory
import faker
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model

from trsAPI.reviews import models as reviews_models

__author__ = 'smirnov.ev'

User = get_user_model()
_faker = faker.Factory.create(locale=settings.LANGUAGE_CODE)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.LazyAttribute(lambda o: _faker.first_name()[:30].strip())
    last_name = factory.LazyAttribute(lambda o: _faker.last_name()[:30].strip())

    username = factory.LazyAttribute(lambda o: _faker.user_name()[:30].strip(
        ).replace('.', '_').replace('-', '_'))
    email = factory.LazyAttribute(lambda o: _faker.free_email())

    date_joined = factory.LazyAttribute(
        lambda o: _faker.date_time_between(start_date='-1y', end_date='-1m')
    )

    password = '12345'


class CompanyFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda o: _faker.user_name())

    class Meta:
        model = reviews_models.Company


class ReviewFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    company = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(
        lambda o: ''.join(random.choice(string.ascii_letters) for _ in range(100)))
    summary = factory.LazyAttribute(
        lambda o: ''.join(random.choice(string.ascii_letters) for _ in range(100)))
    ipaddress = '127.0.0.1'

    class Meta:
        model = reviews_models.Review

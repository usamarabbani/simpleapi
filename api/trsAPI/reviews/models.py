from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from rest_framework.authtoken.models import Token


class Company(models.Model):
    name = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.pk, self.name)


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    title = models.TextField(max_length=64)
    summary = models.TextField(max_length=10000)
    rating = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(5)])
    ipaddress = models.GenericIPAddressField()

    submitted_date = models.DateTimeField(null=True, blank=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    changed_date = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        self.deleted_date = timezone.now()
        self.save(update_fields=('deleted_date',))

    # DRYPermissions
    @staticmethod
    def has_read_permission(request):
        return request.user.is_authenticated

    def has_object_read_permission(self, request):
        return request.user.is_authenticated and request.user == self.user

    @staticmethod
    def has_write_permission(request):
        return request.user.is_authenticated

    def has_object_write_permission(self, request):
        return self.has_object_read_permission(request)

    def has_object_update_permission(self, request):
        return self.has_object_write_permission(request)

    @staticmethod
    def has_create_permission(request):
        return request.user.is_authenticated

    @staticmethod
    def has_remove_permission(request):
        return request.user.is_authenticated

    def has_object_remove_permission(self, request):
        return self.has_object_read_permission(request)

    @staticmethod
    def has_destroy_permission(request):
        return request.user.is_authenticated

    def has_object_destroy_permission(self, request):
        return self.has_object_read_permission(request)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

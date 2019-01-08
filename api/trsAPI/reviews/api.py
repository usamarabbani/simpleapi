import rest_framework.permissions
import rest_framework.viewsets

from dry_rest_permissions.generics import DRYPermissions

from trsAPI.reviews import serializers as reviews_serializers
from trsAPI.reviews import models as reviews_models


class UserViewSet(rest_framework.viewsets.ModelViewSet):
    serializer_class = reviews_serializers.UserSerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    model = reviews_serializers.User
    queryset = model.objects.filter(is_active=True)


class CompanyViewSet(rest_framework.viewsets.ModelViewSet):
    serializer_class = reviews_serializers.CompanySerializer
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    model = reviews_models.Company
    queryset = model.objects.all()


class ReviewViewSet(rest_framework.viewsets.ModelViewSet):
    serializer_class = reviews_serializers.ReviewSerializer
    permission_classes = (rest_framework.permissions.IsAuthenticated, DRYPermissions)
    model = reviews_models.Review
    queryset = model.objects.select_related(
        'user', 'company').filter(deleted_date__isnull=True)

    def filter_queryset(self, queryset):
        qs = super(ReviewViewSet, self).filter_queryset(queryset)
        return qs.filter(user=self.request.user)

from django.contrib.auth import get_user_model

import rest_framework.serializers

from trsAPI import reviews

User = get_user_model()


class UserSerializer(rest_framework.serializers.ModelSerializer):
    """ user serialiser """

    class Meta:
        model = User
        fields = '__all__'


class CompanySerializer(rest_framework.serializers.ModelSerializer):
    """ company serialiser """

    class Meta:
        model = reviews.models.Company
        fields = '__all__'


class ReviewSerializer(rest_framework.serializers.ModelSerializer):
    """ review serialiser """
    user = UserSerializer(read_only=True)
    user_id = rest_framework.serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=rest_framework.serializers.CurrentUserDefault(),
        source="user"
    )
    company = CompanySerializer(read_only=True)
    company_id = rest_framework.serializers.PrimaryKeyRelatedField(
        queryset=reviews.models.Company.objects.all(),
        source="company"
    )

    def validate_user_id(self, value):
        """
            request.user always
        """
        _request = self.context.get('request')
        return getattr(_request, 'user', None)

    class Meta:
        model = reviews.models.Review
        fields = '__all__'

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': 'Invalid email or password'
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        return token


class RegularTokenObtainPairSerializer(UserTokenObtainPairSerializer):

    def validate(self, attrs):
        customer = get_user_model().objects.filter(
            Q(email=attrs[self.username_field]) |
            Q(phone_number=attrs[self.username_field])).first()

        if customer is None:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        credentials = {
            self.username_field: customer.email,
            'password': attrs['password'],
        }

        return super(RegularTokenObtainPairSerializer, self).validate(credentials)

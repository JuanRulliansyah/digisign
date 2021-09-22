from django.contrib.auth import get_user_model, user_logged_in
from django.core.cache import cache
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import Throttled
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from digisign.auth.login_throttling import UserLoginAttemptsThrottle
from digisign.auth.serializers import UserTokenObtainPairSerializer, RegularTokenObtainPairSerializer, \
    RegularTokenObtainPairSerializer


class StaffTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
    throttle_classes = [UserLoginAttemptsThrottle]

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        if result.status_code == status.HTTP_200_OK:
            # Clear login attempts
            throttle = self.get_throttles()
            if throttle:
                throttle_key = throttle[0].get_cache_key(request, [])
                cache.delete(throttle_key)

            user = get_user_model().objects.filter(email=request.data['email']).first()
            if user.is_staff is not True:
                return Response({
                    'message': "You don't have permission to access this resource"
                }, status=status.HTTP_403_FORBIDDEN)

            user_logged_in.send(sender=type(user), request=request, user=user)
        return result

    def throttled(self, request, wait):
        raise Throttled(detail="Too many login attempts. Please try again in %(wait)d seconds" % {'wait': wait})


class RegularTokenObtainPairView(TokenObtainPairView):
    serializer_class = RegularTokenObtainPairSerializer
    throttle_classes = [UserLoginAttemptsThrottle]

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        if result.status_code == status.HTTP_200_OK:
            # Clear login attempts
            throttle = self.get_throttles()
            if throttle:
                throttle_key = throttle[0].get_cache_key(request, [])
                cache.delete(throttle_key)

            user = get_user_model().objects.filter(
                Q(email=request.data['email']) |
                Q(phone_number=request.data['email'])).first()
            user_logged_in.send(sender=type(user), request=request, user=user)
        return result

    def throttled(self, request, wait):
        raise Throttled(detail="Too many login attempts. Please try again in %(wait)d seconds" % {'wait': wait})

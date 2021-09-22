from collections import Counter

from django.contrib.auth import get_user_model
from rest_framework.throttling import SimpleRateThrottle


class UserLoginAttemptsThrottle(SimpleRateThrottle):
    scope = 'login_attempts'

    def get_cache_key(self, request, view):
        user = get_user_model().objects.filter(email=request.data['email']).first()
        identity = user.username if user else self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': identity
        }

    def allow_request(self, request, view):
        """
        Implement the check to see if the request should be throttled.

        On success calls `throttle_success`.
        On failure calls `throttle_failure`.
        """
        if self.rate is None:
            return True

        self.key = self.get_cache_key(request, view)
        if self.key is None:
            return True

        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        # Drop any requests from the history which have now passed the
        # throttle duration
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()
        if len(self.history) >= self.num_requests:
            return self.throttle_failure()

        # Drop any request if login attempts more then 3
        if len(self.history) >= 3:
            data = Counter(self.history)
            for key, value in data.items():
                if value == 2:
                    return self.throttle_failure()

        return self.throttle_success(request)

    def throttle_success(self, request):
        """
        Inserts the current request's timestamp along with the key
        into the cache.
        """
        user = get_user_model().objects.filter(email=request.data['email']).first()
        if user:
            self.history.insert(0, user.username)
        else:
            self.history.insert(0, self.get_ident(request))
        self.history.insert(1, self.now)
        self.cache.set(self.key, self.history, self.duration)
        return True

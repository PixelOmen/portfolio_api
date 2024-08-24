from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonMessageThrottle(AnonRateThrottle):
    scope = "anon_message"


class UserImageThrottle(UserRateThrottle):
    scope = "user_image"

    def allow_request(self, request, view):
        self.request = request  # Save the request to use in get_rate
        return super().allow_request(request, view)

    def get_rate(self):
        return super().get_rate()

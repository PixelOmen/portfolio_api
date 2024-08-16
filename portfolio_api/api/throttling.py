from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonMessageThrottle(AnonRateThrottle):
    scope = 'anon_message'


class UserImageThrottle(UserRateThrottle):
    scope = 'user_image'

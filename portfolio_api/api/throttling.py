from rest_framework.throttling import AnonRateThrottle


class AnonMessageThrottle(AnonRateThrottle):
    scope = 'anon_message'

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonBurstRateThrottle(AnonRateThrottle):
    rate = "10/min"
    scope = "burst_anon"


class AnonDailyThrottle(AnonRateThrottle):
    rate = "100/day"
    scope = "anon_message"


class UserBurstPostThrottle(UserRateThrottle):
    rate = "2/sec"
    scope = "burst_user_post_trx"


class UserDailyPostThrottle(UserRateThrottle):
    rate = "200/day"
    scope = "burst_user_post_trx"


class UserBurstImageThrottle(UserRateThrottle):
    rate = "20/min"
    scope = "burst_user_image_trx"


class UserDailyImageThrottle(UserRateThrottle):
    rate = "50/day"
    scope = "user_image_trx"

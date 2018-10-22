from datetime import datetime as orig_datetime


class datetime(orig_datetime):
    stubed_now = None
    stubed_utcnow = None

    @classmethod
    def now(cls, *args, **kwargs):
        if cls.stubed_now:
            return cls.stubed_now
        else:
            return super().now(*args, **kwargs)

    @classmethod
    def utcnow(cls, *args, **kwargs):
        if cls.stubed_utcnow:
            return cls.stubed_utcnow
        else:
            return super().utcnow(*args, **kwargs)

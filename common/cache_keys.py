class BaseCacheKey:
    VERSION = None
    DOMAIN = None

    @classmethod
    def _build(cls, *args):
        return ':'.join([cls.VERSION, cls.DOMAIN, *map(str, args)])


class HabitsCacheKey(BaseCacheKey):
    VERSION = 'v1'
    DOMAIN = 'habits'

    @classmethod
    def habits(cls, order_by: str) -> str:
        elements = []

        if order_by:
            elements.extend(['order_by', order_by])

        return cls._build(*elements)

    @classmethod
    def logs(cls, habit_id: int) -> str:
        return cls._build('logs', habit_id)
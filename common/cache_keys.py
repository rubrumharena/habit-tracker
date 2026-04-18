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
    def habits(cls, **kwargs) -> str:
        elements = []

        if any(kwargs):
            ordered_keys = sorted(kwargs.keys())
            for key in ordered_keys:
                elements.append(key)
                elements.extend(sorted(kwargs[key]))

        return cls._build(*elements)

    @classmethod
    def logs(cls, habit_id: int) -> str:
        return cls._build('logs', habit_id)
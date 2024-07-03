import logging

logger = logging.getLogger()


class FormatStore:
    def __init__(self):
        self.formatters = {}

    def register(self, func):
        logger.debug('Registering formatter: %s', func.__name__)
        self.formatters[func.__name__] = func

    def get(self, name):
        if name not in self.formatters:
            logger.warning(
                "Given formatter '%s' not found. Switching to default.",
                name
            )
            return self.formatters['default']
        return self.formatters[name]


# Global formatter manager
formatter_store = FormatStore()

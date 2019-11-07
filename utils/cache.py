import logging

from phishtray import settings
from django.core.cache import cache


logger = logging.getLogger(__name__)


def flush_cache():
    try:
        assert settings.CACHES
        cache.clear()
    except AttributeError:
        logger.exception("CACHES is not configured in settings.")

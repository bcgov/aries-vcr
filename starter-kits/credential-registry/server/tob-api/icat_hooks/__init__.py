import sys

if not any(
    k in sys.argv for k in ("collectstatic", "makemigrations", "migrate", "test")
):

    from .celery import app as celery_app

    __all__ = ["celery_app"]

from django.conf import settings


def live(request):
    return {"LIVE": not settings.DEBUG}

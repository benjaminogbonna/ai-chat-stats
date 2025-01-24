from django.utils import timezone

def readTimezoneCookie(request, activate: bool=True):
    gmt_offset = (request.COOKIES.get("GMT_OFFSET") or '').strip()
    if gmt_offset.replace('-', '').isdigit():
        tz = timezone.get_fixed_timezone(int(gmt_offset))
        if activate:
            timezone.activate(tz)
        return tz
    return None


def AutoBrowserTimezoneMiddleware(get_response):
    def middleware(request):
        readTimezoneCookie(request, activate=True)
        return get_response(request)
    return middleware
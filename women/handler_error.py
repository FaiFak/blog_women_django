from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def bad_request(request, exception):
    return HttpResponseBadRequest("<h1>Неверный запрос</h1>")


def denied_access(request, exception):
    return HttpResponseForbidden("<h1>Access is denied</h1>")


def server_error(request):
    return HttpResponseServerError("<h1>Server Error</h1>")

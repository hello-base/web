from django.contrib.sessions.middleware import SessionMiddleware


def add_session_to_request(request):
    # Annotate a request object with a session.
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    return request


def setup_view(view, request, *args, **kwargs):
    # Mimicks .as_view(), but returns the view instance instead of a
    # function. The arguments are similar to that of reverse().
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

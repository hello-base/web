from django.contrib.auth import authenticate


class OAuth2TokenMiddleware(object):
    """
    Middleware for OAuth2 user authentication.

    This middleware is able to work beside AuthenticationMiddleware
    and its behaviour depends on the order it's processed.

    If it comes *after* AuthenticationMiddleware and request.user is
    valid, leave request.user as is and do not not proceed with
    token validation. If request.user is AnonymousUser, proceed and
    try to authenticate the user using the OAuth2 access token.

    If it comes *before* AuthenticationMiddleware, or
    AuthenticationMiddleware is not used at all, try to authenticate the
    user with the OAuth2 access token and set `request.user`. Setting
    `request._cached_user` also makes AuthenticationMiddleware use that
    instead of the one from the existing session.

    """
    def process_request(self, request):
        # Do something only if request contains a Bearer token.
        if request.META.get('HTTP_AUTHORIZATION', '').startswith('Bearer'):
            if not hasattr(request, 'user') or request.user.is_anonymous():
                user = authenticate(request=request)
                if user:
                    request.user = request._cached_user = user

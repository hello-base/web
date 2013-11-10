import time

from django.conf import settings

from requests_oauthlib import OAuth2Session

config = {
    'authorization_url': getattr(settings, 'OAUTH_AUTHORIZATION_URL', ''),
    'client_id': getattr(settings, 'HELLO_BASE_CLIENT_ID', ''),
    'client_secret': getattr(settings, 'HELLO_BASE_CLIENT_SECRET', ''),
    'token_url': getattr(settings, 'OAUTH_TOKEN_URL', ''),
    'redirect_url': getattr(settings, 'OAUTH_REDIRECT_URL', ''),
}


def _clean_token(token):
    return {
        'access_token': token['access_token'],
        'token_type': token['token_type'],
        'refresh_token': token['refresh_token'],
        'expires_at': int(time.time() + token['expires_in'])
    }


def _token_updater(old_token, request):
    def wrapped(new_token):
        token = _clean_token(new_token)

        # Persist the new token... somehow.
        old_token.update(token)
        if hasattr(request, 'user'):
            user = request.user
            user.access_token = token['access_token']
            user.refresh_token = token['refresh_token']
            user.token_expiration = token['expires_at']
            user.save()
    return wrapped


def auth_session(request, token=None, state=None):
    if token and 'expires_at' in token:  # pragma: no branch
        token['expires_in'] = int(token['expires_at'] - time.time())

    return OAuth2Session(
        config['client_id'],
        redirect_uri=config['redirect_url'],
        auto_refresh_url=config['token_url'],
        auto_refresh_kwargs={
            'client_id': config['client_id'],
            'client_secret': config['client_secret']
        },
        token_updater=_token_updater(token, request),
        token=token,
        state=state,
    )


def auth_url(oauth):
    return oauth.authorization_url(config['authorization_url'])


def auth_token(oauth, response_url):
    token = oauth.fetch_token(
        config['token_url'],
        auth=(config['client_id'], config['client_secret']),
        authorization_response=response_url
    )
    return _clean_token(token)

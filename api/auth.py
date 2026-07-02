import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from types import SimpleNamespace
import jwt

logger = logging.getLogger(__name__)


class JWTUser(SimpleNamespace):
    @property
    def is_authenticated(self):
        return True


class JWTAuthentication(BaseAuthentication):
    """Simple JWT authentication compatible with external accessToken.

    Expected header: Authorization: Bearer <token>

    Configure the key in Django settings as `JWT_PUBLIC_KEY` (for RS algorithms)
    or `JWT_SECRET` (for HS algorithms). Also set `JWT_ALGORITHM` (default HS256).
    """

    def authenticate(self, request):
        auth = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION')
        if not auth:
            return None
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        token = parts[1]

        key = getattr(settings, 'JWT_PUBLIC_KEY', None) or getattr(settings, 'JWT_SECRET', None) or getattr(settings, 'SECRET_KEY')
        algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')
        issuer = getattr(settings, 'JWT_ISSUER', None)
        audience = getattr(settings, 'JWT_AUDIENCE', None)

        options = {'verify_aud': False}
        decode_kwargs = {'algorithms': [algorithm]}

        if issuer:
            decode_kwargs['issuer'] = issuer
        if audience:
            decode_kwargs['audience'] = audience
            options['verify_aud'] = True

        try:
            payload = jwt.decode(token, key, options=options, **decode_kwargs)
            if payload.get('type') != 'access':
                raise jwt.InvalidTokenError('Expected access token')
        except jwt.ExpiredSignatureError as exc:
            logger.warning('Expired access token: %s', exc)
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidAudienceError as exc:
            logger.warning('Invalid token audience: %s', exc)
            raise exceptions.AuthenticationFailed('Invalid audience')
        except jwt.InvalidIssuerError as exc:
            logger.warning('Invalid token issuer: %s', exc)
            raise exceptions.AuthenticationFailed('Invalid issuer')
        except jwt.InvalidTokenError as exc:
            logger.warning('Invalid JWT token: %s', exc)
            raise exceptions.AuthenticationFailed('Invalid token')

        user = JWTUser(payload=payload)
        return (user, payload)

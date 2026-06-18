import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import jwt


class LoginView(View):
    def get(self, request):
        return render(request, 'auth_test/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username != 'test' or password != 'test':
            return JsonResponse({'detail': 'Invalid credentials'}, status=401)

        now = datetime.utcnow()
        access_payload = {
            'type': 'access',
            'sub': username,
            'iss': getattr(settings, 'JWT_ISSUER', 'auth_test'),
            'aud': getattr(settings, 'JWT_AUDIENCE', 'lis_api'),
            'iat': now,
            'exp': now + getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME', timedelta(minutes=15)),
        }
        refresh_payload = {
            'type': 'refresh',
            'sub': username,
            'iss': getattr(settings, 'JWT_ISSUER', 'auth_test'),
            'aud': getattr(settings, 'JWT_AUDIENCE', 'lis_api'),
            'iat': now,
            'exp': now + getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME', timedelta(days=7)),
        }

        token = getattr(settings, 'JWT_SECRET', settings.SECRET_KEY)
        algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')

        access_token = jwt.encode(access_payload, token, algorithm=algorithm)
        refresh_token = jwt.encode(refresh_payload, token, algorithm=algorithm)

        response = JsonResponse({'access': access_token})
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=int(getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME', timedelta(days=7)).total_seconds()),
        )
        return response


@method_decorator(csrf_exempt, name='dispatch')
class TokenRefreshView(View):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return JsonResponse({'detail': 'Refresh token missing'}, status=401)

        token = getattr(settings, 'JWT_SECRET', settings.SECRET_KEY)
        algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')
        issuer = getattr(settings, 'JWT_ISSUER', 'auth_test')
        audience = getattr(settings, 'JWT_AUDIENCE', 'lis_api')

        try:
            payload = jwt.decode(
                refresh_token,
                token,
                algorithms=[algorithm],
                issuer=issuer,
                audience=audience,
                options={'verify_aud': True},
            )
            if payload.get('type') != 'refresh':
                raise jwt.InvalidTokenError('Expected refresh token')
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Refresh token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'detail': 'Invalid refresh token'}, status=401)

        now = datetime.utcnow()
        access_payload = {
            'type': 'access',
            'sub': payload.get('sub'),
            'iss': issuer,
            'aud': audience,
            'iat': now,
            'exp': now + getattr(settings, 'JWT_ACCESS_TOKEN_LIFETIME', timedelta(minutes=15)),
        }
        refresh_payload = {
            'type': 'refresh',
            'sub': payload.get('sub'),
            'iss': issuer,
            'aud': audience,
            'iat': now,
            'exp': now + getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME', timedelta(days=7)),
        }
        access_token = jwt.encode(access_payload, token, algorithm=algorithm)
        refresh_token = jwt.encode(refresh_payload, token, algorithm=algorithm)

        response = JsonResponse({'access': access_token})
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=int(getattr(settings, 'JWT_REFRESH_TOKEN_LIFETIME', timedelta(days=7)).total_seconds()),
        )
        return response

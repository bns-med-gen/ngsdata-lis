import json
from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import jwt


def index(request):
    # проверяем, запущен ли отладочный режим (сслыку на админку выводим только в нем)
    # для пущей безопасности, nginx не пропустит переход на url /admin/

    key = 'REMOTE_ADDR'
    local = None
    if key in request.META.keys():
        local = request.META['REMOTE_ADDR'] == '127.0.0.1'

    #if str(request.user) == 'AnonymousUser' or request.user.username == 'admin':
    context = {
        'local': local,
        'ngs_site_login': settings.NGS_ADDRESS + "lis_auth/"
    }
    return render(request, 'index.html', context)


def select_login_method(request):
    # проверяем, запущен ли отладочный режим (сслыку на админку выводим только в нем)
    # для пущей безопасности, nginx не пропустит переход на url /admin/

    key = 'REMOTE_ADDR'
    local = None
    if key in request.META.keys():
        local = request.META['REMOTE_ADDR'] == '127.0.0.1'

    # if str(request.user) == 'AnonymousUser' or request.user.username == 'admin':
    context = {
        'local': local,
        'ngs_site_login': settings.NGS_ADDRESS + "lis_auth/",
        'ngs_site': settings.NGS_ADDRESS,
    }
    return render(request, 'lis_auth/select_login_method.html', context)


def accept_token(request):
    """
    получаем токен от ngs-data
    - проверяем, что он валидный
    - отправляем данные в JS (будут сохранены в локальном хранилище)
    - указываем, куда перейти дальше
    """

    context = {
        'access_token': request.GET['access_token'],
        'refresh_token': request.GET['refresh_token'],
        'target_page': request.GET['target_page']
    }
    refresh_token = request.GET['refresh_token']

    response = render(request, 'lis_auth/accept_token.html', context)
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=int(settings.JWT_REFRESH_TOKEN_LIFETIME.total_seconds()),
    )
    return response


def token_gen(username):
    # username = request.POST.get('username')
    # password = request.POST.get('password')

    now = datetime.utcnow()
    access_payload = {
        'type': 'access',
        'sub': username,
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE,
        'iat': now,
        'exp': now + settings.JWT_ACCESS_TOKEN_LIFETIME,
    }
    refresh_payload = {
        'type': 'refresh',
        'sub': username,
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE,
        'iat': now,
        'exp': now + settings.JWT_REFRESH_TOKEN_LIFETIME,
    }

    jwt_key = settings.JWT_SECRET
    algorithm = settings.JWT_ALGORITHM

    access_token = jwt.encode(access_payload, jwt_key, algorithm=algorithm)
    refresh_token = jwt.encode(refresh_payload, jwt_key, algorithm=algorithm)
    return access_token, refresh_token


class LoginView(View):
    def get(self, request):
        return render(request, 'lis_auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username != 'test' or password != 'test':
            return JsonResponse({'detail': 'Invalid credentials'}, status=401)

        access_token, refresh_token = token_gen(username)
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

        jwt_key = settings.JWT_SECRET
        algorithm = settings.JWT_ALGORITHM
        issuer = settings.JWT_ISSUER
        audience = settings.JWT_AUDIENCE

        try:
            payload = jwt.decode(
                refresh_token,
                jwt_key,
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
            'exp': now + settings.JWT_ACCESS_TOKEN_LIFETIME,
        }
        refresh_payload = {
            'type': 'refresh',
            'sub': payload.get('sub'),
            'iss': issuer,
            'aud': audience,
            'iat': now,
            'exp': now + settings.JWT_REFRESH_TOKEN_LIFETIME,
        }
        access_token = jwt.encode(access_payload, jwt_key, algorithm=algorithm)
        refresh_token = jwt.encode(refresh_payload, jwt_key, algorithm=algorithm)

        response = JsonResponse({'access': access_token})
        response.set_cookie(
            'refresh_token',
            refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=int(settings.JWT_REFRESH_TOKEN_LIFETIME.total_seconds()),
        )
        return response

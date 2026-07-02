# Запустить backend (и открыть страницу в браузере)

    python manage.py runserver
перейти в http://127.0.0.1:8000/

# аутентификация
* внешняя аутентификация через NGS-DATA или через пароль администратора
* в любом случае при успешной аутентификации в храналище браузера записывается полученный токен доступа: LISAuth.setAccessToken(data.access);
* во вронтенде нужно использвать <script src="js/auth.js"></script> как в /home/nik/src/ngsdata-lis/frontend/card2medtest.html
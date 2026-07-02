document.addEventListener("DOMContentLoaded", function() {
    LISAuth.setAccessToken('{{access_token}}');
    //  Перенаправляем пользователя на главную страницу, убирая токен из URL
    window.location.href = '/{{target_page}}';
});
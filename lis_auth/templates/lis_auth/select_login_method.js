document.addEventListener("DOMContentLoaded", function() {
//    const ref = document.referrer;
//    // Проверяем, что реферер существует и ведет с вашего же сайта (внутренний переход)
//    if (ref && ref.includes(window.location.hostname)) {
//      const refUrl = new URL(ref);
//      // Записываем только относительный путь
//      document.getElementById('next-page-input').value = refUrl.pathname + refUrl.search;
//    }

    // если получили токен через сообщение
//    window.addEventListener('message', (event) => {
//      if (event.origin !== '{{ngs_site}}') return;  // Проверка безопасности
//      // сохраняем его и переходим на referrer
//      const token = event.data.token;
//      console.log('Токен получен:', token);
//      LISAuth.setAccessToken(data.access);
//      //window.location.href = document.referrer;
//    });
});
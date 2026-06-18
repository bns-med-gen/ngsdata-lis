(function(window) {
  const ACCESS_TOKEN_KEY = 'lis_access_token';

  function getAccessToken() {
    return localStorage.getItem(ACCESS_TOKEN_KEY) || null;
  }

  function setAccessToken(token) {
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
    } else {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
    }
  }

  function clearAccessToken() {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
  }

  function attachAuthHeaders(options = {}) {
    const token = getAccessToken();
    if (!options.headers) {
      options.headers = {};
    }
    if (token) {
      options.headers.Authorization = 'Bearer ' + token;
    }
    return options;
  }

  function refreshToken() {
    return $.ajax({
      url: 'http://localhost:8000/auth/refresh/',
      method: 'POST',
      xhrFields: { withCredentials: true },
      crossDomain: true
    });
  }

  window.LISAuth = {
    getAccessToken,
    setAccessToken,
    clearAccessToken,
    attachAuthHeaders,
    refreshToken
  };
})(window);

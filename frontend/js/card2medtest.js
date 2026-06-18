const API_BASE = 'http://localhost:8000/api';
let currentPage = 1;
let currentSearch = '';

function showAlert(message) {
  $('#search-alert').text(message).show();
}

function hideAlert() {
  $('#search-alert').hide();
}

function showToast(message, type = 'success') {
  const container = $('#toast-container');
  if (!container.length) return;
  const alertClass = type === 'danger' ? 'alert-danger' : 'alert-success';
  const toast = $(`<div class="alert ${alertClass}" role="alert"></div>`).text(message);
  toast.css({ 'min-width': '220px', 'margin-top': '6px', 'opacity': 0 });
  container.append(toast);
  toast.animate({ opacity: 1, right: '0px' }, 150);
  setTimeout(() => {
    toast.fadeOut(300, () => toast.remove());
  }, 2000);
}

function handleUnauthorized() {
  LISAuth.clearAccessToken();
  updateAuthStatus();
  showToast('Требуется повторная авторизация', 'danger');
}

function authenticatedRequest(options) {
  const requestOptions = $.extend(true, {}, options);
  requestOptions.xhrFields = $.extend(true, {}, requestOptions.xhrFields, { withCredentials: true });
  requestOptions.crossDomain = true;
  requestOptions.headers = requestOptions.headers || {};

  const token = LISAuth.getAccessToken();
  if (token) {
    requestOptions.headers.Authorization = 'Bearer ' + token;
  }

  const deferred = $.Deferred();
  const originalSuccess = requestOptions.success;
  const originalError = requestOptions.error;

  requestOptions.success = function(data, textStatus, jqXHR) {
    if (originalSuccess) {
      originalSuccess(data, textStatus, jqXHR);
    }
    deferred.resolve(data, textStatus, jqXHR);
  };

  requestOptions.error = function(jqXHR, textStatus, errorThrown) {
    if (jqXHR.status === 401 && !requestOptions._retry) {
      LISAuth.refreshToken()
        .done(function(data) {
          if (data.access) {
            LISAuth.setAccessToken(data.access);
            requestOptions._retry = true;
            requestOptions.headers.Authorization = 'Bearer ' + data.access;
            authenticatedRequest(requestOptions).then(deferred.resolve, deferred.reject);
          } else {
            handleUnauthorized();
            deferred.reject(jqXHR, textStatus, errorThrown);
          }
        })
        .fail(function() {
          handleUnauthorized();
          deferred.reject(jqXHR, textStatus, errorThrown);
        });
    } else {
      if (originalError) {
        originalError(jqXHR, textStatus, errorThrown);
      }
      deferred.reject(jqXHR, textStatus, errorThrown);
    }
  };

  $.ajax(requestOptions);
  return deferred.promise();
}

function authenticatedGetJSON(url) {
  return authenticatedRequest({ url, dataType: 'json', method: 'GET' });
}

function updateAuthStatus() {
  const token = LISAuth.getAccessToken();
  if (token) {
    $('#auth-status-text').text('Аутентифицирован');
    $('#login-link').hide();
    $('#logout-button').show();
  } else {
    $('#auth-status-text').text('Не аутентифицирован');
    $('#login-link').show();
    $('#logout-button').hide();
  }
}

function renderMedicalFiles(data) {
  const tbody = $('#medical-files-table tbody');
  tbody.empty();
  if (data.results.length === 0) {
    tbody.append('<tr><td colspan="5" class="text-center">Ничего не найдено</td></tr>');
    $('#medical-files-pagination').hide();
    $('#patients-row').hide();
    return;
  }

  data.results.forEach(item => {
    const row = $('<tr></tr>');
    row.append(`<td>${item.НомерКарты || ''}</td>`);
    row.append(`<td>${item.ДиагнозПриОбращении || ''}</td>`);
    row.append(`<td>${item.ВходящийДиагнозНеизвестен || ''}</td>`);
    row.append(`<td>${item.Примечание || ''}</td>`);
    row.data('medicalFileId', item.medicalFileId);
    row.on('click', () => {
      $('#medical-files-table tbody tr').removeClass('info');
      row.addClass('info');
      if (item.medicalFileId) {
        loadPatients(item.medicalFileId);
      }
    });
    tbody.append(row);
  });

  const firstItem = data.results[0];
  if (firstItem && firstItem.medicalFileId) {
    tbody.find('tr:first').addClass('info');
    loadPatients(firstItem.medicalFileId);
  }

  renderPagination(data, loadMedicalFiles);
  $('#results-panel').show();
}

function renderPagination(data, callback) {
  const pager = $('#medical-files-pagination ul');
  pager.empty();
  if (!data.previous && !data.next) {
    $('#medical-files-pagination').hide();
    return;
  }

  $('#medical-files-pagination').show();

  const addPageItem = (label, page, disabled) => {
    const li = $('<li></li>').addClass(disabled ? 'disabled' : '');
    const a = $('<a href="#"></a>').text(label);
    if (!disabled) {
      a.on('click', (e) => {
        e.preventDefault();
        callback(page);
      });
    }
    li.append(a);
    pager.append(li);
  };

  addPageItem('«', data.previous ? data.current_page - 1 : 1, !data.previous);
  addPageItem('»', data.next ? data.current_page + 1 : data.current_page, !data.next);
}

function loadMedicalFiles(page = 1) {
  currentPage = page;
  const cardNumber = currentSearch;
  const url = `${API_BASE}/medical-files/?page=${page}&page_size=20&search=${encodeURIComponent(cardNumber)}`;

  hideAlert();
  authenticatedGetJSON(url)
    .done(data => renderMedicalFiles(data))
    .fail(() => showAlert('Ошибка запроса к API medical_files.'));
}

function loadPatients(medicalFileId) {
  const url = `${API_BASE}/patients/?medicalFileID=${encodeURIComponent(medicalFileId)}&page=1&page_size=50`;

  authenticatedGetJSON(url)
    .done(data => {
      renderPatients(data, medicalFileId);
    })
    .fail(() => showAlert('Ошибка запроса к API patients.'));
}

function renderPatients(data, medicalFileId) {
  const tbody = $('#patients-table tbody');
  tbody.empty();
  $('#patients-info').text(`Пациенты для medicalFileID: ${medicalFileId}`);
  $('#medical-tests-row').hide();

  if (data.results.length === 0) {
    tbody.append('<tr><td colspan="6" class="text-center">Записей не найдено</td></tr>');
  } else {
    data.results.forEach(item => {
      const row = $('<tr></tr>');
      row.data('patientID', item.patientID);
      row.append(`<td>${item.patientCode || ''}</td>`);
      row.append(`<td>${item.ОтношениеКОбратившемуся || ''}</td>`);
      row.append(`<td>${item.Пол || ''}</td>`);
      row.append(`<td>${item.ДатаРождения || ''}</td>`);
      row.append(`<td>${item.Регион || ''}</td>`);
      row.append(`<td>${item.НомерКарты || ''}</td>`);
      row.on('click', () => {
        $('#patients-table tbody tr').removeClass('info');
        row.addClass('info');
        if (item.patientID) {
          loadMedicalTests(item.patientID);
        }
      });
      tbody.append(row);
    });
    tbody.find('tr:first').addClass('info');
    loadMedicalTests(data.results[0].patientID, true);
  }

  $('#patients-row').show();
}

function loadMedicalTests(patientId, autoLoad = false) {
  $('#medical-tests-info').text(`medical_tests для patientId: ${patientId}`);
  const testsTableBody = $('#medical-tests-table tbody');
  testsTableBody.empty();
  $('#biomater-list').text('Загружаем medicalTestId...');

  const testSamplesUrl = `${API_BASE}/test-samples/?patientId=${encodeURIComponent(patientId)}&page=1&page_size=100`;

  authenticatedGetJSON(testSamplesUrl)
    .done(data => {
      const medicalTestIds = [...new Set(data.results.map(item => item.medicalTestId).filter(Boolean))];
      $('#biomater-list').text(`Найдено medicalTestId: ${medicalTestIds.join(', ')}`);
      if (medicalTestIds.length === 0) {
        testsTableBody.append('<tr><td colspan="6" class="text-center">Нет связанных исследований</td></tr>');
        $('#medical-tests-row').show();
        return;
      }

      const encodedIds = medicalTestIds.map(id => encodeURIComponent(id)).join('&medicalTestId=');
      const medicalTestsUrl = `${API_BASE}/medical-tests/?page=1&page_size=100&medicalTestId=${encodedIds}`;

      authenticatedGetJSON(medicalTestsUrl)
        .done(testData => {
          if (testData.results.length === 0) {
            testsTableBody.append('<tr><td colspan="6" class="text-center">Нет medical_tests для найденных medicalTestId</td></tr>');
          } else {
                testData.results.forEach(item => {
                  const row = $('<tr></tr>');
                  row.append(`<td>${item.medicalTestId || ''}</td>`);
                  row.append(`<td>${item.medicalTestCode || ''}</td>`);
                  row.append(`<td>${item.НазваниеПункта || ''}</td>`);
                  row.append(`<td>${item.ДатаНаправления || ''}</td>`);
                  row.append(`<td>${item.ДатаОплаты || ''}</td>`);
                  row.append(`<td>${item.ТипОплаты || ''}</td>`);
                  row.css('cursor', 'pointer');
                  row.on('click', () => {
                    const id = item.medicalTestId || '';
                    if (!id) {
                      showToast('medicalTestId отсутствует для этой записи.', 'danger');
                      return;
                    }
                    if (navigator.clipboard && navigator.clipboard.writeText) {
                      navigator.clipboard.writeText(id).then(() => {
                        showToast(`Скопировано medicalTestId: ${id}`, 'success');
                      }).catch(() => {
                        showToast('Не удалось скопировать в буфер обмена.', 'danger');
                      });
                    } else {
                      // Fallback for older browsers
                      const tmp = $('<input>');
                      $('body').append(tmp);
                      tmp.val(id).select();
                      try {
                        document.execCommand('copy');
                        showToast(`Скопировано medicalTestId: ${id}`, 'success');
                      } catch (e) {
                        showToast('Браузер не поддерживает копирование в буфер.', 'danger');
                      }
                      tmp.remove();
                    }
                  });
                  testsTableBody.append(row);
                });
              }
          $('#medical-tests-row').show();
        })
        .fail(() => {
          showAlert('Ошибка запроса к API medical_tests.');
        });
    })
    .fail(() => {
      showAlert('Ошибка запроса к API test_samples.');
    });
}

$(document).ready(() => {
  updateAuthStatus();
  if (!LISAuth.getAccessToken()) {
    LISAuth.refreshToken()
      .done(function(data) {
        if (data.access) {
          LISAuth.setAccessToken(data.access);
          showToast('Токен автоматически обновлён.', 'success');
        }
      })
      .always(updateAuthStatus);
  }

  $('#logout-button').on('click', function() {
    LISAuth.clearAccessToken();
    updateAuthStatus();
    showToast('Вышли из системы.', 'success');
  });

  $('#search-form').on('submit', (event) => {
    event.preventDefault();
    currentSearch = $('#card-number').val().trim();
    if (!currentSearch) {
      showAlert('Введите номер карты для поиска.');
      return;
    }
    loadMedicalFiles(1);
  });
});

// Скрипт для сайта объявлений

// Функция для инициализации всех компонентов
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всплывающих подсказок
    initTooltips();
    
    // Инициализация валидации форм
    initFormValidation();
    
    // Инициализация динамического поиска
    initDynamicSearch();
    
    // Инициализация предпросмотра изображений
    initImagePreview();
});

// Инициализация всплывающих подсказок Bootstrap
function initTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Валидация форм
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Динамический поиск (без перезагрузки страницы)
function initDynamicSearch() {
    const searchForm = document.getElementById('dynamic-search-form');
    if (!searchForm) return;
    
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(searchForm);
        const searchParams = new URLSearchParams();
        
        for (const pair of formData) {
            searchParams.append(pair[0], pair[1]);
        }
        
        fetch(`/search/?${searchParams.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById('search-results').innerHTML = html;
        })
        .catch(error => {
            console.error('Ошибка при поиске:', error);
        });
    });
}

// Предпросмотр изображений при загрузке
function initImagePreview() {
    const imageInput = document.getElementById('id_avatar');
    if (!imageInput) return;
    
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const previewElement = document.getElementById('avatar-preview');
                if (previewElement) {
                    previewElement.src = e.target.result;
                    previewElement.style.display = 'block';
                }
            }
            reader.readAsDataURL(file);
        }
    });
}

// Функция для подтверждения действий
function confirmAction(message) {
    return confirm(message || 'Вы уверены?');
}

// Функция для отображения уведомлений
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Автоматически скрыть уведомление через 5 секунд
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

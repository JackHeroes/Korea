document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("form-contact");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        var formData = new FormData(form);
        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data.status === 'success') {
                showAlert('success', 'Formulário enviado com sucesso!');
                form.reset();
            } else if (data.status === 'error') {
                showAlert('error', 'Erro ao enviar formulário: ' + data.message);
            }
        })
        .catch(function(error) {
            showAlert('error', 'Erro ao enviar formulário.');
        });
    });

    function showAlert(type, message) {
        var alertContainer = document.getElementById('alert-container');
        var alertClass = type === 'success' ? 'alert-success' : 'alert-danger';
        var alertHTML = '<div class="alert ' + alertClass + '">' + message + '</div>';
        alertContainer.innerHTML = alertHTML;
        setTimeout(function() {
            alertContainer.innerHTML = '';
        }, 5000); 
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
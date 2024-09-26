var modal = $('#modal-system');

$(document).ready(function () {
    // Get Clients Form to Create or Edit
    $('#clientsList').on('click', '.get-client-form', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = [];
        params['url'] = url;
        AjaxGETClientForm(params);
    });

    // Save client after click save-client class
    modal.on('click', '.save-client', function (event) {
        event.preventDefault();
        var btn = $(this);
        var form = btn.closest('form');
        var url = form.attr('action');
        var params = [];
        params['url'] = url;
        params['method'] = form.attr('method');
        params['query'] = form.serialize();
        AjaxPOSTClientForm(params);
    });
});


// Functions

function AjaxGETClientForm(params) {
    $.ajax({
        url: params['url'],
        type: 'GET',
        success: function (data) {
            modal.find('.modal-content').html(data.template);
            modal.modal();
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}


function AjaxPOSTClientForm(params) {
    $.ajax({
        url: params['url'],
        type: params['method'],
        data: params['query'],
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        },
        success: function (data) {
            notification[data.valid](data.message);

            if (data.valid === 'success') {
                if (params['method'] === 'PUT')
                    $('.clients-list').find(".get-client-form[href='" + params['url'] + "']").closest('tr').replaceWith(data.item);
                else
                    $('.clients-list tbody').prepend(data.item);
                modal.modal('hide');

                setTimeout(function () {
                    location.reload();
                }, 2000);
            }
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}
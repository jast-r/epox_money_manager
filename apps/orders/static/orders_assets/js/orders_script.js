var modal = $('#modal-system');

$(function () {
    // Get Orders Form to Create or Edit
    $('#ordersList').on('click', '.get-order-form', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = [];
        params['url'] = url;
        AjaxGETOrderForm(params);
    });

    $('#ordersList').on('click', '.delete-order', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = [];
        params['url'] = url;
        AjaxDeleteOrder(params);
    });

    // Save order after click save-order class
    modal.on('click', '.save-order', function (event) {
        event.preventDefault();
        var btn = $(this);
        var form = btn.closest('form');
        var url = form.attr('action');
        var params = [];
        params['url'] = url;
        params['method'] = form.attr('method');
        params['query'] = form.serialize();
        AjaxPOSTOrderForm(params);
    });
});


// Functions

function AjaxGETOrderForm(params) {
    $.ajax({
        url: params['url'],
        type: 'GET',
        success: function (data) {
            modal.find('.modal-content').html(data.template);
            modal.modal('show');
        },
        error: function () {
            notification.error('Error occurred');
        }
    });
}

function AjaxPOSTOrderForm(params) {
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
                    $('.orders-list').find(".get-order-form[href='" + params['url'] + "']").closest('tr').replaceWith(data.item);
                else
                    $('.orders-list tbody').append(data.item);
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


function AjaxDeleteOrder(params) {
    $.ajax({
        url: params['url'],
        type: 'DELETE',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        },
        success: function (data) {
            notification[data.valid](data.message);
            if (data.valid === 'success') {
                $('.orders-list').find(".get-order-form[href='" + params['url'] + "']").closest('tr').remove();
            }
        }
    });
}
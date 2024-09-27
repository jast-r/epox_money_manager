var modal = $('#modal-system');

$(function () {
    // Get Products Form to Create or Edit
    $('#productsList').on('click', '.get-product-form', function (event) {
        console.log("AAAAAAA")
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = [];
        params['url'] = url;
        AjaxGETProductForm(params);
    });

    // Save product after click save-product class
    modal.on('click', '.save-product', function (event) {
        event.preventDefault();
        var btn = $(this);
        var form = btn.closest('form');
        var url = form.attr('action');
        var params = [];
        params['url'] = url;
        params['method'] = form.attr('method');
        params['query'] = form.serialize();
        AjaxPOSTProductForm(params);
    });
});


// Functions

function AjaxGETProductForm(params) {
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


function AjaxPOSTProductForm(params) {
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
                    $('.products-list').find(".get-product-form[href='" + params['url'] + "']").closest('tr').replaceWith(data.item);
                else
                    $('.product-list tbody').prepend(data.item);
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
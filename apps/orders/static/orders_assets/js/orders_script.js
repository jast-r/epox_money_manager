var modal = $('#modal-system');

$(function () {
    // Get Orders Form to Create or Edit
    $('#ordersList').on('click', '.get-order-form', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = {};
        params['url'] = url;
        AjaxGETOrderForm(params);
    });
    
    $('#ordersList').on('click', '.delete-order', function (event) {
        event.preventDefault();
        var btn = $(this);
        var url = btn.attr('href');
        var params = {};
        params['url'] = url;
        AjaxDeleteOrder(params);
    });

    // Save order after click save-order class
    modal.on('click', '.save-order', function (event) {
        event.preventDefault();
        var btn = $(this);
        var form = btn.closest('form');
        var url = form.attr('action');
        var method = form.attr('method');
    
        // Сбор данных всех строк продукта
        let products = getProductsArray();
    
        // Сериализация данных формы (все поля, кроме продуктов)
        let formData = form.serializeArray();
    
        // Удаляем все поля, относящиеся к продуктам, чтобы добавить их позже отдельно
        formData = formData.filter(function (field) {
            return field.name !== 'product' && field.name !== 'quantity' && field.name !== 'sell_price';
        });
    
        // Проверяем, что есть продукты для отправки
        if (products.length > 0) {
            products.forEach(product => {
                // Копируем formData для каждого продукта
                let productFormData = formData.slice(); // Создаем копию массива
    
                // Добавляем ID продукта и количество в данные формы
                productFormData.push({ name: 'product', value: product.id });
                productFormData.push({ name: 'quantity', value: product.quantity });
                productFormData.push({ name: 'sell_price', value: product.sell_price });
    
                // Преобразуем данные в нужный формат для отправки
                let params = {
                    url: url,
                    method: method,
                    query: $.param(productFormData) // Преобразуем данные в строку запроса
                };
    
                // Отправляем запрос для каждого продукта
                AjaxPOSTOrderForm(params);
            });
        } else {
            notification.error('No products to save.');
        }
    });

    // Add new product row into order form
    modal.on('click', '.add-product-into-order', function (event) {
        event.preventDefault(); // Предотвращаем стандартное поведение
        let productContainer = document.querySelector('.product-group').parentNode;
        let newProductGroup = document.querySelector('.product-group').cloneNode(true);
        clearFormInputs(newProductGroup);
        productContainer.insertBefore(newProductGroup, this.closest('.d-grid'));
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
                if (params['method'] === 'PUT') {
                    $('.orders-list').find(".get-order-form[href='" + params['url'] + "']").closest('tr').replaceWith(data.item);
                } else {
                    $('.orders-list tbody').prepend(data.item);
                }
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

function clearFormInputs(element) {
    let inputs = element.querySelectorAll('input');
    inputs.forEach(function (input) {
        input.value = ''; // Очищаем значения инпутов
    });
}

function getProductsArray() {
    const products = [];

    // Находим все строки с продуктами
    const productRows = document.querySelectorAll('.product-group');

    productRows.forEach(row => {
        // Получаем ID продукта и количество из соответствующих полей
        const productID = row.querySelector('.product_name select').value;
        const productQuantity = row.querySelector('.product_quantity input').value;
        const productSellPrice = row.querySelector('.product_sell_price input').value;

        // Добавляем продукт только если оба значения заданы
        if (productID && productQuantity) {
            products.push({
                id: productID, // Используем ID продукта
                quantity: parseInt(productQuantity, 10),
                sell_price: parseInt(productSellPrice, 10)
            });
        }
    });

    return products;
}
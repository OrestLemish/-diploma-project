$(document).ready(function () {

    let curent_user_is_busy = false

    // загальна функція для відкриття модалки
    function openModal(url, data) {
        console.log(data)
        $.ajax({
            url: url,
            data: data,
            type: 'GET',
            success: function (response) {
                $(document.body).append(response);
            }
        });
    }


    function sendData(url, method, data) {
        console.log("data", data)
        $.ajax({
            url: url,
            type: method,
            data: data,
            headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
            success: function (response) {
                if (response.success === true) {
                    location.reload();
                } else {
                    console.log(response.errors);
                }
                // if (successCallback) {
                //     successCallback(response);
                // }
            }
        });
    }

    function execCommand(data) {
        const url = `/modal_command_execute/`;

        if (curent_user_is_busy === false) {
            curent_user_is_busy = true
            $.ajax({
                url: url,
                type: "Post",
                data: data,
                headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
                success: function (response) {
                    if (response.success === true) {
                        alert(response.response)
                    } else {

                    }
                }
            });
            curent_user_is_busy = false
        }else {
            alert("куда летиш?? успокойся")
        }

    }


    $('.open_modal_standard_command_execute').click(function () {
        const url = `/modal_standard_command_execute`;
        const data = {
            "command_text": $(this).data("command_text")
        }
        openModal(url, data);

    });

    $('.open_modal_command_execute').click(function () {
        const url = `/modal_command_execute`;
        const data = {
            "command_text": $('.command_area').val()
        }
        openModal(url, data);

    });


    $('body').on('click', '.modal_submit_exec_command', function () {

        const data = {
            "command_text": $('.command_area_modal').val(),
            "server_id": $(".server_detail").data('server_id'),
        }
        execCommand(data);


    });

    $('body').on('click', '.modal_submit_exec_standard_command', function () {

        let formData = $('#exec_standard_command_form').serialize();
        console.log(formData)
        let command_text = $('.command_area_modal').val()


        let formDataObject = {};
        formData.split('&').forEach(function (item) {
            let parts = item.split('=');
            let key = decodeURIComponent(parts[0]);
            let value = decodeURIComponent(parts[1]);
            formDataObject[key] = value;
        });

        console.log(formDataObject)

        for (const key in formDataObject) {
            if (formDataObject.hasOwnProperty(key)) {
                const regex = new RegExp('#' + key + '#', 'g');
                command_text = command_text.replace(regex, formDataObject[key]);
            }
        }
        command_text = command_text.split("?")[0]
        console.log(command_text)

        const data = {
            "command_text": command_text,
            "server_id": $(".server_detail").data('server_id'),
        }

        execCommand(data);

    });


    $('.open_modal_delete').click(function () {
        const model_name = $(this).data('model_name');
        const object_id = $(this).data('object_id');
        const url = `/modal_delete_object/${model_name}/${object_id}`;

        openModal(url);
    });

    $('.open_modal_edit').click(function () {
        const model_name = $(this).data('model_name');
        const object_id = $(this).data('object_id');
        const url = `/modal_edit_object/${model_name}/${object_id}`;

        openModal(url);
    });
    $('.open_modal_add').click(function () {
        const model_name = $(this).data('model_name');
        const url = `/modal_add_object/${model_name}`;

        openModal(url);
    });

    $('body').on('click', '.modal_submit_delete', function () {
        const model_name = $(this).data('model_name');
        const object_id = $(this).data('object_id');
        const url = `/modal_delete_object/${model_name}/${object_id}/`;

        sendData(url, "POST");
    });


    $(document).on('click', '.modal_submit_edit', function () {
        const model_name = $(this).data('model_name');
        const object_id = $(this).data('object_id');
        const url = `/modal_edit_object/${model_name}/${object_id}/`;
        const formData = $('#edit_form').serialize();

        sendData(url, "POST", formData);
    });

    $(document).on('click', '.modal_submit_add', function () {
        const model_name = $(this).data('model_name');
        const url = `/modal_add_object/${model_name}/`;
        const formData = $('#add_form').serialize();

        sendData(url, "POST", formData);
    });


    $(document).on('click', '.modal_cancel', function (e) {
        if (e.target === this) {
            $('.modal_overlay').remove();
        }

    });

});



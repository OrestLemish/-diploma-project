$(document).ready(function () {



    $('.check_server').click(function () {
        const server_id = $(".server_detail").data('server_id');
         let url
        if (server_id) {
            url = `/check_server/${server_id}/`;
        } else {
            url = `/check_server/0/`;
        }



        $.ajax({
            url: url,
            type: 'POST',
            headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
            success: function (response) {
                if (response.success === true) {
                    location.reload();
                    console.log(response.data)
                } else {
                    location.reload();
                    alert("кринж")
                }
                // if (successCallback) {
                //     successCallback(response);
                // }
            }
        });
    });


});



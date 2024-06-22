$(document).ready(function () {

    // Обробник для кнопки додавання
    $('.exit_block').click(function () {
        $('.modal_logout').addClass("active")
    });


    // Обробник для кнопки відміни
    $(document).on('click', '.modal_logout_cancel', function (e) {
        if (e.target === this) {
            $('.modal_logout').removeClass("active")
        }

    });

});



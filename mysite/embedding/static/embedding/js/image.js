function async_call() {
    let original_text = $("textarea[name='text']");
    let csrf = $("input[name='csrfmiddlewaretoken']");
    let generated_img = $("img[name='generated_img']");
    generated_img.hide();
    $("div[name='spinner").show();
    $.ajax({
        type: 'POST',
        url: "/image_async/",
        data: {
            original_text: original_text.val(),
            csrfmiddlewaretoken: csrf.val(),
        },
        success: function (response) {
            generated_img.attr('src', response);
            $("div[name='spinner").hide();
            generated_img.show();
        },
    })
}

function init() {
    $('.send-button').click(function () {
        async_call();
        return false;
    });
}

$(document).ready(function () {
    init();
})
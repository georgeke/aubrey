var app = (function ($) {
    var DEFAULT_DESC = "Drake",
        LOADING_DESC = "Loading...";

    function callTheHotline() {
        event.preventDefault();
        var question = $("#question").val();
        var description = $("#description");

        $.get("/hotline?question=" + question, function(data, status, response) {
            if (response.readyState == 4 && response.status == 200) {
                $("#bling").text(response.responseText).show();
                description.text(DEFAULT_DESC);
                description.removeClass("flashing");
                description.hide();
                $("body div img").hide();
                $("#question").prop('disabled', true);
            }
        });

        $("button").prop('disabled', true);
        description.text(LOADING_DESC).addClass("flashing");
    }

    $( document ).ready(function () {
        $("#question").keyup(function () {
            length = $(this).val().length;
            console.log(length)
            if (length > 33) {
                $(this).css("font-size", "0.9em");
            } else if (length > 25) {
                $(this).css("font-size", "1.3em");
            } else if (length > 18) {
                $(this).css("font-size", "1.5em");
            } else {
                $(this).css("font-size", "2em");
            }
        });
    });

    return {
        callTheHotline: callTheHotline
    }
})(jQuery);

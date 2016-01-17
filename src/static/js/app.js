var app = (function ($) {
    var DEFAULT_DESC = "Drake",
        LOADING_DESC = "Loading...";

    function callTheHotline() {
        event.preventDefault();
        var question = $("#question").val();

        $.get("/hotline?question=" + question, function(data, status, response) {
            if (response.readyState == 4 && response.status == 200) {
            $("#bling").text(response.responseText);
            }
        });

        var description = $("#description")
        description.text(LOADING_DESC);
        description.addClass("flashing");
    }

    return {
        callTheHotline: callTheHotline
    }
})(jQuery);

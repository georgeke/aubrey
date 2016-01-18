var app = (function ($) {
    var DEFAULT_DESC = "Drake",
        LOADING_DESC = "Dialing...",
        DEFAULT_BUTTON = "Send",
        RESTART_BUTTON = "Call again",
        waitingToRestart = false;

    function _showLoading() {
        $("button").prop('disabled', true);
        $("#description").text(LOADING_DESC).addClass("flashing");
    }

    function _showAnswer(answer) {
        var description = $("#description");
        description.text(DEFAULT_DESC);
        description.removeClass("flashing");
        description.fadeOut();
        $("#question").prop('disabled', true);
        $("body div img").fadeOut('slow', function () {
            $("#bling").text(answer).fadeIn();
        });

        $("button").text(RESTART_BUTTON).prop('disabled', false);
        waitingToRestart = true;
    }

    function _showError() {
        _showAnswer("Invalid question, please try again!")
    }

    function _resetApp() {
        $("button").text(DEFAULT_BUTTON);
        waitingToRestart = false;
        $("#bling").fadeOut('slow', function () {
            $("body div img").fadeIn();
            $("#description").fadeIn();
            $("#question").prop('disabled', false).val("");
        });
    }

    function callTheHotline() {
        event.preventDefault();

        if (waitingToRestart) {
            _resetApp();
            return;
        }

        var question = $("#question").val();

        $.get("/aubrey/hotline?question=" + question, function(data, status, response) {
            if (response.readyState == 4 && response.status == 200) {
                _showAnswer(response.responseText);
            }
        }).fail(function () {
            _showError();
        });

        _showLoading();
    }

    $( document ).ready(function () {
        $("#question").keydown(function () {
            length = $(this).val().length;
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

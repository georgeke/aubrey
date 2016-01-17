function callTheHotline() {
    var question = $("#question").val();

    $.get("/hotline?question=" + question, function(data, status, response) {
      if (response.readyState == 4 && response.status == 200) {
        $("#bling").text(response.responseText);
      }
    });

    event.preventDefault();
    return false;
}
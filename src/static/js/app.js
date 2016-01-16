function callTheHotline() {
    var question = document.getElementById("question").value;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (xhttp.readyState == 4 && xhttp.status == 200) {
        document.getElementById("bling").innerHTML = xhttp.responseText;
      }
    };
    xhttp.open("GET", "/hotline?question=" + question, true);
    xhttp.send();
}
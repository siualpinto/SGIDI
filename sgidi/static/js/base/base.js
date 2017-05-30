/**
 * Created by lsmor on 20/02/2017.
 */

// Get the modal
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];


// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    $('#modal_content').empty();
    modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === modal) {
        $('#modal_content').empty();
        modal.style.display = "none";
    }
};

var  blink = $('.blink_me');
function blinker()
{
    blink.fadeOut(500);
    blink.fadeIn(500);
}
if(blink.text() > 0)
{
    setInterval(blinker, 2000);
}
else
{
    blink.remove();
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != "") {
                var cookies = document.cookie.split(";");
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + "=")) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

$("#global_search").click(function () {
    var valor = $('#global_value').val();
    $.ajax({
        type:"GET",
        url: "/search",
        data: {
            "query":valor
        },
        dataType: "json",
        success: function (data) {
            if (data) {
                var resultados = JSON.parse(data.resultados);
                var modalContent = $('#modal_content');
                var html = "";
                modalContent.empty();
                html +=("<ul>");
                for(var i=0 ; i<resultados.length ; i++){
                    console.log(resultados[i].model);
                    html +=("<li><div style='color: red;'>"+resultados[i].model+"</div>");
                    for(var key in resultados[i].fields){
                        if(resultados[i].fields.hasOwnProperty(key)){
                            html +="<b>"+key+": </b>"+ resultados[i].fields[key]+"  ";
                        }
                    }
                   html +="</li>";
                }
                html +="</ul>";
                modalContent.append(html);
                modal.style.display = "block";
            }
        }
    });
});


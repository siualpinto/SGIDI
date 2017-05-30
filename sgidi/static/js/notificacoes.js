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


function my_special_notification_callback(data) {
    $('#notificacoes').empty();
    if(data.unread_list.length===0){
        $('#notificacoes').append("Não tem notificações");
        return;
    }

    for (var i = 0; i < data.unread_list.length; i++) {
        msg = data.unread_list[i];
        type = msg.description.split("-")[0];
        if (type === "tag") {
            id = msg.description.split("-")[1];
            $('#notificacoes').append("<div class='col-md-12'><div class='col-md-8'><a href='/conhecimentos/" + id + "'<p>" + msg.actor + ' ' + msg.verb + "</p></a></div><div class='col-md-4'> <button class='alert-danger conhecimento' id='notificacao_"+msg.id+"'>Eliminar notificação</button></div></div></div>");
            $("#notificacao_"+msg.id+"").click(function () {
                var notificacao_id = this.getAttribute("id").split("_")[1];
                $.ajax({
                    type:"POST",
                    url: "/notificacoes/apagar_notificacao/",
                    data: {
                        "notificacao_id": notificacao_id
                    },
                    dataType: "json",
                    success: function (data) {
                        if (data) {
                            alert("Notificação apagada: "+ (data.notificacao ? "Sucesso" : "Falhou"));
                            if(data.notificacao)
                                location.reload();
                        }
                    }
                });
            });
        }
        else if (type === "atividades"){
            descricao = msg.description.split("-")[1];
            $('#notificacoes').append("<div class='col-md-12'><div class='col-md-8'><a href='/interfaces/'<p>" + msg.verb+" "+ descricao + "</p></a></div><div class='col-md-4'> <button class='alert-danger conhecimento' id='notificacao_"+msg.id+"'>Eliminar notificação</button></div></div></div>");
            $("#notificacao_"+msg.id+"").click(function () {
                var notificacao_id = this.getAttribute("id").split("_")[1];
                $.ajax({
                    type:"POST",
                    url: "/notificacoes/apagar_notificacao/",
                    data: {
                        "notificacao_id": notificacao_id
                    },
                    dataType: "json",
                    success: function (data) {
                        if (data) {
                            alert("Notificação apagada: "+ (data.notificacao ? "Sucesso" : "Falhou"));
                            if(data.notificacao)
                                location.reload();
                        }
                    }
                });
            });
        }
    }
}


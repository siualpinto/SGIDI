/*
 * Modificação do estado do radio button para a escolha de outro tipo de ideia
 *
 * */
$("input[type='radio']").change(function () {
    var outra_text = $("#radio_outra_text");
    if ($("#radio_outra").is(":checked"))
    {
        outra_text.prop("disabled",false);
        outra_text.prop("required",true);
    }
    else
    {
        outra_text.prop("disabled",true);
        outra_text.prop("required",false);
    }
});

function calcularTotal() {
    var sum1 = 0;
    var sum2 = 0;
    var total;
    var table = $("#tabela_avaliacao");
    var x = 0;
    table.find("tr").siblings(":not(:first-child):not(:last-child)").each(function () {
        var tipo = $(this).find("td > i > input").val();
        var peso = $(this).find("td > input").last().val();
        sum1 += tipo * peso;
        sum2 += 5 * peso;
    });
    total = sum1 / sum2;
    table.find("tr:last-child > td:last-child").html((Math.round(total*100)).toString()+"%");
}
calcularTotal();

/*
 * Adicionar uma linha, depois da penultima linha da tabela de analise
 * Novas linhas são editáveis
 * */
$(".add_line").click(function () {
    var table = $("#tabela_avaliacao");
    var rows = table.find("tr").length;
    if( rows < 17) {
        var penultimate_tr = table.find("tr:nth-last-child(2)");
        penultimate_tr.after("<tr><td contenteditable>exemplo<input type='hidden' name='avaliacao"+penultimate_tr.index()+"' class='tabela_avaliacao' maxlength='110' size='50' value='exemplo'></tdcontenteditable>" +
            "<td><i class='fa fa-times smallicon'><input type='hidden' name='tipo" + penultimate_tr.index() + "' value='1'></i></td>" +
            "<td></td><td></td><td></td><td></td>" +
            "<td><input type='text' class='pesos' name='peso"+ (rows - 2) +"' id='peso" + (rows - 2) + "' value='1' size='2' maxlength='2'></td></tr>");
        calcularTotal();
    }
});

/*
 * Eliminar uma linha, depois da penultima linha da tabela de analise
 *
 * */
$(".delete_line").click(function () {
    var table = $("#tabela_avaliacao");
    if(table.find("> tbody:last-child").children().length != 10)
        table.find("> tbody:last-child").children().last().prev().remove();
    calcularTotal();
});

/*
 * O utilizador pode inserir uma cruz na avaliação desejada (muito fraco, ..., Muito Bom) para cada linha
 *
 * */
$("#tabela_avaliacao").on("click", "td:not(:first-child):not(:last-child)", function() {
    if($(this).parent().not("tr:not(:last-child)").length != 1){
        var row = ($(this).parent().index())-1;
        $(this).siblings().children().remove("i");
        $(this).html("<i class='fa fa-times smallicon'><input type='hidden' name='tipo"+row+"' value='"+$(this).index()+"'></i>");
        calcularTotal();
    }
});

$("#tabela_avaliacao").on("change", ".pesos", function () {
    if (!this.value.match(/^[0-9]{1,2}(?!\d)$/))
        this.value = this.value.replace(/[^0-9]/g, "");
    if(this.value == "")
        this.value = 1;
    calcularTotal();
});
//TODO ADICIONAR KEYUP EVENT A TODOS NOVAS LINHAS
//TODO BUG LIMITAR OS CARACTERES DA AVALICAO PK VAI APAGAR O ELEMENTO INPUT
//TODO contenteditable PASSA PARA FORA DO BLOQUEIO DA TABELA!!!

$("#tabela_avaliacao").find("tr td:first-child").on("keyup", function () {
    console.log($(this).text().length);
    if($(this).text().length != null)
        $(this).find("input").val($(this).text());
});

$.ajaxSetup({//TODO POR NUM JS GLOBAL
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


$("#atualizar_estado").click(function () {
    var estados = $("#options");
    var estado_nome = estados.find(":selected").text();
    var estado = estados.find(":selected").val();
    var path = window.location.pathname.split("/");
    var ideia_id = path[4];
    $.ajax({
        type:"POST",
        url: "ajax/change_estado/",
        data: {
            "ideia_id":ideia_id,
            "estado": estado,
            "estado_nome": estado_nome
        },
        dataType: "json",
        success: function (data) {
            if (data) {
                alert("Estado atualizado: "+ (data.ideia ? "Sucesso" : "Falhou"));
            }
        }
    });
});


$("#editar_pre_analise").click(function () {
    $("#pre_analise_text").prop("disabled",false);
    this.remove();
});

$("#pre_analise_text").keypress(function() {
    $("#inserir_pre_analise").prop("disabled",false);
});

$("#editar_analise").click(function () {
    $("#analise_text").prop("disabled",false);
    $("#tabela_avaliacao_div").removeClass("disabledform2");
    this.remove();
});

$("#analise_text").keypress(function() {
    $("#inserir_analise").prop("disabled",false);
});

$("#tabela_avaliacao_div").on("change",function () {
    $("#inserir_analise").prop("disabled",false);
});

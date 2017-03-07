/*
 * Modificação do estado do radio button para a escolha de outro tipo de ideia
 *
 * */
$('input[type="radio"]').change(function () {
    var outra_text = $('#radio_outra_text');
    if ($('#radio_outra').is(':checked'))
    {
        outra_text.prop('disabled',false);
        outra_text.prop('required',true);
    }
    else
    {
        outra_text.prop('disabled',true);
        outra_text.prop('required',false);
    }
});

/*
 * Adicionar uma linha, depois da penultima linha da tabela de analise
 * Novas linhas são editáveis
 * */
$(".add_line").click(function () {
    var rows = $('#tabela_avaliacao').find('tr').length;
    if( rows < 17)
        $('#tabela_avaliacao').find('tr:nth-last-child(2)').after('' +
            '<tr><td><input type="text" class="tabela_avaliacao" maxlength="110" size="50"></td><td></td><td></td><td></td><td></td><td></td><td>' +
            '<input type="text" class="pesos" id="peso'+(rows-1)+'" value="12.5" size="2" maxlength="6"></td></tr>');
});

/*
 * Eliminar uma linha, depois da penultima linha da tabela de analise
 *
 * */
$(".delete_line").click(function () {
    //$('#tabela_avaliacao').find('> tbody:last-child').remove();
    var tabela = $('#tabela_avaliacao');
    if(tabela.find('> tbody:last-child').children().length != 10)
    {
        tabela.find('> tbody:last-child').children().last().prev().remove();
    }

});

/*
 * O utilizador pode inserir uma cruz na avaliação desejada (muito fraco, ..., Muito Bom) para cada linha
 *
 * */
$("#tabela_avaliacao").on("click", "td:not(:first-child):not(:last-child)", function() {
    if($(this).parent().not("tr:not(:last-child)").length != 1){
        if($(this).siblings().children().is("i"))
        {
            $(this).siblings().children().remove("i");
            $(this).html("<i class='fa fa-times smallicon'></i>");
        }else
        {
            $(this).html("<i class='fa fa-times smallicon'></i>");
        }
    }
});

$(".pesos").change(function () {
    if (!this.value.match(/^[0-9]{1,2}$|^[0-9]{1,2}\.[0-9]{1,3}$/))
        this.value = this.value.replace(/[^0-9]/g, '');
    if (!this.value.match(/^[0-9]{1,2}(?!\d)|^[0-9]{1,2}\.[0-9]{1,3}$/))
        this.value = 0;
    if(this.value == '')
        this.value = 0;
});


$.ajaxSetup({//TODO POR NUM JS GLOBAL
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


$("#atualizar_estado").click(function () {
    var estados = $('#options');
    var estado_nome = estados.find(":selected").text();
    var estado = estados.find(":selected").val();
    var path = window.location.pathname.split("/");
    var ideia_id = path[4];
    $.ajax({
        type:"POST",
        url: 'ajax/change_estado/',
        data: {
            'ideia_id':ideia_id,
            'estado': estado,
            'estado_nome': estado_nome
        },
        dataType: 'json',
        success: function (data) {
            if (data) {
                alert("Estado atualizado: "+ data.ideia ? "Sucesso" : "Falhou");
            }
        }
    });
});


$("#editar_pre_analise").click(function () {
    $("#pre_analise_text").prop('disabled',false);
    this.remove();
});

$("#pre_analise_text").change(function() {
    $("#inserir_pre_analise").prop('disabled',false);
});

$("#editar_analise").click(function () {
    $("#analise_text").prop('disabled',false);
    this.remove();
});

$("#analise_text").change(function() {
    $("#inserir_analise").prop('disabled',false);
});


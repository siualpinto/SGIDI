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
    $('#tabela_avaliacao').find('tr:nth-last-child(2)').after('<tr><td><div contenteditable>Nova linha</div></td><td></td><td></td><td></td> <td></td><td></td><td></td></tr>');
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
        console.log(tabela.find('> tbody:last-child').prev().children().last());
        tabela.find('> tbody:last-child').children().last().prev().remove();
    }

});

/*
* O utilizador pode inserir uma cruz na avaliação desejada (muito fraco, ..., Muito Bom) para cada linha
*
* */
$("#tabela_avaliacao").on("click", "td:not(:first-child, :last-child)", function() {
    if($(this).siblings().children().is("i"))
    {
        $(this).siblings().children().remove("i");
        $(this).html("<i class='fa fa-times smallicon'></i>");
    }else
    {
        $(this).html("<i class='fa fa-times smallicon'></i>");
    }
});

 $("#id_username").change(function () {
      console.log( $(this).val() );
    });
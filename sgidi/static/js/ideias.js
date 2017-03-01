

$('input[type="radio"]').change(function () {
    if ($('#radio_outra').is(':checked'))
    {
        $('#radio_outra_text').prop('disabled',false);
        $('#radio_outra_text').prop('required',true);
    }
    else
    {
        $('#radio_outra_text').prop('disabled',true);
        $('#radio_outra_text').prop('required',false);
    }
});

$(".add_line").click(function () {
    $('#tabela_avaliacao').find('> tbody:last-child').append('<tr><td><div contenteditable>Nova linha</div></td><td></td><td></td><td></td> <td></td><td></td><td></td></tr>');
});

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
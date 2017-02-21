

$('input[type="radio"]').change(function () {
    console.log("teste");
    if ($('#radio_outra').is(':checked'))
    {
        $('#radio_outra_text').prop('required',true);

    }
    else
    {
        $('#radio_outra_text').prop('required',false);
    }
});


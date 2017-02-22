

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


$('.name').mouseover(function(e) {
    $that = $(this);
    console.log($that.parent().attr('id'));
    $('.notes').hide();
    console.log($that.next().text());
    if($that.next().text()!== ''){
        $that.siblings().show();
    }
});
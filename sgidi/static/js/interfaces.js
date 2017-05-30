$('.name').mouseover(function(e) {
    $that = $(this);
    console.log($that.parent().attr('id'));
    $('.notes').hide();
    console.log($that.next().text());
    if($that.next().text()!== ''){
        $that.siblings().show();
    }
});

$("ul").each(
  function() {
    var elem = $(this);
    if (elem.children().length === 0) {
      elem.remove();
    }
  }
);

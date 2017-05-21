function my_special_notification_callback(data) {
    $('main').empty();
    for (var i = 0; i < data.unread_list.length; i++) {
        msg = data.unread_list[i];
        $('main').append("<a href='/conhecimentos/"+msg.description+"'<p>"+msg.actor+' '+msg.verb+"</p></a>");
    }
};
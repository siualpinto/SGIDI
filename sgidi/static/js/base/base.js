/**
 * Created by lsmor on 20/02/2017.
 */
function blinker() {
    $('.blink_me').fadeOut(500);
    $('.blink_me').fadeIn(500);
}
if($('.blink_me').text() > 0) {
    setInterval(blinker, 2000);
}else{
    $('.blink_me').remove();
}
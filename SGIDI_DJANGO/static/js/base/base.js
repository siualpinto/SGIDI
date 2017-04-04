/**
 * Created by lsmor on 20/02/2017.
 */
var  blink = $('.blink_me');
function blinker()
{
    blink.fadeOut(500);
    blink.fadeIn(500);
}
if(blink.text() > 0)
{
    setInterval(blinker, 2000);
}
else
{
    blink.remove();
}
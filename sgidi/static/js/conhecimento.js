/**
 * Created by lsmor on 06/05/2017.
 */


$("#add_tag").click(function () {
    $name = $("#id_tag").val();
    if($name)
        $("#tag_group").append("<input type='checkbox' name='existing_tag' value='"+$name+"'>"+$name+"");
});
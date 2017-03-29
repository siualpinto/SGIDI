/**
 * Created by lsmor on 28/03/2017.
 */

var client = Asana.Client.create().useAccessToken('0/ce4e5bf93acd15f0121a88a142be4548');

// var projeto = client.projects.findById($("a.list-group-item.active").attr("id"));
client.projects.findById($("a.list-group-item.active").attr("id")).then(function (projeto) {
    reloadProjectInfo(projeto);
});


function reloadProjectInfo(projeto) {
    $("dd").empty();
    // $(".dl-horizontal").css({"pointer-events": "none", "opacity": "0.4"});
    $("dd.nome").append(projeto.name);
    $("dd.tipo").append(projeto.notes);
    if(projeto.current_status !== null){
        var cor = projeto.current_status.color;
        $("dd.estado").append(projeto.current_status.text).css("background-color",cor).css("color",(cor === "yellow" ? "black" : "whitesmoke"));
    }
    else
        $("dd.estado").css("background-color","transparent");
    $("dd.responsavel").append(projeto.owner.name);
    $("dd.data_criacao").append(projeto.created_at);
    $("dd.data_modificacao").append(projeto.modified_at);
    for(var i=0;i<projeto.followers.length;i++){
        client.users.findById(projeto.followers[i].id).then(function (user) {
            if(user.photo === null)
                $("dd.seguidores").append("<img src='/static/img/default-user-icon-profile.png' alt='imagem do follower' class='img' height='36' width='36'>"+user.name+"");
            else
                $("dd.seguidores").append("<img src='"+user.photo.image_36x36+"' alt='imagem do follower' class='img'>"+user.name+"");
        });
    }
    /*$(".dl-horizontal").css({"pointer-events": "", "opacity": ""});
     $(".dl-horizontal").removeClass("disabledElement");
     $(".loader").remove();*/
    $(".dl-horizontal").show();
}

$('.list-group>a').click(function(e) {
    e.preventDefault();
    $that = $(this);
    $that.parent().find('a').removeClass('active');
    $that.addClass('active');
    client.projects.findById($("a.list-group-item.active").attr("id")).then(function (projeto) {
        reloadProjectInfo(projeto);
    });
});


$('ul>li.projetos>a').click(function(e) {
    e.preventDefault();
    $(".dl-horizontal").hide();
    $that = $(this);
    $that.parent().parent().find('li').removeClass('active');
    $that.addClass('active');
    client.tasks.findByProject($("a.list-group-item.active").attr("id")).then(function (tasks) {
        console.log(tasks);
        $(".well.well").append(tasks);
     });
});


/*
function processAjaxData(response, urlPath){
    document.getElementById("content").innerHTML = response.html;
    document.title = response.pageTitle;
    window.history.pushState({"html":response.html,"pageTitle":response.pageTitle},"", urlPath);
}

window.onpopstate = function(e){
    if(e.state){
        document.getElementById("content").innerHTML = e.state.html;
        document.title = e.state.pageTitle;
    }
};*/

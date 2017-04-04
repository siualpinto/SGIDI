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
    $(".tarefas").hide();
    $("#gantt").hide();
}

$('.list-group>a').click(function(e) {
    e.preventDefault();
    $that = $(this);
    $that.parent().find('a').removeClass('active');
    $that.addClass('active');
    client.projects.findById($("a.list-group-item.active").attr("id")).then(function (projeto) {
        reloadProjectInfo(projeto);
    });
    $li = $('ul>li.projetos>a');
    $li.parent().parent().find('li').removeClass('active');
    $li.parent().parent().find('li#informacao').addClass('active');
});


$('ul>li.projetos>a').click(function(e) {
    e.preventDefault();
    $(".dl-horizontal").hide();
    $tarefas = $(".tarefas");
    $tarefas.empty();
    $tarefas.show();
    $that = $(this);
    $that.parent().parent().find('li').removeClass('active');
    $that.parent().addClass('active');
    $projeto_ativo = $("a.list-group-item.active");

    if($that.parent().attr('id') === "informacao"){
        client.projects.findById($projeto_ativo.attr("id")).then(function (projeto) {
            reloadProjectInfo(projeto);
            return;
        });
    }
    if($that.parent().attr('id') === "li_gantt"){
        $tarefas.hide();
        $("#gantt").show();

       // $(".gantt").dhx_gantt({
		// 	data:demo_tasks
		// });


        console.log("asdasd");
        return;
    }
    client.tasks.findByProject($projeto_ativo.attr("id")).then(function (tasks) {
        for(var i=0;i<tasks.data.length;i++){
            client.tasks.findById(tasks.data[i].id).then(function (task) {
                console.log(task);
                var followers = [];
                for(var i=0;i<task.followers.length;i++){
                    followers.push(task.followers[i].name)
                }
                $tarefas.append("<li class='list-group-item'><dl class='dl-horizontal'><dt>Nome:</dt><dd class='nome'>"+task.name+"</dd><dt>Estado:</dt><dd class='estado'>"+task.assignee_status+"</dd>" +
                    "<dt>Descrição:</dt><dd class='notes'>"+task.notes+"</dd><dt>Data de criação:</dt><dd class='data_criacao'>"+task.created_at+"</dd>" +
                    "<dt>Data de modificação:</dt><dd class='data_modificacao'>"+task.modified_at+"</dd><dt>Data de completação:</dt><dd class='data_completacao'>"+task.complet_at+"</dd>"+
                    "</dl></li>");
            });
        }
    });
});


function gantt() {
    // var tasks =  {
    //     data:[
    //         {id:1, text:"Project #2", start_date:"01-04-2013", duration:18,order:10,
    //             progress:0.4, open: true},
    //         {id:2, text:"Task #1", 	  start_date:"02-04-2013", duration:8, order:10,
    //             progress:0.6, parent:1},
    //         {id:3, text:"Task #2",    start_date:"11-04-2013", duration:8, order:20,
    //             progress:0.6, parent:1}
    //     ],
    //     links:[
    //         { id:1, source:1, target:2, type:"1"},
    //         { id:2, source:2, target:3, type:"0"},
    //         { id:3, source:3, target:4, type:"0"},
    //         { id:4, source:2, target:5, type:"2"}
    //     ]
    // };
    // gantt.init("gantt");
    // gantt.parse(tasks);
    $("#gantt").show();
}


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

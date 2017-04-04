/**
 * Created by lsmor on 28/03/2017.
 */

var client = Asana.Client.create().useAccessToken('0/ce4e5bf93acd15f0121a88a142be4548');
// var projeto = client.projects.findById($("a.list-group-item.active").attr("id"));
/*client.users.me().then(function(me) {
 console.log(me);
 });*/
reloadProjectInfo();

function reloadProjectInfo() {
    $(".dl-horizontal").show();
    $(".seccoes").hide();
    $("#diagrama_gantt").hide();
    $projeto_ativo = $("a.list-group-item.active");
    client.projects.findById($projeto_ativo.attr("id")).then(function (projeto) {

        console.log(projeto);
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
        $("dd.data_criacao").append(cleanData(projeto.created_at));
        $("dd.data_modificacao").append(cleanData(projeto.modified_at));
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
    });
    reloadTasksInfo();
    reloadDiagramInfo();
}

function reloadTasksInfo() {
    $tarefas = $(".seccoes");
    $projeto_ativo = $("a.list-group-item.active");

    client.projects.sections($projeto_ativo.attr("id")).then(function (sections) {
        for(var i=0;i<sections.data.length;i++){
            $(".seccoes").append("<li class='nav-header disabled'><p class='secondary-heading'>"+sections.data[i].name+"</p></li>" +
                "<li class='list-group-item col-md-12'><ul class='list-group tarefas' id="+sections.data[i].id+"></ul></li>");
        }
    });
    client.tasks.findByProject($projeto_ativo.attr("id"),{opt_fields: 'id'}).then(function (tasks) {
        for(var i=0;i<tasks.data.length;i++){
            client.tasks.findById(tasks.data[i].id).then(function (task) {
                console.log(task);
                var followers = "";
                for(var i=0;i<task.followers.length;i++){
                    if(i===0)
                        followers+=task.followers[i].name;
                    else{
                        followers+=" | ";
                        followers+=task.followers[i].name;
                    }
                }
                if(task.memberships[0].section !== null)
                    if(task.id !== task.memberships[0].section.id)
                        $tarefas.find("#"+task.memberships[0].section.id+"").append("<li class='list-group-item col-md-12' id='"+task.id+"'>" +
                            "<div class='col-md-8'><label>Nome:&nbsp</label>"+task.name+"</div>" +
                            "<div class='col-md-4'><label>Estado:&nbsp</label>"+task.assignee_status+"</div>" +
                            "<div class='col-md-4'><label>Data Inicial:&nbsp</label>"+cleanData(task.created_at)+"</div>" +
                            "<div class='col-md-4'><label>Data Final:&nbsp</label>"+(task.due_on === null ?  "Não tem data final" : task.due_on)+"</div>" +
                            "<div class='col-md-4'><label>Tarefa Completa:&nbsp</label>"+(task.completed ? task.completed_at : "Ainda não completa")+"</div>" +
                            "<div class='col-md-4'><label class='responsavel'>Responsavel:&nbsp</label>"+(task.assignee === null ?  "Não tem responsável" : task.assignee.name)+"</div>" +
                            "<div class='col-md-8'><label class='followers'>Followers:&nbsp</label>"+followers+"</div>"+
                            "<div class='col-md-12'><label>Descrição:&nbsp</label>"+task.notes+"</div></li>");
            });
        }

    });
}
function reloadDiagramInfo() {
    $diagrama = $("#diagrama_gantt");

    var tasks =  {
        data:[
            {id:1, text:"Project #2", start_date:"01-04-2013", duration:18,order:10,
                progress:0.4, open: true},
            {id:2, text:"Task #1", 	  start_date:"02-04-2013", duration:8, order:10,
                progress:0.6, parent:1},
            {id:3, text:"Task #2",    start_date:"11-04-2013", duration:8, order:20,
                progress:0.6, parent:1}
        ],
        links:[
            { id:1, source:1, target:2, type:"1"},
            { id:2, source:2, target:3, type:"0"},
            { id:3, source:3, target:4, type:"0"},
            { id:4, source:2, target:5, type:"2"}
        ]
    };

    var users_data = {
        "data":[
            {"id":1, "text":"Project #1", "start_date":"01-04-2013", "duration":"11", "progress": 0.6, "open": true, "users": ["John", "Mike", "Anna"], "priority": "2"},
            {"id":2, "text":"Task #1", "start_date":"03-04-2013", "duration":"5", "parent":"1", "progress": 1, "open": true, "users": ["John", "Mike"], "priority": "1"},
            {"id":3, "text":"Task #2", "start_date":"02-04-2013", "duration":"7", "parent":"1", "progress": 0.5, "open": true, "users": ["Anna"], "priority": "1"},
            {"id":4, "text":"Task #3", "start_date":"02-04-2013", "duration":"6", "parent":"1", "progress": 0.8, "open": true, "users": ["Mike", "Anna"], "priority": "2"},
            {"id":5, "text":"Task #4", "start_date":"02-04-2013", "duration":"5", "parent":"1", "progress": 0.2, "open": true, "users": ["John"], "priority": "3"},
            {"id":6, "text":"Task #5", "start_date":"02-04-2013", "duration":"7", "parent":"1", "progress": 0, "open": true, "users": ["John"], "priority": "2"},
            {"id":7, "text":"Task #2.1", "start_date":"03-04-2013", "duration":"2", "parent":"3", "progress": 1, "open": true, "users": ["Mike", "Anna"], "priority": "2"},
            {"id":8, "text":"Task #2.2", "start_date":"06-04-2013", "duration":"3", "parent":"3", "progress": 0.8, "open": true, "users": ["Anna"], "priority": "3"},
            {"id":9, "text":"Task #2.3", "start_date":"10-04-2013", "duration":"4", "parent":"3", "progress": 0.2, "open": true, "users": ["Mike", "Anna"], "priority": "1"},
            {"id":10, "text":"Task #2.4", "start_date":"10-04-2013", "duration":"4", "parent":"3", "progress": 0, "open": true, "users": ["John", "Mike"], "priority": "1"},
            {"id":11, "text":"Task #4.1", "start_date":"03-04-2013", "duration":"4", "parent":"5", "progress": 0.5, "open": true, "users": ["John", "Anna"], "priority": "3"},
            {"id":12, "text":"Task #4.2", "start_date":"03-04-2013", "duration":"4", "parent":"5", "progress": 0.1, "open": true, "users": ["John"], "priority": "3"},
            {"id":13, "text":"Task #4.3", "start_date":"03-04-2013", "duration":"5", "parent":"5", "progress": 0, "open": true, "users": ["Anna"], "priority": "3"}
        ],
        "links":[
            {"id":"10","source":"11","target":"12","type":"1"},
            {"id":"11","source":"11","target":"13","type":"1"},
            {"id":"12","source":"11","target":"14","type":"1"},
            {"id":"13","source":"11","target":"15","type":"1"},
            {"id":"14","source":"11","target":"16","type":"1"},

            {"id":"15","source":"13","target":"17","type":"1"},
            {"id":"16","source":"17","target":"18","type":"0"},
            {"id":"17","source":"18","target":"19","type":"0"},
            {"id":"18","source":"19","target":"20","type":"0"},
            {"id":"19","source":"15","target":"21","type":"2"},
            {"id":"20","source":"15","target":"22","type":"2"},
            {"id":"21","source":"15","target":"23","type":"2"}
        ]
    };

    $diagrama.dhx_gantt({
        data:users_data
    });
}

$('.list-group>a').click(function(e) {
    e.preventDefault();
    $that = $(this);
    if($that.parent().find('a.active').attr('id') !== $that.attr('id')){
        $that.parent().find('a').removeClass('active');
        $that.addClass('active');
        $(".seccoes").empty();
        $("#diagrama_gantt").empty();
        reloadProjectInfo();
        $li = $('ul>li.projetos>a');
        $li.parent().parent().find('li').removeClass('active');
        $li.parent().parent().find('li#informacao').addClass('active');
    }
});


$('ul>li.projetos>a').click(function(e) {
    e.preventDefault();
    $tarefas = $(".seccoes");
    $diagrama = $("#diagrama_gantt");
    $informacao = $(".dl-horizontal");
    $that = $(this);
    $that.parent().parent().find('li').removeClass('active');
    $that.parent().addClass('active');

    if($that.parent().attr('id') === "informacao"){
        $tarefas.hide();
        $diagrama.hide();
        $informacao.show();
        return;
    }
    if ($that.parent().attr('id') === "li_tarefas"){
        $informacao.hide();
        $diagrama.hide();
        $tarefas.show();
        return;
    }
    if($that.parent().attr('id') === "li_gantt"){
        $tarefas.hide();
        $informacao.hide();
        $diagrama.show();
    }
});

function cleanData(foo) {
    var res;
    if (null !== foo)
    {
        res = (foo.replace(/T/g, " ")).replace(/Z/g,"");
        return res;
    }
}


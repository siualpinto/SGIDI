/**
 * Created by lsmor on 28/03/2017.
 */

var client = Asana.Client.create().useAccessToken('0/ce4e5bf93acd15f0121a88a142be4548'); //meu (Na view.py tbm tem token)
// var client = Asana.Client.create().useAccessToken('0/8f62a923af9681d7530fe81d36ea3f0b');
// var projeto = client.projects.findById($("a.list-group-item.active").attr(id));
/*client.users.me().then(function(me) {
 console.log(me);
 });*/

var gannt_dados = {
    data:[]
};


reloadProjectInfo();

function reloadProjectInfo() {
    $(".dl-horizontal").show();
    $(".seccoes").hide();
    $("#diagrama_gantt").hide();
    $projeto_ativo = $("a.list-group-item.active");
    client.projects.findById($projeto_ativo.attr('id')).then(function (projeto) {
        $("dd").empty();
        // $(".dl-horizontal").css({"pointer-events": "none", "opacity": "0.4"});
        $("dd.nome").append(projeto.name);
        gannt_dados.data.push({
            id: 1,
            text: projeto.name,
            start_date: dataToGantt(projeto.created_at,false),
            duration: "1",
            end_date: "06-04-2017",
            open: true,
            users: [],
            priority: "2"
        });
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
                gannt_dados.data[0].users.push(user.name);
            });
        }
        /*$(".dl-horizontal").css({"pointer-events": "", "opacity": ""});
         $(".dl-horizontal").removeClass("disabledElement");
         $(".loader").remove();*/
    });
    setTimeout(reloadTasksInfo, 2500);
}
function reloadTasksInfo() {
    $tarefas = $(".seccoes");
    $projeto_ativo = $("a.list-group-item.active");

    client.projects.sections($projeto_ativo.attr('id')).then(function (sections) {
        for(var i=0;i<sections.data.length;i++){
            $tarefas.append("<li class='nav-header disabled'><p class='secondary-heading'>"+sections.data[i].name+"</p></li>" +
                "<li class='list-group-item col-md-12'><ul class='list-group tarefas "+((gannt_dados.data[gannt_dados.data.length-1].id)+1)+"' id="+sections.data[i].id+"></ul></li>");
            gannt_dados.data.push({
                id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
                text: sections.data[i].name,
                open: true,
                parent: 1,
                priority: "2"
            });
        }
        $tarefas.append("<li class='nav-header disabled'><p class='secondary-heading'>"+'Sem secção'+"</p></li>" +
            "<li class='list-group-item col-md-12'><ul class='list-group tarefas "+((gannt_dados.data[gannt_dados.data.length-1].id)+1)+"' id='semSeccao'></ul></li>");
        gannt_dados.data.push({
            id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
            text: "Sem secção",
            open: true,
            parent: 1,
            priority: "2"
        });
    });
    client.tasks.findByProject($projeto_ativo.attr('id'),{opt_fields: 'id'}).then(function (tasks) {
        for(var i=0;i<tasks.data.length;i++){
            client.tasks.findById(tasks.data[i].id).then(function (task) {
                var followers = "";
                for(var i=0;i<task.followers.length;i++){
                    if(i===0)
                        followers+=task.followers[i].name;
                    else{
                        followers+=" | ";
                        followers+=task.followers[i].name;
                    }
                }
                if(task.memberships[0].section !== null && task.id !== task.memberships[0].section.id){
                    createTask($tarefas.find("#" + task.memberships[0].section.id + ""),task,followers);
                }
                else if(task.memberships[0].section === null){
                    createTask($tarefas.find('#semSeccao'),task,followers);
                }
            });
        }
        setTimeout(reloadDiagramInfo, 3000);
    });
}

function createTask(tarefa,task,followers) {
    tarefa.append("<li class='list-group-item col-md-12 "+((gannt_dados.data[gannt_dados.data.length-1].id)+1)+"' id='" + task.id + "'>" +
        "<div class='col-md-8'><label>Nome:&nbsp</label>" + task.name + "</div>" +
        "<div class='col-md-4'><label>Estado:&nbsp</label>" + task.assignee_status + "</div>" +
        "<div class='col-md-4'><label>Data Inicial:&nbsp</label>" + cleanData(task.created_at) + "</div>" +
        "<div class='col-md-4'><label>Data Final:&nbsp</label>" + (task.due_on === null ? "Não tem data final" : task.due_on) + "</div>" +
        "<div class='col-md-4'><label>Tarefa Completa:&nbsp</label>" + (task.completed ? cleanData(task.completed_at) : "Ainda não completa") + "</div>" +
        "<div class='col-md-4'><label class='responsavel'>Responsavel:&nbsp</label>" + (task.assignee === null ? "Não tem responsável" : task.assignee.name) + "</div>" +
        "<div class='col-md-8'><label class='followers'>Followers:&nbsp</label>" + followers + "</div>" +
        "<div class='col-md-12'><label>Descrição:&nbsp</label>" + task.notes + "</div></li>");
    gannt_dados.data.push({
        id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
        text: task.name,
        start_date: dataToGantt(task.created_at,false),
        end_date: (task.due_on === null ? null : dataToGantt(task.due_on,true)),
        open: true,
        parent: tarefa.attr('class').split(' ').pop(),
        users: [followers],
        priority: "2"
    });
    client.tasks.subtasks(task.id).then(function (subtasks) {
        for(var i=0;i<subtasks.data.length;i++){
            client.tasks.findById(subtasks.data[i].id).then(function (subtask) {
                $tarefas.find("#"+subtask.parent.id+"").append("<li class='list-group-item col-md-12 subtask' id='" + subtask.id + "'>" +
                    "<div class='col-md-8'><label>Nome:&nbsp</label>" + subtask.name + "</div>" +
                    "<div class='col-md-4'><label>Estado:&nbsp</label>" + subtask.assignee_status + "</div>" +
                    "<div class='col-md-4'><label>Data Inicial:&nbsp</label>" + cleanData(subtask.created_at) + "</div>" +
                    "<div class='col-md-4'><label>Data Final:&nbsp</label>" + (subtask.due_on === null ? "Não tem data final" : subtask.due_on) + "</div>" +
                    "<div class='col-md-4'><label>Tarefa Completa:&nbsp</label>" + (subtask.completed ? cleanData(subtask.completed_at) : "Ainda não completa") + "</div>" +
                    "<div class='col-md-4'><label class='responsavel'>Responsavel:&nbsp</label>" + (subtask.assignee === null ? "Não tem responsável" : subtask.assignee.name) + "</div>" +
                    "<div class='col-md-8'><label class='followers'>Followers:&nbsp</label>" + followers + "</div>" +
                    "<div class='col-md-12'><label>Descrição:&nbsp</label>" + subtask.notes + "</div></li>");
                console.log($tarefas.find("#"+subtask.parent.id+"").attr('class').split(' ').pop());
                gannt_dados.data.push({
                    id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
                    text: subtask.name,
                    start_date: dataToGantt(subtask.created_at,false),
                    end_date: (subtask.due_on === null ? null : dataToGantt(subtask.due_on,true)),
                    open: true,
                    parent: $tarefas.find("#"+subtask.parent.id+"").attr('class').split(' ').pop(),
                    users: [followers],
                    priority: "2"
                });
            });
        }
    });
}

function reloadDiagramInfo() {
    console.log("DIAGRAMA");
    // console.log(JSON.stringify(gannt_dados,0 ,2));
    $diagrama = $("#diagrama_gantt");
    /* var hints = [
     "Global working time is: <b>9:00-18:00</b>",
     "<b>Tuesdays</b> are not working days",
     "<b>Saturdays</b> are working days",
     "<b>Saturdays</b> and <b>Fridays</b> are short days",
     "<b>Sunday, 31th March</b> is working day"
     ];
     for(var i=0; i < hints.length; i++){
     setTimeout(
     (function(i){
     return function(){
     gantt.message(hints[i]);
     } })(i)
     , (i+1)*600);
     }*/

    var weekScaleTemplate = function(date){
        var dateToStr = gantt.date.date_to_str("%d %M");
        var weekNum = gantt.date.date_to_str("(week %W)");
        var endDate = gantt.date.add(gantt.date.add(date, 1, "week"), -1, "day");
        return dateToStr(date) + " - " + dateToStr(endDate) + " " + weekNum(date);
    };
    $diagrama.dhx_gantt({
        data:gannt_dados,
        autosize:true,
        scale_unit:"day",
        date_scale: "%D, %d",
        min_column_width:60,
        duration_unit:"day",
        scale_height:20*3,
        row_height:30,
        subscales:[
            {unit:"month", step:1, date:"%F, %Y"},
            {unit:"week", step:1, template:weekScaleTemplate}
        ],
        columns:[
            {name:"text", label:"Nome da Tarefa", tree:true, align: "left",  width:'*' },
            {name:"assigned", label:"Colaboradores", align: "center", width:'*',
                template: function(item) {
                    if (!item.users) return "---";
                    return item.users.join(", ");
                }
            }
        ]
    });
}

$('.list-group>a').click(function(e) {
    e.preventDefault();
    $that = $(this);
    if($that.parent().find('a.active').attr('id') !== $that.attr('id')){
        $that.parent().find('a').removeClass('active');
        $that.addClass('active');
        gannt_dados = {data:[]};
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


/*  Funcões auxiliares
 *
 *
 *
 */
function cleanData(foo) {
    var res;
    if (null !== foo)
    {
        res = (foo.replace(/T/g, " ")).replace(/Z/g,"");
        return res;
    }
}

function dataToGantt(data, end_date) {
    var dateSplit;
    var formatFunc = gantt.date.date_to_str("%d-%m-%Y");
    dateSplit = (cleanData(data).replace(/-|:/g, ' ')).split(' ');
    if(end_date){
        return formatFunc(gantt.date.add(new Date(dateSplit[0], dateSplit[1] - 1, dateSplit[2]), 1, 'day'));
    }
    return formatFunc(new Date(dateSplit[0], dateSplit[1] - 1, dateSplit[2]));
}


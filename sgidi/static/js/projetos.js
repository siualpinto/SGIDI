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
    $("#diagrama_button_id").hide();
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
    setTimeout(reloadTasksInfo, 3000);
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
                priority: "1"
            });
        }
        $tarefas.append("<li class='nav-header disabled'><p class='secondary-heading'>"+'Sem secção'+"</p></li>" +
            "<li class='list-group-item col-md-12'><ul class='list-group tarefas "+((gannt_dados.data[gannt_dados.data.length-1].id)+1)+"' id='semSeccao'></ul></li>");
        gannt_dados.data.push({
            id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
            text: "Sem secção",
            open: true,
            parent: 1,
            priority: "1"
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
                // console.log(task);
                if(task.memberships[0].section !== null && task.id !== task.memberships[0].section.id){
                    createTask($tarefas.find("#" + task.memberships[0].section.id + ""),task,followers);
                }
                else if(task.memberships[0].section === null){
                    createTask($tarefas.find('#semSeccao'),task,followers);
                }
            });
        }
        setTimeout(reloadDiagramInfo, 4000);
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
    var data_inicial = (task.notes.search("data_inicial=") === -1 ?  dataToGantt(task.created_at,false) : task.notes.substr(task.notes.search("data_inicial=")+13,10));
    gannt_dados.data.push({
        id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
        id_asana:task.id,
        text: task.name,
        notes:task.notes,
        start_date: data_inicial,
        end_date: (task.due_on === null ? gantt.date.add(new Date(data_inicial.substr(6,4), (parseInt(data_inicial.substr(3,2))-1).toString(), data_inicial.substr(0,2)), 1, 'day') : dataToGantt(task.due_on,true)),
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
                gannt_dados.data.push({
                    id: (gannt_dados.data[gannt_dados.data.length-1].id)+1,
                    sub_task: 1,
                    id_asana:subtask.id,
                    text: subtask.name,
                    start_date: (subtask.notes.search("data_inicial=") === -1 ?  dataToGantt(subtask.created_at,false) : subtask.notes.substr(subtask.notes.search("data_inicial=")+13,10)),
                    end_date: (subtask.due_on === null ? gantt.date.add(new Date(data_inicial.substr(6,4), (parseInt(data_inicial.substr(3,2))-1).toString(), data_inicial.substr(0,2)), 1, 'day') : dataToGantt(subtask.due_on,true)),
                    open: true,
                    parent: $tarefas.find("#"+subtask.parent.id+"").attr('class').split(' ').pop(),
                    users: [followers],
                    priority: "2"
                });
            });
        }
    });
}

gantt.attachEvent("onTaskDrag", function(id, mode, task, original){
    var modes = gantt.config.drag_mode;
    if(mode === modes.move){
        var diff = task.start_date - original.start_date;
        gantt.eachTask(function(child){
            child.start_date = new Date(+child.start_date + diff);
            child.end_date = new Date(+child.end_date + diff);
            gantt.refreshTask(child.id, true);
        },id );
    }
    return true;
});

//rounds positions of the child items to scale
gantt.attachEvent("onAfterTaskDrag", function(id, mode, e){
    var modes = gantt.config.drag_mode;
    if(mode === modes.move ){
        var state = gantt.getState();
        gantt.eachTask(function(child){
            child.start_date = gantt.roundDate({
                date:child.start_date,
                unit:state.scale_unit,
                step:state.scale_step
            });
            child.end_date = gantt.calculateEndDate(child.start_date,
                child.duration, gantt.config.duration_unit);
            gantt.updateTask(child.id);
        },id );
    }

    if(mode === "resize"){
        var task = gantt.getTask(id);
        // Data Inicial
        if (task.notes.search("data_inicial=") === -1){
            task.notes = task.notes.concat("\ndata_inicial="+gantt.date.to_fixed(task.start_date.getDate())+"-"+gantt.date.to_fixed((task.start_date.getMonth()+1))+"-"+task.start_date.getFullYear());
            client.tasks.update(task.id_asana,{notes:task.notes});
        }else
        {
            var old_day = task.notes.substr(task.notes.search("data_inicial=")+13,2);
            var old_month = task.notes.substr(task.notes.search("data_inicial=")+16,2);
            var old_year = task.notes.substr(task.notes.search("data_inicial=")+19,4);
            if(gantt.date.to_fixed(task.start_date.getDate()) !== old_day || gantt.date.to_fixed((task.start_date.getMonth()+1)) !== old_month || task.start_date.getFullYear() !== old_year){
                task.notes = task.notes.replace(/\d\d-\d\d-\d\d\d\d/,gantt.date.to_fixed(task.start_date.getDate())+"-"+gantt.date.to_fixed((task.start_date.getMonth()+1))+"-"+task.start_date.getFullYear());
                client.tasks.update(task.id_asana,{notes:task.notes});
            }
        }
        // Data Final TODO DATA FINAL

    }
});


function reloadDiagramInfo() {
    console.log("DIAGRAMA");
    // console.log(JSON.stringify(gannt_dados,0 ,2));
    $diagrama = $("#diagrama_gantt");
    /*
     * ALERTAS!!!!
     *
     var hints = [
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
    gantt.templates.task_class  = function(start, end, task){
        switch (task.priority){
            case "1":
                return "high";
                break;
            case "2":
                return "medium";
                break;
            case "3":
                return "low";
                break;
        }
    };

    var weekScaleTemplate = function(date){
        var dateToStr = gantt.date.date_to_str("%d %M");
        var weekNum = gantt.date.date_to_str("(semana %W)");
        var endDate = gantt.date.add(gantt.date.add(date, 1, "week"), -1, "day");
        return dateToStr(date) + " - " + dateToStr(endDate) + " " + weekNum(date);
    };
    dateLines();
    zoomToFitScale();

    gantt.locale.labels.section_period = "Intervalo Temporal";
    gantt.locale.labels.section_template = "Nome";
    gantt.locale.labels.section_template2 = "Descrição";


    gantt.config.lightbox.sections = [
        {name:"template", height:16, type:"template", map_to:"my_template"},
        {name:"template2", height:16, type:"template", map_to:"my_template2"},
        {name:"period", type:"time", map_to:"auto"}
    ];
    gantt.attachEvent("onBeforeLightbox", function(id) {
        var task = gantt.getTask(id);
        task.my_template = ""+ task.text+"";
        return true;
    });
    gantt.attachEvent("onBeforeLightbox", function(id) {
        var task = gantt.getTask(id);
        if(task.sub_task === 1){
            task.my_template2 = "Sem descrição";
        }
        else
            task.my_template2 = ""+ task.notes+"";
        return true;
    });

    $diagrama.dhx_gantt({
        data:gannt_dados,
        autosize:true,
        show_progress:false,
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

function dateLines() {
    var todayJS = new Date();
    var dd = todayJS.getDate();
    var mm = todayJS.getMonth()+1; //January is 0!
    var yyyy = todayJS.getFullYear();

    var date_to_str = gantt.date.date_to_str(gantt.config.task_date);
    var today = new Date(yyyy, (mm-1), dd);
    gantt.addMarker({
        start_date: today,
        css: "today",
        text: "Today",
        title:"Today: "+ date_to_str(today)
    });
}

/*
 * Zoom do gantt
 *
 */

function zoomToFitScale() {
    function toggleMode(toggle) {
        toggle.enabled = !toggle.enabled;
        if (toggle.enabled) {
            toggle.innerHTML = "Set default Scale";
            //Saving previous scale state for future restore
            saveConfig();
            zoomToFit();
        } else {

            toggle.innerHTML = "Zoom to Fit";
            //Restore previous scale state
            restoreConfig();
            gantt.render();
        }
    }

    var cachedSettings = {};
    function saveConfig() {
        var config = gantt.config;
        cachedSettings = {};
        cachedSettings.scale_unit = config.scale_unit;
        cachedSettings.date_scale = config.date_scale;
        cachedSettings.step = config.step;
        cachedSettings.subscales = config.subscales;
        cachedSettings.template = gantt.templates.date_scale;
        cachedSettings.start_date = config.start_date;
        cachedSettings.end_date = config.end_date;
    }
    function restoreConfig() {
        applyConfig(cachedSettings);
    }

    function applyConfig(config, dates) {
        gantt.config.scale_unit = config.scale_unit;
        if (config.date_scale) {
            gantt.config.date_scale = config.date_scale;
            gantt.templates.date_scale = null;
        }
        else {
            gantt.templates.date_scale = config.template;
        }

        gantt.config.step = config.step;
        gantt.config.subscales = config.subscales;

        if (dates) {
            gantt.config.start_date = gantt.date.add(dates.start_date, -1, config.unit);
            gantt.config.end_date = gantt.date.add(gantt.date[config.unit + "_start"](dates.end_date), 2, config.unit);
        } else {
            gantt.config.start_date = gantt.config.end_date = null;
        }
    }



    function zoomToFit() {
        var project = gantt.getSubtaskDates(),
            areaWidth = gantt.$task.offsetWidth;

        for (var i = 0; i < scaleConfigs.length; i++) {
            var columnCount = getUnitsBetween(project.start_date, project.end_date, scaleConfigs[i].unit, scaleConfigs[i].step);
            if ((columnCount + 2) * gantt.config.min_column_width <= areaWidth) {
                break;
            }
        }

        if (i === scaleConfigs.length) {
            i--;
        }

        applyConfig(scaleConfigs[i], project);
        gantt.render();
    }

// get number of columns in timeline
    function getUnitsBetween(from, to, unit, step) {
        var start = new Date(from),
            end = new Date(to);
        var units = 0;
        while (start.valueOf() < end.valueOf()) {
            units++;
            start = gantt.date.add(start, step, unit);
        }
        return units;
    }

//Setting available scales
    var scaleConfigs = [
        // minutes
        { unit: "minute", step: 1, scale_unit: "hour", date_scale: "%H", subscales: [
            {unit: "minute", step: 1, date: "%H:%i"}
        ]
        },
        // hours
        { unit: "hour", step: 1, scale_unit: "day", date_scale: "%j %M",
            subscales: [
                {unit: "hour", step: 1, date: "%H:%i"}
            ]
        },
        // days
        { unit: "day", step: 1, scale_unit: "month", date_scale: "%F",
            subscales: [
                {unit: "day", step: 1, date: "%j"}
            ]
        },
        // weeks
        {unit: "week", step: 1, scale_unit: "month", date_scale: "%F",
            subscales: [
                {unit: "week", step: 1, template: function (date) {
                    var dateToStr = gantt.date.date_to_str("%d %M");
                    var endDate = gantt.date.add(gantt.date.add(date, 1, "week"), -1, "day");
                    return dateToStr(date) + " - " + dateToStr(endDate);
                }}
            ]},
        // months
        { unit: "month", step: 1, scale_unit: "year", date_scale: "%Y",
            subscales: [
                {unit: "month", step: 1, date: "%M"}
            ]},
        // quarters
        { unit: "month", step: 3, scale_unit: "year", date_scale: "%Y",
            subscales: [
                {unit: "month", step: 3, template: function (date) {
                    var dateToStr = gantt.date.date_to_str("%M");
                    var endDate = gantt.date.add(gantt.date.add(date, 3, "month"), -1, "day");
                    return dateToStr(date) + " - " + dateToStr(endDate);
                }}
            ]},
        // years
        {unit: "year", step: 1, scale_unit: "year", date_scale: "%Y",
            subscales: [
                {unit: "year", step: 5, template: function (date) {
                    var dateToStr = gantt.date.date_to_str("%Y");
                    var endDate = gantt.date.add(gantt.date.add(date, 5, "year"), -1, "day");
                    return dateToStr(date) + " - " + dateToStr(endDate);
                }}
            ]},
        // decades
        {unit: "year", step: 10, scale_unit: "year", template: function (date) {
            var dateToStr = gantt.date.date_to_str("%Y");
            var endDate = gantt.date.add(gantt.date.add(date, 10, "year"), -1, "day");
            return dateToStr(date) + " - " + dateToStr(endDate);
        },
            subscales: [
                {unit: "year", step: 100, template: function (date) {
                    var dateToStr = gantt.date.date_to_str("%Y");
                    var endDate = gantt.date.add(gantt.date.add(date, 100, "year"), -1, "day");
                    return dateToStr(date) + " - " + dateToStr(endDate);
                }}
            ]}
    ];

    $("#diagrama_button_id").click(function () {
        toggleMode(this);
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
    $diagramaButton = $("#diagrama_button_id");
    $informacao = $(".dl-horizontal");
    $that = $(this);
    $that.parent().parent().find('li').removeClass('active');
    $that.parent().addClass('active');

    if($that.parent().attr('id') === "informacao"){
        $tarefas.hide();
        $diagrama.hide();
        $diagramaButton.hide();
        $informacao.show();
        return;
    }
    if ($that.parent().attr('id') === "li_tarefas"){
        $informacao.hide();
        $diagrama.hide();
        $diagramaButton.hide();
        $tarefas.show();
        return;
    }
    if($that.parent().attr('id') === "li_gantt"){
        $tarefas.hide();
        $informacao.hide();
        $diagrama.show();
        $diagramaButton.show();
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


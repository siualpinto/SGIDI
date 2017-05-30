$(".add_line").click(function () {
    var table = $("#tabela_nao_conformidades > tbody");
    var rows = table.find("tr").length;
    var ultima_tr = table.find("tr:nth-last-child(1)");
    console.log(rows);
    console.log(ultima_tr);
    ultima_tr.after("<tr>" +
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-1'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-2'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-3'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-4'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-5'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-6'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-7'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-8'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-9'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-10'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-11'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-12'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-13'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-14'>...</textarea></td>"+
        "<td width=''><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-15'>...</textarea></td>"+
        "</tr>");
});
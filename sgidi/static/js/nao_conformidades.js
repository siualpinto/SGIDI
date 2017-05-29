$(".add_line").click(function () {
    var table = $("#tabela_nao_conformidades");
    var rows = table.find("tr").length;
    var ultima_tr = table.find("tr:nth-last-child(1)");
    console.log(rows);
    ultima_tr.after("<tr>" +
        "<td width='4%'><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-1'>...</textarea></td>"+
        "<td width='15%'><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-2'>...</textarea></td>"+
        "<td width='27%'><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-3'>...</textarea></td>"+
        "<td width='27%'><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-4'>...</textarea></td>"+
        "<td width='27%'><textarea class='tabela_nao_conformidades_inputs' rows='3' maxlength='2000' name='nao_conformidades"+rows+"-5'>...</textarea></td>"+
        "</tr>");
});
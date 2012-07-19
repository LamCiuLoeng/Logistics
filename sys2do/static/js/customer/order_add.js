function add_item() {
    var msg = new Array();
    if(!$("#item_id").val()){
        msg.push('请填写货物名称！');
    }
    if(!$("#item_qty").val() && !$("#item_vol").val() && !$("#item_weight").val()){
        msg.push('请填写数量，体积或者重量中的一项或者多项！');
    }
    
    if(msg.length>0){
        alert(msg.join("\n"));
        return;
    }
    
    var item_name = $("#item_id :selected").text();
    var item_name_id = $("#item_id").val();
    var item_qty = $("#item_qty").val();
    var item_vol = $("#item_vol").val();
    var item_weight = $("#item_weight").val();
    var item_remark = $("#item_remark").val();
    var html = '<tr class="data_table_tr">';
    html += '<th><input type="hidden" name="item_id_'+index+'" value="'+item_name_id+'"/>'+item_name+'</th>';
    html += '<td class="item_qty_td"><input type="hidden" name="item_qty_'+index+'" value="'+item_qty+'"/>'+item_qty+'</td>';
    html += '<td class="item_weight_td"><input type="hidden" name="item_weight_'+index+'" value="'+item_weight+'"/>'+item_weight+'</td>';
    html += '<td class="item_vol_td"><input type="hidden" name="item_vol_'+index+'" value="'+item_vol+'"/>'+item_vol+'</td>';
    html += '<td><input type="hidden" name="item_remark_'+index+'" value="'+item_remark+'"/>'+item_remark+'</td>';
    html += '<td><input type="button" onclick="del_item(this)" value="删除"/></td>';
    html += '</tr>';
    $("#item_list").append(html);
    index++;
    
    $("#item_id").val('');
    $("#item_qty").val('');
    $("#item_vol").val('');
    $("#item_weight").val('');
    $("#item_remark").val('');
    
    $("#qty").val(mysum(".item_qty_td"));
    $("#vol").val(mysum(".item_vol_td"));
    $("#weight").val(mysum(".item_weight_td"));
    
    $("#weight").trigger('change'); //to re-compute the amount
}

function del_item(obj){
    $($(obj).parents('tr')[0]).remove(); 
}

function tosave(){
    var msg = Array();
    
    if(!$('#source_station').val()){
        msg.push('请填写始发站！');
    }
    
    if(!$('#ref_no').val()){
        msg.push('请填写单号！');
    }
    if(!$('#destination_station').val()){
        msg.push('请填写目的站！');
    }
    if(!$('#source_company_id').val()){
        msg.push('请填写发货公司！');
    }
    if(!$('#source_contact').val()){
        msg.push('请填写发货人！');
    }
    if(!$('#destination_company_id').val()){
        msg.push('请填写收货公司！');
    }
    if(!$('#destination_contact').val()){
        msg.push('请填写收货人！');
    }
    if(!$('#amount').val()){
        msg.push('请填写金额！');
    }
    
    if(msg.length < 1){
        $("form").submit();
    }else{
        var s = '<ul>';
        for(var i=0;i<msg.length;i++){
            s += '<li>' + msg[i] + '</li>';
        }
        s += '</ul>';
        
        $.modaldialog.error(s);
        return false;
    }
    
}



$(document).ready(function(){
    
    
    
});
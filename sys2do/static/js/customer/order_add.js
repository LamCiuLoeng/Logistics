var index = 1;

function add_item() {
    var item_name = $("#item_name").val();
    var item_qty = $("#item_qty").val();
    var item_vol = $("#item_vol").val();
    var item_weight = $("#item_weight").val();
    var item_remark = $("#item_remark").val();
    var html = '<tr class="data_table_tr">';
    html += '<th><input type="hidden" name="item_name_'+index+'" value="'+item_name+'"/>'+item_name+'</th>';
    html += '<td><input type="hidden" name="item_qty_'+index+'" value="'+item_qty+'"/>'+item_qty+'</td>';
    html += '<td><input type="hidden" name="item_vol_'+index+'" value="'+item_vol+'"/>'+item_vol+'</td>';
    html += '<td><input type="hidden" name="item_weight_'+index+'" value="'+item_weight+'"/>'+item_weight+'</td>';
    html += '<td><input type="hidden" name="item_remark_'+index+'" value="'+item_remark+'"/>'+item_remark+'</td>';
    html += '<td><input type="button" onclick="del_item(this)" value="Del"/></td>';
    html += '</tr>';
    $("#item_list").append(html);
    index++;
    
    $("#item_name").val('');
    $("#item_qty").val('');
    $("#item_vol").val('');
    $("#item_weight").val('');
    $("#item_remark").val('');
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
    if(!$('#source_company').val()){
        msg.push('请填写发货公司！');
    }
    if(!$('#source_contact').val()){
        msg.push('请填写发货人！');
    }
    if(!$('#destination_company').val()){
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
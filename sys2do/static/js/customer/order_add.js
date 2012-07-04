var index = 1;

function add_item() {
    var item_name = $("#item_name").val();
    var item_qty = $("#item_qty").val();
    var item_vol = $("#item_vol").val();
    var item_weight = $("#item_weight").val();
    var item_remark = $("#item_remark").val();
    var html = '<tr>';
    html += '<td><input type="hidden" name="item_name_'+index+'" value="'+item_name+'"/>'+item_name+'</td>';
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
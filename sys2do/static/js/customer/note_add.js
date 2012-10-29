var item_index = 1;
var tmp_item = {};
var current_item = null;


function show_form(){
    $( "#dialog-form" ).dialog( "open" );
}

function hide_form(){
    $( "#dialog-form" ).dialog( "close" );
}

function search_item(id){
    for(var i=0;i<item_array.length;i++){
        var tmp = item_array[i];
        if(tmp.id == id){
            return {'index' : i, 'obj' : tmp}
        }
    }
    return {'index' : null , 'obj' : null}
}

function add_item(){
    clear_item();
    current_item = null;
    tmp_item = {};
    show_form();
}

function edit_item(id){
    var result = search_item(id);
    current_item = result.obj;
    tmp_item = result.obj;
    clear_item();
    load_item(result.obj);
    show_form();
}


function save_item(){
    var msg = Array();

    if(!$("#item_id").val() && !$("#new_item_name").val()){
        msg.push('请填写新货物的名称！');
    }
    
    if(!$("#item_id").val()){
        var item_name = $("#new_item_name").val();
    }else{
        var item_name = $("#item_id :selected").text();
    }
    
    var qty = $("#item_qty").val();
    var weight = $("#item_weight").val();
    var area = $("#item_area").val();
    
    if( !qty && !weight && !area){
        msg.push('请至少填写 数量，重量，体积 中的一项！');
    }

    if(msg.length > 0){
        alert(msg.join("\n"));
        return false;
    }
    
    tmp_item.item_id = $("#item_id").val();
    tmp_item.item_name = item_name;
    tmp_item.desc = $("#item_desc").val();
    tmp_item.qty = qty;
    tmp_item.weight = weight;
    tmp_item.area = area;
    tmp_item.remark = $("#item_remark").val();
    
    if(current_item){
        var result = search_item(tmp_item.id);
        item_array.splice(result.index,1,tmp_item);
        var html = '<tr class="data_table_tr" id=item_tr_'+tmp_item.id+'>';
        html += '<td>'+tmp_item.item_name+'</td>';
        html += '<td>'+tmp_item.desc+'</td>';
        html += '<td>'+tmp_item.qty+'</td>';
        html += '<td>'+tmp_item.weight+'</td>';
        html += '<td>'+tmp_item.area+'</td>';
        html += '<td>'+tmp_item.remark+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_item(\''+tmp_item.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_item(\''+tmp_item.id+'\')"/></td>';
        html += '</tr>';
        $("#item_tr_"+tmp_item.id).replaceWith(html);    
    }else{
        tmp_item.id = item_index++;
        item_array.push(tmp_item);
        var html = '<tr class="data_table_tr" id=item_tr_'+tmp_item.id+'>';
        html += '<td>'+tmp_item.item_name+'</td>';
        html += '<td>'+tmp_item.desc+'</td>';
        html += '<td>'+tmp_item.qty+'</td>';
        html += '<td>'+tmp_item.weight+'</td>';
        html += '<td>'+tmp_item.area+'</td>';
        html += '<td>'+tmp_item.remark+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_item(\''+tmp_item.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_item(\''+tmp_item.id+'\')"/></td>';
        html += '</tr>'
        $("#item_list").append(html);
    }
    
    hide_form(); 
    tmp_item = {};
    current_item = null;
}


function cancel_item(){
    tmp_item = {};
    current_item = null;
    hide_form();
}


function load_item(obj) {
    $("#item_id").val(obj.item_id);
    $("#item_desc").val(obj.desc);
    $("#item_qty").val(obj.qty);
    $("#item_weight").val(obj.weight);
    $("#item_area").val(obj.area);
    $("#item_remark").val(obj.remark);
    
    if(!obj.item_id){
        $("#new_item_name").val(obj.item_name);
        $("#new_item_tr").show();
    }else{
        $("#new_item_tr").hide();
    }
}

function clear_item(){
    $("#item_id").val('');
    $("#new_item_name").val('');
    $("#item_qty").val('');
    $("#item_desc").val('');
    $("#item_weight").val('');
    $("#item_area").val('');
    $("#item_remark").val('');
}

function del_item(id,obj) {
    var result = search_item(id);
    item_array.splice(result.index,1);
    $($(obj).parents("tr")[0]).remove();
}



function item_change(obj){
    var t = $(obj).val();
    if(!t){
        $("#new_item_tr").show();
        $("#item_qty").val('');
        $("#item_desc").val('');
        $("#item_desc").removeAttr('readonly');
        $("#item_weight").val('');
        $("#item_area").val('');
        $("#item_remark").val('');
    }else{
        $("#new_item_tr").hide();
        $.getJSON('/ajax_master',{
            'm' : 'inventory_item',
            'id' : t,
            't' : nowstr()
        },function(r){
            if(r.code!=0){
                alert(r.msg);
            }else{
                $("#item_desc").val(r.data.desc);
                $("#item_desc").attr('readonly',true)
            }
        });
    }
}



$(document).ready(function(){
    $("#item_id").change(function(){
        item_change(this);
    });
});
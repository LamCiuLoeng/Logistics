var item_index = 1;
var tmp_item = {};
var current_item = null;

function tosave(){
    $(".validate_error").removeClass("validate_error");
    
    var msg = Array();
    if(!$('#source_province_id').val()){
        msg.push('请填写始发站！');
        $('#source_province_id').addClass("validate_error");
    }
    
    if(!$('#ref_no').val()){
        msg.push('请填写单号！');
        $('#ref_no').addClass("validate_error");
    }
    
    if(!$('#note_id').val()){
        msg.push('请选择票据前缀！');
        $('#note_id').addClass("validate_error");
    }
    
    if(!$('#note_no').val()){
        msg.push('请填写票据单号！');
        $('#note_no').addClass("validate_error");
    }
    
    if(!$('#destination_province_id').val()){
        msg.push('请填写目的站！');
        $('#destination_province_id').addClass("validate_error");
    }
    if(!$('#source_company_id').val()){
        msg.push('请填写发货公司！');
        $('#source_company_id').addClass("validate_error");
    }
    if(!$('#source_contact').val()){
        msg.push('请填写发货人！');
        $('#source_contact').addClass("validate_error");
    }
    
    var source_mobile = $("#source_mobile").val();
    if(source_mobile && !check_mobile(source_mobile)){
        msg.push('请正确填写发货人手机号码！');
        $("#source_mobile").addClass("validate_error");
    }
        
    
    if(!$('#destination_company_id').val()){
        msg.push('请填写收货公司！');
        $('#destination_company_id').addClass("validate_error");
    }
    if(!$('#destination_contact').val()){
        msg.push('请填写收货人！');
        $('#destination_contact').addClass("validate_error");
    }
    
    var destination_mobile = $("#destination_mobile").val();
    if(destination_mobile && !check_mobile(destination_mobile)){
        msg.push('请正确填写收货人手机号码！');
        $("#destination_mobile").addClass("validate_error");
    }
    
    if(!$('#amount').val()){
        msg.push('请填写金额！');
        $('#amount').addClass("validate_error");
    }
    
    
    if(!$('#payment_id').val()){
        msg.push('请填写付款方式！');
        $('#payment_id').addClass("validate_error");
    }
    
    
    if(msg.length < 1){
        $.getJSON('/order/check_note',
                  {
                    't' : nowstr(),
                    'note_id' : $('#note_id').val(),
                    'note_no' : $('#note_no').val()
                  },
                  function(r){
                      if(r.code!=0){
                          alert(r.msg);
                          return false;
                      }else{
                          if(r.result!=0){
                              display_error(r.msg);
                              return false;
                          }else{
                              show_hold('正在保存，请稍候。。。');
                              $("#item_json").val(JSON.stringify(item_array));
                              $("form").submit();
                          }
                          
                      }
                  }
        )        
    }else{
        var s = '<ul>';
        for(var i=0;i<msg.length;i++){
            s += '<li>' + msg[i] + '</li>';
        }
        s += '</ul>';

        display_error(s);
        return false;
    }
    
}






function display_error(content){
    $("#msg_div").html(content);
    $("#msg_div").show();
}


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

    if(!$("#item_id").val()){
        msg.push('请填写货物名称名称！');
    }
    
    var item_name = $("#item_id :selected").text();
    var qty = $("#item_qty").val();
    var weight = $("#item_weight").val();
    var vol = $("#item_vol").val();
    
    if( !qty && !weight && !vol){
        msg.push('请至少填写 数量，重量，体积 中的一项！');
    }

    if(msg.length > 0){
        alert(msg.join("\n"));
        return false;
    }
    
    tmp_item.item_id = $("#item_id").val();
    tmp_item.qty = qty;
    tmp_item.weight = weight;
    tmp_item.vol = vol;
    tmp_item.remark = $("#item_remark").val();
    
    if(current_item){
        var result = search_item(tmp_item.id);
        item_array.splice(result.index,1,tmp_item);
        var html = '<tr class="data_table_tr" id=item_tr_'+tmp_item.id+'>';
        html += '<td>'+item_name+'</td>';
        html += '<td>'+tmp_item.qty+'</td>';
        html += '<td>'+tmp_item.weight+'</td>';
        html += '<td>'+tmp_item.vol+'</td>';
        html += '<td>'+tmp_item.remark+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_item(\''+tmp_item.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_item(\''+tmp_item.id+'\')"/></td>';
        html += '</tr>';
        $("#item_tr_"+tmp_item.id).replaceWith(html);    
    }else{
        tmp_item.id = item_index++;
        item_array.push(tmp_item);
        var html = '<tr class="data_table_tr" id=item_tr_'+tmp_item.id+'>';
        html += '<td>'+item_name+'</td>';
        html += '<td>'+tmp_item.qty+'</td>';
        html += '<td>'+tmp_item.weight+'</td>';
        html += '<td>'+tmp_item.vol+'</td>';
        html += '<td>'+tmp_item.remark+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_item(\''+tmp_item.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_item(\''+tmp_item.id+'\')"/></td>';
        html += '</tr>'
        $("#item_list").append(html);
    }
    
    
    //sum the total qty,weight,vol
    sumresult = sum_item();
    $("#qty").val(sumresult.qty);
    $("#weight").val(sumresult.weight);
    $("#vol").val(sumresult.vol);
    $("#vol").trigger("change");
    
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
    $("#item_qty").val(obj.qty);
    $("#item_weight").val(obj.weight);
    $("#item_vol").val(obj.vol);
    $("#item_remark").val(obj.remark);
}


function clear_item(){
    $("#item_id").val('');
    $("#item_qty").val('');
    $("#item_weight").val('');
    $("#item_vol").val('');
    $("#item_remark").val('');
}


function del_item(id,obj) {
    var result = search_item(id);
    item_array.splice(result.index,1);
    $($(obj).parents("tr")[0]).remove();
}


function sum_item(){
    var q = w = v = 0;
    for(var i=0;i<item_array.length;i++){
        var tmp = item_array[i];
        if(!isNaN(parseFloat(tmp.qty))){
            q += parseFloat(tmp.qty);
        } 
        if(!isNaN(parseFloat(tmp.weight))){
            w += parseFloat(tmp.weight);
        }
        if(!isNaN(parseFloat(tmp.vol))){
            v += parseFloat(tmp.vol);
        }  
    }
    return {'qty' : q , 'weight' : w, 'vol' : v} 
}



var attachment_index_id = 1;
function add_attachment(){
    attachment_index_id++;
    var html = '<tr class="data_table_tr">';
    html += '<td><input type="file" name="attahcment_'+attachment_index_id+'" value=""/></td>';
    html += '<td><input type="button" value="删除" onclick="del_attachment(this);"/></td>';
    html += '</tr>';
    $("#attachment_list").append(html);
}

function del_attachment(obj){
    $($(obj).parents("tr")[0]).remove();
}



$(document).ready(function(){    
    $( "#dialog-form" ).dialog({
        modal: true,
        height: 200,
        width:900,
        autoOpen: false
    });

});

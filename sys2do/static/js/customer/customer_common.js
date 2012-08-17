
var contact_index = 1;
//var contact_array = new Array();
var tmp_contact = {};
var current_contact = null;

function show_form(){
    $( "#dialog-form" ).dialog( "open" );
}

function hide_form(){
    $( "#dialog-form" ).dialog( "close" );
}


function search_contact(id){
    for(var i=0;i<contact_array.length;i++){
        var tmp = contact_array[i];
        if(tmp.id == id){
            return {'index' : i, 'obj' : tmp}
        }
    }
    return {'index' : null , 'obj' : null}
}



function add_contact(){
    clear_contact();
    current_contact = null;
    tmp_contact = {};
    show_form();
}


function edit_contact(id){
    var result = search_contact(id);
    current_contact = result.obj;
    tmp_contact = result.obj;
    clear_contact();
    load_contact(result.obj);
    show_form();
}


function clear_contact(){
    $("#contact_name").val('');
    $("#contact_address").val('');
    $("#contact_phone").val('');
    $("#contact_mobile").val('');
    $("#contact_remark").val('');  
}


function load_contact(obj) {
    $("#contact_name").val(obj.contact_name);
    $("#contact_address").val(obj.contact_address);
    $("#contact_phone").val(obj.contact_phone);
    $("#contact_mobile").val(obj.contact_mobile);
    $("#contact_remark").val(obj.contact_remark);  
}


function save_contact(){
    var contact_name = $("#contact_name").val();
    var msg = Array();
    if(!contact_name){
        msg.push('请填写联系人姓名！');
    }
    
    if(!$('#contact_address').val()){
        msg.push('请填写联系人具体地址！');
    }
    
    if( !$('#contact_phone').val() && !$('#contact_mobile').val() ){
        msg.push('请填写联系人的电话或者手提电话！');
    }
    var contact_mobile = $('#contact_mobile').val();
    if( contact_mobile && !check_mobile(contact_mobile)){
        msg.push('请正确填写联系人手提电话！');
    }
    
    if(msg.length > 0){
        alert(msg.join('\n'));
        return;
    }

    tmp_contact.contact_name = $("#contact_name").val();
    tmp_contact.contact_address = $('#contact_address').val();
    tmp_contact.contact_phone = $('#contact_phone').val();
    tmp_contact.contact_mobile = $('#contact_mobile').val();
    tmp_contact.contact_remark = $("#contact_remark").val();
    
    var html = '<tr class="data_table_tr" id=contact_tr_'+tmp_contact.id+'>';
    html += '<td>'+tmp_contact.contact_name+'</td>';
    html += '<td>'+tmp_contact.contact_address+'</td>';
    html += '<td>'+tmp_contact.contact_phone+'</td>';
    html += '<td>'+tmp_contact.contact_mobile+'</td>';
    html += '<td><input type="button" value="删除" onclick="del_contact(\''+tmp_contact.id+'\',this)"/>&nbsp;';
    html += '<input type="button" value="编辑" onclick="edit_contact(\''+tmp_contact.id+'\')"/></td>';
    html += '</tr>'
    
        
    
    if(current_contact){
        var result = search_contact(tmp_contact.id);
        contact_array.splice(result.index,1,tmp_contact);
        var html = '<tr class="data_table_tr" id=contact_tr_'+tmp_contact.id+'>';
        html += '<td>'+tmp_contact.contact_name+'</td>';
        html += '<td>'+tmp_contact.contact_address+'</td>';
        html += '<td>'+tmp_contact.contact_phone+'</td>';
        html += '<td>'+tmp_contact.contact_mobile+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_contact(\''+tmp_contact.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_contact(\''+tmp_contact.id+'\')"/></td>';
        html += '</tr>';
        $("#contact_tr_"+tmp_contact.id).replaceWith(html);    
    }else{
        tmp_contact.id = contact_index++;
        contact_array.push(tmp_contact);
        var html = '<tr class="data_table_tr" id=contact_tr_'+tmp_contact.id+'>';
        html += '<td>'+tmp_contact.contact_name+'</td>';
        html += '<td>'+tmp_contact.contact_address+'</td>';
        html += '<td>'+tmp_contact.contact_phone+'</td>';
        html += '<td>'+tmp_contact.contact_mobile+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_contact(\''+tmp_contact.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_contact(\''+tmp_contact.id+'\')"/></td>';
        html += '</tr>';
        $("#contact_list").append(html);
    }
    
    hide_form(); 
    tmp_contact = {};
    current_contact = null;
}




function cancel_contact(){
    tmp_contact = {};
    current_contact = null;
    hide_form();
}


function del_contact(id,obj) {
    var result = search_contact(id);
    contact_array.splice(result.index,1);
    $($(obj).parents("tr")[0]).remove();
}
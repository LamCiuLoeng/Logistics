var target_index = 1;
var contact_index = 1;
//var targets_array = new Array();
var tmp_target = {};
var current_target = null;




function search_target(id){
    for(var i=0;i<targets_array.length;i++){
        var tmp = targets_array[i];
        if(tmp.id == id){
            return {'index' : i, 'obj' : tmp}
        }
    }
    return {'index' : null , 'obj' : null}
}


function show_form(){
    $( "#dialog-form" ).dialog( "open" );
}

function hide_form(){
    $( "#dialog-form" ).dialog( "close" );
}


function add_target(){
    clear_target();
    current_target = null;
    tmp_target = {};
    show_form();
}

function edit_target(id){
    var result = search_target(id);
    current_target = result.obj;
    tmp_target = result.obj;
    clear_target();
    load_target(result.obj);
    show_form();
}

function clear_target(){
    $("#target_name").val('');
    $("#target_remark").val('');
    clear_contact();
}

function clear_contact(){
    $("#contact_name").val('');
    $("#contact_address").val('');
    $("#contact_phone").val('');
    $("#contact_mobile").val('');
    $("#contact_remark").val('');  
    $("#contact_list").empty();
}

function load_target(obj) {
    $("#target_name").val(obj.target_name);
    $("#target_remark").val(obj.target_remark);
    load_contact(obj.contacts);
}

function load_contact(contacts){
    var html = '';
    for(var i=0;i<contacts.length;i++){
        var tmp_contact = contacts[i];
        html += '<tr class="data_table_tr">';
        html += '<td>'+tmp_contact.contact_name+'</td>';
        html += '<td>'+tmp_contact.contact_address+'</td>';
        html += '<td>'+tmp_contact.contact_phone+'</td>';
        html += '<td>'+tmp_contact.contact_mobile+'</td>';
        html += '<td>'+tmp_contact.contact_remark+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_contact(\''+tmp_contact.id+'\',this)"/></td>'
        html += '</tr>';
    }
    $("#contact_list").html(html);
}


function add_contact(){
    var tmp_contact = {
            'id' : contact_index++,
            'contact_name' : $('#contact_name').val(),
            'contact_address' : $("#contact_address").val(),
            'contact_phone' : $("#contact_phone").val(),
            'contact_mobile' : $("#contact_mobile").val(),
            'contact_remark' : $("#contact_remark").val()
    }
    
    if(tmp_target.contacts == undefined){
        tmp_target.contacts = [tmp_contact];
    }else{
        tmp_target.contacts.push(tmp_contact);
    }
    
    var html = '<tr class="data_table_tr">';
    html += '<td>'+tmp_contact.contact_name+'</td>';
    html += '<td>'+tmp_contact.contact_address+'</td>';
    html += '<td>'+tmp_contact.contact_phone+'</td>';
    html += '<td>'+tmp_contact.contact_mobile+'</td>';
    html += '<td>'+tmp_contact.contact_remark+'</td>';
    html += '<td><input type="button" value="删除" onclick="del_contact("'+tmp_contact.id+'",this)"/></td>'
    html += '</tr>';
    $("#contact_list").append(html);
    
    
    $('#contact_name').val('');
    $("#contact_address").val('');
    $("#contact_phone").val('');
    $("#contact_mobile").val('');
    $("#contact_remark").val('');
}


function del_contact(contact_id,obj){
    var tmp_index = null;
    for(var i=0;i<tmp_target.contacts.length;i++){
        var t = tmp_target.contacts[i];
        if(t.id == contact_id){
            tmp_index = i;
            break;
        }
    }
    if(tmp_index != null){
        tmp_target.contacts.splice(tmp_index,1);
    }
    
    $($(obj).parents("tr")[0]).remove();
}


function save_target(){
    tmp_target.target_name = $("#target_name").val();
    tmp_target.target_remark = $("#target_remark").val();
    
    if(current_target){
//        tmp_target.id = current_target.id;
        var result = search_target(tmp_target.id);
        targets_array.splice(result.index,1,tmp_target);
    }else{
        tmp_target.id = target_index++;
        targets_array.push(tmp_target);
        var html = '<tr class="data_table_tr">';
        html += '<td>'+tmp_target.target_name+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_target("'+tmp_target.id+'",this)"/>';
        html += '<input type="button" value="编辑" onclick="edit_target("'+tmp_target.id+'")"/></td>';
        html += '</tr>'
        $("#targets_list").append(html);
    }
    
    hide_form(); 
    tmp_target = {};
    current_target = null;
}

function cancel_target(){
    tmp_target = {};
    current_target = null;
    hide_form();
}


function del_target(id,obj) {
    var result = search_target(id);
    targets_array.splice(result.index,1);
    $($(obj).parents("tr")[0]).remove();
}
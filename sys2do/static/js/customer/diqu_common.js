var city_index = 1;

//var city_array = new Array();
var tmp_city = {};
var current_city = null;


function search_city(id){
    for(var i=0;i<city_array.length;i++){
        var tmp = city_array[i];
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


function clear_city(){
    $("#city_name").val('');
    $("#city_code").val('');
    $("#city_shixiao").val('');
}


function load_city(obj) {
    $("#city_name").val(obj.city_name);
    $("#city_code").val(obj.city_code);
    $("#city_shixiao").val(obj.city_shixiao);
}

function save_city(){
    if(!$("#city_name").val()){
        alert('请填写市/区/县名称！');
        return false;
    }
    
    if(!$('#city_code').val()){
        alert('请填写邮政编码！');
        return false;
    }
    if(!$('#city_shixiao').val()){
        alert('请填写时效！');
        return false;
    }
    
    tmp_city.city_name = $("#city_name").val();
    tmp_city.city_code = $('#city_code').val();
    tmp_city.city_shixiao = $('#city_shixiao').val();
    
      
    if(current_city){
        var result = search_city(tmp_city.id);
        city_array.splice(result.index,1,tmp_city);
        var html = '<tr class="data_table_tr" id="objtr_"'+tmp_city.id+'>';
        html += '<th>'+tmp_city.city_name+'</th>';
        html += '<td>'+tmp_city.city_code+'</td>';
        html += '<td>'+tmp_city.city_shixiao+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_city(\''+tmp_city.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_city(\''+tmp_city.id+'\')"/></td>';
        html += '</tr>'
        $("#objtr_"+tmp_city.id).replaceWith(html);
    }else{
        tmp_city.id = city_index++;
        city_array.push(tmp_city);
        var html = '<tr class="data_table_tr" id="objtr_"'+tmp_city.id+'>';
        html += '<th>'+tmp_city.city_name+'</th>';
        html += '<td>'+tmp_city.city_code+'</td>';
        html += '<td>'+tmp_city.city_shixiao+'</td>';
        html += '<td><input type="button" value="删除" onclick="del_city(\''+tmp_city.id+'\',this)"/>&nbsp;';
        html += '<input type="button" value="编辑" onclick="edit_city(\''+tmp_city.id+'\')"/></td>';
        html += '</tr>'
        $("#city_list").append(html);
    }
    
    hide_form(); 
    tmp_city = {};
    current_city = null;
}


function cancel_city(){
    tmp_city = {};
    current_city = null;
    hide_form();
}


function del_city(id,obj) {
    var result = search_city(id);
    city_array.splice(result.index,1);
    $($(obj).parents("tr")[0]).remove();
}

function edit_city(id){
    var result = search_city(id);
    current_city = result.obj;
    tmp_city = result.obj;
    clear_city();
    load_city(result.obj);
    show_form();
}

function add_city(){
    clear_city();
    current_city = null;
    tmp_city = {};
    show_form();
}
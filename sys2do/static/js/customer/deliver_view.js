function ajax_save(params,handler){
    params['id'] = $("#id").val();
    $.post(
            "/deliver/ajax_save",
            params,
            handler
    );
}

function save_sendout() {
    var params = {
            'form_type' : 'sendout',
            'send_out_time' : $("#send_out_time").val(),
            'send_out_remark' : $("#send_out_remark").val()
    };
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
        }else{
            alert(r.msg);
        }
    })
}


function save_transit(){
    var params = {
            'form_type' : 'transit',
            'transit_time' : $("#transit_time").val(),
            'transit_remark' : $("#transit_remark").val()
    };
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr class="data_table_tr">';
            html += '<td>'+$("#transit_time").val()+'</td>';
            html += '<td>'+$('#transit_remark').val()+'</td>';
            html += '</tr>';
            
            $("#transit_list").append(html);
            $("#transit_time").val('');
            $('#transit_remark').val('');
            
        }else{
            alert(r.msg);
        }
    })
}


function save_arrived(){
    var params = {
            'form_type' : 'arrived',
            'arrived_time' : $("#arrived_time").val(),
            'arrived_remark' : $("#arrived_remark").val()
    };
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
        }else{
            alert(r.msg);
        }
    })
}
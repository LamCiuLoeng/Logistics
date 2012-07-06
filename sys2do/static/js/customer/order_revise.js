function ajax_save(params,handler){
    params['id'] = $("#id").val();
    $.post(
            "/order/ajax_save",
            params,
            handler
    );
}

function save_header() {
    var params = {
            'form_type' : 'order_header'
    };
    $("input[type=text],input[type=hidden],select,textarea","#order_header").each(function(){
       var t = $(this);
       var name = t.attr("name");
       var value = t.val();
       params[name] = value;
    });
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
        }else{
            alert(r.msg);
        }
    })
    
}

function save_item(){
    var params = {
            'form_type' : 'item_detail',
            'action_type' : 'ADD',
            'item' : $("#item_name").val(),
            'qty'  : $("#item_qty").val(),
            'vol'  : $("#item_vol").val(),
            'weight' : $("#item_weight").val(),
            'remark' : $("#item_remark").val()
    }
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr class="data_table_tr">';
            html += '<th>'+params['item']+'</th>';
            html += '<td>'+params['qty']+'</td>';
            html += '<td>'+params['vol']+'</td>';
            html += '<td>'+params['weight']+'</td>';
            html += '<td>'+params['remark']+'</td>';
            html += '<td><input type="button" onclick="del_item('+r.id+',this)" value="删除"/></td>';
            html += '</tr>';
            $("#item_list").append(html);
            
            $("#item_name").val('');
            $("#item_qty").val('');
            $("#item_vol").val('');
            $("#item_weight").val('');
            $("#item_remark").val('');
        }else{
            alert(r.msg);
        }
    })
}


function del_item(id,obj) {
    var params = {
            'form_type' : 'item_detail',
            'action_type' : 'DELETE',
            'item_id' : id
    }
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);
            $($(obj).parents('tr')[0]).remove(); 
        }else{
            alert(r.msg);
        }
    })
}

function save_receiver() {
    var params = {
            'form_type' : 'receiver',
            'receiver_contact' : $("#receiver_contact").val(),
            'receiver_tel' : $("#receiver_tel").val(),
            'receiver_mobile' : $("#receiver_mobile").val(),
            'receiver_remark' : $("#receiver_remark").val()
    }
    
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);
        }else{
            alert(r.msg);
        }
    })
    
}

function save_transit() {
    var params = {
            'form_type' : 'transit',
            'action_type' : 'ADD',
            'action_time' : $("#transit_action_time").val(),
            'remark' : $('#transit_remark').val()
    }
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr>';
            html += '<td>'+$("#transit_action_time").val()+'</td>';
            html += '<td>'+$('#transit_remark').val()+'</td>';
            html += '<td><input type="button" value="删除" onclick="del_transit('+r.transit_id+',this)"/></td>';
            html += '</tr>';
            
            $("#transit_list").append(html);
            $("#transit_action_time").val('');
            $('#transit_remark').val('');
        }else{
            alert(r.msg);
        }
    })
}


function del_transit(id,obj) {
    var params = {
            'form_type' : 'transit',
            'action_type' : 'DELETE',
            'transit_id' : id
    }
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);
            $($(obj).parents('tr')[0]).remove(); 
        }else{
            alert(r.msg);
        }
    })
}


function save_pickup() {
    var params = {
            'form_type' : 'pickup',
            'action_type' : 'ADD',
            'action_time' : $("#pickup_action_time").val(),
            'contact' : $("#pickup_contact").val(),
            'tel' : $("#pickup_tel").val(),
            'qty' : $("#pickup_qty").val(),
            'remark' : $("#pickup_remark").val()
    }
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr>';
            html += '<td>'+$("#pickup_action_time").val()+'</td>';
            html += '<td>'+$('#pickup_contact').val()+'</td>';
            html += '<td>'+$('#pickup_tel').val()+'</td>';
            html += '<td>'+$('#pickup_qty').val()+'</td>';
            html += '<td>'+$('#pickup_remark').val()+'</td>';
            html += '<td><input type="button" value="删除" onclick="del_pickup('+r.pickup_id+',this)"/></td>';
            html += '</tr>';
            
            $("#pickup_list").append(html);
            $("#pickup_action_time").val('');
            $('#pickup_contact').val('');
            $("#pickup_tel").val('');
            $('#pickup_qty').val('');
            $('#pickup_remark').val('')
        }else{
            alert(r.msg);
        }
    })
}


function del_pickup(id,obj){
    var params = {
            'form_type' : 'pickup',
            'action_type' : 'DELETE',
            'pickup_id' : id
    }
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);
            $($(obj).parents('tr')[0]).remove(); 
        }else{
            alert(r.msg);
        }
    })
}

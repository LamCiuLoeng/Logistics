function ajax_save(params,handler){
    params['id'] = $("#id").val();
    $.post(
            "/order/ajax_save",
            params,
            handler
    );
}

function open_receiver() {
    $("#reveiver_review_div").hide();
    $("#reveiver_update_div").show();
}

function close_receiver() {
    $("#reveiver_review_div").show();
    $("#reveiver_update_div").hide();
}


function save_receiver() {
    var msg = Array();
    
    if(!$('#receiver_contact_id').val()){
        msg.push('请填写收件联系人！');
    }
    if(!$('#receiver_tel').val() && !$('#receiver_mobile').val()){
        msg.push('请填写联系人电话或者手机！');
    }
    
    if(msg.length > 0){
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
        return false;
    }
    
    var params = {
            'form_type' : 'receiver',
            'receiver_contact_id' : $("#receiver_contact_id").val(),
            'receiver_tel' : $("#receiver_tel").val(),
            'receiver_mobile' : $("#receiver_mobile").val(),
            'receiver_remark' : $("#receiver_remark").val()
    }
    
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);

            $("#receiver_contact_id_span").text($("#receiver_contact_id :selected").text());
            $("#receiver_tel_span").text($("#receiver_tel").val());
            $("#receiver_mobile_span").text($("#receiver_mobile").val());
            $("#receiver_remark_span").text($("#receiver_remark").val());
        }else{
            alert(r.msg);
        }
        
        close_receiver();
        
    })
    
}


function save_warehouse(type){
    
    var msg = Array();
    if(!$('#wh_time').val()){
        if(type == 'IN'){
            msg.push('请填写货物入仓时间！');
        }else{
            msg.push('请填写货物出仓时间！');
        }
    }

    if(msg.length > 0){
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
        return false;
    }
    
    var params = {
            'form_type' : 'warehouse',
            'action' : type,
            'wh_time' : $("#wh_time").val(),
            'wh_remark' : $("#wh_remark").val()
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
    var msg = Array();
    if(!$('#transit_action_time').val()){
        msg.push('请填写运输信息时间！');
    }

    if(msg.length > 0){
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
        return false;
    }
    
    var params = {
            'form_type' : 'transit',
            'action_type' : 'ADD',
            'action_time' : $("#transit_action_time").val(),
            'remark' : $('#transit_remark').val()
    }
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr class="data_table_tr">';
            html += '<td>'+$("#transit_action_time").val()+'</td>';
            html += '<td>'+$('#transit_remark').val()+'</td>';
            /*html += '<td><input type="button" value="删除" onclick="del_transit('+r.transit_id+',this)"/></td>'; */
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



function open_signed() {
    $("#signed_review_div").hide();
    $("#signed_update_div").show();
}

function close_signed() {
    $("#signed_review_div").show();
    $("#signed_update_div").hide();
}


function save_signed(){
var msg = Array();
    
    if(!$('#signed_contact').val()){
        msg.push('请填写签收联系人！');
    }
    if(!$('#signed_time').val()){
        msg.push('请填写签收时间！');
    }
    
    if(msg.length > 0){
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
        return false;
    }
    
    var params = {
            'form_type' : 'signed',
            'signed_contact' : $("#signed_contact").val(),
            'signed_tel' : $("#signed_tel").val(),
            'signed_time' : $("#signed_time").val(),
            'signed_remark' : $("#signed_remark").val()
    }
    
    ajax_save(params,function(r){
        if(r.code == 0){
            alert(r.msg);
            $('#signed_contact_span').text($('#signed_contact').val());
            $('#signed_tel_span').text($('#signed_tel').val());
            $('#signed_time_span').text($('#signed_time').val());
            $('#signed_remark_span').text($('#signed_remark').val());
        }else{
            alert(r.msg);
        }
        close_signed();
    })
}


function save_pickup() {
    var msg = Array();
    if(!$('#pickup_action_time').val()){
        msg.push('请填写提货信息时间！');
    }
    if(!$('#pickup_contact').val()){
        msg.push('请填写提货联系人！');
    }
    if(!$('#pickup_qty').val()){
        msg.push('请填写提货数量！');
    }

    if(msg.length > 0){
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
        return false;
    }
    
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
            var html = '<tr class="data_table_tr">';
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


function change_receiver(obj){
    var t = $(obj);
    
    $("#receiver_tel").val('');
    $("#receiver_mobile").val('');
    
    if(!t.val()){
        return;
    }
    
    $.getJSON('/ajax_master',
              {
                  'm' : 'receiver_detail',
                  't' : nowstr(),
                  'id' : t.val()
              },
              function(r){
                  if(r.code!=0){
                      return;
                  }
                  $("#receiver_tel").val(r.data.tel);
                  $("#receiver_mobile").val(r.data.mobile);
              }
    );
    
}



function todo_approve(obj){ 
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('APPROVE',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='1'){
                    $(".approval_span").text("通过");
                }else{
                    $(".approval_span").text("不通过");
                }           
                show_info(r.msg);
            }   
        });
    }
}
                    

function todo_paid(obj){
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('PAID',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='0'){
                    $(".paid_span").text("未付");
                }else{
                    $(".paid_span").text("已付");
                }           
                show_info(r.msg);
            }   
        });
    }
}


function todo_supplier_paid(obj){
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('SUPLLIER_PAID',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='0'){
                    $(".supplier_paid_span").text("未付");
                }else{
                    $(".supplier_paid_span").text("已付");
                }           
                show_info(r.msg);
            }   
        });
    }
}


function todo_order_return(obj){
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('ORDER_RETURN',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='0'){
                    $(".order_return_span").text("未返");
                }else{
                    $(".order_return_span").text("已返");
                }           
                show_info(r.msg);
            }   
        });
    }
}


function todo_exception(obj){
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('EXCEPTION',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='1'){
                    $(".exception_span").text("是");
                }else{
                    $(".exception_span").text("否");
                }           
                show_info(r.msg);
            }   
        });
    }
}


function todo_less_qty(obj){
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('LESS_QTY',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                if(v=='1'){
                    $(".lessqty_span").text("是");
                }else{
                    $(".lessqty_span").text("否");
                }           
                show_info(r.msg);
            }   
        });
    }
}


function todo(type,flag,handler){   
    $.getJSON("/order/ajax_change_flag",
             {
                't' : nowstr(),
                'order_ids' : $("#id").val(),
                'type' : type,
                'flag' : flag
             },
             handler
    )
}


function display_error(content){
    $("#msg_div").html(content);
    $("#msg_div").show();
}
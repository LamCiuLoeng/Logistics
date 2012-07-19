function ajax_save(params,handler){
    params['id'] = $("#id").val();
    $.post(
            "/order/ajax_save",
            params,
            handler
    );
}

function save_header() {
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
    if(!$('#source_company_id').val()){
        msg.push('请填写发货公司！');
    }
    if(!$('#source_contact').val()){
        msg.push('请填写发货人！');
    }
    if(!$('#destination_company_id').val()){
        msg.push('请填写收货公司！');
    }
    if(!$('#destination_contact').val()){
        msg.push('请填写收货人！');
    }
    if(!$('#amount').val()){
        msg.push('请填写金额！');
    }
    
    
    if(msg.length < 1){
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
                header_have_update = 0;
            }else{
                alert(r.msg);
            }
        })
    }else{
        var s = '';
        for(var i=0;i<msg.length;i++){
            s += msg[i] + '\n';
        }
        alert(s);  
    }
}

function save_item(){
    var msg = Array();
    
    if(!$('#item_id').val()){
        msg.push('请填写货物名称！');
    }
    if(!$("#item_qty").val() && !$("#item_vol").val() && !$("#item_weight").val()){
        msg.push('请填写数量，体积或者重量中的一项或者多项！');
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
            'form_type' : 'item_detail',
            'action_type' : 'ADD',
            'item_id' : $("#item_id").val(),
            'qty'  : $("#item_qty").val(),
            'vol'  : $("#item_vol").val(),
            'weight' : $("#item_weight").val(),
            'remark' : $("#item_remark").val()
    }
    
    ajax_save(params, function(r){
        if(r.code == 0){
            alert(r.msg);
            var html = '<tr class="data_table_tr">';
            html += '<th>'+$("#item_id :selected").text()+'</th>';
            html += '<td class="item_qty_td">'+params['qty']+'</td>';
            html += '<td class="item_weight_td">'+params['weight']+'</td>';
            html += '<td class="item_vol_td">'+params['vol']+'</td>';
            html += '<td>'+params['remark']+'</td>';
            html += '<td><input type="button" onclick="del_item('+r.id+',this)" value="删除"/></td>';
            html += '</tr>';
            $("#item_list").append(html);
            
            $("#item_id").val('');
            $("#item_qty").val('');
            $("#item_vol").val('');
            $("#item_weight").val('');
            $("#item_remark").val('');
            
            $("#qty").val(mysum(".item_qty_td"));
            $("#vol").val(mysum(".item_vol_td"));
            $("#weight").val(mysum(".item_weight_td"));
            
            $("#weight").trigger('change'); //to re-compute the amount
            
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

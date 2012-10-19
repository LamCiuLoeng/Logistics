function show_form(){
    $( "#dialog-form" ).dialog( "open" );
}

function hide_form(){
    $( "#dialog-form" ).dialog( "close" );
}

function clear_discount(){
    $("#order_id").val('');
    $("#discount_ref_no").text('');
    $("#discount_amount").val('');
    $("#discount_person").val('');
    $("#discount_time").val('');
    $("#discount_remark").val('');
}



function add_discount(){
    var id = $("input[@name='order_ids']:checked").val();
    if(!id){
        show_error('请选择一条记录以进行操作！');
        return ;
    }
    clear_discount();    
    $.getJSON('/fin/ajax_get_discount',{
       't' : nowstr(),
       'id' : id
    },function(r){
        if(r.code == 0){
            var d = r.data;
            $("#order_id").val(id);
            $("#discount_ref_no").text(d.ref_no);
            $("#actual_proxy_charge").val(d.actual_proxy_charge);
            $("#discount_person_id").val(d.discount_return_person_id);
            $("#discount_return_time").val(d.discount_return_time);
            $("#discount_return_remark").val(d.discount_return_remark);
            show_form();
        }
    })
}


function discount_remark(){
    clear_discount();
    hide_form();
}

function save_discount(){
    var msg = Array();
    
    var charge = $('#actual_proxy_charge').val();
    if(!charge){
        msg.push('请填写已退回扣金额！');
    }else if(!check_number(charge)){
        msg.push('请正填写已退回扣金额，必须为数值！');
    }
    
    if(!$("#discount_return_time").val()){
        msg.push('请填写退款时间');
    }
    
    if(!$("#discount_person_id").val()){
        msg.push('请填写退款人员');
    }
    
    if(msg.length > 0){
        alert(msg.join('\n'));
        return;
    }
    
    
    $.getJSON('/fin/ajax_save_discount',{
        't' : nowstr(),
        'id' : $("#order_id").val(),
        'actual_proxy_charge' : $('#actual_proxy_charge').val(),
        'discount_return_time' : $("#discount_return_time").val(),
        'discount_return_person_id' : $("#discount_person_id").val(),
        'discount_return_remark' : $("#discount_return_remark").val()
    },function(r){
        if(r.code==0){
            alert(r.msg);
            
            var tr = $($("input[@name='order_ids']:checked").parents("tr")[0]);
            $(".td_actual_proxy_charge",tr).text($('#actual_proxy_charge').val());
            $(".td_discount_return_person",tr).text($("#discount_person_id :selected").text());
            $(".td_discount_return_time",tr).text($("#discount_return_time").val());
            $(".td_discount_return_remark",tr).text($("#discount_return_remark").val());
            
            hide_form();
        }else{
            alert(r.msg);
            hide_form();
            clear_discount();
        }
    })
}


function cancel_discount(){
    clear_discount();
    hide_form();
}
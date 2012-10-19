function todo_approve(obj){ 
    var v = $(":selected",obj).val();
    $(obj).val('');
    if(v){
        return todo('APPROVE',v,function(r){
            if(r.code != 0 ){
                show_error(r.msg);
            }else{
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='1'){
                        $(".approval_span",tr).text("通过");
                    }else{
                        $(".approval_span",tr).text("未通过");
                    }
                });             
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
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='0'){
                        $(".paid_span",tr).text("未付");
                    }else{
                        $(".paid_span",tr).text("已付");
                    }
                });             
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
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='0'){
                        $(".supplier_paid_span",tr).text("未付");
                    }else{
                        $(".supplier_paid_span",tr).text("已付");
                    }
                });             
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
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='0'){
                        $(".order_return_span").text("未返");
                    }else{
                        $(".order_return_span").text("已返");
                    }   
                });         
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
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='1'){
                        $(".exception_span").text("是");
                    }else{
                        $(".exception_span").text("否");
                    } 
                });                 
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
                $("input[name='order_ids']:checked").each(function(){
                    var tmp = $(this);
                    var tr = $(tmp.parents("tr")[0]);
                    if(v=='1'){
                        $(".lessqty_span").text("是");
                    }else{
                        $(".lessqty_span").text("否");
                    } 
                });            
                show_info(r.msg);
            }   
        });
    }
}

function todo(type,flag,handler){
    var ids = new Array();
    
    $("input[name='order_ids']:checked").each(function(){
        ids.push($(this).val());
    });
    if(ids.length < 1){
        show_error('请先选择订单然后再进行操作！');
        return false;
    }
    
    $.getJSON("/order/ajax_change_flag",
             {
                't' : nowstr(),
                'order_ids' : ids.join('|'),
                'type' : type,
                'flag' : flag
             },
             handler
    )
}
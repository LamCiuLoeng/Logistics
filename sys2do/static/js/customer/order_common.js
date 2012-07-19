function mysum(prefix){
    var count = 0;
    $(prefix).each(function(){
        var t = $(this);
        try{
            if(!isNaN(parseFloat(t.text()))){
                count += parseFloat(t.text());
            }                
        }catch (e){
            
        }
    });
    return count;
}

function compute(){
    var qty = $("#qty").val();
    var qty_ratio = $("#qty_ratio").val();
    var vol = $("#vol").val();
    var vol_ratio = $("#vol_ratio").val();
    var weight = $("#weight").val();
    var weight_ratio = $("#weight_ratio").val();
    var amount = qty * qty_ratio + vol * vol_ratio + weight * weight_ratio;
    $("#amount").val(amount);
}

function clear_source(){
    $('#source_contact').val('');
    $('#source_address').val('');
    $('#source_tel').val('');
    $('#source_mobile').val('');
    $('#payment_id').val('');
}

function clear_destination(){
    $('#destination_contact').val('');
    $('#destination_address').val('');
    $('#destination_tel').val('');
    $('#destination_mobile').val('');
}


$(document).ready(function(){
    $(".order_add_info_tab_div").tabs();
    
    $(".compute").each(function(){
        var t = $(this);
        t.change(compute);
    });
    
    $("#source_company_id").change(function(){
        var tmp = $(this);
        
        if(!tmp.val()){
            clear_source();
            clear_destination();
            $('#destination_company_id').html('');
            return
        }
        
        $.getJSON(
                '/ajax_master',
                {
                    'm' : 'customer_detail',
                    't' : nowstr(),
                    'id' : tmp.val()
                },
                function(r){
                    if(r.code==0){
                        $('#source_contact').val(r.data.contact_person);
                        $('#source_address').val(r.data.address);
                        $('#source_tel').val(r.data.phone);
                        $('#source_mobile').val(r.data.mobile);
                        $('#payment_id').val(r.data.payment_id);
                        
                        var html = '<option value=""></option>';
                        for(var i=0;i<r.targets.length;i++){
                            var t = r.targets[i];
                            html += '<option value="'+t.id+'">'+t.name+'</option>';
                        }
                        $('#destination_company_id').html(html);
                        clear_destination();
                    }else{
                        alert(r.msg)  
                    }
                }
        );
    });
    
    
    
    
    $("#destination_company_id").change(function(){
        var tmp = $(this);
        
        if(!tmp.val()){
            clear_destination();
            return
        }
        
        $.getJSON(
                '/ajax_master',
                {
                    'm' : 'target_detail',
                    't' : nowstr(),
                    'id' : tmp.val()
                },
                function(r){
                    if(r.code==0){
                        $('#destination_contact').val(r.data.contact_person);
                        $('#destination_address').val(r.data.address);
                        $('#destination_tel').val(r.data.phone);
                        $('#destination_mobile').val(r.data.mobile);                        
                    }else{
                        alert(r.msg)  
                    }
                }
        );
    });
})
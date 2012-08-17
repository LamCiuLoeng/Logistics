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
    var amount = 0;

    var qty = $("#qty").val();
    var qty_ratio = $("#qty_ratio").val();
    var vol = $("#vol").val();
    var vol_ratio = $("#vol_ratio").val();
    var weight = $("#weight").val();
    var weight_ratio = $("#weight_ratio").val();
    
    if(qty && !isNaN(qty) && qty_ratio && !isNaN(qty_ratio)){
        amount += parseInt(qty) * parseFloat(qty_ratio); 
    }
    
    if(vol && !isNaN(vol) && vol_ratio && !isNaN(vol_ratio)){
        amount += parseFloat(vol) * parseFloat(vol_ratio); 
    }
    
    if(weight && !isNaN(weight) && weight_ratio && !isNaN(weight_ratio)){
        amount += parseFloat(weight) * parseFloat(weight_ratio); 
    }
    
    var charge = ['insurance_charge','sendout_charge','receive_charge','package_charge','load_charge','unload_charge','proxy_charge','other_charge'];
    for(var i=0;i<charge.length;i++){
        var t = charge[i];
        var v = $("#"+t).val();
        if(v && !isNaN(v)){
            amount += parseFloat(v);
        }
    }
    $("#amount").val(amount);    
}

function clear_source(){
    $('#source_contact').val('');
    $('#source_address').val('');
    $('#source_tel').val('');
    $('#source_mobile').val('');
    $('#payment_id').val('');
    $('#source_province_id').val('');
    $("#source_city_id").empty();
    $("input[type='checkbox'][name='source_sms']").removeAttr('checked');
    $("#note_id").val('');
    $("#note_no").val('');
}

function clear_destination(){
    $('#destination_contact').val('');
    $('#destination_address').val('');
    $('#destination_tel').val('');
    $('#destination_mobile').val('');
    $("#destination_province_id").val('');
    $("#destination_city_id").empty();
    $("#estimate_time").val('');
    $('#destination_province_id').val('');
    $("#destination_city_id").empty();
    $("input[type='checkbox'][name='destination_sms']").removeAttr('checked');
}



function customer_change(){
    var tmp = $("#customer_id");
    
    if(!tmp.val()){
        clear_source();
        $('#source_company_id').empty();
        clear_destination();
        $('#destination_company_id').empty();
        return;
    }
    
    $.getJSON(
            '/ajax_master',
            {
                'm' : 'customer_detail',
                't' : nowstr(),
                'need_city_list' : 1, //also return back the city master list
                'id' : tmp.val()
            },
            function(r){
                if(r.code==0){
                    var html = '<option value=""></option>';
                    for(var i=0;i<r.sources.length;i++){
                        var t = r.sources[i];
                        html += '<option value="'+t.id+'">'+t.name+'</option>';
                    }
                    $('#source_company_id').html(html);
                    clear_source();
                    
                    var html = '<option value=""></option>';
                    for(var i=0;i<r.targets.length;i++){
                        var t = r.targets[i];
                        html += '<option value="'+t.id+'">'+t.name+'</option>';
                    }
                    $('#destination_company_id').html(html);
                    clear_destination();
                    
                    $("#note_id").val(r.data.note_id);
                }else{
                    alert(r.msg)  
                }
            }
    );
    
}


function source_change(){
var tmp = $("#source_company_id");
    
    if(!tmp.val()){
        clear_source();
        return
    }
    
    $.getJSON(
            '/ajax_master',
            {
                'm' : 'source_detail',
                't' : nowstr(),
                'need_city_list' : 1, //also return back the city master list
                'id' : tmp.val()
            },
            function(r){
                if(r.code==0){
                    if(r.data.contact.address){
                        $('#source_address').val(r.data.contact.address);
                    }
                    if(r.data.contact.name){
                        $('#source_contact').val(r.data.contact.name);
                    }
                    if(r.data.contact.phone){
                        $('#source_tel').val(r.data.contact.phone);
                    }
                    if(r.data.contact.mobile){
                        $('#source_mobile').val(r.data.contact.mobile);                        
                    }
                    
                    $("#source_province_id").val(r.data.province_id);
                    var city_html = '<option value=""></option>';
                    for(var j=0;j<r.cities.length;j++){
                        var t = r.cities[j];
                        city_html += '<option value="'+t.id+'">'+t.name+'</option>';
                    }
                    $("#source_city_id").html(city_html);
                    $("#source_city_id").val(r.data.city_id);
                    //$("#source_city_id").trigger('change');
                    $("#payment_id").val(r.data.payment_id);
                }else{
                    alert(r.msg);
                }
            }
    );
}



function destination_change(){
    var tmp = $("#destination_company_id");
    
    if(!tmp.val()){
        clear_destination();
        return
    }
    
    $.getJSON(
            '/ajax_master',
            {
                'm' : 'target_detail',
                't' : nowstr(),
                'need_city_list' : 1, //also return back the city master list
                'id' : tmp.val()
            },
            function(r){
                if(r.code==0){
                    if(r.data.contact.address){
                        $('#destination_address').val(r.data.contact.address);
                    }
                    if(r.data.contact.name){
                        $('#destination_contact').val(r.data.contact.name);
                    }
                    if(r.data.contact.phone){
                        $('#destination_tel').val(r.data.contact.phone);
                    }
                    if(r.data.contact.mobile){
                        $('#destination_mobile').val(r.data.contact.mobile);                        
                    }
                    
                    $("#destination_province_id").val(r.data.province_id);
                    var city_html = '<option value=""></option>';
                    for(var j=0;j<r.cities.length;j++){
                        var t = r.cities[j];
                        city_html += '<option value="'+t.id+'">'+t.name+'</option>';
                    }
                    $("#destination_city_id").html(city_html);
                    $("#destination_city_id").val(r.data.city_id);
                    $("#destination_city_id").trigger('change');
                    
                }else{
                    alert(r.msg);
                }
            }
    );
}



function estimate_by_diqu(){
    $.getJSON('/compute_by_diqu',
              {
                't' : nowstr(),
                'province_id' : $("#destination_province_id").val(),
                'city_id' : $("#destination_city_id").val(),
                'customer_id' : $("#customer_id").val()
              },
              function(r){
                  if(r.code == 0){
                      $("#estimate_time").val(r.day);
                      $("#qty_ratio").val(r.qty_ratio);
                      $("#weight_ratio").val(r.weight_ratio);
                      $("#vol_ratio").val(r.vol_ratio);
                      $("#vol_ratio").trigger('change');
                  }
              }
    )
}


//function get_ratio(){
//    var province_id = $("#destination_province_id").val();
//    var city_id = $("#destination_city_id").val();
//    var customer_id = $("#source_company_id").val();
//    $.getJSON('/compute_ratio',{
//        't' : nowstr(),
//        'province_id' : province_id,
//        'city_id' : city_id,
//        'customer_id' : customer_id
//    },function(r){
//        if(r.code != 0 ){
//            
//        }else{
//            $("#qty_ratio").val(r.qty_ratio);
//            $("#weight_ratio").val(r.weight_ratio);
//            $("#vol_ratio").val(r.vol_ratio);
//            $("#vol_ratio").trigger('change');
//        }
//    });
//    
//}





$(document).ready(function(){
    $(".order_add_info_tab_div").tabs();
    
    $(".compute").each(function(){
        var t = $(this);
        t.change(compute);
    });
    
    $("#source_province_id").change(function(){
        province_change(this,'#source_city_id');
    });
    
    $("#destination_province_id").change(function(){
        province_change(this,'#destination_city_id',estimate_by_diqu);
    });
    
    
    $("#destination_city_id").change(function(){
        estimate_by_diqu();
    });
    
    
    $("#customer_id").change(function(){
        customer_change();
    });

    
    $("#source_company_id").change(function(){
        source_change();
    });
    
    
    $("#source_contact").autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/ajax_master",
                dataType: "json",
                data: {
                    't' : nowstr(),
                    'm' : 'contact_search',
                    'type' : 'S',
                    'refer_id' : $('#source_company_id').val(),
                    'customer_contact' : $("#source_contact").val()
                },
                success: function( data ) {
                    response( $.map( data.data, function( item ) {
                        return {
                            label: item.name,
                            value: item.name,
                            phone : item.phone,
                            mobile : item.mobile,
                            address : item.address
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function( event, ui ) {            
            $("#source_tel").val(ui.item.phone);
            $("#source_mobile").val(ui.item.mobile);
            $("#source_address").val(ui.item.address);
        }
    });
    
    
    $("#destination_company_id").change(function(){
        destination_change();
    });
    
    
    
    $("#destination_contact").autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "/ajax_master",
                dataType: "json",
                data: {
                    't' : nowstr(),
                    'm' : 'contact_search',
                    'type' : 'T',
                    'refer_id' : $('#destination_company_id').val(),
                    'customer_contact' : $("#destination_contact").val()
                },
                success: function( data ) {
                    response( $.map( data.data, function( item ) {
                        return {
                            label: item.name,
                            value: item.name,
                            phone : item.phone,
                            mobile : item.mobile,
                            address : item.address
                        }
                    }));
                }
            });
        },
        minLength: 1,
        select: function( event, ui ) {            
            $("#destination_tel").val(ui.item.phone);
            $("#destination_mobile").val(ui.item.mobile);
            $("#destination_address").val(ui.item.address);
        }
    });
    
    
})
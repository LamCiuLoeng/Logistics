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
    
    var charge = ['insurance_charge','sendout_charge','receive_charge','package_charge','other_charge'];
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
}

function clear_destination(){
    $('#destination_contact').val('');
    $('#destination_address').val('');
    $('#destination_tel').val('');
    $('#destination_mobile').val('');
    $("#destination_province_id").val('');
    $("#destination_city_id").empty();
    $("#estimate_time").val('');
}



function customer_change(){
    var tmp = $("#source_company_id");
    
    if(!tmp.val()){
        clear_source();
        clear_destination();
        $('#destination_company_id').html('');
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
                    
                    $("#source_province_id").val(r.data.province_id);
                    
                    var city_html = '<option value=""></option>';
                    for(var j=0;j<r.cities.length;j++){
                        var t = r.cities[j];
                        city_html += '<option value="'+t.id+'">'+t.name+'</option>';
                    }
                    $("#source_city_id").html(city_html);
                    $("#source_city_id").val(r.data.city_id);
                }else{
                    alert(r.msg)  
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
    $.getJSON('/compute_day_by_diqu',
              {
                't' : nowstr(),
                'province_id' : $("#destination_province_id").val(),
                'city_id' : $("#destination_city_id").val()
              },
              function(r){
                  if(r.code == 0){
                      $("#estimate_time").val(r.day)
                  }
              }
    )
}




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
    
    
    $("#source_company_id").change(function(){
        customer_change();
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
                    'm' : 'target_contact_search',
                    'customer_target_id' : $('#destination_company_id').val(),
                    'customer_target_contact' : $("#destination_contact").val()
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
function clear_supplier(){
    $('#supplier_contact').val('');
    $('#supplier_tel').val('');
}

/*
function compute(){
    var amount = 0;
    $(".compute").each(function(){
        var tmp = $(this).val();
        if(tmp && !isNaN(tmp)){
            amount += parseFloat(tmp);
        }
    });
    $("#amount").val(amount);
    //$("#amount_span").text(amount);
}
*/

function compute_total_amount(){
    var amount = 0;
    $(".compute").each(function(){
        var tmp = $(this).val();
        if(tmp && !isNaN(tmp)){
            amount += parseFloat(tmp);
        }
    });
    
    var fields = ['qty','vol','weight'];
    for(var i=0;i<fields.length;i++){
        var n = fields[i];
        var v1 = $("#"+n).val();
        var v2 = $("#"+n+"_ratio").val();
        
        if(v1 && !isNaN(v1) && v2 && !isNaN(v2)){
            amount += parseFloat(v1) * parseFloat(v2);
        }
    }  
    $("#amount").val(amount);
}



function count_charge(prefix,total){
    var result = 0;
    $("input[type='text'][name^='"+prefix+"']").each(function(){
        var tmp = $(this).val();
        if(tmp && !isNaN(tmp)){
            result += parseFloat(tmp);
        }
    });
    $(total).val(result).trigger('change');

}


function count_charge_by_row(obj){
    var t = $(obj);
    var id = getid(obj);
    var qty = 0;
    var qty_ratio = 0;
    var vol = 0;
    var vol_ratio = 0;
    var weight = 0;
    var weight_ratio = 0;
    
    var qty_input = $("#qty_"+id).val();
    if(qty_input && !isNaN(qty_input)){ qty = parseInt(qty_input); }
    var qty_ratio_input = $("#qty_ratio").val();
    if(qty_ratio_input && !isNaN(qty_ratio_input)){ qty_ratio = parseFloat(qty_ratio_input); }
    
    var vol_input = $("#vol_"+id).val();
    if(vol_input && !isNaN(vol_input)){ vol = parseFloat(vol_input); }
    var vol_ratio_input = $("#vol_ratio").val();
    if(vol_ratio_input && !isNaN(vol_ratio_input)){ vol_ratio = parseFloat(vol_ratio_input); }
    
    var weight_input = $("#weight_"+id).val();
    if(weight_input && !isNaN(weight_input)){ weight = parseFloat(weight_input); }
    var weight_ratio_input = $("#weight_ratio").val();
    if(weight_ratio_input && !isNaN(weight_ratio_input)){ weight_ratio = parseFloat(weight_ratio_input); }
    
    var tr = $(t.parents("tr")[0]);
    var result = qty*qty_ratio + vol*vol_ratio + weight*weight_ratio;
    $(".number_field",tr).each(function(){
        var tmp = $(this).val();
        if(tmp && !isNaN(tmp)){
            result += parseFloat(tmp);
        }
    });
    $("input[type='text'][name^='amount_']",tr).val(result);
}




function value_change(prefix,result_id,method){
    var total = 0;
    $(".data_table_tr input[type='text'][name^='"+prefix+"']").each(function(){
        var t = $(this).val();
        
        if(t && !isNaN(t)){
            total += parseFloat(t);
        }
    });
    $("#"+result_id).val(total).trigger('change');
}



var attachment_index_id = 1;
function add_attachment(){
    attachment_index_id++;
    var html = '<tr class="data_table_tr">';
    html += '<td><input type="file" name="attahcment_'+attachment_index_id+'" value="" size="60"/></td>';
    html += '<td><input type="button" value="删除" onclick="del_attachment(this);"/></td>';
    html += '</tr>';
    $("#attachment_list").append(html);
}

function del_attachment(obj){
    $($(obj).parents("tr")[0]).remove();
}



function getdiqu(){
    var province_id = $("#destination_province_id").val();
    var supplier_id = $("#supplier_id").val();
    var city_id = $("#destination_city_id").val();
    if(city_id == null){
        city_id = '';
    }
    
    
    if(!province_id || !supplier_id){
        return;
    }
    
    $.getJSON('/deliver/ajax_compute_ratio',
              {
                'province_id' : province_id,
                'city_id' : city_id,
                'supplier_id' : supplier_id,
                't' : nowstr()
              },
              function(r){
                  if(r.code!=0){
                      
                  }else{
                      $("#qty_ratio").val(r.qty_ratio);
                      $("#weight_ratio").val(r.weight_ratio);
                      $("#vol_ratio").val(r.vol_ratio);
                      $("input[type='text'][name^='insurance_charge_']").trigger('change');
                  }
              }
    );
    
}




$(document).ready(function(){
    $("#destination_province_id").change(function(){
        province_change(this,'#destination_city_id');
    });
    
    $(".compute").change(compute_total_amount);
    $("#qty,#qty_ratio,#vol,#vol_ratio,#weight,#weight_ratio").change(compute_total_amount);
    
    $("#supplier_id").change(function(){
        var tmp = $(this);
        
        if(!tmp.val()){
            clear_supplier();
            return;
        }
        
        $.getJSON('/ajax_master',
                  {
                    'm' : 'supplier_detail',
                    't' : nowstr(),
                    'id' : tmp.val()
                  },
            
                  function(r){
                      if(r.code==0){
                          $('#supplier_contact').val(r.data.contact_person);
                          $('#supplier_tel').val(r.data.phone);
                      }else{
                          
                      }
                  }
        );
    });
    
    $("#destination_province_id,#destination_city_id,#supplier_id").change(function(){
        getdiqu();
    });
    
    
    
    $("input[type='text'][name^='insurance_charge_']").change(function(){
        count_charge("insurance_charge_","#insurance_charge");
        count_charge_by_row(this);
    });

    $("input[type='text'][name^='sendout_charge_']").change(function(){
        count_charge("sendout_charge_","#sendout_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='receive_charge_']").change(function(){
        count_charge("receive_charge_","#receive_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='package_charge_']").change(function(){
        count_charge("package_charge_","#package_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='load_charge_']").change(function(){
        count_charge("load_charge_","#load_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='unload_charge_']").change(function(){
        count_charge("unload_charge_","#unload_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='proxy_charge_']").change(function(){
        count_charge("proxy_charge_","#proxy_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='other_charge_']").change(function(){
        count_charge("other_charge_","#other_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='carriage_charge_']").change(function(){
        count_charge("carriage_charge_","#carriage_charge");
        count_charge_by_row(this);
    });
    
    $("input[type='text'][name^='amount_']").change(function(){
        count_charge("amount_","#amount");
        count_charge_by_row(this);
    });
    
    
    $(".data_table_tr input[type='text'][name^='qty_']").change(function(){
        value_change('qty_','qty',parseInt);
        var id = getid(this);
        $("input[name='insurance_charge_"+id+"']").trigger('change');
        
    });
    
    $(".data_table_tr input[type='text'][name^='vol_']").change(function(){
        value_change('vol_','vol',parseFloat);
        var id = getid(this);
        $("input[name='insurance_charge_"+id+"']").trigger('change');
    });
    
    $(".data_table_tr input[type='text'][name^='weight_']").change(function(){
        value_change('weight_','weight',parseFloat);
        var id = getid(this);
        $("input[name='insurance_charge_"+id+"']").trigger('change');
    });
    
});


function getid(obj){
    var t = $(obj);
    var name = t.attr("name");
    var id = name.substr(name.lastIndexOf("_")+1);
    return id;
}
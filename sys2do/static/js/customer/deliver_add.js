function clear_supplier(){
    $('#supplier_contact').val('');
    $('#supplier_tel').val('');
}


function compute(){
    var amount = 0;
    $(".compute").each(function(){
        var tmp = $(this).val();
        if(tmp && !isNaN(tmp)){
            amount += parseFloat(tmp);
        }
    });
    $("#amount").val(amount);
    $("#amount_span").text(amount);
}


function count_charge(prefix,total){
    var result = 0
    $("input[type='text'][name^='"+prefix+"']").each(function(){
        var tmp = $(this).val();
        if(check_number(tmp)){
            result += parseFloat(tmp);
        }
    });
    $(total).val(result).trigger('change');
    
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



$(document).ready(function(){
    $("#destination_province_id").change(function(){
        province_change(this,'#destination_city_id');
    });
    
    $(".compute").change(compute);
    
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
    
    
    $("input[type='text'][name^='insurance_charge_']").change(function(){
        count_charge("insurance_charge_","#insurance_charge");
    });

    $("input[type='text'][name^='sendout_charge_']").change(function(){
        count_charge("sendout_charge_","#sendout_charge");
    });
    
    $("input[type='text'][name^='receive_charge_']").change(function(){
        count_charge("receive_charge_","#receive_charge");
    });
    
    $("input[type='text'][name^='package_charge_']").change(function(){
        count_charge("package_charge_","#package_charge");
    });
    
    $("input[type='text'][name^='load_charge_']").change(function(){
        count_charge("load_charge_","#load_charge");
    });
    
    $("input[type='text'][name^='unload_charge_']").change(function(){
        count_charge("unload_charge_","#unload_charge");
    });
    
    $("input[type='text'][name^='proxy_charge_']").change(function(){
        count_charge("proxy_charge_","#proxy_charge");
    });
    
    $("input[type='text'][name^='other_charge_']").change(function(){
        count_charge("other_charge_","#other_charge");
    });
    
    $("input[type='text'][name^='carriage_charge_']").change(function(){
        count_charge("carriage_charge_","#carriage_charge");
    });
    
    $("input[type='text'][name^='amount_']").change(function(){
        count_charge("amount_","#amount");
    });
    
    
    $(".sub_charge_tr").each(function(){
        var tr = $(this);
        $(".number_field",tr).change(function(){
            var result = 0;
            $(".number_field",tr).each(function(){
                var tmp = $(this).val();
                if(check_number(tmp)){
                    result += parseFloat(tmp);
                }
            });
            $("input[type='text'][name^='amount']").val(result);
        });
    });
});
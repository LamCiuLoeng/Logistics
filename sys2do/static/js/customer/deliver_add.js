function clear_supplier(){
    $('#supplier_contact').val('');
    $('#supplier_tel').val('');
}

$(document).ready(function(){
    $("#destination_province_id").change(function(){
        province_change(this,'#destination_city_id');
    });
    
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
    
});
function redirect(url) {
    window.location = url;
}

function bind_province_city_district(province_id,city_id,district_id){
//    alert(province_id+city_id+district_id);
    //bind province and city
    $(province_id).change(function(){
        var s = $(this);
        $.getJSON(
                '/ajax_master',
                {
                    'm'   : 'city',
                    'pid' : s.val()
                },
                function(req){
                    if(req.status != 0){
                        alert('Error!');
                    }else{
                        var city = $(city_id);
                        city.empty();
                        city.append('<option>Please Select One</option>');
                        $.each(req.data,function(i,item){
                            city.append('<option value="'+item.id+'">'+item.name+'</option>');
                        });
                    }
                }
        );
        
    });
    
    if(district_id){
        //bind city and district
        $(city_id).change(function(){
            var s = $(this);
            $.getJSON(
                    '/ajax_master',
                    {
                        'm'   : 'district',
                        'cid' : s.val()
                    },
                    function(req){
                        if(req.status != 0){
                            alert('Error!');
                        }else{
                            var district = $(district_id);
                            district.empty();
                            district.append('<option>Please Select One</option>');
                            $.each(req.data,function(i,item){
                                district.append('<option value="'+item.id+'">'+item.name+'</option>');
                            });
                        }
                    }
            );
            
        });
    }
    
}
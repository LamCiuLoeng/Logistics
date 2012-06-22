function menu_hover(menu_bt){
$(menu_bt).attr("class","menu_hover_highlight"); 
}
function menu_hover_highlight(menu_bt){
$(menu_bt).attr("class","menu_hover"); 
}

function MM_jumpMenu(targ,selObj,restore){ //v3.0
  eval(targ+".location='"+selObj.options[selObj.selectedIndex].value+"'");
  if (restore) selObj.selectedIndex=0;
}

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
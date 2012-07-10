function check_ids(id,obj){
    var t = $(obj);
    var params = {
            'id' : id
    }
    
    if(t.attr("checked")){
        params['action'] = 'ADD';
    }else{
        params['action'] = 'DEL';
    }
        
    $.getJSON(
            '/deliver/ajax_check_ids',
            params,
            function (r){
                
            }
    )
}
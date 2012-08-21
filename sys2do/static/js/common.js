function menu_move_over(menu_bt) {
    $(menu_bt).addClass('bt_highlight');
}
function menu_move_out(menu_bt) {
    $(menu_bt).removeClass('bt_highlight');
}

function MM_preloadImages() { //v3.0
    var d = document;
    if (d.images) {
        if (!d.MM_p)
            d.MM_p = new Array();
        var i, j = d.MM_p.length, a = MM_preloadImages.arguments;
        for (i = 0; i < a.length; i++)
            if (a[i].indexOf("#") != 0) {
                d.MM_p[j] = new Image;
                d.MM_p[j++].src = a[i];
            }
    }
}

function MM_swapImgRestore() { //v3.0
    var i, x, a = document.MM_sr;
    for (i = 0; a && i < a.length && (x = a[i]) && x.oSrc; i++)
        x.src = x.oSrc;
}

function MM_findObj(n, d) { //v4.01
    var p, i, x;
    if (!d)
        d = document;
    if ((p = n.indexOf("?")) > 0 && parent.frames.length) {
        d = parent.frames[n.substring(p + 1)].document;
        n = n.substring(0, p);
    }
    if (!(x = d[n]) && d.all)
        x = d.all[n];
    for (i = 0; !x && i < d.forms.length; i++)
        x = d.forms[i][n];
    for (i = 0; !x && d.layers && i < d.layers.length; i++)
        x = MM_findObj(n, d.layers[i].document);
    if (!x && d.getElementById)
        x = d.getElementById(n);
    return x;
}

function MM_swapImage() { //v3.0
    var i, j = 0, x, a = MM_swapImage.arguments;
    document.MM_sr = new Array;
    for (i = 0; i < (a.length - 2); i += 3)
        if ((x = MM_findObj(a[i])) != null) {
            document.MM_sr[j++] = x;
            if (!x.oSrc)
                x.oSrc = x.src;
            x.src = a[i + 2];
        }
}
function MM_jumpMenu(targ, selObj, restore) { //v3.0
    eval(targ + ".location='" + selObj.options[selObj.selectedIndex].value
            + "'");
    if (restore)
        selObj.selectedIndex = 0;
}


function redirect(url) {
    window.location = url;
}

function redirect_alert(msg,url){
    if(confirm(msg)){
        redirect(url);
    }else{
        return false;
    }
}

function refresh(){
    window.location.reload();
}


function province_change(obj,city,handler){
    var t = $(obj);
    
    var c = $(city);
    c.empty();
    if(!t.val()){
        return ;
    }
    
    $.getJSON('/ajax_master',
             {
                't' : nowstr(),
                'm' : 'province_city',
                'pid' : $(":selected",t).val()
             },
             function(r){
                 if(r.code!=0){
                     
                 }else{
                     var html = '<option value=""></option>';
                     for(var i=0;i<r.data.length;i++){
                         var tmp = r.data[i];
                         html += '<option value="'+tmp.id+'">'+tmp.name+'</option>';
                     }
                     c.html(html);
                 }
                 
                 if(handler){
                     handler();
                 }
                 
             }
    );
    
}


function nowstr(){
    return Date.parse(new Date())
}

function check_mobile(v){
    var pattern = /^1\d{10}$/;
    return pattern.test(v);
}


function check_number(v){
    var pattern = /^[\d\.]+$/;
    return pattern.test(v); 
}
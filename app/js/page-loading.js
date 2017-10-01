var lastLoaded;
function loadPage(page){

    $("#content").load(page+'.html');
    var selector = "." + page;
    if(page != lastLoaded){
        $(".subElement"+ selector).css("display","none");
        $(".subElement").slideUp(200);
    }
    $(".subElement"+ selector).slideDown(200,function(){
        $(".subElement"+ selector).css("display","table");
    });
    lastLoaded = page;

}
function loadSubPage(page){
    $("#content").load(page+'.html');
}
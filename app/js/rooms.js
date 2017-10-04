var list = {
    "L35": {
    "temperature": 24,
        "lampe": true
    },
    "L41": {
    "temperature": 16,
        "lampe": false
    },
    "L42": {
    "temperature": 16,
        "lampe": false
    },
    "L63": {
        "temperature": 46,
        "lampe": false
    }
};

$(document).ready(function(){
    for(i in list){
        $("<div class='room col-md-3' data-room='"+i+"'></div>").appendTo("#roomList");
        var selector =  $(".room[data-room='"+i+"']");
        selector.append("<div class='row'>");
        selector.append("<h3 class='col-md-4'>"+i+"</h3>");
        selector.append("<div class='col-md-8'>");
        selector.append("<img src='img/thermometer.png'>");
        selector.append("<h3>"+list[i]["temperature"]+" °C</h3>");
        selector.append("</div>");
        selector.append("</div>");
        selector.append("<div class='row'>");
        selector.append("<span class='col-md-4'>&nbsp</span>");
        selector.append("<div class='col-md-8'>");
        if(list[i]["lampe"]){
            selector.append("<img src='img/light-on.png'>");
            selector.append("<h3>ON</h3>");
        }else{
            selector.append("<img src='img/light-off.png'>");
            selector.append("<h3>OFF</h3>");
        }
        selector.append("</div>");
        selector.append("</div>");

    }
});
function createList(rooms) {
    for (i in rooms) {
        $("<div class='roomContainer col-md-4 ' data-room='" + i + "'></div>").appendTo("#roomList");
        $("<div class='room'></div>").appendTo(".roomContainer[data-room='" + i + "']");
        var selector = $(".roomContainer[data-room='" + i + "'] > .room");
        selector.bind("click",function(){
            selectRoom($(this).parent().data("room"));
        });
        var floor;
        if(rooms[i].typeRoom == "1"){
            selector.addClass("room_auditorium");
        }
       else if(rooms[i].typeRoom == "2"){
            selector.addClass("room_regular");
        }

        if(rooms[i].numFloor == "0"){
            floor = "Rez de chaussée";
        }
        else if(rooms[i].numfloor == "1"){
            floor = "1er étage";
        }
        selector.append("<h2 class='col-md-12'>" + i + "</h2>");
       if(rooms[i].idBuilding == "1"){
           selector.append("<h3 class='col-md-12'>Louvain-la-Neuve </h3>");
       }
       selector.append("<h4 class='col-md-12'>"+floor+"</h4>");
    }
}

function selectRoom(room_id){

        $(".roomContainer").removeClass('col-md-8');
        $(".roomContainer").addClass('col-md-4');
        $(".roomContainer").css("height","33%");
        $(".roomContainer").css("background-size","24%");
        $(".roomContainer[data-room='"+room_id+"']").removeClass('col-md-4');
        $(".roomContainer[data-room='"+room_id+"']").addClass('col-md-8');
        $(".roomContainer[data-room='"+room_id+"']").css("height","66%");
        $(".roomContainer[data-room='"+room_id+"']").css("order","1");
        $(".roomContainer[data-room='"+room_id+"']>.room").css("background-size","12%");

}
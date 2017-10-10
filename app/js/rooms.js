function createList(rooms) {
    for (i in rooms) {
        $("<div class='roomContainer col-md-6 col-xs-6' data-room='" + i + "'></div>").appendTo("#roomList");
        $("<div class='room'></div>").appendTo(".roomContainer[data-room='" + i + "']");
        var selector = $(".roomContainer[data-room='" + i + "'] > .room");
            if(rooms[i].typeRoom == "1"){
                selector.addClass("room_auditorium");
            }
           else if(rooms[i].typeRoom == "2"){
                selector.addClass("room_regular");
            }

            selector.append("<h3 class='col-md-12'>" + i + "</h3>");
    }
}
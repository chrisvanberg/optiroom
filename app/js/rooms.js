function createList(rooms) {
    for (i in rooms) {
        $("<div class='roomContainer col-md-4 ' data-room='" + rooms[i].room_id + "'></div>").appendTo("#roomList");
        $("<div class='room'></div>").appendTo(".roomContainer[data-room='" + rooms[i].room_id + "']");
        var selector = $(".roomContainer[data-room='" + rooms[i].room_id + "'] > .room");
        selector.bind("click",function(){
            selectRoom($(this).parent().data("room"));
        });
        var floor;
        if(rooms[i].roomType == "1"){
            selector.addClass("room_auditorium");
        }
       else if(rooms[i].roomType == "2"){
            selector.addClass("room_regular");
        }

        if(rooms[i].floorNum == "0"){
            floor = "Rez de chaussée";
        }
        else if(rooms[i].floorNum == "1"){
            floor = "1er étage";
        }
        selector.append("<h2 class='col-md-12'>" + rooms[i].room_id + "</h2>");
        selector.append("<h3 class='col-md-12'>"+rooms[i].building_name+ "</h3>");
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

function getOutput(phpFile) {
    var output;
    $.ajax({
        async : false,
        url:phpFile+'.php',
        complete: function (response) {
           output = (response.responseText);
        },
        error: function () {
            console.log("Erreur PHP");
        }
    });
    return output;
}
$(document).ready(function() {
    var roomList = getOutput("room-list");
    createList(JSON.parse(roomList));
});
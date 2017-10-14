function createList(rooms) {
    var floor;
    for (i in rooms) {
        $("<div class='room-container col-md-4 ' data-room='" + rooms[i].room_id + "'></div>").appendTo("#room-list");
        $("<div class='room'></div>").appendTo(".room-container[data-room='" + rooms[i].room_id + "']");
        var selector = $(".room-container[data-room='" + rooms[i].room_id + "'] > .room");
        selector.bind("click",function(){
            selectRoom($(this).parent().data("room"));
        });
        if(rooms[i].roomType == "1"){
            selector.addClass("room-auditorium");
        }
       else if(rooms[i].roomType == "2"){
            selector.addClass("room-regular");
        }
        switch (rooms[i].floorNum){
            case 0:
                floor = "Rez de chaussée";
                break;
            case 1:
                floor = "1er étage";
                break;
            case 2:
                floor = "2ème étage";
                break;
            case 3:
                floor = "3ème étage";
        }
        selector.append("<h2 class='col-md-12'>" + rooms[i].room_id + "</h2>");
        selector.append("<h3 class='col-md-12'>"+rooms[i].building_name+ "</h3>");
        selector.append("<h4 class='col-md-12'>"+floor+"</h4>");
    }
}
var selectedRoom;
function selectRoom(room_id){
    $(".room-container").removeClass('col-md-8');
    $(".room-container").addClass('col-md-4');
    $(".room-container").css("height","33%");
    $(".room-container").css("background-size","24%");
    if(room_id != selectedRoom){
        selectedRoom = room_id;
        $(".room-container[data-room='"+room_id+"']").removeClass('col-md-4');
        $(".room-container[data-room='"+room_id+"']").addClass('col-md-8');
        $(".room-container[data-room='"+room_id+"']").css("height","66%");
        $(".room-container[data-room='"+room_id+"']").css("order","1");
        $(".room-container[data-room='"+room_id+"']>.room").css("background-size","12%");
    }else{
        selectedRoom = "";
    }
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
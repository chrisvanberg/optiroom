var rooms;


function createList() {
    for (i in rooms) {
        $("<div class='room col-md-2 col-xs-3' data-room='" + i + "'></div>").appendTo("#roomList");

        var selector = $(".room[data-room='" + i + "']");
        selector.append("<div class='row'>");
        selector.append("<h3 class='col-md-12'>" + i + "</h3>");
        selector.append("</div>");
        selector.append("</div>");
    }
}
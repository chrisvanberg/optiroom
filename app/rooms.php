<script src="js/rooms.js"></script>
<?php
    $rooms = file_get_contents("http://dev.optiroom.net:5000/rooms");
    echo "<script>rooms = ".$rooms.";createList();</script>";
?>
<link rel="stylesheet" href="css/rooms.css">

<div id="roomList">

</div>
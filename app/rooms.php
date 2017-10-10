<script src="js/rooms.js"></script>
<?php
    $rooms = file_get_contents("http://dev.optiroom.net:5000/rooms");
    echo "<script>createList(".$rooms.")</script>"
?>
<link rel="stylesheet" href="css/rooms.css">
<div class="container-fluid">
    <div class="row">
        <div class="col-md-8" id="roomList">
            <div class="container-fluid">
                <div class="row" id="filters">
                    <select class="col-md-3">
                        <option value="" disabled selected>Batiment</option>
                    </select>
                    <select class="col-md-3">
                        <option value="" disabled selected>Etage</option>
                    </select>
                    <select class="col-md-3">
                        <option value="" disabled selected>Type</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</div>

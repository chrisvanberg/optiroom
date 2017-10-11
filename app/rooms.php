<script src="js/rooms.js"></script>
<?php
    $rooms = file_get_contents("http://dev.optiroom.net:5000/rooms/full");
    echo "<script>createList(".$rooms.")</script>"
?>

<link rel="stylesheet" href="css/rooms.css">
<div class="container-fluid">
    <div class="row" id="filters">
        <div class="col-md-4">
            <select>
                <option value="" disabled selected>Batiment</option>
            </select>
        </div>
        <div class="col-md-4">
            <select>
                <option value="" disabled selected>Etage</option>
            </select>
        </div>
        <div class="col-md-4">
            <select>
                <option value="" disabled selected>Type</option>
            </select>
        </div>
    </div>

    <div class="row">
        <div class="col-md-12">
            <div id="divTest">
                <div class="container-fluid" id="roomList">

                </div>
            </div>
        </div>
        <!--<div class="col-md-4" id="selectedRoom"></div>-->
    </div>
</div>

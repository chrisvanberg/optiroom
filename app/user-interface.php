<!DOCTYPE html>
<html lang="fr">
<head>
    <title>Optiroom</title>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="icon" type="image/png" href="img/favicon.png" />
    <link rel="stylesheet" href="css/UI.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.4/angular-route.js"></script>
    <script src="js/jQueryRotate.js"></script>
    <script src="js/page-loading.js"></script>
</head>
<body ng-app="optiroom" ng-controller="ctrl">
    <div class="container-fluid">
        <div id="mobile_menu" class="visible-xs visible-sm hidden-md hidden-lg">
            <img src="img/mobile_menu_icon.png" width="12%" onclick="showMenu()">
        </div>
        <div class="row">
            <div class="col-md-3 hidden-xs hidden-sm visible-md visible-lg" id="menu">
                <a href="#!"><img src="img/logo_grey.png" width="100%"></a>
                <nav>
                    <ul>
                        <li>
                            <a class="menu-item mainElement overview" href="#!">Acceuil</a>
                        </li>
                        <hr>
                        <li>
                            <a class="menu-item mainElement rooms" href="#!rooms" >Locaux</a>
                            <a class="menu-item subElement rooms book" href="#!book" >Réserver</a>
                            <a class="menu-item subElement rooms my-bookings" href="#!my-bookings" >Mes réservations</a>
                        </li>
                        <hr>
                        <li>
                            <a class="menu-item mainElement management" href="#!management">Gestion</a>
                        </li>
                        <hr>
                        <li>
                            <a class="menu-item mainElement logout" href="index.html">Se déconnecter</a>
                        </li>
                    </ul>
                </nav>
            </div>
            <div class="col-md-9" id="content">
                <div id="top-bar"><span></span></div>
                <div ng-view></div>
            </div>
        </div>
    </div>
</body>
</html>
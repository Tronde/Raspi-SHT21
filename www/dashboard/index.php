<!DOCTYPE html>
<html>
<head>
    <title>Raspi-SHT21 - Monitoring</title>

    <<meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Les Styles -->
    <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css" />
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/portal.css">

</head>
<body class="container">
<div class="row">
  <?php
  $WEBROOT = "/var/www/html";
  $files = scandir($WEBROOT);
  $json_files = array();

  foreach ($files as $file) {
    if (preg_match('/.*\.json/',$file)) { 
      array_push($json_files,$file);
    }
  }

  foreach ($json_files as $card) {
    print("<a href=\"http://<Enter-URL-here>\" class=\"col-xs-12 col-sm-3 col-md-2 col    -lg-2\">");
    print("<div class=\"card\">");
    print("<b>$card</b>");
    print("<p>");
    $path="$WEBROOT/$card";
    $json = file_get_contents($path);
    $data = json_decode($json,TRUE);
    print("T: ".$data['temp']." &deg;C H: ".$data['humidity']." %");
    print("</p>");
    print("</div>");
    print("</a>");
  }
  ?>
    <a href="http://<Enter-URL-here>" class="col-xs-12 col-sm-3 col-md-2 col-lg-2">
        <div class="card">
            <b>Raspi-SHT21</b>
            <p>
                <?php
                $lines = file("http://localhost/sht21-data.csv");
                $letzte_zeile = $lines[count($lines)-1];
                $res = explode ("\t", $letzte_zeile);
                print($res[0]. "<br />   Temperatur: ".$res[2]."&deg;C<br />   Luftfeuchtigkeit: ".$res[3]." %");
                ?>
            </p>
        </div>
    </a>
    <a href="http://<Enter-URL-here>" class="col-xs-12 col-sm-3 col-md-2 col-lg-2">
        <div class="card">
            <b>Sensor Name</b>
            <p>
                <?php
                $lines = file("http://localhost/esp8266_data.csv");
                $letzte_zeile = $lines[count($lines)-1];
                $res = explode (" ", $letzte_zeile);
                print($res[0]. "<br />   Temperatur: ".$res[2]."&deg;C<br />   Luftfeuchtigkeit: ".$res[3]." %");
                ?>
            </p>
        </div>
    </a>
</div>

<!-- Javascript Libraries -->
<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js"></script>
<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
<script src="js/portal.js"></script>
</body>
</html>

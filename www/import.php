<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="refresh" content="600" >
    <title>
	Import ESP8266
    </title>
 </head>

 <body>
 <?php
	$temp=$_GET["temp"];
	$humd=$_GET["humd"];
	$id=$_GET["id"];
	$logentry = date('Y-m-d'). "T" . date('H:i:s', time()) . " " . $id . " " .  $temp . " " . $humd . "\n";

	print("<h1>". "Datenimport von ESP8266" ."</h1>");
	print("<h2>". "Sensor-ID: ".$id."</h2>");
	print("<h3>". "Aktuelle  Temperatur: ".$temp."&deg;C<br />   Luftfeuchtigkeit: ".$humd."%</h3>");

	$data = fopen("esp8266_data.csv","a");
	fwrite($data, $logentry);
	fclose($data);
 ?>
 </body>
</html>

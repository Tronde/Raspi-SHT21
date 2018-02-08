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
  $name=$_POST["sysname"];
  $taskname=$_POST["taskname"];
	$id=$_POST["id"];
	$temp=$_POST["Temperature"];
	$humd=$_POST["Humidity"];
	$logentry = date('Y-m-d'). "T" . date('H:i:s', time()) . " " . $name . " " .  $temp . " " . $humd . "\n";

  echo("name: $name\n"); 
  echo("taskname: $taskname\n"); 
  echo("ID: $id\n"); 
  echo("temp: $temp\n"); 
  echo("humd: $humd\n"); 

	print("<h1>". "Datenimport von ESP8266" ."</h1>");
	print("<h2>". "Sensor-ID: ".$name."</h2>");
	print("<h3>". "Aktuelle  Temperatur: ".$temp."&deg;C<br />   Luftfeuchtigkeit: ".$humd."%</h3>");
  print("<h3>". "Taskname: ".$taskname." ID: ".$id."</h3>");

#	$data = fopen("esp8266_data.csv","a");
#	fwrite($data, $logentry);
#	fclose($data);
  $webroot="/var/www/html";
  $filename="$name.html";
  $filecontentstart="<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN' 'http://www.w3.org/TR/html4/loose.dtd'><html><head><title>$filename</title></head><body>";
  $filecontentdend='</body></html>';

  // Sichergehen, dass Datei existiert und beschreibbar ist
  if (is_writable($webroot)) {
    if (!$handle = fopen($filename, "w")) {
      print "Kann die Datei $filename nicht oeffnen";
      exit;
    }

    if (!fwrite($handle, $filecontentstart)) {
      print "Kann nicht in die Datei schreiben";
      exit;
    }
    fwrite($handle, $logentry);
    fwrite($handle, $filecontendend);
    print "Fertig, in die Datei $filename wurde $filecontentstart geschrieben";

    fclose($handle);
  } else {
      print "Die Datei $filename ist nicht schreibbar.";
  }
 ?>
 </body>
</html>

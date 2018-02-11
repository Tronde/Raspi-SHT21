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
  $textmuster='/^[^\.\/\\\\ ]+$/';
  if (preg_match($textmuster,$_POST["sysname"])) { 
    $name=$_POST["sysname"];
  } else {
    print("Der Systemname enthaelt ungueltige Zeichen.");
    exit;
  }

  if (preg_match($textmuster,$_POST["taskname"])) { 
    $taskname=$_POST["taskname"];
  } else {
    print("Der Taskname enthaelt ungueltige Zeichen.");
    exit;
  }

  if (is_numeric($_POST["id"])) {
	  $id=$_POST["id"];
  } else {
    print("Die ID enthaelt untueltige Zeichen.");
    exit;
  }

  if (is_numeric($_POST["Temperature"])) {
	  $temp=$_POST["Temperature"];
  } else {
    print("Die ID enthaelt untueltige Zeichen.");
    exit;
  }

  if (is_numeric($_POST["Humidity"])) {
	  $humd=$_POST["Humidity"];
  } else {
    print("Die ID enthaelt untueltige Zeichen.");
    exit;
  }

  $data = array('time' => date('Y-m-d'). "T" . date('H:i:s', time()), 'temp' => $temp, 'humidity' => $humd);

  echo("name: $name\n"); 
  echo("taskname: $taskname\n"); 
  echo("ID: $id\n"); 
  echo("temp: $temp\n"); 
  echo("humd: $humd\n"); 

  $webroot="/var/www/html";
  $filename="$name.json";

  // Sichergehen, dass Datei existiert und beschreibbar ist
  if (is_writable($webroot)) {
    if (!file_put_contents($filename, json_encode($data))) {
      print "In Datei $filename kann nicht geschrieben werden.";
    }
  } else {
      print "Die Datei $filename ist nicht schreibbar.";
  }

 ?>
 </body>
</html>

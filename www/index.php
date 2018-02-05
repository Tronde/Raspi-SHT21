<!DOCTYPE html>
<html>
<?php
$json = file_get_contents("sht21.json");
$data = json_decode($json,TRUE);
?>
<head>
<style>
h1   {color:grey}
p    {color:green}
body    {font-family:verdana}
</style>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta http-equiv="refresh" content="600">
<title>
  <?php
    print("T: ".$data['temp']." &deg;C H: ".$data['humidity']." %");
  ?>
</title>
</head>
<body>
  <?php

  //print_r($data);

  print("<h1>".$data['time']." &nbsp;&nbsp;&nbsp;");
  print("Temperature: ".$data['temp']." &deg;C &nbsp;&nbsp;&nbsp;");
  print("Humidity: ".$data['humidity']." %</h1>");


  ?>
	<img src="chart-day.png">
	<img src="chart-week.png">
</body>
</html>

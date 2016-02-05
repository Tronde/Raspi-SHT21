 <!DOCTYPE html>
<html>
<head>
<style>
h1   {color:grey}
p    {color:green}
body    {font-family:verdana}
</style>
</head>
<body>
<?php


$json = file_get_contents("data.json");
$data = json_decode($json,TRUE);

//print_r($data);

print("<h1>".$data['time']." &nbsp;&nbsp;&nbsp;");
print("Temperature: ".$data['temp']." &deg;C &nbsp;&nbsp;&nbsp;");
print("Humidity: ".$data['humidity']." %</h1>");


?>
	<img src="chart-day.png">
	<img src="chart-week.png">
</body>
</html>

<?php 
	
	/*function GetVarsAll( )
	{
		$var_temperature = "var temperature = [";
		$var_humidity = "var humidity = [";
		
		$fp = @fopen("sht21-data.csv", "r") or die ("Kann Datei nicht lesen.");
		while($line = fgets($fp, 1024))
		{
			$res = explode ("\t", $line);
			if(substr($var_temperature, -1, 1) == "]") $var_temperature = $var_temperature . ",";
			if(substr($var_humidity, -1, 1) == "]") $var_humidity = $var_humidity . ",";
			$var_temperature = $var_temperature . "[".$res[1] ."000,".$res[2] ."]";
			$var_humidity    = $var_humidity . "[".$res[1] ."000,".$res[3] ."]";
		}
		fclose($fp);
	
		$var_temperature = $var_temperature . "];";
		$var_humidity = $var_humidity . "];";
		return ($var_temperature . "\r\n". $var_humidity);
	}
	*/	
	
	function GetVarsDays($days)
	{
		$days = intval($days);
		if($days < 1 || $days > 10) $days = 2;
			
		$var_temperature = "var temperature = [";
		$var_humidity = "var humidity = [";
		$lines = file("sht21-data.csv");
		if(count($lines) > (144*$days)) $i = count($lines) - (144*$days);
			else				 $i = 1;
		while($i < count($lines))
		{
			$res = explode ("\t", $lines[$i]);
			if(substr($var_temperature, -1, 1) == "]") $var_temperature = $var_temperature . ",";
			if(substr($var_humidity, -1, 1) == "]") $var_humidity = $var_humidity . ",";
			$var_temperature = $var_temperature . "[".$res[1] ."000,".$res[2] ."]";
			$var_humidity    = $var_humidity . "[".$res[1] ."000,".$res[3] ."]";
			
			$i++;
		}
		$var_temperature = $var_temperature . "];";
		$var_humidity = $var_humidity . "];";
		return ($var_temperature . "\r\n". $var_humidity);
	}			
	
 ?>




<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Raspi-SHT21</title>
    <link href="layout.css" rel="stylesheet" type="text/css">
    <!--[if lte IE 8]><script language="javascript" type="text/javascript" src="../excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="js/jquery.js"></script>
    <script language="javascript" type="text/javascript" src="js/jquery.flot.js"></script>
 </head>
    <body>
	
	
	<?php 
		$lines = file("sht21-data.csv");
		$letzte_zeile = $lines[count($lines)-1]; 
		$res = explode ("\t", $letzte_zeile);
		print("<h2>". $res[0]. "   Temperatur: ".$res[2]."&deg;C   Luftfeuchtigkeit: ".$res[3]."%</h2>");
	?>
	
	
    <h3>Raspi-SHT21 (Temperature and Humidity with SHT21 Sensor) <a href="http://www.emsystech.de/">(www.emsystech.de)</a></h3>
	
    <div id="placeholder" style="width:900px;height:420px;"></div>

	</br>
	
	<form action="index.php" method="get">
	Tage: <input type="text" name="days" />
	<input type="submit" />
	</form> 
	
    <p>
	</p>
	
	
<script type="text/javascript">
$(function () {

	<?php 
	print(GetVarsDays(@$_GET["days"]));	 
	?>
	
	
    function euroFormatter(v, axis) {
        return v.toFixed(axis.tickDecimals) +"%";
    }
	
	function TempFormatter(v, axis) {
        return v.toFixed(axis.tickDecimals) +"&deg;C";
    }
    
    function doPlot(position) {
        $.plot($("#placeholder"),
           [ { data: temperature, label: "Temperature [&deg;C]" },
             { data: humidity, label: "Humidity", yaxis: 2 }],
           { 
               xaxes: [ { mode: 'time' } ],
               yaxes: [ { min: -20 , max: 40,
							tickFormatter: TempFormatter },
                        {
						  min: 0 , max: 100 ,
                          // align if we are to the right
                          alignTicksWithAxis: position == "right" ? 1 : null,
                          position: position,
                          tickFormatter: euroFormatter
                        } ],
               legend: { position: 'sw' }
           });
    }

    doPlot("right");
    
  /*  $("button").click(function () 
	{
        doPlot($(this).text());
    });*/
});
</script>
 </body>
</html>

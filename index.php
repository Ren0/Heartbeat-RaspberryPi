<html>
<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:15px 10px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:18px;font-weight:normal;padding:15px 10px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
</style>
<body>

<?php

$filename = "machinesList.txt";

if (isset($_GET["show"])) {
    $file = fopen($filename, "c+");
    $line = fgets($file, 4090);
    fclose($file);
    print("<center><table class='tg'>");
    print("<tr><th>Host</th><th>Alias</th><th>Location</th><th>Url</th><th>Date</th></tr>");
    $entries = explode("|", $line);
    foreach ($entries as $key => $value) {
        if (isset($value) && trim($value) !== '') {
            list($hostname, $machinename, $location, $url, $date) = explode(" ?", $value);
            print("<tr><td>$hostname</td><td>$machinename</td><td>$location</td><td>$url</td><td>$date</td></tr>");
        }
    }
    print("</table></center>");
} else {
    if (isset($_POST["hostname"]) && isset($_POST["machinename"]) && isset($_POST["url"]) && isset($_POST["location"]) && $_POST["hostname"] != '' && $_POST["machinename"] != '' && $_POST["url"] != '' && $_POST["location"] != '') {
        $hostname     = trim($_POST['hostname']);
        $machinename  = trim($_POST['machinename']);
        $location     = trim($_POST['location']);
        $url          = trim($_POST['url']);
        $date         = date("Y-m-d H:i:s");
        $tocleanLimit = strtotime("-7 day");
        print("<center> $machinename $location $hostname $url</center>");
        
        $file = fopen($filename, "c+");
        $line = fgets($file, 4090);
        ftruncate($file, 0);
        rewind($file);
        $entries = explode("|", $line);
        foreach ($entries as $key => $value) {
            if (isset($value) && trim($value) !== '') {
                list($oldmachine, $oldname, $oldlocation, $oldurl, $olddate) = explode(" ?", $value);
                
                $oldtime = strtotime($olddate);
                if (($oldmachine == $hostname && $oldname == $machinename) || ($oldtime < $tocleanLimit)) {
                    $line = str_replace("|$value", '', $line);
                }
            }
        }
        $line = $line . '|' . "$hostname ?$machinename ?$location ?$url ?$date";
        fputs($file, $line);
        
        fclose($file);
    } else {
		print("<a href='?show'>Show list</a></br>");
        print("<form method='post' >
			Host <input type='text' name='hostname' size='12'>
			Alias <input type='text' name='machinename' size='12'>
			Location <input type='text' name='location' size='12'>
			Connection string <input type='text' name='url' size='12'>
			<input type='submit' value='Add'>
			</form>");
    }
}

?> 
</body>
</html>
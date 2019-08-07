<?php
	include_once('1.php');
	$name = $_POST['name'];
	$age = $_POST['age'];
	if(mysql_query("INSERT INTO user VALUES('$name','$age')"))
		echo "success";
	else
		echo "fail";
?>
<?php
include 'connect.php';


pg_query($dbconn, "INSERT INTO testing (name) values ('Mokoang')");

?>
<?php

$pdo = new PDO(
    'mysql:host=academic-mysql.cc.gatech.edu;dbname=cs4400_Group_',
    'cs4400_Group_',
    ''
);

$sth = $pdo->query('SELECT * FROM User');
var_dump($sth->fetch());

?>
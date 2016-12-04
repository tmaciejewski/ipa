<html>
    <head>
        <title>InfoPasażer Archiver - archiwum opóźnień pociągów</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="style.css" type="text/css" />
    </head>
    <body>
        <h1>InfoPasazer Archiver</h1>

        <p><small><a href="http://old.ipa.lovethosetrains.com">old version</a></small></p>

<?php
require 'db.php';

$db = new Db();
$res = $db->get_trains();
while ($row = $res->fetch_assoc()) {
    echo '        <span><a href="' . $row['train_name'] . '">' . $row['train_name'] . "</a></span>\n";
}
?>

    </body>
</html>

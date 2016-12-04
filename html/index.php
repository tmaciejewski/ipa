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
while ($row = $res->fetch(PDO::FETCH_ASSOC)) {
    echo '        <span><a href="train/' . $row['train_name'] . '">' . join('&nbsp;', split(' ', $row['train_name'])) . "</a></span>\n";
}
?>

        <hr>
        <small><a href="https://github.com/tmaciejewski/ipa">Source on GitHub</a></small>
    </body>
</html>

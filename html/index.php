<html>
    <head>
        <title>InfoPasażer Archiver - archiwum opóźnień pociągów</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="/style.css" type="text/css" />
    </head>
    <body>
        <h1>InfoPasazer Archiver</h1>
        <h5>(<a href="http://old.ipa.lovethosetrains.com">old version</a>)</h5>
        <table id="main">
        <tr><th>Nazwa</th><th>Skąd</th><th>Dokąd</th></tr>
<?php
require 'db.php';

$starttime = microtime(true);

$db = new Db();
$res = $db->get_trains();
while ($train = $res->fetch(PDO::FETCH_ASSOC)) {
    $schedule_infos = $db->get_schedule_infos($train['last_schedule_id'])->fetchAll();
    echo '        <tr><td>';
    echo '<a href="train/' . $train['train_name'] . '">' . $train['train_name'] . '</a>';
    echo '</td><td>';
    echo $schedule_infos[0]['station_name'];
    echo '</td><td>';
    echo end($schedule_infos)['station_name'];
    echo "</td></tr>\n";
}
?>
        </table>
        <hr>
        <div id="footer">
            <p>
                <a href="https://github.com/tmaciejewski/ipa">source on GitHub</a>
            </p>
        </div>
    </body>
</html>
<!-- Generated in <?php echo round(microtime(true) - $starttime, 2); ?> seconds -->

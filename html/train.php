<?php
require 'api/db.php';

$starttime = microtime(true);
$date_freq = 10;
$name = htmlspecialchars($_GET["name"]);
$db = new Db();

$train = $db->get_train($name)->fetch(PDO::FETCH_ASSOC);
$train or die('No train');
?>
<html>
    <head>
        <title><?php echo $name ?> - archiwum opóźnień pociągów</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="/style.css" type="text/css" />
        <link href="https://fonts.googleapis.com/css?family=PT+Sans" rel="stylesheet"/>
    </head>
    <body>
        <h1><div><a href="/">&lt;&lt;</a></div> <?php echo $name ?></h1>
        <table>

<?php

function make_station_row($schedule_infos, $date, $date_freq, $stations_width)
{
    $i = 0;
    echo '<tr>';
    foreach ($schedule_infos as $info) {
        if ($i % $date_freq == 0) {
            echo '<th rowspan=2 class="date">' . $date . '</th>';
        }
        echo '<th>' . $info['station_name'] . '</th>';
        $i += 1;
    }

    while ($i <= $stations_width) {
        echo '<th rowspan=2 class="date"></th>';
        $i += 1;
    }
    echo "</tr>\n";
}

function get_delay_class($info)
{
   $delay = max($info['arrival_delay'], $info['departure_delay']);

   if ($delay >= 60)
       return 'critical';
   else if ($delay >= 20)
       return 'moderate';
   else if ($delay >= 5)
       return 'minor';
   else
       return 'normal';
}

function make_time_row($schedule_infos)
{
    echo '<tr>';
    foreach ($schedule_infos as $info) {
        echo '<td class="' . get_delay_class($info) . '">';

        if ($info['arrival_time'] != '') {
            $arrival_time = date_format(date_create($info['arrival_time']), 'H:i');
            echo '<p class="arr">&#8594; ' . $arrival_time . ' (' . $info['arrival_delay'] . ' min)</p>';
        } else {
            echo '<p class="arr">&#8212;</p>';
        }

        if ($info['departure_time'] != '') {
            $departure_time = date_format(date_create($info['departure_time']), 'H:i');
            echo '<p class="dep">' . $departure_time . ' (' . $info['departure_delay'] . ' min) &#8594;</p>';
        } else {
            echo '<p class="dep">&#8212;</p>';
        }

        echo '</td>';
    }
    echo "</tr>\n";
}

$stations_width = $db->get_max_stop_number($train['train_id'])->fetch(PDO::FETCH_ASSOC)['max'];

$schedules = $db->get_schedules($train['train_id']);
while ($schedule = $schedules->fetch(PDO::FETCH_ASSOC)) {
    $schedule_infos = $db->get_schedule_infos($schedule['schedule_id'])->fetchAll();
    make_station_row($schedule_infos, $schedule['schedule_date'], $date_freq, $stations_width);
    make_time_row($schedule_infos);
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

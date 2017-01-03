<?php

require 'db.php';

$db = new Db();

if (isset($_GET["name"])) {
    $name = htmlspecialchars($_GET["name"]);
    $train = $db->get_train($name)->fetch(PDO::FETCH_ASSOC);
    $train or die('No train ' . $name);

    $train['max_stations'] = $db->get_max_stop_number($train['train_id'])->fetch(PDO::FETCH_ASSOC)['max'];
    $train['schedules'] = $db->get_schedules($train['train_id'])->fetchAll(PDO::FETCH_ASSOC);
    foreach ($train['schedules'] as &$schedule) {
        $schedule['info'] = $db->get_schedule_infos($schedule['schedule_id'])->fetchAll(PDO::FETCH_ASSOC);
    }

    echo json_encode($train, JSON_PRETTY_PRINT);
} else {
    $trains = array();
    $res = $db->get_trains();

    while ($trainRow = $res->fetch(PDO::FETCH_ASSOC)) {
        $schedule_infos = $db->get_schedule_infos($trainRow['last_schedule_id'])->fetchAll();
        array_push($trains, array('train_id' => $trainRow['train_id'],
                                  'train_name' => $trainRow['train_name'],
                                  'from' => $schedule_infos[0]['station_name'],
                                  'to' => end($schedule_infos)['station_name']));
    }

    echo json_encode($trains, JSON_PRETTY_PRINT);
}
?>


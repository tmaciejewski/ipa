<?php

require 'db.php';

$trains = array();
$db = new Db();
$res = $db->get_trains();

while ($trainRow = $res->fetch(PDO::FETCH_ASSOC)) {
    $schedule_infos = $db->get_schedule_infos($trainRow['last_schedule_id'])->fetchAll();
    array_push($trains, array('id' => $trainRow['train_name'],
                              'from' => $schedule_infos[0]['station_name'],
                              'to' => end($schedule_infos)['station_name']));
}

echo json_encode($trains);
?>

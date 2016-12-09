<?php

class Db {
    private $host = '127.0.0.1';
    private $user = 'ipa';
    private $password = 'ipapass';
    private $database = 'ipa';

    private $pdo;

    public function __construct()
    {
        $this->pdo = new PDO('mysql:host=' . $this->host . ';dbname=' . $this->database . ';charset=utf8',
                             $this->user, $this->password);
    }

    public function get_trains()
    {
        return $this->pdo->query('SELECT * FROM train ORDER BY train_name');
    }

    public function get_train($train_name)
    {
        $stmt = $this->pdo->prepare('SELECT * FROM train WHERE train_name = :name');
        $stmt->execute(array('name' => $train_name));
        return $stmt;
    }

    public function get_max_stop_number($train_id)
    {
        $stmt = $this->pdo->prepare('SELECT MAX(stop_number) AS max FROM schedule WHERE train_id = :id');
        $stmt->execute(array('id' => $train_id));
        return $stmt;
    }

    public function get_schedules($train_id)
    {
        $stmt = $this->pdo->prepare('SELECT * FROM schedule WHERE train_id = :id ORDER BY schedule_date DESC, schedule_id DESC');
        $stmt->execute(array('id' => $train_id));
        return $stmt;
    }

    public function get_schedule_infos($schedule_id)
    {
        $stmt = $this->pdo->prepare('SELECT station_name, departure_time, departure_delay, arrival_time, arrival_delay
                                     FROM schedule_info INNER JOIN station USING (station_id) WHERE schedule_id = :id ORDER BY stop_number');
        $stmt->execute(array('id' => $schedule_id));
        return $stmt;
    }
}

?>

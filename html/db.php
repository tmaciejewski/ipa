<?php

class Db {
    private $host = '127.0.0.1';
    private $user = 'ipa';
    private $password = 'ipapass';
    private $database = 'ipa';

    private $mysqli;
   
    public function __construct()
    {
        $this->mysqli = new mysqli($this->host, $this->user, $this->password, $this->database);
        $this->mysqli->set_charset('utf8');
    }

    public function get_trains()
    {
        return $this->mysqli->query('SELECT * FROM train ORDER BY train_name');
    }
}

?>

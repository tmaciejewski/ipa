# IPA

IPA stands for InfoPasażer Archives. InfoPasażer is a site maintained by PKP (National Polish Railways)
that shows informations about all trains (even not owned by PKP), eg. their current position and delay. The site is great, but trains
disappear as soon as they reach their destinations; hence the idea of archiving it.

This project consists of three things:

- library for obtaining data from InfoPasażer: `station_api.py` `train_api.py` 
- script for updating the data and storing it in the database: `src` directory
- simple web frontend: `html` directory

## Requirements

Python 2.7 is used as main language with BeautifulSoup and MySQL connnector. Data is stored in MySQL Server 5.5.
Frontend is served by Apache 2.4 using PHP 5.6.

## Using as a CLI tool

Mainly for testing purpose, there are scripts for printing the contents directly from the site on console.

### Printing station details

Go to infopasazer.intercity.pl and find interestring station, then copy `stationid` value from URL and run:

    ./station_api.py stationid

### Printing train details

Go to infopasazer.intercity.pl and find interestring train, then copy `trainid` value from URL and run:

    ./train_api.py trainid

## Storing the data

### Creating database

Create new MySQL database and edit `ipa_config.py` with credentials. Then create database schema:

    ./ipa.py create_schema

### Updating train info

This will go to every stations defined in `ipa_config.py` and fetch data for every train available:

    ./ipa.py update_trains

Please, do not abuse InfoPasażer site by executing this too often! To keep the data up to date add
this line to crontab.

## Checking current data

After gathering some data, you can use this commands to examine them.

### Printing trains

This will list all train numbers (+ names):

    ./ipa.py print_trains

### Printing train history

This will print `2700/1 SIEMIRADZKI` train history:

    ./ipa.py print_train '2700/1 SIEMIRADZKI'

## Setting up web frontend

Edit `db.php` file to set database credential and then start apache service with document root pointing to `html` directory.

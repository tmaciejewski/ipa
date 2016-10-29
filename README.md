# IPA

IPA stands for InfoPasażer Archives. InfoPasażer is a site maintained by PKP (National Polish Railways)
that shows informations about all trains (even not owned by PKP), eg. their current position and delay. The site is great, but trains
disappear as soon as they reach their destinations; hence the idea of archiving it.

## Using as a CLI tool

Mainly for testing purpose, there are scripts for printing the contents directly from the site on console.

### Printing station details

1. Go to infopasazer.intercity.pl and find interestring station
2. Copy stationid from URL
3. Run:

    ./station.py stationid

### Printing train details

1. Go to infopasazer.intercity.pl and find interestring train
2. Copy trainid from URL
3. Run:

    ./train.py trainid

## Storing the data

The key function of this tool is to archive the data. First, you have to create database file. Then you have to periodically
(I use `cron` for that) execute script updating database.

### Creating database

This will recreate database file in a path defined in `ipa_config.py`:

    ./ipa.py create_db

### Updating train info

This will go to every stations defined in `ipa_config.py` and fetch data for every train available:

    ./ipa.py update_trains

Please, do not abuse InfoPasażer site by executing this too often!

## Checking current data

After gathering some data, you can use this commands to examine them.

### Printing trains

This will list all train numbers (+ names):

    ./ipa.py print_trains

### Printing train history

This will print `2700/1 SIEMIRADZKI` train history:

    ./ipa.py print_train '2700/1 SIEMIRADZKI'

## Generating HTML from the data

This will read the database and generate HTML pages for every train in `output_dir` directory:

    ./ipa_printer.py output_dir

You can use `style.css` stylesheet file to display it nicely.

## Known issues
There is a couple of known issues:
* dates of night trains (ie. riding at midnight) may be wrong by 1 day
* sometimes in generated HTML not every timestamp has its station name column 

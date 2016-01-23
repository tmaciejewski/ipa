## Getting single train schedule

1. Go to infopasazer.intercity.pl and find interestring train
2. Copy trainid from URL
3. Run:

    ./train.py trainid

## Getting station schedule

1. Go to infopasazer.intercity.pl and find interestring station
2. Copy stationid from URL
3. Run:

    ./station.py stationid

## Creating DB

This will recreate DB file in a path defined in `ipa_config.py`:

    ./ipa.py create_db

## Updating train info

This will go every stations defined in `ipa_config.py` and fetch all train info:

    ./ipa.py update_trains

## Printing trains

This will list all train number (+ names):

    ./ipa.py print_trains

## Printins single train history

This will print `2700/1 SIEMIRADZKI` train history:

    ./ipa.py print_train '2700/1 SIEMIRADZKI'

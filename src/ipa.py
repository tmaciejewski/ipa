#!/usr/bin/env python

import sys

import commands
import ipa_db
import ipa_config

if __name__ == "__main__":
    commands = {c.name: c for c in commands.all_commands}
    try:
        command = commands[sys.argv[1]]()
        assert(len(sys.argv[2:]) >= len(command.args))
    except:
        print 'Commands:'
        for c in commands:
            print '\t', commands[c].name, ' '.join(commands[c].args), '--', commands[c].desc
    else:
        database = ipa_db.Db(ipa_config.db['dev'])
        command.run(database, sys.argv[2:])

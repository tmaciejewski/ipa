import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/opt/ipa_dev/src")
sys.path.insert(0,"/opt/ipa_dev/api")

from api import app as application
application.secret_key = 'Add your secret key'

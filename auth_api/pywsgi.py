from gevent import monkey

monkey.patch_all()

import os
import sys

from app import start_app
from gevent.pywsgi import WSGIServer

sys.path.append(os.path.dirname(__file__))

app = start_app()

http_server = WSGIServer(("", 5000), app)
http_server.serve_forever()

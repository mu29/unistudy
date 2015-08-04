# -*- coding: utf-8 -*-

from server import *

if __name__ == '__main__':
    init_server()
    app.debug = True
    app.run(host='0.0.0.0')
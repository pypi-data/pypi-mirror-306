#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2024/10/25 14:46
Author  : ren
"""

import sanic
from sanic_ext import Extend
from sanic_nacos import NacosExt

app = sanic.Sanic("sanic-nacos")
app.config.update({"NACOS_CONFIG_DATA_ID": "test.json"})
Extend.register(NacosExt)

if __name__ == '__main__':
    import logging
    logging.getLogger("sanic.root").setLevel(logging.DEBUG)

    app.run(port=9001)

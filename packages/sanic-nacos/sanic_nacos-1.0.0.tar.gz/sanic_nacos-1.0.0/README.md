SANIC-NACOS

[sanic](https://sanic.dev/) extension for [nacos](https://nacos.io/) service register.

# Config

| config               | default        | description                                                        |
|----------------------|----------------|--------------------------------------------------------------------|
| NACOS_SERVER_ADDR    | 127.0.0.1:8848 | nacos server addr                                                  |
| NACOS_ENABLE         | TRUE           | enable                                                             |
| NACOS_AK             | None           | access key                                                         |
| NACOS_SK             | None           | secret key                                                         |
| NACOS_USERNAME       | None           | username                                                           |
| NACOS_PASSWORD       | None           | password                                                           |
| NACOS_NAMESPACE      | public         | namespace                                                          |
| NACOS_GROUP          | DEFAULT        | group                                                              |
| NACOS_CLUSTER_NAME   | DEFAULT        | cluster name                                                       |
| NACOS_PREFER_SUBNET  | 192.0.0.0/8    | if  `NACOS_SERVER_IP` not present,node ip in this sub will be used |
| NACOS_SERVICE_NAME   | None           | service name                                                       |
| NACOS_SERVER_IP      | None           | server ip                                                          |
| NACOS_SERVER_PORT    | None           | server port or else the port that app listening                    |
| NACOS_HB_INTERVAL    | 30             | nacos heartbeat interval                                           |
| NACOS_CONFIG_DATA_ID | None           | nacos config data id                                               |
| NACOS_CONFIG_GROUP   | DEFAULT_GROUP  | nacos config group                                                 |

exapmle:

```python
import sanic
from sanic_ext import Extend
from sanic_nacos import NacosExt

app = sanic.Sanic("sanic-nacos")
app.config.update({"NACOS_CONFIG_DATA_ID": "test.json"})
Extend.register(NacosExt)

if __name__ == '__main__':
    app.run(port=9001)

```
# python3-rpm
## 安装
```bash
pip3 install python3-rpm
```

## 设置变量
修改 [env.sh](env.sh) 中变量的值，然后执行如下命令使变量生效
```bash
source env.sh
```



## 用法
### rpm_ai 命令用法
* 获取指定软件包的所有服务
```bash
rpm_ai rpm get_service httpd
```

* 获取指定软件包的命令参数列表
```bash
rpm_ai rpm get_cmd_and_param acl
```

### rpm 库用法
* 获取软件包提供的服务列表
```python
from rpm.rpm import RpmService

rpm=RpmService()
service_list=rpm.get_service("httpd")
print(service_list)
```
其中 service_list 的内容为：
```json
[
    "htcacheclean.service",
    "httpd.service"
]
```
* 获取命令参数列表
```
cmd_param_list=rpm.get_cmd_and_param("acl")
print(cmd_param_list)
```
其中 cmd_param_list 格式如下：
```json
[
    {"cmd": "getfacl", "param": "-a"},
    {"cmd": "getfacl", "param": "-d"},
    {"cmd": "getfacl", "param": "-c"},
    {"cmd": "getfacl", "param": "-e"},
    {"cmd": "getfacl", "param": "-E"},
    {"cmd": "getfacl", "param": "-s"},
    {"cmd": "getfacl", "param": "-R"},
    {"cmd": "getfacl", "param": "-L"},
    {"cmd": "getfacl", "param": "-P"},
    {"cmd": "getfacl", "param": "-t"},
    {"cmd": "getfacl", "param": "-n"},
    {"cmd": "getfacl", "param": "-p"},
    {"cmd": "getfacl", "param": "-v"},
    {"cmd": "getfacl", "param": "-h"},
    {"cmd": "getfacl", "param": "--access"},
    {"cmd": "getfacl", "param": "--default"},
    {"cmd": "getfacl", "param": "--omit-header"},
    {"cmd": "getfacl", "param": "--all-effective"},
    {"cmd": "getfacl", "param": "--no-effective"},
    {"cmd": "getfacl", "param": "--skip-base"},
    {"cmd": "getfacl", "param": "--recursive"},
    {"cmd": "getfacl", "param": "--logical"},
    {"cmd": "getfacl", "param": "--physical"},
    {"cmd": "getfacl", "param": "--tabular"},
    {"cmd": "getfacl", "param": "--numeric"},
    {"cmd": "getfacl", "param": "--absolute-names"},
    {"cmd": "getfacl", "param": "--version"},
    {"cmd": "getfacl", "param": "--help"},
    {"cmd": "setfacl", "param": "-m"},
    {"cmd": "setfacl", "param": "-M"},
    {"cmd": "setfacl", "param": "-x"},
    {"cmd": "setfacl", "param": "-X"},
    {"cmd": "setfacl", "param": "-b"},
    {"cmd": "setfacl", "param": "-k"},
    {"cmd": "setfacl", "param": "-n"},
    {"cmd": "setfacl", "param": "-d"},
    {"cmd": "setfacl", "param": "-R"},
    {"cmd": "setfacl", "param": "-L"},
    {"cmd": "setfacl", "param": "-P"},
    {"cmd": "setfacl", "param": "-v"},
    {"cmd": "setfacl", "param": "-h"},
    {"cmd": "setfacl", "param": "--modify=acl"},
    {"cmd": "setfacl", "param": "--modify-file=file"},
    {"cmd": "setfacl", "param": "--remove=acl"},
    {"cmd": "setfacl", "param": "--remove-file=file"},
    {"cmd": "setfacl", "param": "--remove-all"},
    {"cmd": "setfacl", "param": "--remove-default"},
    {"cmd": "setfacl", "param": "--no-mask"},
    {"cmd": "setfacl", "param": "--default"},
    {"cmd": "setfacl", "param": "--recursive"},
    {"cmd": "setfacl", "param": "--logical"},
    {"cmd": "setfacl", "param": "--physical"},
    {"cmd": "setfacl", "param": "--version"},
    {"cmd": "setfacl", "param": "--help"}
]
```
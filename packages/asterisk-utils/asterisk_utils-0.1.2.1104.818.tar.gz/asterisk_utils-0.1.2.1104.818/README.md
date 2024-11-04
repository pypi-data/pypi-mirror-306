# Asterisk-Utils

## 介绍

对于常用的一些功能，做了一些封装，例如print与log整合封装，对于python内置的email以及smtplib的封装等，如发现任何缺陷或者新想法，请在[这里](https://gitee.com/zhangxin_1/asterisk-utils/issues)报告缺陷，或者[email](mailto:geoshan@163.com)交流。

## 软件架构

文件架构说明

```markdown
/
|-- asteriskutils/
|   |-- setup.py
|   |   |-- AppConfig
|   |
|   |-- tools.py
|   |   |-- succes_print
|   |   |-- error_print
|   |   |-- iprint
|   |   |-- dprint
|   |   |-- wprint
|   |
|   |-- mail.py
|   |   |-- AsteriskMailMsg
|   |   |-- AsteriskMail
```

## 安装教程

1. 建议 pip install astersik-utils
2. 或者到[gitee](https://gitee.com/zhangxin_1/asterisk-utils)下载源码，运行`python -m build`命令，直接安装dist目录下的whl文件

## 使用说明

1. 本软件是个中间件，并不能直接解决任何应用问题
2. 在开发软件程序时，可以另外做相关软件设置，覆盖本软件的内置设定。具体请参见[文档](https://e.gitee.com/zhangxin_1/repos/zhangxin_1/asterisk-utils/blob/master/docs/documentation.md)
3. 在使用print系列函数前需要先设置log目录到项目目录。

```python
from asteriskutils.setting import AppConfig

AppConfig['log']['log_file_name'] = 'Your/App/log/Path'
```

## 参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request

## 特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5. Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

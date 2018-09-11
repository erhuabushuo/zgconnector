# wlconnector

[![Build Status](https://www.travis-ci.org/erhuabushuo/wlconnector.svg?branch=master)](https://www.travis-ci.org/erhuabushuo/wlconnector)

旺龙设备通信服务器，采用异步协程自定义协议的高性能TCP通信服务器

## 依赖

**Python 3.7**

## 安装

    python3.7 -m venv venv
    source venv/bin/active
    python setup install
    wlconnector

## 配置

查看配置文件 **/etc/wlconnector.ini**

## 包格式

    +---------+---------+----------+----------+---------+---------+----------------+
    | Ver     | Token   | From     | To       | Cmd     | Length  | Body           |
    +---------+---------+----------+----------+---------+---------+----------------+
    | 2 bytes | 6 bytes | 20 bytes | 20 bytes | 2 bytes | 4 bytes | N length bytes |
    +---------+---------+----------+----------+---------+---------+----------------+

* Ver：版本号，2个字节
* Token: 消息认证，6个字节
* From: 发送方ID， 40个字节
* To: 接收方ID, 40个字节
* Cmd: 指令（下面有详情），2个字节
* Length: 消息主体长度，4个字节
* Body: 主体内容，由Length长度决定

## 指令

1-9为保留指令：

* HEARTBEAT = 1
* REPLY = 2
* ERROR = 3
* ...

自定义指令从10开始

## 心跳表

{id}_heartbeat为key写入到redis，包含内容为json格式。

* uid：终端ID
* ver：版本号
* client_address：终端连接IP和Port
* server_address：服务器连接IP和Port


## 单元测试

    python setup.py test

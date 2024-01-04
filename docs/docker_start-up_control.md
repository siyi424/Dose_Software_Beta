# docker compose start-up order

ref: https://blog.csdn.net/weixin_60748184/article/details/130999845

## 一、基础
1. docker容器本质是多个容器卷的叠加，启动后的容器卷处于容器卷最顶层，不做特殊配置和处理的话，**不同的容器之间是相互隔离的**，包括**文件存储**和**网络**的隔离
2. 其中，文件存储可以通过挂载volumes来实现文件同步。
3. 网络部分：
每个容器创建时，会默认创建一对**虚拟网卡**，用于连接容器和宿主机，也就是veth-pair (Virtual Ethernet, 虚拟以太网卡).

查看docker容器的ip
```
docker run -it ubuntu:16.04
apt-get update && apt-get install -y iproute2

ip addr
```

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
639: eth0@if640: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.2/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

如上，容器内部有一个639的网卡，而
eth0@if640是指连接宿主机的640虚拟网卡。

**需要注意的是，wsl2使用docker desktop进行docker的使用。它的docker0网卡被隐藏在了docker虚拟机中。**
```
There is no docker0 bridge on the host
Because of the way networking is implemented in Docker Desktop, you cannot see a docker0 interface on the host. This interface is actually within the virtual machine.
```

4. From the Networking in Compose (ref: https://docs.docker.com/compose/networking/): 
compose会默认把同一个compose.yaml文件内的services放置在同一个bridge网络下，各个子服务之间是可以互相网络通信的。

eg. docker项目文件夹的名称是：myapp
```
1. A network called myapp_default is created.
2. A container is created using web's configuration. It joins the network myapp_default under the name web.
3. A container is created using db's configuration. It joins the network myapp_default under the name db.

Each container can now look up the hostname web or db and get back the appropriate container's IP address. For example, web's application code could connect to the URL postgres://db:5432 and start using the Postgres database.
```

## 二、wait-for-it
wait-for-it.sh脚本目的：
检测服务端口（例如nacos的8848端口）是否启动成功，成功后才能启动下一个服务。

**但是，查看docker compose的文档发现，已有非常完善的方式来支持各容器的启动顺序。...,  where dependencies are determined by depends_on, links, volumes_from, and network_mode: "service:...".**

所以，wait-for-it在本项目中，不再进行使用。

## 三、depends_on
The solution for **detecting the ready state** of a service is to use the **condition attribute** with one of the following options:

- **service_started**
- **service_healthy**. This specifies that a dependency is expected to be “healthy”, which is defined with healthcheck, before starting a dependent service.
- **service_completed_successfully**. This specifies that a dependency is expected to run to successful completion before starting a dependent service.

depends_on有两层含义：
1. 在db启动以后，再启动；
2. 先结束，之后db再结束。

eg. 
```
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres
```





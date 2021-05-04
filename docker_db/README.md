$ docker pull mysql

$ docker run -it --name sandbox-db -e MYSQL_ROOT_PASSWORD=sandbox-pw -d mysql:latest

$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                 NAMES
60a1fd16bdfa   mysql:latest   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   3306/tcp, 33060/tcp   sandbox-db

$ docker exec -it sandbox-db bash -p

$ mysql -u root -p -h 127.0.0.1

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.01 sec)
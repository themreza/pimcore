#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import docker
import requests

client = docker.from_env()

time.sleep(10)
for c in client.containers.list():
    assert c.status == 'running'
    print(c.name)
    print(c.status)

# PHP
php = client.containers.get('pimcore')
assert php.status == 'running'
php_conf = php.exec_run("php-fpm -t")
print(php_conf.output.decode())
assert 'configuration file /usr/local/etc/php-fpm.conf test is successful' in php_conf.output.decode()
# php_proc = php.exec_run("sh -c 'ps aux|grep php-fpm'")
# print(php_proc.output.decode())
# assert 'php-fpm: master process (/etc/php/7.3/fpm/php-fpm.conf)' in php_proc.output.decode()
# assert 'php-fpm: pool www' in php_proc.output.decode()

mysql = client.containers.get('pimcoredb')
assert mysql.status == 'running'
mycnf = mysql.exec_run("/usr/sbin/mysqld --verbose --help")
# print(mycnf.output.decode())
assert 'mysqld  Ver 5.7' in mycnf.output.decode()
mysql_log = mysql.logs()
assert "mysqld: ready for connections" in mysql_log.decode()
print(mysql_log.decode())

# response = requests.get("http://localhost")
# print(response)
# assert response.status_code == 200

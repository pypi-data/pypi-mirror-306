import consul
import pymysql
import sys
from sshtunnel import SSHTunnelForwarder

c = consul.Consul(host="10.68.69.136", token="30126abf-691c-4d1a-b7da-e4c4b578dd4a")
user = c.kv.get("flex/shared/flex-enterprise/mysql/username")[1]['Value'].decode('utf-8')
password = c.kv.get("flex/shared/flex-enterprise/mysql/password")[1]['Value'].decode('utf-8')
host = c.kv.get("flex/shared/mysql/host")[1]['Value'].decode('utf-8')
dbname = c.kv.get("flex/shared/flex-enterprise/mysql/database")[1]['Value'].decode('utf-8')
port = int(c.kv.get("flex/shared/mysql/port")[1]['Value'].decode('utf-8'))

print(user, password, host, dbname, port)

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=dbname,
        port=port
    )
except Exception as ex:
    print(f"NOPE! {ex}")
    sys.exit(1)

print(connection.ping())
print(connection)

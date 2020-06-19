#导入SQLite驱动：
import sqlite3
#连接到SQlite数据库
#数据库文件是test.db，不存在，则自动创建
conn = sqlite3.connect('test.db')
#创建一个cursor：
cursor = conn.cursor()
#执行一条SQL语句：创建user表
cursor.execute('create table user(id varchar(20) primary key,name varchar(20))')
#插入一条记录：
cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
#通过rowcount获得插入的行数：
print(cursor.rowcount) #reusult 1
#关闭Cursor:
cursor.close()
#提交事务：
conn.commit()
#关闭connection：
conn.close()
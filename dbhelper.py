import logging
import traceback
import pymysql
from config import *

db = pymysql.connect(DOMAIN, USER, PASSWORD, DB, charset='utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


getall_sql = 'select * from kaoyan'
try:
    cursor.execute(getall_sql)
    results = cursor.fetchall()
    exists = [(result[1], result[2], result[3]) for result in results]
except Exception as ec:
    db.rollback()
    print(e.args)


def create_table():
    create_sql = '''CREATE TABLE IF NOT EXISTS `kaoyan`(
   `info_id` INT UNSIGNED AUTO_INCREMENT,
   `title` VARCHAR(255) NOT NULL,
   `tdate` VARCHAR(40) NOT NULL,
   `href` VARCHAR (255) NOT NULL,
   PRIMARY KEY ( `info_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
    try:
        cursor.execute(create_sql)
        db.commit()
    except:
        db.rollback()


def insert_db(to_insert):
    for item in to_insert:
        insert_sql = '''insert into kaoyan (title, tdate, href) VALUES (%s,%s,%s)'''
        try:
            cursor.execute(insert_sql, item)
            db.commit()
        except Exception as e:
            db.rollback()
            print(e.args)


if __name__ == '__main__':
    create_table()

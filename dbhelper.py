import logging
import traceback
import pymysql
from config import db_pass

db = pymysql.connect(db_pass.domain, db_pass.user, db_pass.password, db_pass.db, charset='utf8')
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

sql_str = '''select from '''


def create_table():
    create_sql = "CREATE TABLE IF NOT EXISTS `kaoyan`(
   `runoob_id` INT UNSIGNED AUTO_INCREMENT,
   `runoob_title` VARCHAR(100) NOT NULL,
   `runoob_author` VARCHAR(40) NOT NULL,
   `submission_date` DATE,
   PRIMARY KEY ( `runoob_id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;"

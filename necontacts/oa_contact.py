#! -*- coding:utf-8 -*-

import json
import itertools
import db
import config

def mysql_execute(query):
    with db.MySQLConn(config.MYSQL_DB, config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWD) as conn:
        return conn.execute(query)


def department_sql(contact_json):
    department = dict()
    for contact_info in itertools.chain(*contact_json.values()):
        email = contact_info['email']
        dept3Id = contact_info['dept3Id']
        dept3Name = contact_info['dept3Name']
        lastName = contact_info['lastName']
        sex = contact_info['sex']
        loginId = contact_info['loginId']
        department[dept3Id] = dept3Name
    
    for key, val in department.items():
        department_sql = '''INSERT INTO department VALUES(NULL, '%s', '%s', 3);''' % (val, key)
        print mysql_execute(department_sql)

def create_user_table():
    pass


if __name__ == '__main__':
    json_file = './people.json'
    with open(json_file, 'rb') as myfile:
        contact_json = json.loads(myfile.read())

    department_sql(contact_json)

#! -*-coding:utf-8 -*-

import db
import logging
import MySQLdb

class MySQLConn(object):

    def __init__(self, database, host = 'localhost', user = None, password = None):
        self.args = {'charset':'utf8', 'db':database, 'user':user, 'passwd':password}
        
        respair = host.split(':')
        if len(respair) == 2:
            self.args['host'] = respair
            self.args['port'] = int(respair[1])
        else:
            self.args['host'] = host
            self.args['port'] = 3306
        
        self.db = None
        try:
            self.connect()
        except Exception, e:
            logging.error('Can not connect to database %s on %s' % (self.args['db'], self.args['port']))
            logging.error('----Error: ' + str(e))
            self.close()
            
    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None

    def connect(self):
        self.close()    
        self.db = MySQLdb.connect(**self.args)
#       self.db.autocommit(True)

    def _get_cursor(self):
        if self.db is None:
            self.connect()
        return self.db.cursor()
    
    def execute(self, query, *args):
        cursor = self._get_cursor()
        try:
            cursor.execute(query, args)
            command = query.lower().strip()
            if command.startswith('select'):
                colkey = [row[0] for row in cursor.description]
                return [dict(zip(colkey, colval)) for colval in cursor]
            if command.startswith('insert'):
                return self.db.insert_id()
            return None
        except Exception, e:
            logging.error('Can not execute: ' + (query % args))
            logging.error('----Error: ' + str(e))
#       except:
#           logging.error('Can not execute: ' + (query % args))
#           logging.error('----Can not connect to database %s on %s' % (self.args['db'], self.args['port']))
        finally:
            if cursor is not None:
                cursor.close()
            #self.close()
        

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if self.db is None:
            return
        if isinstance(exception_value, Exception):
            self.db.rollback()
        else:
            self.db.commit()
        self.close()

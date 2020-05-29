import sys, os
import pandas as pd
import numpy as np
from scipy import signal
import math
from datetime import datetime
import requests
import time
import mysql.connector
from mysql.connector import errorcode
import hashlib

class CrawlerUtils: 
    def __init__(self, db_settings):
        self.db_settings = db_settings
        self.db_connection = None
        self.log_dir = './log'
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = os.path.join(self.log_dir, f'log_{now}.txt')
        self.print_to_console = True

        if self.connect_db():
            self.prepare_db()
        else:
            self.log('Could not connect database')
            raise Exception('Could not connect database')        
    
    def __del__(self):
        if self.db_connection is not None and self.db_connection.is_connected():
            self.db_connection.close()

    def is_db_connected(self):
        return self.db_connection is not None and self.db_connection.is_connected()
        
    def connect_db(self):
        try:
            self.db_connection = mysql.connector.connect(**self.db_settings)
            return self.db_connection.is_connected()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.log("Something is wrong with your username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.log("Database does not exist.")
            else:
                self.log(err) 
            return False    
        
    def get_article_hash(self, article):
        article_url, article_title = article['article_url'], article['article_title']
        string_to_hash = f'{article_url} :: {article_title}' 
        hash_object = hashlib.sha1(str.encode(string_to_hash))
        return str(hash_object.hexdigest())

    def has_article_with_hash(self, _hash):
        exists = False
        if not self.is_db_connected():
            self.connect_db()         
        cursor = self.db_connection.cursor()
        query = ("SELECT article_id FROM articles WHERE article_hash = %(hash)s")
        cursor.execute(query, {'hash': _hash})
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def save_article_to_db(self, article, _hash, source_info):
        # self.print_article_info(article, source_info)
        article_id = -1

        if article is None: return -1     
        if source_info is None: return -1  

        if not self.is_db_connected():
            self.connect_db()         
        cursor = self.db_connection.cursor()

        add_article = ("INSERT INTO articles "
                       "(article_hash, source_id, source_name, article_url, article_title, article_body, date_published, timestamp) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

        if _hash is None: _hash = self.get_article_hash(article)
        article_data = (_hash, source_info['source_id'], source_info['source_name'], 
                        article['article_url'], article['article_title'], article['article_body'], 
                        article['date_published'], article['timestamp'])

        try:
            cursor.execute(add_article, article_data)
            article_id = cursor.lastrowid
        except mysql.connector.Error as err:
            self.log(f'Save article to db :: {err}')

        cursor.close()        
        return article_id

    def get_articles_count(self):    
        count = 0  
        if not self.is_db_connected():
            self.connect_db()         
        cursor = self.db_connection.cursor()
        query = 'SELECT count(*) AS count FROM articles'
        try:
            cursor.execute(query)
            row = dict(zip(cursor.column_names, cursor.fetchone()))            
            count = row['count']
        except mysql.connector.Error as err:
            self.log(f'Get article count :: {err}')
        return count
    
    def print_article_info(self, article, source):
        print('Source id     : ', source['source_id'])
        print('Source name   : ', source['source_name'])
        print('Article url   : ', article['article_url'])
        print('Article title : ', article['article_title'])
        print('Article body  : ', article['article_body'])
        print('Date published: ', article['date_published'])
        print('Timestamp     : ', article['timestamp'])

    def log(self, log_data):
        if self.log_file is not None:
            f = open(self.log_file ,'a')
            now = datetime.now()
            f.write(f'{now} :: {log_data}')
            f.close()
        if self.print_to_console:
            print(log_data)

    def prepare_db(self):
        if self.db_connection is None:
            self.connect_db()         
        cursor = self.db_connection.cursor()

        TABLES = {}
        TABLES['articles'] = (
            "CREATE TABLE `articles` ("
            "  `article_id`     int(11) NOT NULL AUTO_INCREMENT,"
            "  `article_hash`   varchar(128) NOT NULL UNIQUE,"
            "  `source_id`      int(11) NOT NULL,"
            "  `source_name`    varchar(50) NOT NULL,"           
            "  `article_url`    varchar(1000) NOT NULL,"
            "  `article_title`  varchar(1000) NOT NULL,"
            "  `article_body`   text NOT NULL,"
            "  `date_published` varchar(50) NULL,"
            "  `timestamp`      datetime NOT NULL,"
            "  PRIMARY KEY (`article_id`)"
            ") ENGINE=InnoDB")

        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                self.log(f'Creating table {table_name}..')
                cursor.execute(table_description)
                self.log(f'Table {table_name} created.')
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    self.log(f'Table {table_name} already exists.')
                else:
                    self.log(err.msg)     
        cursor.close()

    def start_over(self):
        success = False
        if self.db_connection is None:
            self.connect_db()         
        cursor = self.db_connection.cursor()
        query = 'DROP table articles'
        try:
            cursor.execute(query)            
            success = True
            self.log(f'Table articles dropped')
        except mysql.connector.Error as err:
            self.log(f'Get article count :: {err}')
        return success
        

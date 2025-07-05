import mysql.connector
import os

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'ALX_prodev',
  'raise_on_warnings': True
}

#connects mysql server db
def connect_db(config):
    return mysql.connector.connect(**config)

#create database
def create_database(db_name):
    session = connect_db(config)
    session.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    session.commit()

def connect_to_prodev():
    return connect_db(config)

#seeds db with data
def seed_db(db_name):
    session = connect_db(config)
    session.execute(f"USE {db_name}")
    session.commit()

def drop_table(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    connection.commit()

def create_table(connection, table_name, columns):
    cursor = connection.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
    connection.commit()

def insert_data(connection, table_name, data):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {table_name} (name, email, age) VALUES ({data})")
    connection.commit()
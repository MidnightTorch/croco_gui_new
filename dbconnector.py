import pymysql.cursors
from dbconfig import *


def connect_to_db(func):
    def wrapper(*args, **kwargs):
        with pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cursor:
                sql = func(*args, **kwargs)
                cursor.execute(sql, args)
                conn.commit()
                return cursor.fetchall()

    return wrapper


def connect_to_db_with_no_args(func):
    def wrapper(*args, **kwargs):
        with pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cursor:
                sql = func(*args, **kwargs)
                cursor.execute(sql)
                conn.commit()
                return cursor.fetchall()

    return wrapper


@connect_to_db
def push_to_db(json_obj, path_to_file):
    sql = 'INSERT INTO `data` (`description`, `path_to_picture`) VALUES (%s, %s)'
    return sql


@connect_to_db
def check_exists(path_to_picture):
    sql = 'SELECT * FROM `data` WHERE `path_to_picture` LIKE (%s)'
    return sql


@connect_to_db
def delete_rows_by_path_to_file(path_to_file):
    sql = 'DELETE FROM `data` WHERE `path_to_picture` LIKE (%s)'
    return sql


@connect_to_db
def get_description_by_path(path_to_file):
    sql = 'SELECT description FROM data WHERE path_to_picture LIKE (%s)'
    return sql

@connect_to_db_with_no_args
def get_json_col_for_completer(attr):
    sql = f'SELECT JSON_EXTRACT(description, "$.{attr}") FROM data'
    return sql

# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json

import psycopg2
from psycopg2 import connect, Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys


try:
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="",
                                  host="127.0.0.1",
                                  port="5432")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    create_table='''CREATE TABLE matches_info (
        CPM             integer,
        KDA             integer,
        assists         integer,
        avatar          varchar(400),
        deaths          integer,
        duration        varchar(40),
        gold_per_min    integer,
        hero            varchar(40),
        hero_damage     integer,
        hero_healing    integer,
        kills           integer,
        last_hits       integer,
        match_result    varchar(40),
        nickname        varchar(40),
        profileurl      varchar(200),
        side            varchar(40),
        start_time      varchar(200),
        total_value     integer,
        tower_damage    integer,
        xp_per_min      integer
    );'''
    # cursor.execute(create_table)
    table_name = "matches_info"
    cursor.execute(f"SELECT * FROM {table_name}")
    record = cursor.fetchall()
    for i in record:
        print(i)
    with open('result.json') as json_data:
        record_list = json.load(json_data)

    sql_string = 'INSERT INTO {} '.format(table_name)

    if type(record_list) == list:
        first_record = record_list[0]

        columns = list(first_record.keys())
    else:
        sys.exit()

    sql_string += "(" + ', '.join(columns) + ")\nVALUES "
    for i, record_dict in enumerate(record_list):
        values = []
        for col_names, val in record_dict.items():
            if type(val) == str:
                val = val.replace("'", "''")
                val = "'" + val + "'"
            values += [str(val)]
        sql_string += "(" + ', '.join(values) + "),\n"

    sql_string = sql_string[:-2] + ";"

    # cursor.execute(sql_string)
except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")

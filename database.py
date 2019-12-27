#!/usr/bin/env python3
# https://stackabuse.com/working-with-postgresql-in-python/

# import database
# database.create_table("sdfd")

import json
import psycopg2


parsed = []

user = "pythonuser"
password = "pythonuser"
host = "127.0.0.1"
port = "5432"
database = "duparcer"


def openbase(file, text):
    dict_var = []
    try:
        with open(file, "r", encoding="utf-8") as old_file:  # encoding='utf-8'
            dict_var = json.load(old_file)
        print("{} results are available: {} cars".format(text, len(dict_var)))
        return dict_var
    except FileNotFoundError:
        print("No " + text + " results")
        return dict_var


def create_table(tablename):
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE ''' + tablename + '''
                (ID INT PRIMARY KEY     NOT NULL,
                POSTED VARCHAR(10)    NOT NULL,
                MODEL VARCHAR(25),
                PRICE INT,
                OLDPRICE VARCHAR(6),
                YEAR INT,
                MILEAGE INT,
                LINK VARCHAR(200),
                TITLE TEXT,
                TITLETEST TEXT);'''

        cursor.execute(create_table_query)

        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def truncate_table(tablename):
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)

        cursor = connection.cursor()

        truncate_table_query = 'TRUNCATE TABLE ' + tablename

        cursor.execute(truncate_table_query)

        connection.commit()
        print("Table successfully clearedin PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while clearing PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def write_to_database(dictname, tablename):
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)

        cursor = connection.cursor()

        m = 1
        for i in dictname:
            command = "INSERT INTO " + tablename + " (ID,POSTED,MODEL,PRICE,OLDPRICE,YEAR,MILEAGE,LINK,TITLE,TITLETEST) VALUES ("
            to_insert = command + str(m) + ", '" + i['ad_posted'] + "', '" + i['brand'] + "-" + i['model'] + "', " + i['price'] + ", '" + str(i['oldprice']) + "', " + i['year'] + ", " + i['mileage'] + ", '" + i['href'] + "', '" + i['title'] + "', '" + i['title_test'] + "');"
            #print(to_insert)
            cursor.execute(to_insert)
            m += 1

        connection.commit()
        print("Data added ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while addind data PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def read_from_database(tablename, dictname):
    try:
        connection = psycopg2.connect(user = user,
                                      password = password,
                                      host = host,
                                      port = port,
                                      database = database)

        cursor = connection.cursor()

        cursor.execute("SELECT * from " + tablename)
        rows = cursor.fetchall()
        for row in rows:
            z = row[2].split("-",1)
            brand = z.pop(0)
            model = str(z[0])
            dictname.append({
                'title': row[8],
                'href': row[7],
                'price': row[3],
                'year': row[5],
                'mileage': row[6],
                'brand': brand,
                'model': model,
                'ad_posted': row[1],
                'title_test': row[9],
                'oldprice': row[4],
                })
            '''
            print("ID =", row[0])
            print("POSTED =", row[1])
            print("MODEL =", row[2])
            print("PRICE =", row[3])
            print("OLDPRICE =", row[4])
            print("YEAR =", row[5])
            print("MILEAGE =", row[6])
            print("HREF =", row[7])
            print("TITLE =", row[8])
            print("TITLETEST = ", row[9], "\n")
            '''
        print("Data read ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while reading data PostgreSQL table", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


#  ================== execution ==================
'''
dictold = openbase("lxml_data.json", "Old")
create_table("soldcars")
write_to_database(dictold, "soldcars")
read_from_database("soldcars", parsed)

print(parsed)
result = 0
for i in parsed:
    result += i['year']
print(result)
'''

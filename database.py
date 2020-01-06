#!/usr/bin/env python3
# https://stackabuse.com/working-with-postgresql-in-python/


import json
import psycopg2

parsed = []

user = "udiovrzasgdmfb"
#user = "pythonuser"
password = "07ae622ed6fbb9db7c637fae65609a3a42f179d3751c4ad1f2f215aca0d717c9"
#password = "pythonuser"
host = "ec2-174-129-33-14.compute-1.amazonaws.com"
#host = "127.0.0.1"
port = "5432"
database = "d59nu1h4fi30n4"
#database = "duparcer"


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
                LINK VARCHAR(300),
                TITLE TEXT,
                TITLETEST TEXT);'''

        cursor.execute(create_table_query)

        connection.commit()
        print("Table: " + tablename + " created successfully in PostgreSQL ")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while creating PostgreSQL table:", error)
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
        print("Table " + tablename + " - successfully cleared in PostgreSQL ")

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
            if 'oldprice' in i and i['oldprice'] != None:
                to_insert = command + str(m) + ", '" + str(i['ad_posted']) + "', '" + i['brand'] + "-" + i['model'] + "', " + str(i['price']) + ", '" + str(i['oldprice']) + "', " + str(i['year']) + ", " + str(i['mileage']) + ", '" + i['href'] + "', '" + i['title'] + "', '" + i['title_test'] + "');"
            else:
                to_insert = command + str(m) + ", '" + str(i['ad_posted']) + "', '" + i['brand'] + "-" + i['model'] + "', " + str(i['price']) + ", '" + "null" + "', " + str(i['year']) + ", " + str(i['mileage']) + ", '" + i['href'] + "', '" + i['title'] + "', '" + i['title_test'] + "');"
            #print(to_insert)
            cursor.execute(to_insert)
            m += 1

        connection.commit()
        print("Data added to table: " + tablename + ". " + str(len(dictname)) + " items")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while addind data PostgreSQL table:", dictname, tablename, error)
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
        print("Data read: " + str(len(dictname)) + " rows")

    except (Exception, psycopg2.DatabaseError) as error :
        print ("Error while reading data PostgreSQL table: ", error)
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


def dump_to_base(olddict, newdict, nameofbase):
    if olddict != newdict:
        truncate_table(nameofbase)
        write_to_database(newdict, nameofbase)

#  ================== execution ==================


# create_table("soldcars")
# write_to_database(dictold, "soldcars")
# read_from_database("soldcars", parsed)
# dictsold = openbase("data/lxml_data_sold.json", "sold")
# dictdisc = openbase("data/lxml_data_disc.json", "disc")
# dictnew = openbase("data/lxml_data.json", "new")
# create_table("soldcars")
# create_table("discounted")
# create_table("newcars")
# truncate_table("soldcars")
# truncate_table("discounted")
# truncate_table("newcars")
# write_to_database(dictsold, "soldcars")
# write_to_database(dictdisc, "discounted")
# write_to_database(dictnew, "newcars")

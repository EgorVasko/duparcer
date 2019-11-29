'''
import pypyodbc


connection = pypyodbc.connect('Driver={SQL SERVER};'
                              'Server=DESKTOP-P07GV3N\SQLEXPRESS;'
                              'Database=Northwind;'
                              'uid=;'
                              'pwd=;')

cursor = connection.cursor()

mysqlquery = ('DROP TABLE dbo.Cars')
mysqlquery1 = ("""
CREATE TABLE dbo.Cars (
    ID int,
    Posted varchar(255),
    Model varchar(255),
    Price int,
    Year int,
    Mileage int,
    Link varchar(255)
);
""")

cursor.execute(mysqlquery)

results = cursor.fetchall()
print(results)
'''


import requests
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

pa = ["https://dubai.dubizzle.com", "https://fujairah.dubizzle.com","https://tut.by"]
for i in pa:
    print(i)
    response = requests.head(i, timeout=15,headers={'User-Agent': user_agent})
    if response.status_code == 200:
        print(i,"checked & avaliable")
        continue
    else:
        print("Not avaliable")

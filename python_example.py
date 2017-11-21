# pip install pymysql
import pymysql

# Connect to the database
connection = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='cs4400_Group_',
                             password='',
                             db='cs4400_Group_',
)

try:
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM User;'
        cursor.execute(sql)
        print(cursor.fetchall())

finally:
    connection.close()
    print("Done")
import MySQLdb
con=MySQLdb.connect(host="172.21.15.14",user="root",passwd="123456",db="article_spider",charset="utf8")
cursor = con.cursor()
with con:
    #获取连接的cursor，只有获取了cursor，我们才能进行各种操作
    cur = con.cursor()
    #创建一个数据表 writers(id,name)

    #以下插入了5条数据
    sql = """
INSERT INTO jobbole_article(title, url, url_object_id, create_date, fav_nums) 
VALUES (%s, %s, %s, %s, %s)
"""
    # cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
    # cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
    # cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
    # cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
    # cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
    cur.execute(sql,('111','www.baidu.com','12345','2017/06/08','5'))
    # print(n)
con.close()

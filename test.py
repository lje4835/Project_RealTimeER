import sqlite3

conn = sqlite3.connect('project.db')
cur = conn.cursor()
sido = "서울특별시"
sigungu = "종로구"
cur.execute(f"SELECT * FROM ER_table WHERE Sido='{sido}' AND Sigungu='{sigungu}';")
rows = [r for r in cur.fetchall()]
for row in rows :
    print(row[0], row[1])
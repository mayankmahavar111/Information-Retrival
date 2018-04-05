import sqlite3
from random import randint
a=[]

def getBody(table_name,db):
    query='select idf from {}'.format(table_name)
    res = db.execute(query)
    temp=res.fetchall()
    res=[]
    for x in temp:
        res.append(x[0])
    return (res)

if __name__ == '__main__':
	for i in range(10):
		b=[]
		n=10000
		for j in range(10):
			b.append(n)
			n=randint(0,n)
		a.append(b)

	for i in range(10):
		x=0
		for j in range(10):
			x+=a[i][j]
		for j in range(10):
			a[i][j]/=float(x)

	# for i in a:
	# 	print i

	db_name = 'document'
	table_name = "term"
	conn = sqlite3.connect('{}.db'.format(db_name))
	db = conn.cursor()
	corpse=getBody(table_name,db)
	print corpse


from py_cerebro import cclib, database
import datetime

host = 'db.cerebrohq.com'
port = 45432

def main():
	db = database.Database(host, port)

	if (db.connect_from_cerebro_client() == 0):
		res = db.execute('select mtm, name from "listUsers"(false)')
		for r in res:
			dt = str(r[0].day) + '-' + str(r[0].month) + '-' + str(r[0].year) + ' ' + str(r[0].hour) + ':' + str(r[0].minute) + ':' + str(r[0].second)   
			print('User: ' + r[1] + '		Last login: ' + dt)
		pass
	else:
		print('Can not connect to database. Host: ' + host + ' or port: ' + str(port) + ' is not correct, or Cerebro client is not running!')
	pass

main()
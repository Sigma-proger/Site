import sqlite3
import datetime
import ast

def create_table():
	db_file = "db.db"
	conn = sqlite3.connect(db_file)

	conn.execute(f"""
		CREATE TABLE IF NOT EXISTS Admins (  
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL,
			password TEXT NOT NULL
		)""")

	conn.execute(f"""
		CREATE TABLE IF NOT EXISTS Users (  
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL,
			password TEXT NOT NULL
		)""")

	conn.execute(f"""
		CREATE TABLE IF NOT EXISTS Topics (  
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL
		)""")

	conn.execute(f"""
		CREATE TABLE IF NOT EXISTS SUBtopics (  
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			topicID INTEGER NOT NULL,
			name TEXT NOT NULL,
			content JSON NOT NULL
		)""")

	conn.commit()

def add_user(_name, _pass):
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT * FROM users WHERE username = "{_name}" """ #шукає в таблиці
		cur.execute(sql)
		data = cur.fetchone() #fetchone() = один рядок, видає 1 рядок
		print("Data:", data)
		if data is None:
			sql = """INSERT INTO users (username, password) VALUES(?, ?)"""
			cur.execute(sql, (_name, _pass))

		conn.commit() #щоб зберегти зміни в БД (треби писати завжди)
		cur.close() #закриває метод курсора
	except Exception as e:
		print('add_user: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()

def user_exists(_name, _pass):
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT * FROM users WHERE username = "{_name}" AND password = "{_pass}" """ #шукає в таблиці
		cur.execute(sql)
		data = cur.fetchone() #fetchone() = один рядок, видає 1 рядок
		if data is not None:
			cur.close() #закриває мотод курсора
			#add_user(_pass, _name)
			return True
		else:
			cur.close() #закриває метод курсора
			return False
	except Exception as e:
		#пишемо що робити якщо виникає помилка у try
		print('user_exists: ', e)
	finally:#те що робити при завершені роботи незалежно була помилка чи ні
		#закриваємо підключення до БД
		if conn is not None: #чи зміна conn не = None
			conn.close()

def get_topic():
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT * FROM Topics"""
		cur.execute(sql)
		data = cur.fetchall() #fetchone() = один рядок, видає 1 рядок
		cur.close() #закриває мотод курсора
		return data
	except Exception as e:
		print('get_topic: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()
			
create_table()

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
		print('check_user: ', e)
	finally:#те що робити при завершені роботи незалежно була помилка чи ні
		#закриваємо підключення до БД
		if conn is not None: #чи зміна conn не = None
			conn.close()

def ovner_user(_pass, _name):
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT * FROM users WHERE password = "{_pass}" AND login = "{_name}" """ #шукає в таблиці users_id
		cur.execute(sql)
		data = cur.fetchone() #fetchone() = один рядок, видає 1 рядок
		cur.close() #закриває мотод курсора
		if data != None:
			return True
		else:
			return False
	except Exception as e:
		print('ovner_user: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()

def get_product():
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT * FROM itstore"""
		cur.execute(sql)
		data = cur.fetchall() #fetchone() = один рядок, видає 1 рядок
		cur.close() #закриває мотод курсора
		return data
	except Exception as e:
		print('get_product: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()

def get_id_products(_id_tov: int):
	db_file = 'db.db'
	conn = None
	state = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor() #закриває метод курсора
		sql = f"""SELECT * FROM ITstore WHERE id = "{_id_tov}" """
		cur.execute(sql)
		data = cur.fetchall()
		cur.close()

	except Exception as e:
		print('get_products: ', e)
	finally:
		if conn is not None:
			conn.close()
		return data

def get_basket(_name):
	db_file = 'db.db'
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		cur = conn.cursor()
		sql = f"""SELECT prd_id FROM basket WHERE login = "{_name}" """
		cur.execute(sql)
		data = cur.fetchone() #fetchone() = один рядок, видає 1 рядок
		cur.close() #закриває мотод курсора
		return str(data)
	except Exception as e:
		print('get_tov_basket: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()

def add_tov_basket(_name, prd_id):
	db_file = 'db.db'
	prd_list = []
	try:
		conn = sqlite3.connect(db_file)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM basket WHERE login = ?", (_name,))
		existing_row = cursor.fetchone()
		if existing_row or None:
			existing_row = existing_row[2]
			existing_row = [x.replace("'", "").strip() for x in existing_row.split(',')]
			prd_list.extend(existing_row)
			prd_list.append(prd_id)
			cursor.execute("UPDATE Basket SET prd_id = ? WHERE login = ?", (str(prd_list).strip("[]"), _name))
		else:
			cursor.execute("INSERT INTO Basket(login, prd_id) VALUES (?, ?)", (_name, str(prd_id)))
		conn.commit()
	except Exception as e:
		print('add_tov_basket: ', e)
	finally:
		if conn is not None: #чи зміна conn не = None
			conn.close()
			
create_table()
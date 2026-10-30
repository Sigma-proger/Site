from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
#import json
import db_cmd

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

#registration methods
@app.route('/registration', methods=['GET', 'POST'])
def registration():
	if request.method == 'POST':
		reg_name = request.form.get('UserName')
		reg_pas = request.form.get('Password')

		# Передаємо дані у вашу функцію БД
		db_cmd.add_user(reg_name, reg_pas)
		print(reg_name, reg_pas)

	return render_template('create-account/registration.html', message=None)

@app.route('/registration/style.css')
def registration_css():
    return send_from_directory('templates/create-account', 'style.css')

@app.route('/registration/assets/<path:filename>')
def registration_assets(filename):
    return send_from_directory('templates/create-account/assets', filename)

#login methods
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		log_name = request.form.get('UserName')
		log_pas = request.form.get('Password')
		print(db_cmd.user_exists(log_name, log_pas) == True)
		if db_cmd.user_exists(log_name, log_pas) == True:
			return render_template('index.html', name=log_name)
		else:
			return render_template('create-account/login.html')
		
	else:
		return render_template('create-account/login.html')

@app.route('/login/style.css')
def login_css():
    return send_from_directory('templates/create-account', 'style.css')

@app.route('/login/assets/<path:filename>')
def login_assets(filename):
    return send_from_directory('templates/create-account/assets', filename)


if __name__ == '__main__':
	app.run(debug=True)

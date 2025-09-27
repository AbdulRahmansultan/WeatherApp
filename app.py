from flask import Flask, render_template,request, redirect,url_for,session,flash
import requests
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps


app = Flask(__name__)
app.secret_key=''
api_key = 'a3e1cb9df52a112d22730391976c94cc'
users = {
    'user1':{
        'password_hash':generate_password_hash("passwoed123"),
        'email':'user1@gmail.com'
    },
}
@app.route('/', methods=['GET','POST'])
def  index():
    if 'username' not in session:
        return redirect(url_for('login'))
    weather_data = None
    if request.method== 'POST':
        city = request.form.get('city')
        if city:
            
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            response = requests.get(url)
            if response.status_code==200:
                weather_data=response.json()
            else:
                weather_data={'error':'city not found or api limit reached'}
    return render_template('index.html', username=session['username'],weather_data=weather_data)        
users = {
    'user1': {
        'password_hash': generate_password_hash("passwoed123"),
        'email': 'user1@gmail.com'
    },
}

@app.route('/register', methods=['GET','POST'])
def register():
    register_message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not( username and email and password and confirm_password):
            register_message = 'All fields are required'
        elif password != confirm_password:
            register_message = 'Passwords do not match'
        elif username in users:
            register_message = 'Username already exists'
        else:
            users[username] = {
                'password_hash': generate_password_hash(password),
                'email': email
            }
            return redirect(url_for('login'))
    return render_template('register.html', register_message=register_message)

@app.route('/login', methods=['GET','POST'])
def login():
    login_message=""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            login_message = 'Invalid username or password'
    return render_template('login.html', login_message=login_message)

if __name__=="__main__":
    app.run(debug=True)



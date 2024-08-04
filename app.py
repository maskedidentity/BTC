from flask import Flask, request, render_template, session
from flask import jsonify
import mysql.connector
import yaml
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def load_db_config():
    with open('db.yaml', 'r') as file:
        config =  yaml.safe_load(file)
    return config['database']

db_config = load_db_config()

def get_db_connection():
    conn=mysql.connector.connect(**db_config)
    return conn

@app.route('/', methods=['GET','POST'])
def home():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        tiers = request.form.getlist('tier')

        if not tiers:
            return render_template('forbidden.html')
        
        tier_for_validation = tiers[0]
        tier_for_storage = tiers[-1]

        if 'gold' in tier_for_validation:
            return render_template('forbidden.html')

        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO user2024 (name, password, tier) VALUES (%s, %s, %s)", (name, hashed_password, tier_for_storage))
            conn.commit()
        except mysql.connector.errors.IntegrityError:
            return ('Name for every user should always be unique')

        cursor.close()
        conn.close()
        return render_template('successful.html', name=name, password=password, tier=tier_for_validation)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, password, tier FROM user2024 WHERE name = %s", (name,))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            if 'gold' in user['tier']:
                return render_template('CEO2024_uythdyrrtx.html', name=user['name'], password=user['password'], tier=user['tier'])
            return render_template('login_successful.html', name=user['name'], password=user['password'], tier=user['tier'])
        else:
            return render_template('login_failed.html',name=name, password=password)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

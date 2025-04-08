from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a real secret key


# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()


# Route for Home page (landing page)
@app.route('/')
def home():
    return render_template('index.html')


# Route for Sign Up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
                       (name, email, phone, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('signup.html')


# Route for Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]  # Store the user_id in session
            session['user_name'] = user[1]  # Store the user_name in session
            return redirect(url_for('recipes'))
        else:
            return 'Invalid credentials. Please try again.'

    return render_template('login.html')


# Route for Recipe listing page
@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, ingredients, instructions FROM recipes WHERE user_id=?", (session['user_id'],))
    recipes = cursor.fetchall()
    conn.close()

    return render_template('recipes.html', recipes=recipes)


# Route for adding a recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (user_id, title, ingredients, instructions) VALUES (?, ?, ?, ?)",
                       (session['user_id'], title, ingredients, instructions))
        conn.commit()
        conn.close()

        return redirect(url_for('recipes'))

    return render_template('add_recipe.html')


# Run the app
if __name__ == "__main__":
    init_db()  # Initialize the db
    app.run(debug=True)

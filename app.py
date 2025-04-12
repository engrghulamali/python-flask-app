from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a real secret key
from werkzeug.utils import secure_filename

# Database setup
def init_db():
    # if os.path.exists('users.db'):
    # os.remove('users.db')
    # print("Existing database deleted. Starting fresh.")

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
            user_id INTEGER,
            name TEXT,
            cuisine TEXT,
            meal_type TEXT,
            dietary TEXT,
            difficulty TEXT,
            image_url TEXT,
            ingredients TEXT,
            steps TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favourites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            recipe_id INTEGER,
            category_id INTEGER,
            UNIQUE(user_id, recipe_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')


    conn.commit()
    conn.close()

@app.context_processor
def inject_current_page():
    return dict(current_page=request.endpoint)


# Route for Home page (landing page)
@app.route('/')
def home():
    return render_template('index.html', title='Home')


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

    return render_template('signup.html', title='Sign Up')


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
        # else:
            # flash('Login failed. Please check your email and password.')

    return render_template('login.html')


# Route for Recipe listing page
@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE user_id = ?", (session['user_id'],))
    recipes = cursor.fetchall()

    cursor.execute("SELECT * FROM categories ORDER BY name ASC")
    categories = cursor.fetchall()

    conn.close()
  
    return render_template('recipes.html', recipes=recipes, categories=categories, title='Recipes')


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        cuisine = request.form['cuisine']
        meal_type = request.form['meal_type']
        dietary = request.form['dietary']
        difficulty = request.form['difficulty']
        ingredients = request.form['ingredients']
        steps = request.form['steps']
        image = request.files.get('image')

        # Handle image upload
        image_url = ''
        if image:
            filename = secure_filename(image.filename)  # Fixed this line, previously `c` was here
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, filename)
            image.save(image_path)
            image_url = '/' + image_path  # for browser use

        # Insert into DB
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recipes 
            (user_id, name, cuisine, meal_type, dietary, difficulty, image_url, ingredients, steps) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session['user_id'], name, cuisine, meal_type,
            dietary, difficulty, image_url, ingredients, steps
        ))
        conn.commit()
        conn.close()
        # flash("Recipe added successfully!", "success")
    return redirect(url_for('recipes'))

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            try:
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
                conn.commit()
            except sqlite3.IntegrityError:
                pass  # handle duplicate if needed

    cursor.execute("SELECT * FROM categories ORDER BY name ASC")
    categories = cursor.fetchall()
    conn.close()
    return render_template('categories.html', categories=categories, title='Favourites')

@app.route('/profile')
def profile():
    user = get_user()  # Fetch user details using the function
    if user:
        # If the user exists, pass the data to the template
        return render_template('profile.html', user=user, title='Profile')
    else:
        return redirect(url_for('login'))  # Redirect to login if no user is found

def get_user():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    return None  # Return None if no user is found

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/add_favourite', methods=['POST'])
def add_favourite():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    category_id = request.form.get('category_id')
    recipe_id = request.form.get('recipe_id')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO favourites (user_id, recipe_id, category_id) VALUES (?, ?, ?)",
            (user_id, recipe_id, category_id)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already favorited
    conn.close()

    return redirect(url_for('recipes'))

@app.route('/category/<int:category_id>', methods=['GET'])
def category_detail(category_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search_query = request.args.get('q', '').strip().lower()

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
    category = cursor.fetchone()

    if not category:
        return "Category not found", 404

    if search_query:
        cursor.execute("""
            SELECT r.*
            FROM favourites f
            JOIN recipes r ON f.recipe_id = r.id
            WHERE f.category_id = ? AND f.user_id = ? AND LOWER(r.name) LIKE ?
        """, (category_id, session['user_id'], f'%{search_query}%'))
    else:
        cursor.execute("""
            SELECT r.*
            FROM favourites f
            JOIN recipes r ON f.recipe_id = r.id
            WHERE f.category_id = ? AND f.user_id = ?
        """, (category_id, session['user_id']))

    recipes = cursor.fetchall()
    conn.close()

    return render_template('category_detail.html',
                           category_id=category_id, 
                           category_name=category[0],
                           recipes=recipes,
                           search_query=search_query,
                           title=f"Category: {category[0]}")


@app.route('/category/<int:category_id>/remove/<int:recipe_id>', methods=['POST'])
def remove_recipe_from_category(category_id, recipe_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM favourites
        WHERE user_id = ? AND category_id = ? AND recipe_id = ?
    """, (session['user_id'], category_id, recipe_id))
    conn.commit()
    conn.close()

    return redirect(url_for('category_detail', category_id=category_id))

# Run the app
if __name__ == "__main__":
    init_db()  # Initialize the db
    app.run(debug=True)

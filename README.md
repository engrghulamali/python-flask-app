# Recipe Management Flask Application

A simple Flask web application that allows users to sign up, log in, add recipes, manage categories, and mark recipes as favourites.

## 🔗 Repository

**GitHub:** [https://github.com/engrghulamali/python-flask-app](https://github.com/engrghulamali/python-flask-app)

---

## 🚀 Features

- 🧑‍🍳 User Authentication (Sign up, log in, log out)
- 📖 Add and manage your own recipes
- 🗂️ Create and manage recipe categories
- ❤️ Mark recipes as favourites and organize them
- 📸 Upload recipe images

---


## 📦 Dependencies

Install required packages via pip:

```bash
pip install Flask werkzeug
```


---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/engrghulamali/python-flask-app.git
cd python-flask-app
```

### 2. (Optional) Create a Virtual Environment

#### 🐧 Linux / 🍎 macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install Flask werkzeug
```

### 4. Initialize the Database

The database is auto-created on first run, but you can manually initialize it:

```bash
python -c "from app import init_db; init_db()"
```

### 5. Run the App

```bash
python3 app.py
```

### 6. Open in Browser

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Project Structure

```
/python-flask-app
│
├── static/
│   └── uploads/              # Image uploads
│
├── templates/                # HTML templates
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── recipes.html
│   ├── categories.html
│   ├── profile.html
│   └── category_detail.html
│
├── app.py                    # Main Flask application
├── users.db                  # SQLite database
```

---

## ✅ Functionality Overview

| Route                  | Description                            |
|------------------------|----------------------------------------|
| `/`                    | Home page                              |
| `/signup`              | Register a new user                    |
| `/login`               | User login                             |
| `/logout`              | Logout current session                 |
| `/recipes`             | List user’s recipes                    |
| `/add_recipe`          | Add a new recipe                       |
| `/categories`          | Manage categories                      |
| `/add_favourite`       | Add recipe to a category               |
| `/category/<id>`       | View favourites in a category          |
| `/profile`             | View user profile                      |

---


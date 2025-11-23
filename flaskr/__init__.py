import os
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from .helpers import register_user, query_db, validate_field
import sqlite3
from flask import g, redirect, url_for


# === MAIN APP CONFIGURATION === #
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # === DATABASE INITIALISATION BOILERPLATE CONFIG === #
    DATABASE = 'instance/todo.db'

    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            print(f"=== Connected to database: {DATABASE} ===")
        db.row_factory = sqlite3.Row
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
            

    # ============= APP ROUTES HERE ============= #
    @app.route('/')
    def todolist():
        return render_template("index.html")
    
    @app.route('/login', methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")
        else:
            return render_template("login.html")

    @app.route('/register', methods=["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")
        else: 
            # Retrieve data from form
            name = request.form['name']
            username = request.form['username']
            email = request.form['email']
            pw1 = request.form['password']
            pw2 = request.form['cfm_password']

            # Backend check for matching passwords
            if not (pw1 == pw2):
                return redirect(url_for('register'))

            # Validate fields
            if validate_field(email, "email") and validate_field(username, "user") and validate_field(pw1, "pw"):
                # Generate PW Hash
                pw_hash = generate_password_hash(pw1)
                # Insert into DB
                register_user(get_db, username, email, pw_hash, name)
                # Redirect user to index page
                redirect(url_for('index'))

            # IF registration fails
            return redirect(url_for('register'))
    
    # === END OF APP === #
    return app

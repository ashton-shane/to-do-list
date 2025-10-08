import os
from flask import Flask, render_template, request


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
            return render_template("register.html")
        
    return app

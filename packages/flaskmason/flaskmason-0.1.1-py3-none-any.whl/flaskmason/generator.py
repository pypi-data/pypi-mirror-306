import os
import argparse

project_structure = {
    "": ["app.py", "config.py", "requirements.txt", ".env", "urls.py", "models.py", "README.md"],
    "blueprints": [],
    "blueprints/auth": ["__init__.py", "urls.py", "forms.py"],
    "blueprints/admin": ["__init__.py", "urls.py", "forms.py"],
    "static": ["style.css"],
    "templates": ["base.html", "index.html", "login.html", "register.html", "dashboard.html"],
}

file_templates = {
    "app.py": """\
from urls import *
from models import db

db.register_app(app)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
""",
    "config.py": """\

if __name__ == "__main__":
    app.run(debug=True)
""",
    
    "config.py": """\
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    DEBUG = True
""",
    ".env": """\
FLASK_APP=app.py
FLASK_ENV=development
""",
"urls.py": """\
from flask import Flask, render_template, redirect, url_for
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/login')
def login():
    return redirect('/auth/login')
    
@app.route('/register')
def register():
    return redirect('/auth/register')
    
@app.route('/logout')
def logout():
    return redirect('/auth/logout')
    
@app.route('/dashboard')
def dashboard():
    return redirect('/admin/dashboard')
""",

    "models.py": """\
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# define the database models
""",

    "requirements.txt": """\
Flask
Flask-WTF
Flask-SQLAlchemy
""",
    "blueprints/auth/__init__.py": """\
from flask import Blueprint

auth = Blueprint('auth_bp', __name__)

from .urls import *
        
        """
    ,
    "blueprints/auth/urls.py": """\
from flask import render_template, request, redirect, url_for
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login
        pass
    return render_template('auth/login.html')
    
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration
        pass
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    # Process logout
    return redirect(url_for('auth.login'))
"""
    ,
    "blueprints/auth/forms.py": """\
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
"""
    ,
    "blueprints/admin/__init__.py": """\
from flask import Blueprint

admin = Blueprint('admin_bp', __name__)

from .urls import *
"""
    ,
    "blueprints/admin/urls.py": """\
from flask import render_template, request, redirect, url_for
from . import admin_bp

@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')
"""
    ,
    "blueprints/admin/forms.py": """\
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
class DashboardForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')
"""
    ,
    "static/style.css": "",
    "templates/base.html": """\
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
"""
}


def create_file(path, content):
    content = file_templates.get(path, "# " + os.path.basename(path))
    with open(path, "w") as file:
        file.write(content)

def create_project_structure(project_name):
    os.makedirs(project_name, exist_ok=True)
    
    for folder, files in project_structure.items():
        folder_path = os.path.join(project_name, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            create_file(os.path.join(folder_path, file), "# " + file)
    
    print(f"Flask project '{project_name}' created successfully!")

def main():
    parser = argparse.ArgumentParser(description="Generate a Flask project structure.")
    parser.add_argument("project_name", help="Name of the Flask project")
    
    args = parser.parse_args()
    create_project_structure(args.project_name)

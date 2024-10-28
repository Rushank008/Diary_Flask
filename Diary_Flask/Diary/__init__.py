from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager
from .models import User
# Initialize MySQL
db = MySQL()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'Your_secretkey'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Ypur_pass'
    app.config['MYSQL_DB'] = 'diary'

    # Initialize MySQL
    db.init_app(app) #Connects database with the app

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app) #Connects flask login with the app
    login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated

  
    @login_manager.user_loader #This decorator tells Flask-Login to use this function to get user information when a user is logged in.
    def load_user(user_id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        if user:
            return User(id=user[0], username=user[1], password=user[2])
        return None
    
    # Register Blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create tables (if needed)
    create_tables(app)

    return app

def create_tables(app):
    # Function to create tables if they don't exist
    with app.app_context():
        cur = db.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                hint VARCHAR(255)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS diary_entries (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE,
                title VARCHAR(50),
                content TEXT,
                user_id INT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cur.close()

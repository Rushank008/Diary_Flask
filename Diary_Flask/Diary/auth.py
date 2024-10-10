from flask import Flask,Blueprint,render_template,request,redirect,url_for
from Diary import db
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user

auth = Blueprint('auth', __name__)

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        hint = request.form.get('hint', '')  # Get the hint, default to an empty string if not provided

        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()  # Fetch one record
        if existing_user:
            cur.close()
            return "Username already exists"
        
        if password1 != password2:
            cur.close()
            return "Passwords don't match"

        else: 
            hashed_password = generate_password_hash(password1)
            cur.execute("INSERT INTO users (username, password,hint) VALUES (%s, %s,%s)", (username, hashed_password,hint)) 
            db.connection.commit()
            cur.close()
            return redirect(url_for('auth.login'))  # Redirect to the login page
            

    return render_template('sign-up.html')

@auth.route("/login",methods=["POST","GET"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if username == user[1]: #Using indexes as the data returns in tuple
            if check_password_hash(user[2], password):
                user_obj = User(id=user[0], username=user[1], password=user[2])  #Assigns the value to user class 
                login_user(user_obj)  # Log the user in with following data
                return redirect(url_for('views.home'))
            else:
                return"Password invalid"
        else:
            cur.close()
            return"Username invalid"
    
    return render_template('login.html')

@auth.route("/forgot-password",methods=["GET", "POST"])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        hint = request.form.get('hint')
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND hint = %s", (username, hint))
        user = cur.fetchone()
        if user:
            return redirect(url_for('auth.reset_password', username=username))
        else:
            return "Username or hint is incorrect"
    return render_template('forgot.html')

@auth.route("/reset-password/<username> ",methods=["GET","POST"]) #As this function cannot take arguement normally arguement needs to be passed via url so that's why using <username>
def reset_password(username):
    if request.method == 'POST':
        password1 = request.form.get('new_password')
        password2 = request.form.get('confirm_password')
        if password1 == password2:
            hashed_password = generate_password_hash(password1)
            cur = db.connection.cursor()
            cur.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password,username))
            db.connection.commit()
            cur.close()
            return redirect(url_for('auth.login'))
        else:
            return "Passwords do not match"
    return render_template("reset.html")    

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
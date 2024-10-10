from flask import Flask,Blueprint,render_template,request,redirect,url_for,flash
from Diary import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import current_user,login_required

views = Blueprint('views', __name__)

@views.route('/home')
@views.route('/')
def home():
    return render_template('layout.html')

@views.route('/create-entry',methods=['POST','GET'])
@login_required
def create_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        date = request.form.get('date')
       
        user_id = current_user.id

        cur = db.connection.cursor()
        cur.execute("INSERT INTO diary_entries (title,content,date,user_id) VALUES (%s,%s,%s,%s)",(title,content,date,user_id))
        db.connection.commit()
        cur.close()
    return render_template('create-entry.html')

@views.route('/view-entries',methods=['POST','GET'])
@login_required
def view_entries():
    search_query = request.args.get('search','') #If no arguments passed then by default set to empty string
    cur = db.connection.cursor()
    if search_query:
                cur.execute("SELECT * FROM diary_entries WHERE user_id = %s AND (title LIKE %s OR content LIKE %s)",(current_user.id, f"%{search_query}%", f"%{search_query}%") )
    else:
          cur.execute("SELECT * FROM diary_entries WHERE user_id = %s",(current_user.id,))

    entries = cur.fetchall()
    cur.close()
    # Convert database results to a list of dictionaries
    entries = [{'id': entry[0], 'date': entry[1], 'title': entry[2], 'content': entry[3]} for entry in entries]

    return render_template('view-entries.html',entries = entries)

@views.route('/delete-entry/<entry_id>',methods=['POST','GET'])
@login_required
def delete_entry(entry_id):
      cur = db.connection.cursor()
      cur.execute("DELETE FROM diary_entries WHERE id = %s AND user_id = %s",(entry_id,current_user.id))
      db.connection.commit()
      cur.close()
      flash("Entry deleted successfully",category="success")
      return redirect(url_for("views.view_entries"))


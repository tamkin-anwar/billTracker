from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models.show import Show
from flask_app.models.user import User
from flask import flash

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html",user=User.get_by_id(data), shows=Show.get_all())

@app.route('/create/job',methods=['POST'])
def create():
    print(request.form)
    Show.save(request.form)

    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "user_id": session['user_id']
    }
    Show.save(data)
    return redirect('/dashboard')

@app.route('/view/job/<int:id>')
def view(id):
    show = Show.get_one({"id": id})
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id": session['user_id']})
    return render_template("view_job.html", show=show, user=user)

@app.route('/update/job',methods=['POST'])
def update():
    Show.update(request.form)
    return redirect('/dashboard')

@app.route('/destroy/job/<int:id>')
def destroy(id):
    data ={
        'id': id
    }
    Show.destroy(data)
    return redirect('/dashboard')

@app.route('/edit/job/<int:id>')
def edit(id):
    show = Show.get_one({"id": id})
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id": session['user_id']})
    return render_template("edit_job.html", show=show, user=user)

@app.route('/new/job')
def new_job():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id": session['user_id']})
    return render_template("new_job.html", user=user)

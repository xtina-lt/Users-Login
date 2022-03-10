from flask import Flask, render_template, request, redirect, get_flashed_messages, session
# 1) import flask packages
from flask_app import app
# 2) import app from folder
from flask_app.models.user import User
# 3) import User class from model
from flask_bcrypt import Bcrypt
# 4) import Bcrypt
bcrypt = Bcrypt(app)
# 4) create a Bcrypt object with our application
# 4) name bcyrpt

'''HOME'''
@app.route("/")
def index():
    return render_template("index.html")


'''READ ALL'''
@app.route("/users/read")
def read_all():
    return render_template("output.html", output=User.select_all())
    # select * from users
    # [cls(i) for i in results]

'''READ ONE'''
@app.route("/user/read/<id>")
def read_one(id):
    data={"id": id}
    # 1) get data from url
    return render_template("output_one.html", output=User.select_one(data))
    # 2) return results from query
    # 2) select * from users WHERE id=data
    # 2) return cls(result[0])

'''CREATE / REGISTER'''
@app.route("/user/create")
def create_show():
    return render_template("create.html")
    # 1) show form with user fields to input

@app.route("/user/create/process", methods=["POST"])
def create_process():
    data={k:v for k,v in request.form.items()}
    # 2) get all form inputs
    # 2) save to a new data dictionary
    if not User.validate_insert(data):
    # 3) VALIDATE form data
    # 3) if not TRUE 
    # 3)== False
        return redirect("/user/create")
        # 3a) IF FALSE
        # 3a) return to create/register page
    else:
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        # 4) IF TRUE
        # 4) hash the password from form
        # 4) so as to not input an unhashed password
        session["logged_in"] = User.insert(data)
        # 5) logged in user = inserted user with data
        # 5) returns id number
        # 5) save to use for later
        return redirect(f"/user/read/{session['logged_in']}")
        # 6) redirect to the user's information


'''UPDATE'''
@app.route("/user/update/<int:id>")
def edit_show(id):
    data={"id":id}
    # 1) get id from url
    # 1) save to data dictionary
    result = User.select_one(data)
    # 2) select * from users WHERE id = data
    # 2) return cls(result[0])
    return render_template("edit.html", output=result)
    # 3) send to html

@app.route("/user/update/process", methods=["POST"])
def edit_process():
    data={k:v for k,v in request.form.items()}
    # 4) get updated form data
    # 4) save to dictionary
    if not User.validate_update(data):
    # 5) IF NOT VALIDATED
    # 5) Valdiate Update with data from form
        return redirect(f"/user/update/{data['id']}") 
        # 5a) go back to update form
    else:
    # 6) IF VALIDATED
        if data["new_pass"]:
        # 7) IF VALIDATED
        # 7) & new password
            data["password"] = bcrypt.generate_password_hash(data["new_pass"])
            # 8) hash new password
            User.update(data)
            # 9) update users WHERE id = data
        else:
        # 7) IF VALIDATED
        # 7) & no new password
            data["password"] = bcrypt.generate_password_hash(data["password"])
            # 8) has password
            User.update(data)
            # 9) update users WHERE id = data['id']
        return redirect(f"/user/read/{data['id']}")
        # 10) if validated 
        # 10) redirect to show user data

'''DELETE'''
@app.route("/user/delete/<int:id>")
def delete(id):
    # 1) get user id from url
    data={"id":id}
    print(data)
    # 2) save id as dictionary
    User.delete(data)
    # 3) delete from users WHERE id = data
    return redirect("/users/read")

'''LOGIN'''
@app.route("/user/login")
def login_show():
    return render_template("login.html")
    # 1) show form

@app.route("/user/log_in/process", methods=["POST"])
def login_process():
    data={k:v for k,v in request.form.items()}
    # 2) data dict with form inputs
    if not User.validate_login(data):
    # 3) VALIDATE
        return redirect("/user/login")
        # 3a) if validate != True
        # 3a) redirect back to form
    else:
        session["logged_in"] = User.is_email(data)["id"]
        # 3b) if validate == True
        print(session)
        # 4) store user as session
        # 4) get user information from email in form
        return redirect(f"/user/read/{session['logged_in']}")
        # 5) redirect to user information 

'''LOGOUT'''
@app.route("/user/logout/process")
def logout_process():
    session.clear()
    # 1) session.clear() method
    return redirect("/")
    # 2) redirect to home

'''CATCHALL'''
@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("catchall.html")
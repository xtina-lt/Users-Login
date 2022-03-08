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
    # 3) if not TRUE == if False
        return redirect("/user/create")
        # 3a) IF FALSE
        # 3a) return to create page
    else:
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        # 3b) IF TRUE
        # 3b) hash the password from form
        session["logged_in"] = User.insert(data)
        # 4) logged in user = inserted user with data
        # 4) save to use for later
        return redirect("/users/read")


'''UPDATE'''
@app.route("/user/update/<int:id>")
def edit_show(id):
    data={"id":id}
    # 1) get id from url
    # 1) save to data dictionary
    output = User.select_one(data)
    print(output)
    # 2) select * from users WHERE id = data
    # 2) return cls(result[0])
    return render_template("edit.html", output=output)
    # 3) send to html

@app.route("/user/update/process", methods=["POST"])
def edit_process():
    data={k:v for k,v in request.form.items()}
    # 4) get updated form data
    # 4) save to dictionary
    if not User.validate_update(data):
    # 5) Valdiate Update with data from form
        return redirect(f"/user/update/{data['id']}") 
        # 5a) IF FALSE
        # 5a) go back
    else:
    # 5b) IF TRUE
        if data["new_pass"]:
        # 5b) IF TRUE
        # & 5bi) and there is a new password
            data["password"] = bcrypt.generate_password_hash(data["new_pass"])
            User.update(data)
            # 6) update users WHERE id = data['id']
        else:
        # 5b) IF TRUE
        # & 5bii) and there is NOT a new passowrd
            data["password"] = bcrypt.generate_password_hash(data["password"])
            User.update(data)
            # 6) update users WHERE id = data['id']
        return redirect(f"/user/read/{data['id']}")
        # 7) IF TRUE redirect to show user data

'''DELETE'''
@app.route("/user/delete/<int:id>")
def delete(id):
    # 1) get user id from url
    data={"id":id}
    print(data)
    # 2) save id as dictionary
    User.delete(data)
    # 3) delete from users WHERE id = data
    return redirect("/read/all")

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
        return redirect("/login")
        # 3a) if validate != True
        # 3a) redirect back to form
    else:
        session["logged_in"] = User.is_email(data)["id"]
        # 3b) if validate == True
        print(session)
        # 4) store user as session
        # 4) use info gathered by email from data dict
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
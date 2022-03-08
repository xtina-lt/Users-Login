from flask_app import app
# 1) IMPORT APPLICATION


from flask_app.controllers import users
# 2) IMPORT ROUTES

if __name__=="__main__":
    app.run(debug=True)
# 3) IF IN SERVER.PY
# 3) RUN IN DEBUG MODE
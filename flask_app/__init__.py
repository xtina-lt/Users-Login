from flask import Flask
# 1) import flask object from flask module

app = Flask(__name__)
# 2) create a new instance of flask object

app.secret_key="xtina.codes"
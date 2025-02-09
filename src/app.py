from flask import Flask,render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from config import config

app=Flask(__name__)

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():

    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():

    return render_template('register.html')


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()
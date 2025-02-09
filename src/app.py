from flask import Flask,render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from config import config
from flask_mysqldb import MySQL
from forms import Persona,Inicar
from models.entities.User import User
from models.ModelUser import ModelUser

app=Flask(__name__)
db=MySQL(app)

login_manager=LoginManager(app)


@login_manager.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():

    return render_template('home.html')

@app.route('/login',methods=['POST','GET'])
def login():
    form=Inicar()

    if form.validate() and request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        

        print(email,password)


        user=User(0,'',email,'',password)

        logged_user=ModelUser.login(db,user)

        if logged_user:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('perfil'))
            else:
                flash('Incorrect Password')
                return render_template('login.html',form=form)
                
        else:
            flash('Incorrect email')
            return render_template('login.html',form=form)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('perfil'))
        else:
            return render_template('login.html',form=form)

    

@app.route('/register',methods=['POST','GET'])
def register():
    form=Persona()

    if form.validate() and request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        image=request.form.get('image')
        password=request.form.get('password')
        confirm=request.form.get('confirm')

        print(username,email,image,password,confirm)


        user=User(0,username,email,image,password)

        logged_user=ModelUser.register(db,user)

        if logged_user:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('perfil'))
            else:
                flash('Incorrect Password')
                return render_template('register.html',form=form)
                
        else:
            flash('User exists')
            return render_template('register.html',form=form)
    else:
        if current_user.is_authenticated:
            return redirect(url_for('perfil'))
        else:
            return render_template('register.html',form=form)


@app.route('/perfil',methods=['GET','POST'])
@login_required
def perfil():
    return render_template('perfil.html')


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()
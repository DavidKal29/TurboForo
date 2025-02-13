from flask import Flask,render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from config import config
from flask_mysqldb import MySQL
from forms import Persona,Inicar,Perfil,Hilo,Mensaje
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
    print('Configracion:',config['production'])
    cursor=db.connection.cursor()
    #cursor.execute('SELECT id, titulo, categoria,mensajes FROM hilos')
    cursor.execute('SELECT id, titulo, categoria,mensajes FROM hilos ORDER BY fecha DESC')
    rows=cursor.fetchall()

    hilos=[]
    for row in rows:
        hilo={'id':row[0],'titulo':row[1],'categoria':row[2],'mensajes':row[3]}
        hilos.append(hilo)
    print(hilos)
    
    return render_template('home.html',hilos=hilos)
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
    cursor=db.connection.cursor()
    print('Id:',current_user.id)
    cursor.execute('SELECT * FROM datos WHERE id_user=%s',(current_user.id,))
    row=cursor.fetchone()
    print('El row:',row)

    datos={'hilos':row[1],'mensajes':row[2],'fecha':row[3]}
    return render_template('perfil.html',datos=datos)



@app.route('/perfil/edit/<id>',methods=['GET','POST'])
@login_required
def editar_perfil(id):
    if request.method=='GET':
        form=Perfil()

        form.username.data=current_user.username
        form.email.data=current_user.email
        form.image.data=current_user.image



        return render_template('editarPerfil.html',form=form)
    elif request.method=='POST':
        try:
            username=request.form.get('username')
            email=request.form.get('email')
            image=request.form.get('image')

            print(username,email,image)

            cursor=db.connection.cursor()
            values=(username,email,image,id)

            cursor.execute('UPDATE users SET username=%s,email=%s,image=%s WHERE id=%s',values)
            db.connection.commit()
            return redirect(url_for('perfil'))
        except:
            flash('Username or Email exists')
            return redirect(url_for('perfil'))

@app.route('/perfil/crearHilo',methods=['GET','POST'])
@login_required
def crearHilo():
    form=Hilo()
    if request.method=='GET':
        return render_template('crearHilo.html',form=form)
    elif request.method=='POST' and form.validate():
        titulo=request.form.get('titulo')
        mensaje=request.form.get('mensaje')
        categoria=request.form.get('categoria')

        print(titulo,mensaje,categoria)

        try:
            cursor=db.connection.cursor()
            cursor.execute('INSERT INTO hilos (titulo,id_user,categoria,mensajes) VALUES (%s,%s,%s,%s)',(titulo,current_user.id,categoria,1))
            db.connection.commit()

            cursor.execute('SELECT id from hilos WHERE id_user=%s  ORDER BY id DESC LIMIT 1',(current_user.id,))
            id_hilo=cursor.fetchone()
            print(id_hilo[0])

            cursor.execute('INSERT INTO mensajes (contenido,id_user,id_hilo) VALUES (%s,%s,%s)',(mensaje,current_user.id,id_hilo))
            db.connection.commit()

            cursor.execute('UPDATE datos SET hilos=hilos+1, mensajes=mensajes+1 WHERE id_user=%s',(current_user.id,))
            db.connection.commit()

            flash('Añadido con éxito')
        except Exception as Error:
            print(Error)
            flash('error')

        return render_template('crearHilo.html',form=form)



@app.route('/perfil/verHilos',methods=['GET'])
@login_required
def verHilos():
    cursor=db.connection.cursor()
    cursor.execute('SELECT id, titulo, categoria,mensajes FROM hilos WHERE id_user=%s',(current_user.id,))
    rows=cursor.fetchall()

    hilos=[]
    for row in rows:
        hilo={'id':row[0],'titulo':row[1],'categoria':row[2],'mensajes':row[3]}
        hilos.append(hilo)
    print(hilos)
    
    return render_template('verHilos.html',hilos=hilos)

@app.route('/perfil/delete/<id>')
@login_required
def deletear_hilo(id):
    cursor=db.connection.cursor()

    cursor.execute('SELECT id_user FROM mensajes WHERE id_hilo=%s',(id,))
    data=cursor.fetchall()
    print('data:',data)

    for id_user in data:
        print('id_user:',id_user[0])
        cursor.execute('UPDATE datos SET mensajes=mensajes-1 WHERE id_user=%s',(id_user[0],))
        db.connection.commit()
        cursor.execute('DELETE FROM mensajes WHERE id_hilo=%s and id_user=%s ',(id,id_user[0]))
        db.connection.commit()

    cursor.execute('DELETE FROM mensajes WHERE id_hilo=%s and id_user=%s',(id,current_user.id))
    db.connection.commit()
    
    cursor.execute('DELETE FROM hilos WHERE id=%s',(id,))
    db.connection.commit()

    cursor.execute('UPDATE datos SET hilos=hilos-1 WHERE id_user=%s',(current_user.id,))
    db.connection.commit()

    return redirect(url_for('verHilos'))

@app.route('/foro/<id>',methods=['POST','GET'])
def foroVista(id):
    try:
        cursor=db.connection.cursor()
        if request.method=='POST':
        
            mensaje=request.form.get('mensaje')
            mensaje=mensaje.strip()

            cursor.execute('INSERT INTO mensajes (contenido,id_user,id_hilo) VALUES (%s,%s,%s)',(mensaje,current_user.id,id))
            db.connection.commit()

            cursor.execute('UPDATE datos SET mensajes=mensajes+1 WHERE id_user=%s',(current_user.id,))
            db.connection.commit()

            cursor.execute('UPDATE hilos SET mensajes=mensajes+1 WHERE id=%s',(id,))
            db.connection.commit()

        
        cursor.execute('SELECT id,titulo,fecha,id_user FROM hilos WHERE id=%s',(id,))
        data=cursor.fetchone()
        print(data)
            
        datos_hilo={'id':data[0],'titulo':data[1],'fecha':data[2],'id_user':data[3]}
        print(datos_hilo)

        form=Mensaje()



        cursor.execute('SELECT contenido,id_user,fecha FROM mensajes WHERE id_hilo=%s',(id,))
        data=cursor.fetchall()

        mensajes=[]
        for dato in data:
            contenido=dato[0]
            id_user=dato[1]
            fecha=dato[2]

            cursor.execute('SELECT username, image FROM users WHERE id=%s',(id_user,))
            row=cursor.fetchone()
            username=row[0]
            image=row[1]

            objeto={'contenido':contenido,'fecha':fecha,'username':username,'image':image}

            mensajes.append(objeto)
    except Exception as e:
        print('Error:',e)
        return redirect(url_for('index'))
        
    return render_template('foroVista.html',datos_hilo=datos_hilo,mensajes=mensajes,form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



def staus_404(error):
    return render_template('404.html')

def status_401(error):
    return redirect(url_for('login'))


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,staus_404)
    app.register_error_handler(401,staus_404)
    app.run()

    
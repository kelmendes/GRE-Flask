from flask import Flask, render_template, request, url_for, redirect, session
from flask_bootstrap import Bootstrap
import flask_login
import flask
#IMPORTANDO O FLASK ADMIN
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Bootstrap
Bootstrap(app)
#Branco de Dados dos Formularios
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dv.sqlite'
db = SQLAlchemy(app)

#Conectando App com Flask Admin
admin = Admin(app)
app.secret_key = 'super secret string'

#Login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class Formulario(db.Model):

    __tablename__= 'Requerimentos'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    matricula = db.Column(db.String)
    campus = db.Column(db.String)
    periodo = db.Column(db.String)
    curso = db.Column(db.String)
    turno = db.Column(db.String)
    iten = db.Column(db.String)
    identidade = db.Column(db.String)
    orgaoexpedidor = db.Column(db.String)
    estadomunucipio = db.Column(db.String)
    estado = db.Column(db.String)

    def __init__(self, nome, telefone, cpf, email, matricula, campus, periodo, curso, turno, iten,estado,identidade, orgaoexpedidor, estadomunucipio):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
        self.matricula = matricula
        self.campus = campus
        self.periodo = periodo
        self.curso = curso
        self.turno = turno
        self.iten = iten
        self.estado = estado
        self.identidade = identidade
        self.orgaoexpedidor = orgaoexpedidor
        self.estadomunucipio = estadomunucipio


db.create_all()

class User(flask_login.UserMixin):
    pass
###############################
###   Telas no Flask Admin  ###
###############################

#Tela da Tabela de Formularios


class MeuModelo(ModelView):
    column_filters  =  ( 'estado' ,  'curso','periodo','turno' )
    column_searchable_list = ['nome','cpf','matricula','estado','curso','periodo','turno','email','iten','identidade', 'orgaoexpedidor', 'estadomunucipio']
    form_excluded_columns = ['nome','cpf','matricula',  'curso','periodo','turno', 'telefone'  , 'email',  'campus', 'iten', 'identidade', 'orgaoexpedidor', 'estadomunucipio']
    can_create = True #Removendo permisao de criar formularios
    can_edit = True #Permitindo permisao de edita formulario
    can_delete = True #Permitindo/Removendo permisao de deleta formularios
    form_choices  =  {
    'estado' :  [
        ( 'EM ANDAMENTO' ,  'EM ANDAMENTO' ),
        ( 'INDEFERIDO' ,  'INDEFERIDO' ),
        ( 'DEFERIDO' ,  'DEFERIDO' ),
    ]
}


admin.add_view(MeuModelo(Formulario, db.session))


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return ("Email ou Senha Invalido")

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

users = {
    'MELQUE':
        {'pw': 'melque',
        'email':'melquesedeque-santos@gmail.com',
        'nome':'Melquesedeque Mauricio',
        'root':'NAO'},
    '20162TRPM0300':
        {'pw': 'klebson',
        'email':'klebsonmendes@gmail.com',
        'nome':'Klebson Mendes',
        'root':'NAO'},
    'TESTE':
        {'pw':'teste',
        'email':'emaildetestes@gmail.com',
        'nome':'Teste Nome',
        'root':'NAO'},
    'ADMIN':
        {'pw':'admin',
        'email':'emaildetadmin@gmail.com',
        'nome':'Admin Nome',
        'root':'SIM'}
        }

@app.route('/', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('index.html')
    email_normal = flask.request.form['email']
    email = email_normal.upper()
    senha = flask.request.form['pw']
    if email in users and senha == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        session['login'] = user.id
        session['email'] = users[email]['email']
        session['nome'] = users[email]['nome']
        session['root'] = users[email]['root']
        return render_template('home.html', session=session)
    else:
        return render_template('index2.html')
    return render_template('index2.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('index.html')

#Caso User nao tenha logado ira retorna
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(render_template('erro.html'))
    #return render_template('erro')


@app.route('/home')
@flask_login.login_required #precisa de Login para acessar
def index():
    return render_template('home.html')

@app.route('/root')
@flask_login.login_required #precisa de Login para acessar
def root():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)

@app.route('/filtroAll')
@flask_login.login_required #precisa de Login para acessar
def filtroAll():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)

@app.route('/filtroDef')
@flask_login.login_required #precisa de Login para acessar
def filtroDef():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.filter_by(estado='DEFERIDO').all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)

@app.route('/filtroIndef')
@flask_login.login_required #precisa de Login para acessar
def filtroIndef():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.filter_by(estado='INDEFERIDO').all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)

@app.route('/filtroCalcell')
@flask_login.login_required #precisa de Login para acessar
def filtroCalcell():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.filter_by(estado='CANCELADO PELO USUARIO').all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)


@app.route('/filtroOpen')
@flask_login.login_required #precisa de Login para acessar
def filtroOpen():
    if session['root'] == 'SIM':
        pessoas = Formulario.query.filter_by(estado='EM ANDAMENTO').all()
        pessoas.reverse ( )
    else:
        pessoas = 'NADA'
    return render_template('root.html', pessoas=pessoas)


@app.route('/cadastrar')
@flask_login.login_required #precisa de Login para acessar
def cadastrar():
    return render_template('cadastro.html')

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        matricula = request.form.get('matricula')
        campus = request.form.get('campus')
        periodo = request.form.get('periodo')
        curso = request.form.get('curso')
        turno = request.form.get('turno')
        iten = request.form.get('iten')
        identidade = request.form.get('identidade')
        orgaoexpedidor = request.form.get('orgaoexpedidor')
        estadomunucipio = request.form.get('estadomunucipio')
        estado = 'EM ANDAMENTO'


        if nome and telefone and cpf and email and matricula and campus and periodo and curso and turno and iten and identidade and orgaoexpedidor and estadomunucipio:
            p = Formulario(nome, telefone, cpf, email, matricula,campus, periodo, curso, turno, iten,estado,identidade, orgaoexpedidor, estadomunucipio, )
            db.session.add(p)
            db.session.commit()

    return redirect(url_for('index'))


@app.route('/lista')
@flask_login.login_required #precisa de Login para acessar
def lista():
    usuario = session['login']
    pessoas = Formulario.query.filter_by(matricula=usuario).all()
    #pessoas = Formulario.query.all()
    return render_template('lista.html', pessoas=pessoas)

@app.route('/cancelar/<int:id>')
@flask_login.login_required #precisa de Login para acessar
def cancelar(id):
    pessoa = Formulario.query.filter_by(_id=id).first()

    pessoa.estado = 'CANCELADO PELO USUARIO'
    db.session.commit()

    usuario = session['login']
    pessoas = Formulario.query.filter_by(matricula=usuario).all()
    return render_template('lista.html', pessoas=pessoas)

# New codigo editar formulario
@app.route('/editar/<int:id>')
@flask_login.login_required #precisa de Login para acessar
def editar(id):

    pessoa = Formulario.query.filter_by(_id=id).first()

    return render_template('editar.html', requerimento=pessoa)

#if __name__ == "__main__":
#    app.run(debug=True)#, host='10.36.70.182')

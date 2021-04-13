import psycopg2
import pandas as pd
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, request
from flask_cors import CORS
from waitress import serve
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Api(app)
cors = CORS(app)

conn = psycopg2.connect(
    host="ec2-34-225-167-77.compute-1.amazonaws.com",
    database="d76l1rkkcfbufc",
    user="imwtjcynbamcnr",
    password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
)

routes_efetuar_login = [
    '/efetuar_login'
]

routes_cadastrar = [
    '/cadastrar'
]

routes_cadastrar_medico = [
    '/cadastrar_medico'
]

routes_select_all = [
    '/select_all'
]

routes_delete = [
    '/delete'
]

routes_next_schedule = [
    '/next_schedule=<string:time>'
]

try:
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS PACIENTES (Cpf VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Genre VARCHAR(50) NOT NULL, Email VARCHAR(255) NOT NULL, Convenio VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL); CREATE TABLE IF NOT EXISTS MEDICOS (Crm VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Address VARCHAR(50) NOT NULL, Cidade VARCHAR(255) NOT NULL, Estado VARCHAR(255) NOT NULL, Phone VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Especialidade VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL)")
	conn.commit()
	conn.close()
except Exception as e:
        print({'Exception First:': str(e)})


class Cadastrar(Resource):
    """docstring for Insert"""

    def __init__(self):
        self.nome = None
        self.cpf = None
        self.birthday = None
        self.genre = None
        self.phone = None
        self.email = None
        self.convenio = None

    def post(self):
        req_data = request.get_json()  # obtendo os dados do model
        self.nome = req_data['nome']
        self.cpf = req_data['cpf']
        self.birthday = req_data['birthday']
        self.genre = req_data['genre']
        self.email = req_data['email']
        self.convenio = req_data['convenio']
        self.password = bcrypt.generate_password_hash(req_data['password']).decode('utf-8')
        
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()


            cur.execute("INSERT INTO PACIENTES (Nome, Cpf, Birthday, Genre, Email, Convenio, Password) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                            (self.nome, self.cpf, self.birthday, self.genre, self.email, self.convenio, self.password))
            conn.commit()
            conn.close()
            return {'insertion': 'ok'}
        except Exception as e:
            print('FALHA NO CADASTRO')
            print (str(e))
            return {'insertion error': str(e)}

class Cadastrar_Medico(Resource):
    """docstring for Insert"""

    def __init__(self):
        self.address = None
        self.birthday = None
        self.cidade = None
        self.crm = None
        self.email = None
        self.especialidade = None
        self.estado = None
        self.nome = None
        self.password = None
        self.phone = None

    def post(self):
        req_data = request.get_json()  # obtendo os dados do model
        
        self.address =  req_data['address']
        self.birthday =  req_data['birthday']
        self.cidade =  req_data['cidade']
        self.crm =  req_data['crm']
        self.email =  req_data['email']
        self.especialidade =  req_data['especialidade']
        self.estado =  req_data['estado']
        self.nome =  req_data['nome']
        self.password = bcrypt.generate_password_hash(req_data['password']).decode('utf-8')
        self.phone =  req_data['phone']
        
        print(self.password)

        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()


            cur.execute("INSERT INTO MEDICOS (address, birthday, cidade, crm, email, especialidade, estado, nome, password, phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                            (self.address, self.birthday, self.cidade, self.crm, self.email, self.especialidade, self.estado, self.nome, self.password, self.phone))
            conn.commit()
            conn.close()
            return {'insertion': 'ok'}
        except Exception as e:
            print('FALHA NO CADASTRO MÉDICO')
            print (str(e))
            return {'insertion error': str(e)}

class Efetuar_Login(Resource):
    def __init__(self):
        self.username = None
        self.password = None

    def post(self):
        req_data = request.get_json()
        self.user = req_data['user']
        self.password = req_data['password']#.encode('utf-8')
        self.tipo_usuario = req_data['tipo_usuario']
        print('logando ' + self.user)
        
        try:
            return self.checkUser()
        except Exception as e:
            conn.close()
            return {'error': str(e)}

    def checkUser(self):
        
        conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
        cur = conn.cursor()
        
        print(self.tipo_usuario)

        if self.tipo_usuario == "paciente":
            df_password =  pd.read_sql_query("SELECT password FROM PACIENTES WHERE Cpf = '"+self.user+"'", conn)
        elif self.tipo_usuario == "medico":
            df_password =  pd.read_sql_query("SELECT password FROM MEDICOS WHERE Crm = '"+self.user+"'", conn)
        
        conn.close()

        if(len(df_password) == 0):
            return 'Usuário não cadastrado'
        else:
            bd_password = df_password.to_dict()["password"][0]
            if(bcrypt.check_password_hash(bd_password, self.password)):
                print('entrou')
                return "success"
            else:
                print('falha')
                return "Usuário e senha não coincidem"

api.add_resource(Cadastrar, *routes_cadastrar)
api.add_resource(Cadastrar_Medico, *routes_cadastrar_medico)
api.add_resource(Efetuar_Login, *routes_efetuar_login)


@app.route('/', methods=['GET', 'POST'])
@app.route('/cadastro', methods=['GET', 'POST'])
def index():
    return render_template('cadastro.html')

@app.route('/cadastro-medico', methods=['GET', 'POST'])
def cadastro_medico():
    return render_template('cadastro-medico.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/busca', methods=['GET', 'POST'])
def busca():
    return render_template('busca.html')


if __name__ == '__main__':
    app.run()

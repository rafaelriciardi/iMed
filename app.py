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

routes_getespecialidades = [
    '/getespecialidades'
]

routes_getcidades = [
    '/getcidades'
]

routes_getconvenios = [
    '/getconvenios'
]

routes_realizarbusca = [
    '/realizarbusca'
]

try:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PACIENTES (Cpf VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Genre VARCHAR(50) NOT NULL, Email VARCHAR(255) NOT NULL, Convenio VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL); CREATE TABLE IF NOT EXISTS MEDICOS (Crm VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Address VARCHAR(50) NOT NULL, Cidade VARCHAR(255) NOT NULL, Estado VARCHAR(255) NOT NULL, Phone VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Especialidade VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL);CREATE TABLE IF NOT EXISTS MEDICOS_CONVENIOS (IDRelacao SERIAL PRIMARY KEY, Crm VARCHAR(255), IDConvenio INT NOT NULL);CREATE TABLE IF NOT EXISTS CONVENIOS (IDConvenio INT NOT NULL PRIMARY KEY, Convenio VARCHAR(255))")
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
        self.convenios_atendidos = None

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
        self.convenios_atendidos =  req_data['convenios_atendidos']
        
        

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
            
            for convenio in self.convenios_atendidos:
                print(int(convenio))
                cur.execute("INSERT INTO MEDICOS_CONVENIOS (Crm, IDConvenio) VALUES(%s,%s)",(self.crm, int(convenio)))
            
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

class GetEspecialidades(Resource):

    def get(self):
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT DISTINCT Especialidade FROM MEDICOS ORDER BY Especialidade")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}
        
class GetCidades(Resource):

    def get(self):
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT DISTINCT Cidade FROM MEDICOS ORDER BY Cidade")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}

class GetConvenios(Resource):

    def get(self):
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT DISTINCT Convenio FROM CONVENIOS ORDER BY Convenio")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}

class RealizarBusca(Resource):
    def __init__(self):
        self.nome = None
        self.cidade = None
        self.especialidade = None
        self.convenio = None
    
    def post(self):
        req_data = request.get_json() 
        self.nome = req_data['nome']
        self.cidade = req_data['cidade']
        self.especialidade = req_data['especialidade']
        self.convenio = req_data['convenio']
        
        filtros = ['nome','cidade','especialidade','convenio']
        filtrosRecebidos = [self.nome, self.cidade, self.especialidade,self.convenio]

        indices = [i for i, x in enumerate(filtrosRecebidos) if x == ""]
        for index in reversed(indices):
            filtros.pop(index)
            filtrosRecebidos.pop(index)

        if len(filtros) == 0:
            sWhere = ''
        elif len(filtrosRecebidos) == 1:
            sWhere = "WHERE MEDICOS."+filtros[0]+" LIKE '"+filtrosRecebidos[0]+"%'" 
        else:
            sWhere = "WHERE MEDICOS."+filtros[0]+" LIKE '"+filtrosRecebidos[0]+"%'" 
            for i in range(1, len(b)):
                sWhere += " AND MEDICOS."+filtros[i]+" LIKE '"+filtrosRecebidos[i]+"%'" 
        query = "SELECT MEDICOS.Nome, MEDICOS.Cidade, MEDICOS.Especialidade, CONVENIOS.Convenio FROM ((MEDICOS INNER JOIN MEDICOS_CONVENIOS ON MEDICOS.Crm = MEDICOS_CONVENIOS.Crm) INNER JOIN CONVENIOS ON MEDICOS_CONVENIOS.IDConvenio = CONVENIOS.IDConvenio) "+sWhere+" ORDER BY Especialidade, CONVENIOS.Convenio, Cidade, Nome"
        
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            cur.execute(query)
            query = cur.fetchall()
            conn.close()
            return query
            
        except Exception as e:
            print('FALHA AO REALIZAR BUSCA')
            print (str(e))
            return {'insertion error': str(e)}
        

api.add_resource(Cadastrar, *routes_cadastrar)
api.add_resource(Cadastrar_Medico, *routes_cadastrar_medico)
api.add_resource(Efetuar_Login, *routes_efetuar_login)
api.add_resource(GetEspecialidades, *routes_getespecialidades)
api.add_resource(GetCidades, *routes_getcidades)
api.add_resource(GetConvenios, *routes_getconvenios)
api.add_resource(RealizarBusca, *routes_realizarbusca)


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

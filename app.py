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

### Definição das rotas para o backend ###
routes_efetuar_login = [
    '/efetuar_login'
]

routes_cadastrar = [
    '/cadastrar'
]

routes_cadastrar_medico = [
    '/cadastrar_medico'
]

routes_getespecialidades = [
    '/getespecialidades'
]

routes_getcidades = [
    '/getcidades'
]

routes_gethorarios = [
    '/gethorarios'
]

routes_getconvenios = [
    '/getconvenios'
]

routes_realizarbusca = [
    '/realizarbusca'
]

routes_agendarconsulta = {
    '/agendarconsulta'
}

routes_getconsultas_medico = {
    '/getconsultas_medico'
}


### Cria as tabelas caso ainda não existam ###

try:
    conn = psycopg2.connect(
        host="ec2-34-225-167-77.compute-1.amazonaws.com",
        database="d76l1rkkcfbufc",
        user="imwtjcynbamcnr",
        password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
    )
    cur = conn.cursor()    
    cur.execute("""CREATE TABLE IF NOT EXISTS PACIENTES (Cpf VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Genre VARCHAR(50) NOT NULL, Email VARCHAR(255) NOT NULL, Convenio VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL); 
                   CREATE TABLE IF NOT EXISTS MEDICOS (Crm VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Address VARCHAR(50) NOT NULL, Cidade VARCHAR(255) NOT NULL, Estado VARCHAR(255) NOT NULL, Phone VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL, Especialidade VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL);
                   CREATE TABLE IF NOT EXISTS MEDICOS_CONVENIOS (IDRelacao SERIAL PRIMARY KEY, Crm VARCHAR(255), IDConvenio INT NOT NULL);
                   CREATE TABLE IF NOT EXISTS CONVENIOS (IDConvenio INT NOT NULL PRIMARY KEY, Convenio VARCHAR(255));
                   CREATE TABLE IF NOT EXISTS CONSULTAS (IDConsulta SERIAL NOT NULL PRIMARY KEY, Data VARCHAR(50), Horario VARCHAR (50), Cpf VARCHAR(255), Crm VARCHAR(255))""")
    conn.commit()
    conn.close()
except Exception as e:
        print({'Exception First:': str(e)})

class Cadastrar(Resource):
    """Metodo responsavel por fazer o cadastro dos pacientes"""

    def __init__(self):
        self.nome = None
        self.cpf = None
        self.birthday = None
        self.genre = None
        self.phone = None
        self.email = None
        self.convenio = None
        self.phone = None

    def post(self):
        req_data = request.get_json()  # obtendo os dados do model
        self.nome = req_data['nome']
        self.cpf = req_data['cpf']
        self.birthday = req_data['birthday']
        self.genre = req_data['genre']
        self.email = req_data['email']
        self.convenio = req_data['convenio']
        self.password = bcrypt.generate_password_hash(req_data['password']).decode('utf-8')
        self.phone = req_data['phone']
        
        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO PACIENTES (Nome, Cpf, Birthday, Genre, Email, Convenio, Password, Phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                            (self.nome, self.cpf, self.birthday, self.genre, self.email, self.convenio, self.password, self.phone))
            conn.commit()
            conn.close()
            return {'insertion': 'ok'}
        except Exception as e:
            print (str(e))
            return {'insertion error': str(e)}

class Cadastrar_Medico(Resource):
    """Metodo responsavel por fazer o cadastro dos medicos"""

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
                cur.execute("INSERT INTO MEDICOS_CONVENIOS (Crm, IDConvenio) VALUES(%s,%s)",(self.crm, int(convenio)))
            
            conn.commit()
            conn.close()
            return {'insertion': 'ok'}
        except Exception as e:
            print (str(e))
            return {'insertion error': str(e)}

class Efetuar_Login(Resource):
    """Metodo que valida usuario e senha para fazer o login"""

    def __init__(self):
        self.username = None
        self.password = None

    def post(self):
        req_data = request.get_json()
        self.user = req_data['user']
        self.password = req_data['password']#.encode('utf-8')
        self.tipo_usuario = req_data['tipo_usuario']
        
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

        if self.tipo_usuario == "paciente":
            df_password =  pd.read_sql_query("SELECT password, nome, cpf as id FROM PACIENTES WHERE Cpf = '"+self.user+"'", conn)
        elif self.tipo_usuario == "medico":
            df_password =  pd.read_sql_query("SELECT password, nome, crm as id FROM MEDICOS WHERE Crm = '"+self.user+"'", conn)
        
        conn.close()

        if(len(df_password) == 0):
            return 'Usuário não cadastrado'
        else:
            bd_password = df_password.to_dict()["password"][0]
            if(bcrypt.check_password_hash(bd_password, self.password)):
                return {"login": "ok", "nome": df_password.to_dict()["nome"][0], "id": df_password.to_dict()["id"][0]}
            else:
                return {"login": "bad password"}

class GetEspecialidades(Resource):
    """Metodo que lista as especialidades cadastradas no banco para preenchimento dos elementos do front"""

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
    """Metodo que lista as cidades cadastradas no banco para preenchimento dos elementos do front"""
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
    """Metodo que lista os convenios cadastrados no banco para preenchimento dos elementos do front"""
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

class GetHorarios(Resource):
    """Metodo que lista os horarios ocupados para medico e dia """

    def __init__(self):
        self.data = None
        self.crm = None

    def post(self):
        req_data = request.get_json() 
        self.data = req_data['data']
        self.crm = req_data['crm']

        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT Horario FROM CONSULTAS WHERE Data = '"+self.data+"' AND Crm = '"+self.crm+"' ORDER BY Horario")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}

class AgendarConsulta(Resource):
    """Metodo que faz o agendamento da consulta de um paciente com um medico em um dia e horario"""
    def __init__(self):
        self.data = None
        self.horario = None
        self.cpf = None
        self.crm = None

    def post(self):
        req_data = request.get_json()
        self.data = req_data['data']
        self.horario = req_data['horario']
        self.cpf = req_data['cpf']
        self.crm = req_data['crm']

        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO CONSULTAS (data, horario, cpf, crm) VALUES (%s,%s,%s,%s)",
                                            (self.data, self.horario, self.cpf, self.crm))
            conn.commit()
            conn.close()
            return {'insertion': 'ok'}
        except Exception as e:
            print (str(e))
            return {'insertion error': str(e)}

class RealizarBusca(Resource):
    """Busca os medicos cadastrados no banco com base nos filtros passados pelo front"""
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
        
        try:
            conv = lambda i : i or ''
            filtrosRecebidos = [conv(i) for i in filtrosRecebidos]
            indices = [i for i, x in enumerate(filtrosRecebidos) if x == ""]
            for index in reversed(indices):
                filtros.pop(index)
                filtrosRecebidos.pop(index)

            if len(filtros) == 0:
                sWhere = ''
            elif len(filtrosRecebidos) == 1:
                sWhere = "WHERE UPPER(MEDICOS."+filtros[0]+") LIKE UPPER('%"+filtrosRecebidos[0]+"%')" 
            else:
                sWhere = "WHERE MEDICOS."+filtros[0]+" LIKE '"+filtrosRecebidos[0]+"%'" 
                for i in range(1, len(filtrosRecebidos)):
                    sWhere += " AND UPPER(MEDICOS."+filtros[i]+") LIKE UPPER('"+filtrosRecebidos[i]+"%')" 
            
            sWhere = sWhere.replace("UPPER(MEDICOS.convenio)","CONVENIOS.Convenio")
            
            query = "SELECT MEDICOS.Crm, MEDICOS.Nome, MEDICOS.Cidade, MEDICOS.Estado, MEDICOS.Especialidade, MEDICOS.Address, STRING_AGG(Convenio, ' - ') Convenio_list FROM ((MEDICOS INNER JOIN MEDICOS_CONVENIOS ON MEDICOS.Crm = MEDICOS_CONVENIOS.Crm) INNER JOIN CONVENIOS ON MEDICOS_CONVENIOS.IDConvenio = CONVENIOS.IDConvenio) "+sWhere+" GROUP BY MEDICOS.Crm, MEDICOS.Nome, MEDICOS.Cidade, MEDICOS.Estado, MEDICOS.Especialidade, MEDICOS.Address ORDER BY Especialidade, Cidade, Nome"
            #print(query)
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
            if query == []:
                return([('-1', 'Não foi possível encontrar um médico ou clínica.', '', '', '', '', 'Por gentileza, revise os filtros utilizados.')])
            else:
                return query
            
        except Exception as e:
            print (str(e))
            return {'insertion error': str(e)}

class GetConsultas_Medico(Resource):
    def __init__(self):
        self.data = None
        self.crm = None

    def post(self):
        req_data = request.get_json() 
        self.data = req_data['data']
        self.crm = req_data['crm']

        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT PACIENTES.Nome, PACIENTES.Cpf, PACIENTES.Birthday, CONSULTAS.Horario, PACIENTES.Convenio, PACIENTES.Phone FROM CONSULTAS INNER JOIN PACIENTES ON CONSULTAS.Cpf = PACIENTES.Cpf WHERE Data = '"+self.data+"' AND Crm = '"+self.crm+"' ORDER BY Horario")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}

class GetConsultas_Paciente(Resource):
    def __init__(self):
        self.data = None
        self.Cpf = None

    def post(self):
        req_data = request.get_json() 
        self.data = req_data['data']
        self.cpf = req_data['cpf']

        try:
            conn = psycopg2.connect(
                host="ec2-34-225-167-77.compute-1.amazonaws.com",
                database="d76l1rkkcfbufc",
                user="imwtjcynbamcnr",
                password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT PACIENTES.Convenio, CONSULTAS.Horario, MEDICOS.Address AS Endereco, MEDICOS.Cidade, MEDICOS.Estado, MEDICOS.Phone AS Telefone, MEDICOS.Especialidade FROM ((CONSULTAS INNER JOIN PACIENTES ON CONSULTAS.Cpf = PACIENTES.Cpf) INNER JOIN MEDICOS ON CONSULTAS.Crm = MEDICOS.Crm WHERE Data = '"+self.data+"' AND Cpf = '"+self.cpf+"' ORDER BY Horario)")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}
        

### Associa as rotas com os métodos criados ###
api.add_resource(Cadastrar, *routes_cadastrar)
api.add_resource(Cadastrar_Medico, *routes_cadastrar_medico)
api.add_resource(Efetuar_Login, *routes_efetuar_login)
api.add_resource(GetEspecialidades, *routes_getespecialidades)
api.add_resource(GetCidades, *routes_getcidades)
api.add_resource(GetConvenios, *routes_getconvenios)
api.add_resource(GetHorarios, *routes_gethorarios)
api.add_resource(RealizarBusca, *routes_realizarbusca)
api.add_resource(AgendarConsulta, *routes_agendarconsulta)
api.add_resource(GetConsultas_Medico, *routes_getconsultas_medico)


### Define as rotas e carregamento das páginas de front-end ###
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

@app.route('/agenda', methods=['GET', 'POST'])
def agenda():
    return render_template('agenda.html')

#Inicia o aplicativo
if __name__ == '__main__':
    app.run()

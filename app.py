import psycopg2
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse, request
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

conn = psycopg2.connect(
    host="ec2-34-225-167-77.compute-1.amazonaws.com",
    database="d76l1rkkcfbufc",
    user="imwtjcynbamcnr",
    password="56f0769106cdcc30822e56e90d56828ccc1bc032f513e37698eede66a48cf1b9",
)

routes_cadastrar = [
    '/cadastrar'
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
	cur.execute("CREATE TABLE IF NOT EXISTS PACIENTES (Cpf VARCHAR(255) PRIMARY KEY, Nome VARCHAR(255), Birthday VARCHAR(50), Genre VARCHAR(50) NOT NULL, Email VARCHAR(255) NOT NULL, Convenio VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL);")
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
        print(req_data)
        self.nome = req_data['nome']
        self.cpf = req_data['cpf']
        self.birthday = req_data['birthday']
        self.genre = req_data['genre']
        self.email = req_data['email']
        self.convenio = req_data['convenio']
        self.password = req_data['password']

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


class Delete(Resource):
    """docstring for Insert"""

    def __init__(self):
        self.time = None

    def post(self):
        req_data = request.get_json()  # obtendo os dados do model
        self.time = req_data['time']
        print(req_data)

        try:
            conn = psycopg2.connect(
                host="ec2-54-197-48-79.compute-1.amazonaws.com",
                database="dnjubkir1nj8r",
                user="vlaisatyrcsqmw",
                password="f84aaf47723cddeb2bddb79c299fa23c4b8ddfbd26ff0eb6144169f30c4dc424",
            )
            cur = conn.cursor()
            cur.execute("DELETE FROM lights WHERE time = %s;", (self.time,))
            conn.commit()
            conn.close()
            return {'deletion': 'ok'}
        except Exception as e:
            return {'deletion error': str(e)}

"""
class Get_schedule(Resource):

    def get(self):
        try:
            conn = psycopg2.connect(
                host="ec2-54-197-48-79.compute-1.amazonaws.com",
                database="dnjubkir1nj8r",
                user="vlaisatyrcsqmw",
                password="f84aaf47723cddeb2bddb79c299fa23c4b8ddfbd26ff0eb6144169f30c4dc424",
            )
            cur = conn.cursor()
            query = cur.execute("SELECT * FROM lights ORDER BY time")
            query = cur.fetchall()
            conn.close()
            return query
        except Exception as e:
            print(e)
            return {'selection error': str(e)}

class Get_next_schedule(Resource):

    def get(self, time):
        self.time = str(time).replace('h', ':')
        print(self.time)


        try:
            conn = psycopg2.connect(
                host="ec2-54-197-48-79.compute-1.amazonaws.com",
                database="dnjubkir1nj8r",
                user="vlaisatyrcsqmw",
                password="f84aaf47723cddeb2bddb79c299fa23c4b8ddfbd26ff0eb6144169f30c4dc424",
            )
            cur = conn.cursor()
            query = cur.execute("WITH fq as (SELECT * FROM(SELECT * ,LEAD(time, 1, (SElECT time FROM lights ORDER BY time LIMIT 1)) OVER(ORDER BY time) as Next_Time FROM lights ORDER BY time DESC) as aux WHERE time <= %s LIMIT 1) SELECT * FROM fq UNION ALL SELECT * , LEAD(time, 1, (SElECT time FROM lights ORDER BY time LIMIT 1)) OVER(ORDER BY time) as Next_Time FROM lights WHERE NOT EXISTS (SELECT * FROM fq) ORDER BY time LIMIT 1;", (self.time,))
            query = cur.fetchall()[0]
            conn.close()
            return "{time:"+query[0]+"&value:"+str(map(query[1], 0, 100, 0, 255))+"-"+str(map(query[2], 0, 100, 0, 255))+"-"+str(map(query[3], 0, 100, 0, 255))+"&next_time:"+query[4]+"}"
        except Exception as e:
            print(e)
            return {'Exception' : str(e)}

def map(x, in_min, in_max, out_min, out_max):
    return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
"""

api.add_resource(Cadastrar, *routes_cadastrar)
api.add_resource(Delete, *routes_delete)

"""
api.add_resource(Get_schedule, *routes_select_all)
api.add_resource(Get_next_schedule, *routes_next_schedule)
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('cadastro.html')


@app.route('/cadastro-medico')
def cadastro_medico():
    return render_template('cadastro-medico.html')


@app.route('/lights')
def lights():
    return render_template('lights.html')


@app.route('/temp')
def temp():
    return render_template('temp.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    #logging.basicConfig(filename='logs/flask_logging.log', level=logging.DEBUG)
    # serve(app)#, host='0.0.0.0', port=7000
    app.run()

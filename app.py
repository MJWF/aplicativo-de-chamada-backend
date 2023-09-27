### pip install Flask
### pip install mysql.connector

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'database-project.cayd3qorxcai.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '145acf1435'
app.config['MYSQL_DB'] = 'PROJETOSCRUM'

db = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1> Olá, Mundo! <h1>'


#TROCAR DE GET PARA POST
@app.route('/cadastro', methods=['GET'])
def cadastro():
    mycursor = db.cursor()
    sql_command = "CREATE TABLE teste(NOME VARCHAR(255))"
    
    mycursor.execute(sql_command,)
    db.commit()
    return 'teste de database'




if __name__ == '__main__':
    app.run()
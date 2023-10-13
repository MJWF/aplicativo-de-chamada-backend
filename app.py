### pip install Flask
### pip install mysql.connector

from flask import Flask, request, jsonify
import mysql.connector
import random

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

#Rota padrão da aplicação
@app.route('/')
def hello_world():
    return '<h1> Olá, Mundo! <h1>'


#Rota para fazer o cadastro dos usuários de forma geral
@app.route('/cadastro', methods=['POST'])
def cadastro():

    # Recebendo os parâmetros do frontend
    # Parâmetros devem ser lido utilizando request.form
    
    email_usuario = request.form['email']
    password_usuario = request.form['password']
    nome_usuario = request.form['nome']
    tipo_usuario = request.form['tipo_usuario']
    

    # Inicializando parâmetros do banco de dados e passando para tabela usuario (padrão)
    # Comandos para inserção no banco de dados
    mycursor = db.cursor()
    sql_command_for_database = "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s)"
    values_for_database = (nome_usuario, email_usuario, password_usuario, tipo_usuario)
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'cadastro': 'error'})
    db.commit()

    # Inicializando parâmetros do banco de dados e passando para tabela
    # de professor ou aluno.
    # Comandos para inserção no banco de dados
    mycursor = db.cursor()
    values_for_database = (nome_usuario, email_usuario, password_usuario)
    
    if(tipo_usuario == 'professor'):
        sql_command_for_database = "INSERT INTO professor (nome, email, senha) VALUES (%s, %s, %s)"
    elif(tipo_usuario == 'aluno'):
        sql_command_for_database = "INSERT INTO aluno (Nome, Email, Senha) VALUES (%s, %s, %s)"

    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'cadastro': 'error'})    
            
    db.commit()
    return jsonify({'cadastro': 'Cadastrado com sucesso!'})
    

@app.route('/login', methods=['POST'])
def login():

    # Recebendo email e senha do usuário
    email = request.form['email']
    password = request.form['password']
    
    # Inicialiazação dos parâmetros para o banco de dados
    mycursor = db.cursor()

    # Procura no banco de dados um usuário com o email que foi passado
    sql_command = "SELECT Email, Senha FROM usuario Where Email = %s"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()

    # Verefica se o retorno não foi nulo e se a senha inserida é igual a cadastrada
    if email_res is not None:
        senha_encontrada = email_res[1] #posicao da coluna da tabela do banco de dado
        if senha_encontrada == password:

            print("Logado com sucesso")
            sql_command = "SELECT Tipo_usuario from usuario WHERE Email = %s"
            value = (email,)
            mycursor.execute(sql_command, value)
            tipo_user = mycursor.fetchone()

            return jsonify({'acesso': 'OK', 'Tipo_aluno': tipo_user, 'email': email})
        else:
            print("Senha incorreta")
    else:
        print("Email nao encontrado")

    return jsonify({'acesso': 'false', 'Tipo_aluno': 'Null'})



@app.route('/Registrar_materia', methods=['POST'])
def Registrar_materia():
    Nome_materia = request.form['Nome_materia']
    Nome_professor = request.form['Nome_professor']
    Ementa = request.form['Ementa']
    #Gerar o codigo da materia pelo back (prefixo 23 (2023))
    codigo = random.randint(230000, 239999)
    #Insere na tabela Materia
    mycursor = db.cursor()
    sql_command_for_database = "INSERT INTO Materia (Codigo, Nome, Ementa) VALUES (%s, %s, %s)"
    values_for_database = (codigo, Nome_materia, Ementa)
    mycursor.execute(sql_command_for_database, values_for_database)

    #Insere na tabela Materia x Professor
    sql_command_for_database = "INSERT INTO Materia_Professor (Nome_Professor, Nome_Materia) VALUES (%s, %s)"
    values_for_database = (Nome_professor, Nome_materia)
    mycursor.execute(sql_command_for_database, values_for_database)

    db.commit()


    return jsonify({'Status': 'Materia criada com sucesso!!!'})
if __name__ == '__main__':
    app.run()
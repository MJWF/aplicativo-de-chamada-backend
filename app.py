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
    database=app.config['MYSQL_DB'],
    charset="utf8"
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
    sql_command_for_database = "INSERT INTO usuario (nome, email, senha, tipo_usuario) VALUES (%s, %s, %s, %s);"
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
        sql_command_for_database = "INSERT INTO professor (nome, email, senha) VALUES (%s, %s, %s);"
    elif(tipo_usuario == 'aluno'):
        sql_command_for_database = "INSERT INTO aluno (Nome, Email, Senha, Representante) VALUES (%s, %s, %s, False);"

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
    sql_command = "SELECT Email, Senha FROM usuario Where Email = %s;"
    value = (email,)
    mycursor.execute(sql_command, value)
    email_res = mycursor.fetchone()

    # Verefica se o retorno não foi nulo e se a senha inserida é igual a cadastrada
    if email_res is not None:
        senha_encontrada = email_res[1] #posicao da coluna da tabela do banco de dado
        if senha_encontrada == password:

            print("Logado com sucesso")
            sql_command = "SELECT Tipo_usuario from usuario WHERE Email = %s;"
            value = (email,)
            mycursor.execute(sql_command, value)
            tipo_user = mycursor.fetchone()

            return jsonify({'acesso': 'OK', 'Tipo_aluno': tipo_user[0], 'email': email})
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
    sql_command_for_database = "INSERT INTO Materia (Codigo, Nome, Ementa, Aulas_Dadas) VALUES (%s, %s, %s, 0);"
    values_for_database = (codigo, Nome_materia, Ementa)
    mycursor.execute(sql_command_for_database, values_for_database)

    #Insere na tabela Materia x Professor
    sql_command_for_database = "INSERT INTO Materia_Professor (Nome_Professor, Nome_Materia) VALUES (%s, %s);"
    values_for_database = (Nome_professor, Nome_materia)
    mycursor.execute(sql_command_for_database, values_for_database)

    db.commit()

    return jsonify({'Status': 'Materia criada com sucesso!!!'})




@app.route('/ReturnInfoGerais', methods=['POST'])
def ReturnInfoGerais():
    email = request.form['email']

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT Tipo_usuario FROM usuario WHERE Email = %s;"
    values_for_database = (email,)

    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'ReturnInfoGerais': 'error'})
    
    user_type = mycursor.fetchone()
    print(user_type)
    if user_type is not None:
        if(user_type[0] == 'aluno'):
            sql_command_for_database = "SELECT * FROM aluno WHERE Email = %s;"
        elif(user_type[0] == 'professor'):
            sql_command_for_database = "SELECT * FROM professor WHERE Email = %s;"
        elif(user_type[0] == 'admin'):
            sql_command_for_database = "SELECT * FROM Admin WHERE Email = %s;"

        try:
            mycursor.execute(sql_command_for_database, values_for_database)
        except:
            return jsonify({'ReturnInfoGerais': 'error'})
        
        user_data = mycursor.fetchone()
        print(user_data)
        if user_data is not None:
            user_RegisterNumber = str(user_data[0])
            user_nome = user_data[1]
            user_email = user_data[2]
        
            return jsonify({'user_RegisterNumber': user_RegisterNumber, 'user_nome': user_nome, 'user_email': user_email})
        else:
            return jsonify({'user_RegisterNumber': "NULL", 'user_nome': "NULL", 'user_email': "NULL"})
    else:
        return jsonify({'ReturnInfoGerais': 'Null'})


@app.route('/return_aluno', methods=['POST'])
def return_aluno():

    email = request.form['email']
    #email = "janedoe@gmail.com" teste de execução

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT * FROM aluno WHERE Email = %s;"
    values_for_database = (email,)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'return_aluno': 'error'})

    aluno_data = mycursor.fetchone()

    # parâmetros separados pra retornar para o backend
    aluno_RA = aluno_data[0]
    aluno_nome = aluno_data[1]
    aluno_email = aluno_data[2]

    return jsonify({'aluno_RA': aluno_RA, 'aluno_nome': aluno_nome, 'aluno_email': aluno_email})


@app.route('/Materia_Aluno', methods=['POST'])
def Materia_Aluno():

    Nome_Aluno = request.form['Nome']
    Nome_Materia = request.form['Materia']

    #Nome_Aluno = 'Rafael Sato'
    #Nome_Materia = 'calculo'

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "INSERT INTO Materia_Aluno (Nome_Aluno, Nome_Materia, Frequencia) VALUES (%s, %s, 0);"
    values_for_database = (Nome_Aluno, Nome_Materia)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'Materia_Aluno': 'error'})

    db.commit()

    return jsonify({'status':'O aluno foi inscrito com sucesso na materia'})


@app.route('/return_professor', methods=['POST'])
def return_professor():

    Email = request.form['Email']

    #Email = "professor@gmail.com"

    # Inicialização do cursor
    mycursor = db.cursor()
    # Comando e valores para consultar o banco de dados
    sql_command_for_database = "SELECT * FROM professor WHERE Email = %s;"
    values_for_database = (Email,)

    # Tenta executar o camando no banco de dados para fazer a consulta
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'return_professor': 'error'})

    professor_data = mycursor.fetchone()

    # parâmetros separados pra retornar para o backend
    professor_RP = professor_data[0]
    professor_nome = professor_data[1]
    professor_email = professor_data[2]

    return jsonify({'professor_RP': professor_RP, 'professor_nome': professor_nome, 'professor_email': professor_email})


@app.route('/return_materias', methods=['POST'])
def return_materias():

    mycursor = db.cursor()
    sql_command_for_database = "SELECT * FROM Materia"

    mycursor.execute(sql_command_for_database)

    materias_data = mycursor.fetchall()
    size = len(materias_data)

    data = []

    for i in range(size):
        materias = {
        'codigo_materias': str(materias_data[i][0]),
        'nome_materias': materias_data[i][1],
        'ementa_materias': materias_data[i][2]
        }
        data.append(materias)

    return jsonify(data)


@app.route('/verificar_inscricao', methods=['POST'])
def verificar_inscricao():

    Email = request.form['Email']
    ID_materia = request.form['ID_materia']

    mycursor = db.cursor()
    sql_command_for_database = "SELECT * FROM Materia_Aluno WHERE Nome_Aluno = %s and Nome_Materia = %s"
    values_for_database = (Email, ID_materia)
    try:
        mycursor.execute(sql_command_for_database, values_for_database)
    except:
        return jsonify({'verificar_inscricao': 'Error'})

    response = mycursor.fetchone()

    if response is not None:
        return jsonify('True')
    else:
        return jsonify('False')
    

@app.route('/retorna_materias_professor', methods=['POST'])
def retorna_materias_professor():

    email = request.form['Email']

    mycursor = db.cursor()

    command = "SELECT Nome_Materia FROM Materia_Professor WHERE Nome_Professor = %s"
    values = (email,)

    mycursor.execute(command, values)

    response = mycursor.fetchall()

    size = len(response)
    data = []

    for i in range(size):
        materias_retornadas = {
        'nome_materia': str(response[i][0]),
        }
        data.append(materias_retornadas)

    print(data)
    return jsonify(data)
    
@app.route('/return_alunos_materias', methods=['POST'])
def return_alunos_materias():

    materia = request.form['materia_escolhida']

    mycursor = db.cursor()
    sql_command_for_database = "SELECT Nome FROM aluno WHERE Email IN (SELECT Nome_Aluno FROM Materia_Aluno WHERE Nome_Materia = (SELECT Codigo FROM Materia WHERE Nome = %s))"

    values = (materia,)
    mycursor.execute(sql_command_for_database, values)

    alunos_materias_data = mycursor.fetchall()

    data = []

    for aluno_materia in alunos_materias_data:
        aluno = {
            'nome_aluno': aluno_materia[0],
        }

        data.append(aluno)

    return jsonify(data)

@app.route('/return_presenca_pela_materia', methods=['POST'])
def return_presenca_pela_materia():

    #Recebe os parâmetros do frontend
    # materia precisa ser o código dela !!!!!
    materia = request.form['materia_escolhida']
    #materia = "Portugues"

    # Seleciona o total de aulas daquela matéria
    mycursor = db.cursor()
    sql_command_for_database = "SELECT Aulas_Dadas, Codigo FROM Materia where Nome = %s" 
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)
    sql_response = mycursor.fetchone()

    aulas_dadas_materia = sql_response[0]
    Codigo_Materia = sql_response[1]

    # Nesse select eu juntei as tabelas aluno e materia_aluno para conseguir pegar as informações certas para retorno
    # Deixei ordenado de ordem alfabética
    mycursor = db.cursor()
    sql_command_for_database = "SELECT Nome, RA, Frequencia, representante FROM aluno LEFT JOIN Materia_Aluno ON aluno.Email = Materia_Aluno.Nome_Aluno Where Nome_Materia = %s order by Nome;" 
    values = (int(Codigo_Materia),)
    mycursor.execute(sql_command_for_database, values)
    sql_response = mycursor.fetchall()

    # Fiz o cálculo da frequencia em poncentagem e depois passei para string
    for i in range(len(sql_response)):
        # Certifique-se de que o terceiro elemento não seja zero para evitar divisão por zero
        if aulas_dadas_materia != 0:
            # Atualize o terceiro elemento
            sql_response[i] = list(sql_response[i]) 
            sql_response[i][2] =  str(round((sql_response[i][2] / aulas_dadas_materia) * 100)) + "%" # Divisão
            sql_response[i] = tuple(sql_response[i])
        else:  
            sql_response[i] = list(sql_response[i])    
            sql_response[i][2] = "100%"  # Divisão
            sql_response[i] = tuple(sql_response[i])

    #print(sql_response)
    
    #jsonify contém Nome, Ra, Frequencia(%) nessa ordem

    mycursor = db.cursor()
    sql_command_for_database = "SELECT Nome FROM aluno WHERE Email IN(SELECT EmailAluno FROM Representante WHERE CodigoMateria = (SELECT Codigo FROM Materia WHERE Nome = %s));"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)
    representantes = mycursor.fetchall()
    representantes = list(representantes)

    lista_representantes = []
    for i in range(len(representantes)):
        lista_representantes.append(representantes[i][0])
    
    for i in range(len(sql_response)):
        print(lista_representantes)
        print(sql_response[i][0])

        if sql_response[i][0] in lista_representantes:
            
            sql_response[i] = list(sql_response[i]) 
            sql_response[i][3] =  "True"
            sql_response[i] = tuple(sql_response[i])
        else:
            sql_response[i] = list(sql_response[i]) 
            sql_response[i][3] =  "False"
            sql_response[i] = tuple(sql_response[i])

    return jsonify(sql_response)

@app.route('/fazer_chamada', methods=['POST'])
def fazer_chamada():
    materia = request.form['materia_escolhida']
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    
    codigo_chamada = random.randint(230000, 239999)
    codigo_chamada_str = str(codigo_chamada)
    mycursor = db.cursor()

    sql_command_for_database = "UPDATE Materia SET Aulas_Dadas = Aulas_Dadas + 1, Codigo_da_Chamada = %s WHERE Nome = %s;" 
    values = (codigo_chamada_str, materia)
    mycursor.execute(sql_command_for_database, values)
    db.commit()

    sql_command_for_database = "SELECT Codigo FROM Materia WHERE Nome = %s;"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)

    codigo_da_materia = mycursor.fetchone() #nao sei se funciona, qualquer coisa deixa que nem o de cima
    codigo_da_materia = str(codigo_da_materia[0])

    sql_command_for_database = "INSERT INTO Aulas_dadas VALUES (%s, %s, %s, %s, 0);"
    values = (codigo_da_materia, codigo_chamada_str, descricao, titulo)
    mycursor.execute(sql_command_for_database, values)

    try:  
        db.commit()
    except:
        return jsonify({'realizar_chamada': 'Error'})
    
    return jsonify({'codigo_chamada': codigo_chamada_str})

@app.route('/return_materias_inscritas_do_aluno', methods=['POST'])
def return_alunos_materias_inscritas_do_aluno():

    email = request.form['email']

    mycursor = db.cursor()
    sql_command_for_database = "SELECT Nome FROM Materia WHERE Codigo IN (SELECT Nome_Materia FROM Materia_Aluno WHERE Nome_Aluno = %s);"

    values = (email,)
    mycursor.execute(sql_command_for_database, values)

    materias_do_aluno= mycursor.fetchall()

    data = []

    for materia_aluno in materias_do_aluno:
        materias = {
            'nome_materia': materia_aluno[0],
        }

        data.append(materias)

    return jsonify(data)

@app.route('/verificar_codigo_inserido_pelo_aluno', methods=['POST'])
def verificar_codigo_inserido_pelo_aluno():

    email = request.form['email']
    code_from_user = request.form['code']
    materia = request.form['materia']

    # email = "janedoe@gmail.com"
    # code_from_user = "238261"
    # materia = "Projetos"

    mycursor = db.cursor()
    sql_command_for_database = "SELECT Codigo_da_chamada, Codigo FROM Materia WHERE Nome = %s"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)

    sql_response = mycursor.fetchone()
    code_from_discipline = sql_response[0]
    discipline_code = sql_response[1]

    if code_from_user == code_from_discipline:
        sql_command_for_database = "UPDATE Materia_Aluno SET Frequencia = Frequencia + 1 WHERE Nome_Aluno = %s AND Nome_Materia = %s"
        values = (email, discipline_code)
        mycursor.execute(sql_command_for_database, values)
        db.commit()


        #Alteração feitas para organizar as aulas
        mycursor = db.cursor()
        sql_command_for_database = "INSERT INTO Aulas_com_Presenca (Codigo_Usuario, Codigo_Presenca, Codigo_Materia) VALUES (%s, %s, %s);"
        values = (email, code_from_discipline, discipline_code)
        mycursor.execute(sql_command_for_database, values)
        db.commit()
        return jsonify({'presenca': "OK"})

    else:
        return jsonify({'presenca': "Erro"})
    
    

@app.route('/retornar_presenca_para_aluno_por_materia', methods=['POST'])
def retornar_presenca_para_aluno_por_materia():

    email = request.form['email']
    materia = request.form['materia']

    mycursor = db.cursor()
    sql_command_for_database = "SELECT Frequencia FROM Materia_Aluno WHERE Nome_Aluno = %s AND Nome_Materia = (SELECT Codigo FROM Materia WHERE Nome = %s) "
    values = (email,materia)
    mycursor.execute(sql_command_for_database, values)

    sql_response = mycursor.fetchone()
    user_frequency = sql_response[0]

    sql_command_for_database = "SELECT Aulas_Dadas FROM Materia WHERE Nome = %s"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)

    sql_frequency_response = mycursor.fetchone()
    given_classes = sql_frequency_response[0]

    if given_classes == 0:
        frequecy = "100%"

    else:
        frequecy = str(round(((int(user_frequency) / int(given_classes))) * 100)) + "%"
    return jsonify(frequecy)



@app.route('/presenca_coletiva', methods=['POST'])
def presenca_coletiva():

    nomeMateria = request.form['materia']
    titulo = request.form['titulo']
    descricao = request.form['descricao']

    codigo_chamada = random.randint(230000, 239999)
    codigo_chamada_str = str(codigo_chamada)

    try:
        mycursor = db.cursor()
        sqlCommand = "UPDATE Materia_Aluno SET Frequencia = Frequencia + 1 WHERE Nome_Materia IN (SELECT Codigo FROM Materia WHERE Nome = %s);"
        valuesDatabase = (nomeMateria,)
        mycursor.execute(sqlCommand, valuesDatabase)

    except: 
        return jsonify({'presenca_coletiva': "error"})

    try:
        sqlCommand = "UPDATE Materia SET Aulas_Dadas = (Aulas_Dadas + 1) WHERE Nome = %s;"
        valuesDatabase = (nomeMateria,)
        mycursor.execute(sqlCommand, valuesDatabase)
        db.commit()

    except: 
        return jsonify({'presenca_coletiva': "error"})

    try:
        sql_command_for_database = "SELECT Codigo FROM Materia WHERE Nome = %s;"
        values = (nomeMateria,)
        mycursor.execute(sql_command_for_database, values)
    except: 
        return jsonify({'presenca_coletiva': "error"})
    
    codigo_da_materia = mycursor.fetchone()
    codigo_da_materia = str(codigo_da_materia[0])

    sql_command_for_database = "INSERT INTO Aulas_dadas VALUES (%s, %s, %s, %s, 1);"
    values = (codigo_da_materia, codigo_chamada_str, descricao, titulo)
    
    try:
        mycursor.execute(sql_command_for_database, values)
    except:
        return jsonify({'presenca_coletiva': "error"})

    return jsonify({'presenca_coletiva': "OK"})


@app.route('/representante', methods=['POST'])
def representante():

    nomeAluno = request.form['Nome']
    nomeMateria = request.form['Materia']
    
    mycursor = db.cursor()
    sqlCommand = "SELECT * FROM Representante WHERE CodigoMateria = (SELECT Codigo FROM Materia WHERE Nome = %s) AND EmailAluno = (SELECT Email FROM aluno WHERE Nome = %s);"
    valuesDatabase = (nomeAluno, nomeMateria)

    mycursor.execute(sqlCommand, valuesDatabase)

    temEsseAluno = mycursor.fetchone()

    if temEsseAluno is None:
        mycursor = db.cursor()
        sqlCommand = "SELECT Email FROM aluno WHERE Nome = %s;"
        valuesDatabase = (nomeAluno,)
        mycursor.execute(sqlCommand, valuesDatabase)

        
        SqlResponse = mycursor.fetchone()
        EmailAluno = SqlResponse[0]

        mycursor = db.cursor()
        sqlCommand = "SELECT Codigo FROM Materia WHERE Nome = %s;"
        valuesDatabase = (nomeMateria,)
        mycursor.execute(sqlCommand, valuesDatabase)
        
        SqlResponse = mycursor.fetchone()
        CodigoMateia = SqlResponse[0]

        mycursor = db.cursor()
        sqlCommand = "INSERT INTO Representante (EmailAluno, CodigoMateria) VALUES (%s, %s);"
        valuesDatabase = (EmailAluno, CodigoMateia)
        try:
            mycursor.execute(sqlCommand, valuesDatabase)
            db.commit()
            return jsonify({'representante': "True"})
        
        except:
            return jsonify({'representante': "error"})
        
    else:
       return jsonify({'representante': "False"}) 



@app.route('/remover_representante', methods=['POST'])
def remover_representante():

    nomeAluno = request.form['Nome']
    nomeMateria = request.form['Materia']

    mycursor = db.cursor()
    sqlCommand = "SELECT * FROM Representante WHERE EmailAluno = (SELECT Email FROM aluno WHERE Nome = %s) AND CodigoMateria = (SELECT Codigo FROM Materia WHERE Nome = %s);"
    valuesDatabase = (nomeAluno, nomeMateria)
    mycursor.execute(sqlCommand, valuesDatabase)

    temEsseAluno = mycursor.fetchone()
    print(temEsseAluno)
    if temEsseAluno is not None:

        mycursor = db.cursor()
        sqlCommand = "DELETE FROM Representante WHERE EmailAluno = (SELECT Email FROM aluno WHERE Nome = %s) AND CodigoMateria  = (SELECT Codigo FROM Materia WHERE Nome = %s);"
        valuesDatabase = (nomeAluno, nomeMateria)
        try:
            mycursor.execute(sqlCommand, valuesDatabase)
            db.commit()
            return jsonify({'representante': "True"})
        
        except:
            return jsonify({'representante': "error"})
        
    else:
        return jsonify({'representante': "False"}) 


@app.route('/returnAulasPresentes', methods=['POST'])
def returnAulasPresentes():

    emailAluno = request.form['email']
    nomeMateria = request.form['materia']

    mycursor = db.cursor()
    sqlCommand = "SELECT * FROM Aulas_dadas WHERE codigo_presenca IN (SELECT Codigo_Presenca FROM Aulas_com_Presenca WHERE Codigo_Usuario = %s AND Codigo_Materia IN (SELECT Codigo FROM Materia WHERE Nome = %s));"
    valuesDatabase = (emailAluno, nomeMateria)

    mycursor.execute(sqlCommand, valuesDatabase)
    sql_response = mycursor.fetchall()

    data = []

    for linha in sql_response:
        AulasPresenca = {
            'Titulo': linha[3],
            'CodigoPresenca': linha[1],
            'Descricao': linha[2]
        }

        data.append(AulasPresenca)
    print(data)

    try:
        sqlCommand = "SELECT * FROM Aulas_dadas WHERE coletiva = 1 AND codigo_materia = (SELECT Codigo FROM Materia WHERE Nome = %s);"
        valuesDatabase = (nomeMateria,)
        mycursor.execute(sqlCommand, valuesDatabase)
        sql_response = mycursor.fetchall()

        for linha in sql_response:
            AulasPresenca = {
                'Titulo': linha[3],
                'CodigoPresenca': linha[1],
                'Descricao': linha[2]
            }

            data.append(AulasPresenca)

        return jsonify(data)
        
    except:
        return jsonify({'presenca_coletiva': "error"})


@app.route('/return_aulas_da_materia', methods=['POST'])
def aulas_materia():
    materia = request.form['materia']
    mycursor = db.cursor()

    sql_command_for_database = "SELECT Codigo FROM Materia WHERE Nome = %s;"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)
    res_codigo = mycursor.fetchone()
    codigo_res = str(res_codigo[0])

    sql_command_for_database = "SELECT * FROM Aulas_dadas WHERE codigo_materia = %s"
    values = (codigo_res,)
    mycursor.execute(sql_command_for_database, values)
    aulas_dadas = mycursor.fetchall()
    print(aulas_dadas)

    return jsonify({'Aulas_dadas': aulas_dadas})


@app.route('/returnAulasFaltantes', methods=['POST'])
def returnAulasFaltantes():

    emailAluno = request.form['email']
    nomeMateria = request.form['materia']

    mycursor = db.cursor()

    sql_command_for_database = "SELECT Codigo FROM Materia WHERE Nome = %s;"
    values = (nomeMateria,)
    mycursor.execute(sql_command_for_database, values)
    res_codigo = mycursor.fetchone()
    codigo_res = str(res_codigo[0])


    #sqlCommand = "SELECT * from Aulas_com_presenca WHERE Codigo_Usuario = %s AND Codigo_Materia = %s;"
    sqlCommand = "SELECT * FROM Aulas_dadas where codigo_materia = %s AND codigo_presenca NOT IN (SELECT Codigo_Presenca from Aulas_com_Presenca WHERE Codigo_Usuario = %s AND Codigo_Materia = %s);"
    valuesDatabase = (codigo_res, emailAluno, codigo_res)

    try:
        mycursor.execute(sqlCommand, valuesDatabase)
        aulas_sem_presenca = mycursor.fetchall()

        print(aulas_sem_presenca)

        data = []

        for linha in aulas_sem_presenca:

            if linha[4] == 0:
                AulasSemPresenca = {
                    'Titulo': linha[3],
                    'CodigoPresenca': linha[1],
                    'Descricao': linha[2]
                }
                data.append(AulasSemPresenca)
        
        return jsonify(data)
        
    except:
        return jsonify({'presenca_coletiva': "error"})
    
    

@app.route('/fechar_chamada', methods=['POST'])
def fechar_chamada():
    materia = request.form['materia']
    # materia = "Portugues"
    mycursor = db.cursor()

    sql_command_for_database = "UPDATE Materia SET Codigo_da_Chamada = 'xxxxxx' WHERE Nome = %s;"
    values = (materia,)
    mycursor.execute(sql_command_for_database, values)
    db.commit()

    return jsonify({'status': "chamada fechada com sucesso!"})

  
  
@app.route('/enviar_solicitacao', methods=['POST'])
def enviar_solicitacao():
    Aluno = request.form['nomeAluno']
    nome_materia = request.form['nomeMateria']
    descricao = request.form['descricao']

    # Aluno = 'Jane Doe'
    # nome_materia = 'Geografia'
    # descricao = 'nao consigo criar um node4'

    mycursor = db.cursor()
    sqlCommand = "SELECT Nome FROM aluno WHERE Email = %s;"
    valuesDatabase = (Aluno,)
    mycursor.execute(sqlCommand, valuesDatabase) 
    SqlResponse = mycursor.fetchone()
    NomeAluno = SqlResponse[0]


    sql_command_for_database = "INSERT INTO Solicitacoes (Descricao, Aluno, NomeMateria) VALUES (%s, %s, %s);"
    values = (descricao, NomeAluno, nome_materia)
    mycursor.execute(sql_command_for_database, values)
    db.commit()
    return jsonify({'status': 'solicitacao enviada'})

  
  
@app.route('/ler_solicitacao', methods=['POST'])
def ler_solicitacao():
    #PRECISA DE ALTERCAO
    Rep = request.form['emailAluno']
    #Rep = 'janedoe@gmail.com'

    mycursor = db.cursor()

    #resultados = []

    #for materia in materias:
        # Usando a cláusula IN para verificar se a matéria está na lista de matérias
    sql_command_for_database = "SELECT * FROM Solicitacoes WHERE NomeMateria IN (select Nome From Materia where Codigo IN (select CodigoMateria FROM Representante WHERE EmailAluno = %s));"
    values = (Rep,)
    mycursor.execute(sql_command_for_database, values)
    resultados = mycursor.fetchall()

    return jsonify(resultados)


@app.route('/remover_solicitacao', methods=['POST'])
def remover_solicitacao():

    ID = request.form['ID']

    mycursor = db.cursor()
    sql_command_for_database = "DELETE FROM Solicitacoes WHERE id = %s"
    values = (ID,)
    try:
        mycursor.execute(sql_command_for_database, values)
        db.commit()
    except:
        return jsonify({'remover_solicitacao': 'Error'})
    
    return jsonify({'remover_solicitacao': 'True'})


  
  

@app.route('/return_Reposicoes', methods=['POST'])
def return_Reposicoes():

    Email_aluno = request.form['Email']

    mycursor = db.cursor()
    sql_command_for_database = "SELECT * FROM reposicao_solicitacoes WHERE codigo_usuario = %s);"
    values = (Email_aluno,)
    try:
        mycursor.execute(sql_command_for_database, values)
        db.commit()
        Reposicoes = mycursor.fetchall()
        
        data = []

        for linha in Reposicoes:
            Json_reposicoes = {
                'Motivo': linha[0],
                'CodigoMateria': linha[1],
                'CodigoPresenca': linha[2],
                'RA': linha[3],
                'Status': linha[4],
            }
            data.append(Json_reposicoes)
        
        return jsonify(data)
    except:
        return jsonify({'remover_solicitacao': 'Error'})

      
      
@app.route('/enviar_solicitacao_reposicao', methods=['POST'])
def enviar_solicitacao_reposicao():
    mycursor = db.cursor()

    motivo = request.form['motivo']
    codigo_materia = request.form['codigo_materia']
    codigo_presenca = request.form['codigo_presenca']
    codigo_usuario = request.form['codigo_usuario']
    status = "Pendente"

    # motivo = "bati com o node na cabeca do amigo4"
    # codigo_materia = "Portugues"
    # codigo_presenca = "231871"
    # codigo_usuario = "janedoe@gmail.com"
    # status = "Pendente"

    sql_command_for_database = "SELECT * from reposicao_solicitacoes WHERE codigo_usuario = %s and codigo_presenca = %s"
    values = (codigo_usuario, codigo_presenca)
    mycursor.execute(sql_command_for_database, values)
    res = mycursor.fetchall()

    if not res:
        sql_command_for_database = "INSERT INTO reposicao_solicitacoes (motivo, codigo_materia, codigo_presenca, codigo_usuario, status) VALUES (%s, %s, %s, %s, %s);"
        values = (motivo, codigo_materia, codigo_presenca, codigo_usuario, status)

        try:
            mycursor.execute(sql_command_for_database, values)
            db.commit()
        except:
            return jsonify({'enviar_solicitacao_reposical': 'Error'})
    
        return jsonify({'enviar_solicitacao_reposical': 'solicitacao enviada com sucesso!'})
    else:
        return jsonify({'enviar_solicitacao_reposical': 'existente'})

  
  
  
@app.route('/verificar_solicitacao_reposicao', methods=['POST'])
def verificar_solicitacao_reposicao():

    resposta = request.form['resposta'] ##Sim ou Nao
    codigo_usuario = request.form['codigo_usuario']
    codigo_materia = request.form['codigo_materia']
    codigo_presenca = request.form['codigo_presenca']
    mycursor = db.cursor()

    # resposta = "Nao"
    # codigo_usuario = "janedoe@gmail.com"
    # codigo_materia = "231258"
    # codigo_presenca = "xxxxxx"

    if resposta == "Sim":
        sql_command_for_database = "INSERT INTO Aulas_com_Presenca (Codigo_Usuario, Codigo_Presenca, Codigo_Materia) VALUES (%s, %s, %s);"
        values = (codigo_usuario, codigo_presenca, codigo_materia)
        try:
            mycursor.execute(sql_command_for_database, values)
            db.commit()
        except:
            return jsonify({'Aulas_com_Presenca': 'Error'})
    
        sql_command_for_database = "UPDATE Materia_Aluno SET Frequencia = Frequencia + 1 WHERE Nome_Aluno = %s AND Nome_Materia = %s;"
        values = (codigo_usuario, codigo_materia)
        try:
            mycursor.execute(sql_command_for_database, values)
            db.commit()
        except:
            return jsonify({'Update_Frequencia': 'Error'})
        
        sql_command_for_database = "UPDATE reposicao_solicitacoes SET status = 'Aceito' WHERE codigo_usuario = %s AND codigo_presenca = %s;"
        values = (codigo_usuario, codigo_presenca)
        try:
            mycursor.execute(sql_command_for_database, values)
            db.commit()
        except:
            return jsonify({'atualizar status': 'Error'})

    elif resposta == "Nao":
        sql_command_for_database = "UPDATE reposicao_solicitacoes SET status = 'Negado' WHERE codigo_usuario = %s AND codigo_presenca = %s;"
        values = (codigo_usuario, codigo_presenca)
        try:
            mycursor.execute(sql_command_for_database, values)
            db.commit()
        except:
            return jsonify({'atualizar status': 'Error'})


    return jsonify({'verificar_solicitacao_reposicao': 'Atualizado com sucesso!'})


  
@app.route('/ler_solicitacoes_reposicao', methods=['POST'])
def ler_solicitacoes_reposicao():
    mycursor = db.cursor()
    email_prof = request.form['email_prof']
    sqlCommand = "SELECT * FROM reposicao_solicitacoes WHERE status = 'Pendente' AND codigo_materia IN (SELECT Codigo from Materia WHERE Nome IN (SELECT Nome_Materia from Materia_Professor WHERE Nome_Professor = %s));"
    values = (email_prof,)
    try:
        mycursor.execute(sqlCommand, values)
        solicitacoes = mycursor.fetchall()

        print(solicitacoes)

        data = []

        for linha in solicitacoes:
                
            solicitacoes_arr = {
                'motivo': linha[0],
                'codigo_materia': linha[1],
                'codigo_presenca': linha[2],
                'codigo_usuario': linha[3],
                'status': linha[4]
                }
            data.append(solicitacoes_arr)
        
        return jsonify(data)
        
    except:
        return jsonify({'ler_solicitacoes': "error"})
  
  
  
if __name__ == '__main__':
    app.run()